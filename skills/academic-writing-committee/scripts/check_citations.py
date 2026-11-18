#!/usr/bin/env python3
# check_citations.py - audit of citation keys, bibliography entries and reference lists, with
# optional online verification of each reference.
#
# ADAPTED WORK. This file is not an unchanged copy of any source script. It rewrites and
# extends two MIT-licensed scripts from K-Dense-AI/claude-scientific-skills
# (MIT License, Copyright (c) 2025 K-Dense Inc.):
#
#   1. skills/peer-review/scripts/audit_citations.py
#      Taken from it: comparing in-text citation keys with a reference list (cited without
#      an entry, entry never cited, entry without DOI or URL, unverified entries).
#   2. skills/scientific-writing/scripts/check_references.py (with scripts/_common.py)
#      Taken from it: offline DOI, ISBN and URL syntax checks, duplicate DOI and duplicate
#      title detection, bounded UTF-8 input, symbolic-link rejection.
#
# Main changes: reads BibTeX/BibLaTeX (.bib) and CSL JSON (.json) instead of the custom
# K-Dense CSV and JSON manifests; reads LaTeX \cite commands (natbib and biblatex, including
# multicite commands) as well as Pandoc [@key] citations; the source ledger is an optional
# plain CSV; findings name the citation key and line; no dependency on other modules.
# Written for this skill and not taken from the sources: the required-field, arXiv and year
# checks, the free-form reference-list parser (--reference-list) and the online verification
# against Crossref, arXiv and DataCite (--online).
#
# The license text is in ../LICENSES/. Standard library only. Without --online nothing is
# sent over a network. With --online the script sends identifiers, titles and first-author
# surnames to api.crossref.org, export.arxiv.org, doi.org and api.datacite.org, and requests
# the URLs of references that have no DOI or arXiv identifier. Input files are opened
# read-only; the only file written is the --cache file, when one is given.
"""Audit citations and references: keys against a bibliography, bibliography entries, free-
form reference lists and, with --online, whether each reference exists with that metadata.

Usage:
    python3 check_citations.py paper.tex --bib refs.bib
    python3 check_citations.py paper.tex references.bib --online
    python3 check_citations.py ch1.md ch2.md --bib refs.json --ledger sources.csv
    python3 check_citations.py paper.tex            # uses \\bibitem entries in the files
    python3 check_citations.py --reference-list sources.tex --online --max-online 50 \\
        --cache refcache.json

Modes (they combine):
  Citation keys. Manuscripts (.tex, .texview, .md, .markdown, .txt) are scanned for LaTeX
    citation commands (\\cite, \\citep, \\citet, \\citealp, \\citeauthor, \\citeyear,
    \\parencite, \\textcite, \\autocite, \\footcite, \\smartcite, \\nocite, starred forms,
    several keys, pre- and postnotes, and multicite forms such as \\parencites) and for
    bracketed Pandoc groups such as [@key; see @other, p. 4]. A bare @key outside brackets
    is read only in .md and .markdown files; if it matches nothing in the bibliography (or the
    ledger, when no bibliography is given), it is reported as BARE_KEY_NOT_IN_BIBLIOGRAPHY,
    because it may be a social-media handle; --no-bare-keys turns bare keys off.
  Bibliography. Each positional argument ending in .bib or .json, and each --bib file, is a
    BibTeX/BibLaTeX or CSL JSON bibliography. Entries are checked for duplicate keys, DOIs,
    arXiv identifiers and titles; required fields by type (author or editor, title, year,
    and journal, booktitle, publisher, school or institution as the type needs); malformed
    DOIs (10.NNNN/...), arXiv identifiers (YYMM.NNNNN or archive/YYMMNNN, optional version)
    and ISBN checksums; years after next year or before 1500; and entries with no DOI, arXiv
    identifier, ISBN or URL. An entry never cited is a note, unless \\nocite{*} is used. For a
    CSL JSON bibliography the number after the file name is the item's position.
  Reference list (--reference-list FILE). For documents without a bibliography database:
    the entries of a LaTeX thebibliography (\\bibitem) or list (\\item), or of a Markdown or
    plain-text numbered or bulleted list ("1.", "-", "[1]"), are parsed into authors, year,
    title (\\emph{}, \\textit{}, quotation marks or *...*), DOI, arXiv identifier and URLs,
    and receive the same format checks. When the file has a heading such as References,
    Bibliography or Sources, only the entries after it are read.
  Ledger (--ledger CSV). A CSV with a header row. Required columns: key, status. Optional
    columns: locator, verified_by, verified_on. A source counts as verified when its status
    starts with "verified" (for example "verified" or "verified_primary").
  Online (--online, off by default). DOIs are looked up at api.crossref.org (and, when
    Crossref has no record, at doi.org and api.datacite.org); arXiv identifiers at
    export.arxiv.org; other entries by Crossref bibliographic search on the title and first
    author; a URL with no DOI or arXiv identifier is requested (HEAD, then GET). The title
    (similarity of normalized titles), the first author's surname and the year (one year of
    difference allowed for preprint and publication) are compared, and each reference is
    classified: VERIFIED (note), NOT_FOUND (error: the DOI or arXiv identifier does not
    exist), METADATA_MISMATCH (error when the title differs, warning when only the first
    author or the year differs), UNVERIFIED (warning: nothing matched with confidence, or the
    network failed; the finding says which) or URL_ONLY (warning: the link resolves, but the
    work and its metadata must be checked by a person). A reference is never VERIFIED unless
    its metadata matched. Requests use a 20 s timeout, at most about five per second (one
    per second for Crossref searches, one every three seconds to arXiv, which receives
    batched queries; a 429 or 5xx answer is retried twice) and a generic User-Agent;
    no e-mail address is sent unless --mailto is given (Crossref's polite pool). HTTPS proxy
    settings are taken from the environment. --cache FILE keeps the responses as JSON so
    that reruns are fast; --max-online N caps the number of references looked up.

Every finding is a prompt for human judgment. Even a VERIFIED reference is only known to
exist with that metadata; whether it supports the sentence that cites it must be read.

Exit status: 0 without error-level findings, 1 with at least one, 2 when an input is
rejected (symbolic link, unsupported extension, not UTF-8, over 5 MB, missing, unreadable
CSL JSON, a ledger without key and status columns) or an option is invalid. Network
failures are warnings (UNVERIFIED), not errors.
"""

from __future__ import annotations

import argparse
import bisect
import csv
import datetime
import difflib
import html
import http.client
import io
import ipaddress
import json
import os
import re
import sys
import tempfile
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

TOOL = "check_citations"
MAX_FILE_BYTES = 5_000_000
LATEX_SUFFIXES = {".tex", ".texview"}
MANUSCRIPT_SUFFIXES = {".md", ".markdown", ".tex", ".texview", ".txt"}
BIB_SUFFIXES = {".bib", ".json"}
SEVERITIES = ("error", "warning", "info")
SEVERITY_RANK = {name: rank for rank, name in enumerate(SEVERITIES)}
SEVERITY_ALIASES = {"note": "info"}

USER_AGENT = "academic-writing-checker/1.0 (+https://github.com/gacikgoz/academic-writing-committee)"
TIMEOUT = 20
MIN_INTERVAL = 0.2          # at most about five requests per second
ARXIV_INTERVAL = 3.0        # arXiv asks for one request every three seconds
SEARCH_INTERVAL = 1.0       # Crossref allows one search (list) query per second
ARXIV_BATCH = 40
MAX_RESPONSE_BYTES = 5_000_000
TITLE_MATCH = 0.8           # identifier lookups: below this the title is a mismatch
SEARCH_MATCH = 0.9          # bibliographic search: a confident match needs this
ONLINE_CLASSES = ("VERIFIED", "METADATA_MISMATCH", "NOT_FOUND", "UNVERIFIED", "URL_ONLY")

RULES = (
    ("CITATION_PLACEHOLDER", "error", "[citation needed], [?], (Author, Year), \\cite{TODO}"),
    ("EMPTY_CITATION", "error", "a citation command or [@...] group without a key"),
    ("CITED_KEY_NOT_IN_BIBLIOGRAPHY", "error", "a cited key with no bibliography entry"),
    ("BARE_KEY_NOT_IN_BIBLIOGRAPHY", "warning", "a bare @key (Markdown) matching no entry"),
    ("ENTRY_NEVER_CITED", "info", "a bibliography entry that no file cites"),
    ("NO_BIBLIOGRAPHY_GIVEN", "info", "manuscripts given without a bibliography or \\bibitem"),
    ("BIB_PARSE_PROBLEM", "warning", "an unreadable BibTeX entry or field"),
    ("DUPLICATE_KEY", "error", "a key defined more than once"),
    ("DUPLICATE_DOI", "warning", "two entries with the same DOI"),
    ("DUPLICATE_ARXIV", "warning", "two entries with the same arXiv identifier"),
    ("POSSIBLE_DUPLICATE_TITLE", "warning", "two entries with the same normalized title"),
    ("MISSING_FIELD", "warning",
     "no title, author or editor, year, or the venue its type needs (journal, booktitle, "
     "publisher, school or institution)"),
    ("IMPLAUSIBLE_YEAR", "warning", "a year after next year or before 1500"),
    ("MALFORMED_DOI", "error", "a DOI that is not 10.NNNN/..."),
    ("MALFORMED_ARXIV_ID", "warning", "an arXiv identifier of neither YYMM.NNNNN nor archive/YYMMNNN"),
    ("MALFORMED_ISBN", "warning", "an ISBN-10 or ISBN-13 with a wrong checksum"),
    ("MALFORMED_URL", "warning", "a URL that is not http(s)"),
    ("NO_IDENTIFIER", "warning", "no DOI, arXiv identifier, ISBN or URL: verify it by search"),
    ("REFERENCE_LIST_EMPTY", "warning", "--reference-list found no entries in the file"),
    ("DUPLICATE_LEDGER_KEY", "warning", "a ledger key listed twice"),
    ("LEDGER_KEY_NOT_IN_BIBLIOGRAPHY", "info", "a ledger key with no bibliography entry"),
    ("CITED_SOURCE_NOT_IN_LEDGER", "warning", "a cited key with no ledger row"),
    ("CITED_SOURCE_NOT_VERIFIED", "warning", "a cited key whose ledger status is not verified"),
    ("LEDGER_ROW_WITHOUT_LOCATOR", "info", "a verified ledger row without a locator"),
    ("VERIFIED", "info", "--online: the record matches title, first author and year"),
    ("NOT_FOUND", "error", "--online: the DOI or arXiv identifier does not exist"),
    ("METADATA_MISMATCH", "error/warning",
     "--online: the record's title differs (error) or only its first author or year (warning)"),
    ("UNVERIFIED", "warning", "--online: nothing matched with confidence, or the network failed"),
    ("URL_ONLY", "warning", "--online: the link resolves, but a person must verify the work"),
)

LATEX_COMMENT_RE = re.compile(r"(?<!\\)%.*")
UNESCAPED_PERCENT_RE = re.compile(r"(?<!\\)%")
# Lowercase and capitalized natbib and biblatex commands: \citet, \Citet, \Parencite, \Textcite.
CITE_COMMAND_RE = re.compile(r"\\([A-Za-z]*[Cc]ite[A-Za-z]*)(\*?)")
NOT_CITE_COMMANDS = {"citetext", "defcitealias", "citestyle", "setcitestyle", "citeindexfalse",
                     "citeindextrue", "citeauthorfont", "citepunct", "citesetup"}
# Definitions and configuration rather than citations: \DeclareCiteCommand, \newcitecommand.
NOT_CITE_PREFIX_RE = re.compile(r"^(?:Declare|Execute|Provide|declare|new|renew|provide|set|def)")
# pandoc-crossref references ([@fig:loss], @sec:method) are cross-references, not citations.
CROSSREF_KEY_RE = re.compile(r"^(?:fig|sec|tbl|eq|lst|thm|lem|def|cor|prp|app|alg):")
LATEX_VERBATIM_BEGIN_RE = re.compile(r"\\begin\{(verbatim|Verbatim|lstlisting|minted|comment)\*?\}")
LATEX_VERB_RE = re.compile(r"\\(?:verb|lstinline)\*?([^\sA-Za-z{])[^\n]*?\1|\\lstinline\{[^{}\n]{0,400}\}")
LATEX_BIBITEM_RE = re.compile(r"\\bibitem(?:\[[^\]]{0,200}\])?\{([^}]+)\}")
PANDOC_GROUP_RE = re.compile(r"\[(?=[^\]\n]{0,1000}\])([^\]\n@]*@[^\]\n]*)\]")
BARE_KEY_SUFFIXES = {".md", ".markdown"}
PANDOC_KEY_RE = re.compile(r"(?<![\w.])-?@\{?([A-Za-z0-9_][\w:.#$%&+?<>~/-]*)\}?")
PLACEHOLDER_RE = re.compile(
    r"\[\s*(?:citation needed|cite|citation|ref|reference)\s*\]|\[\?+\]|\(\s*Author,?\s+Year\s*\)"
    r"|\\[A-Za-z]*[Cc]ite[A-Za-z]*\*?\{\s*(?:TODO|TBD|XXX|\?+)\s*\}",
    re.IGNORECASE,
)
DOI_RE = re.compile(r"^10\.[0-9]{4,9}/\S+$")
URL_RE = re.compile(r"^https?://[^\s]+$", re.IGNORECASE)
YEAR_RE = re.compile(r"(?<!\d)(\d{4})(?!\d)")
NO_YEAR_TYPES = {"misc", "online", "unpublished", "software", "dataset", "manual", "electronic", "www"}
# The venue a BibTeX type needs; each tuple lists alternatives.
VENUE_FIELDS: dict[str, tuple[tuple[str, ...], ...]] = {
    "article": (("journal", "journaltitle"),),
    "inproceedings": (("booktitle",),),
    "conference": (("booktitle",),),
    "incollection": (("booktitle",), ("publisher",)),
    "inbook": (("publisher",),),
    "book": (("publisher",),),
    "phdthesis": (("school", "institution"),),
    "mastersthesis": (("school", "institution"),),
    "thesis": (("school", "institution"),),
    "techreport": (("institution",),),
    "report": (("institution",),),
}
CSL_TYPES = {
    "article-journal": "article", "paper-conference": "inproceedings", "chapter": "incollection",
    "book": "book", "thesis": "phdthesis", "report": "techreport", "webpage": "online",
    "post": "online", "post-weblog": "online", "dataset": "dataset", "software": "software",
    "manuscript": "unpublished",
}
NEW_ARXIV_RE = re.compile(r"(\d{2})(\d{2})\.(\d{4,5})(v\d+)?")
OLD_ARXIV_RE = re.compile(r"([a-z]+(?:-[a-z]+)*)(\.[A-Z]{2})?/(\d{2})(\d{2})(\d{3})(v\d+)?")
ARXIV_URL_RE = re.compile(r"arxiv\.org/(?:abs|pdf|html|format)/([^\s?#\"'<>{}]+)", re.IGNORECASE)
ARXIV_TEXT_RE = re.compile(r"\barXiv\s*:\s*([^\s,;)\]}]+)", re.IGNORECASE)
ARXIV_DOI_RE = re.compile(r"^10\.48550/arxiv\.(.+)$", re.IGNORECASE)
DOI_URL_RE = re.compile(r"^https?://(?:dx\.)?doi\.org/(.+)$", re.IGNORECASE)
DOI_IN_URL_RE = re.compile(r"/(10\.\d{4,9}/[^?#\s]+)")
DOI_TEXT_RE = re.compile(r"\bdoi\s*:\s*(\S+)", re.IGNORECASE)
BARE_DOI_RE = re.compile(r"(?<![\w/.])(10\.\d{4,9}/[^\s,;\"<>{}]+)")
LINK_RE = re.compile(r"https?://[^\s<>\"{}\\|^`]+", re.IGNORECASE)
LATEX_ACCENT_RE = re.compile(
    r"\\['`^\"~=.]\{?([A-Za-z])\}?|\\[Hcvudbtkr](?:\{([A-Za-z])\}|\s([A-Za-z]))"
    r"|\\(i|j|o|O|l|L|ss|ae|AE|oe|OE|aa|AA)(?![A-Za-z])"
)


class InputError(ValueError):
    """Raised when an input file fails a safety check."""


def read_text(path_value: str, suffixes: set[str]) -> tuple[Path, str]:
    path = Path(path_value)
    if path.is_symlink():
        raise InputError(f"{path}: symbolic links are not accepted")
    if not path.is_file():
        raise InputError(f"{path}: not an existing regular file")
    if path.suffix.lower() not in suffixes:
        raise InputError(f"{path}: extension must be one of {', '.join(sorted(suffixes))}")
    if path.stat().st_size > MAX_FILE_BYTES:
        raise InputError(f"{path}: larger than {MAX_FILE_BYTES} bytes")
    try:
        return path, path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise InputError(f"{path}: not UTF-8 text") from exc


class Report:
    def __init__(self) -> None:
        self.findings: list[dict[str, object]] = []

    def add(self, source: object, line: int, severity: str, code: str, detail: str) -> None:
        self.findings.append(
            {"file": str(source), "line": line, "severity": severity, "code": code, "detail": detail}
        )


def _accent(match: re.Match[str]) -> str:
    return match.group(1) or match.group(2) or match.group(3) or match.group(4) or ""


def latex_to_plain(text: str) -> str:
    """Approximate the printed text of a LaTeX fragment (accents to base letters)."""
    text = LATEX_ACCENT_RE.sub(_accent, text)
    for escaped, plain in (("\\&", "&"), ("\\%", "%"), ("\\_", "_"), ("\\#", "#"), ("\\$", "$")):
        text = text.replace(escaped, plain)
    text = re.sub(r"\\text(?:en|em)dash(?![A-Za-z])", "-", text)
    text = text.replace("---", "\u2014").replace("--", "\u2013")
    text = re.sub(r"\\[A-Za-z]+\*?", " ", text)
    text = re.sub(r"\\.", " ", text)
    text = text.replace("{", "").replace("}", "").replace("~", " ")
    return " ".join(text.split())


# ---------------------------------------------------------------------------
# Citations in the manuscript
# ---------------------------------------------------------------------------


Uses = dict[str, tuple[Path, int]]


def _skip_space(text: str, position: int) -> int:
    limit = min(len(text), position + 200)
    while position < limit and text[position].isspace():
        position += 1
    return position


def latex_citations(text: str):
    """Yield (command, key group, offset) for every key group of every LaTeX citation
    command, including optional pre- and postnotes and biblatex multicite commands such as
    \\parencites(pre)(post)[p.~4]{a}[ch.~2]{b}."""
    for match in CITE_COMMAND_RE.finditer(text):
        name = match.group(1)
        if name in NOT_CITE_COMMANDS or NOT_CITE_PREFIX_RE.match(name):
            continue
        multi = name.endswith("cites")
        position = match.end()
        if multi:
            for _ in range(2):   # global (pre)(post) notes
                start = _skip_space(text, position)
                if start < len(text) and text[start] == "(":
                    end = text.find(")", start, start + 400)
                    if end < 0:
                        break
                    position = end + 1
                else:
                    break
        while True:
            start = _skip_space(text, position)
            for _ in range(2):   # [prenote][postnote]
                if start < len(text) and text[start] == "[":
                    end = text.find("]", start, start + 202)
                    if end < 0:
                        break
                    start = _skip_space(text, end + 1)
                else:
                    break
            if start >= len(text) or text[start] != "{":
                break
            end = text.find("}", start, start + 4000)
            if end < 0:
                break
            yield name, text[start + 1:end], match.start()
            position = end + 1
            if not multi:
                break


def scan_manuscript(path: Path, text: str, report: Report,
                    bare_keys: bool = True) -> tuple[Uses, Uses, set[str], bool]:
    """Return first use of each cited key, first use of each bare @key (Markdown only),
    keys defined by \\bibitem, and a cite-all flag."""
    cited: Uses = {}
    bare: Uses = {}
    bibitems: set[str] = set()
    cite_all = False
    latex = path.suffix.lower() in LATEX_SUFFIXES
    bare_keys = bare_keys and path.suffix.lower() in BARE_KEY_SUFFIXES
    in_fence = False
    verbatim = ""
    lines = text.splitlines()
    # LaTeX: the preamble holds configuration (\setcitestyle, macro bodies such as \citep{#1}),
    # so only \nocite is read there; verbatim environments and \verb are code, not citations.
    body_start = 0
    if latex:
        for number, original in enumerate(lines):
            if "\\begin{document}" in LATEX_COMMENT_RE.sub("", original):
                body_start = number
                break
    clean: list[str] = []
    for index, line in enumerate(lines):
        if latex:
            line = LATEX_COMMENT_RE.sub("", line)
            if index < body_start and "\\nocite" not in line:
                clean.append("")
                continue
            if verbatim:
                if re.search(r"\\end\{" + re.escape(verbatim) + r"\*?\}", line):
                    verbatim = ""
                clean.append("")
                continue
            begun = LATEX_VERBATIM_BEGIN_RE.search(line)
            if begun:
                if not re.search(r"\\end\{" + re.escape(begun.group(1)) + r"\*?\}", line):
                    verbatim = begun.group(1)
                clean.append(line[:begun.start()])
                continue
            line = LATEX_VERB_RE.sub(" ", line)
        else:
            if line.strip().startswith(("```", "~~~")):
                in_fence = not in_fence
                clean.append("")
                continue
            if in_fence:
                clean.append("")
                continue
            line = re.sub(r"`[^`]*`", " ", line)
        clean.append(line)
    # LaTeX citations may span lines; they are read from the joined text and attributed to
    # the line where the command starts.
    joined = "\n".join(clean)
    starts = [0]
    for line in clean:
        starts.append(starts[-1] + len(line) + 1)
    latex_by_line: dict[int, list[tuple[str, str]]] = {}
    for command, group, offset in latex_citations(joined):
        number = bisect.bisect_right(starts, offset)
        latex_by_line.setdefault(number, []).append((command, group))
    for number, line in enumerate(clean, start=1):
        if PLACEHOLDER_RE.search(line):
            report.add(path, number, "error", "CITATION_PLACEHOLDER",
                       "a citation placeholder is still in the text")
        bibitems.update(key.strip() for key in LATEX_BIBITEM_RE.findall(line))
        for command, group in latex_by_line.get(number, []):
            keys = [key.strip() for key in group.split(",")]
            if not any(keys):
                report.add(path, number, "error", "EMPTY_CITATION", f"\\{command} has no key")
            for key in keys:
                if key == "*":
                    cite_all = True
                elif key and "#" not in key:   # "#1" is a macro parameter, not a key
                    cited.setdefault(key, (path, number))
        if not latex:
            for group in PANDOC_GROUP_RE.findall(line):
                if not re.search(r"(?:^|[^\w.])-?@", group):
                    continue   # an e-mail address in brackets, not a citation marker
                keys = PANDOC_KEY_RE.findall(group)
                if not keys:
                    report.add(path, number, "error", "EMPTY_CITATION",
                               "bracketed citation without a readable key")
                for key in keys:
                    key = key.rstrip(".,;:")
                    if not CROSSREF_KEY_RE.match(key):
                        cited.setdefault(key, (path, number))
            if bare_keys:
                outside = PANDOC_GROUP_RE.sub(" ", line)
                for key in PANDOC_KEY_RE.findall(outside):
                    key = key.rstrip(".,;:")
                    if key and not CROSSREF_KEY_RE.match(key):
                        bare.setdefault(key, (path, number))
    return cited, bare, bibitems, cite_all


# ---------------------------------------------------------------------------
# Bibliography readers
# ---------------------------------------------------------------------------


def clean_value(value: str) -> str:
    value = value.strip()
    while len(value) >= 2 and value[0] == "{" and value[-1] == "}":
        value = value[1:-1].strip()
    return " ".join(value.replace("{", "").replace("}", "").split())


def parse_bibtex(path: Path, text: str, report: Report) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    length = len(text)
    position = 0
    newlines = [match.start() for match in re.finditer("\n", text)]

    def line_of(index: int) -> int:
        return bisect.bisect_left(newlines, index) + 1

    def skip_space(index: int) -> int:
        while index < length and (text[index].isspace() or text[index] == ","):
            index += 1
        return index

    def read_value(index: int) -> tuple[str, int]:
        parts: list[str] = []
        while index < length:
            while index < length and text[index].isspace():
                index += 1
            if index >= length:
                break
            char = text[index]
            if char == "{":
                depth, start = 0, index
                while index < length:
                    if text[index] == "{":
                        depth += 1
                    elif text[index] == "}":
                        depth -= 1
                        if depth == 0:
                            break
                    index += 1
                parts.append(text[start + 1:index])
                index += 1
            elif char == '"':
                depth, start = 0, index + 1
                index += 1
                while index < length and not (text[index] == '"' and depth == 0):
                    if text[index] == "{":
                        depth += 1
                    elif text[index] == "}":
                        depth -= 1
                    index += 1
                parts.append(text[start:index])
                index += 1
            else:
                start = index
                while index < length and text[index] not in ",}#\n)":
                    index += 1
                parts.append(text[start:index].strip())
            while index < length and text[index] in " \t":
                index += 1
            if index < length and text[index] == "#":
                index += 1
                continue
            break
        return " ".join(parts), index

    for match in re.finditer(r"@([A-Za-z]+)\s*([{(])", text):
        if match.start() < position:
            continue
        entry_type = match.group(1).lower()
        closer = "}" if match.group(2) == "{" else ")"
        index = match.end()
        if entry_type in {"comment", "preamble", "string"}:
            depth = 1
            while index < length and depth:
                if text[index] in "{(":
                    depth += 1
                elif text[index] in "})":
                    depth -= 1
                index += 1
            position = index
            continue
        key_match = re.compile(r"\s*([^,\s{}()]*)\s*,").match(text, index)
        line = line_of(match.start())
        if not key_match or not key_match.group(1):
            report.add(path, line, "warning", "BIB_PARSE_PROBLEM", "entry without a readable key")
            position = index
            continue
        fields: dict[str, str] = {}
        index = key_match.end()
        while index < length:
            index = skip_space(index)
            if index >= length or text[index] == closer:
                index += 1
                break
            name_match = re.compile(r"([A-Za-z][\w:-]*)\s*=").match(text, index)
            if not name_match:
                report.add(path, line_of(index), "warning", "BIB_PARSE_PROBLEM",
                           f'could not read a field of "{key_match.group(1)}"')
                break
            value, index = read_value(name_match.end())
            fields[name_match.group(1).lower()] = clean_value(value)
        position = index
        entries.append({"key": key_match.group(1), "type": entry_type, "fields": fields,
                        "line": line, "source": path})
    return entries


def parse_csl_json(path: Path, text: str) -> list[dict[str, object]]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise InputError(f"{path}: not valid JSON") from exc
    if isinstance(data, dict):
        data = data.get("items") or data.get("references") or []
    if not isinstance(data, list):
        raise InputError(f"{path}: expected a CSL JSON array")
    entries: list[dict[str, object]] = []
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict) or "id" not in item:
            raise InputError(f"{path}: item {index} has no id")
        fields: dict[str, str] = {}
        for source, target in (("title", "title"), ("DOI", "doi"), ("URL", "url"),
                               ("ISBN", "isbn"), ("PMID", "pmid"), ("publisher", "publisher"),
                               ("note", "note"), ("number", "number"), ("archive", "archive"),
                               ("archive_location", "archive_location")):
            if item.get(source):
                value = item[source]
                fields[target] = str(value[0] if isinstance(value, list) and value else value)
        for role in ("author", "editor"):
            people = item.get(role)
            if isinstance(people, list) and people:
                fields[role] = "; ".join(
                    str(p.get("family") or p.get("literal") or "") for p in people if isinstance(p, dict)
                )
        issued = item.get("issued")
        if isinstance(issued, dict):
            parts = issued.get("date-parts")
            if isinstance(parts, list) and parts and isinstance(parts[0], list) and parts[0]:
                fields["year"] = str(parts[0][0])
            elif issued.get("raw") or issued.get("literal"):
                fields["year"] = str(issued.get("raw") or issued.get("literal"))
        csl_type = str(item.get("type", "")).lower()
        entry_type = CSL_TYPES.get(csl_type, "misc")
        container = item.get("container-title")
        if isinstance(container, list):
            container = container[0] if container else ""
        if container:
            fields["journal" if entry_type == "article" else "booktitle"] = str(container)
        if fields.get("publisher") and entry_type in {"phdthesis"}:
            fields["school"] = fields["publisher"]
        if fields.get("publisher") and entry_type in {"techreport"}:
            fields["institution"] = fields["publisher"]
        entries.append({"key": str(item["id"]), "type": entry_type, "fields": fields,
                        "line": index, "source": path})
    return entries


# ---------------------------------------------------------------------------
# Free-form reference lists
# ---------------------------------------------------------------------------

REF_HEADING_WORDS = r"(?:references|bibliography|sources|works\s+cited|literature|reading)"
LATEX_REF_HEADING_RE = re.compile(
    r"\\(?:part|chapter|section|subsection|subsubsection|paragraph)\*?\{[^}]{0,200}"
    + REF_HEADING_WORDS, re.IGNORECASE)
LATEX_LIST_ITEM_RE = re.compile(r"\\(?:bibitem(?:\[[^\]]{0,200}\])?\{([^}]*)\}|item(?![A-Za-z])(?:\s*\[[^\]]{0,200}\])?)")
LATEX_LIST_END_RE = re.compile(r"\\end\{(?:enumerate|itemize|description|thebibliography)\}")
MD_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
MD_REF_ITEM_RE = re.compile(r"^\s{0,3}(?:[-*+]|\d{1,4}[.)]|\[\d{1,4}\])\s+(.*)$")
URL_COMMAND_RE = re.compile(r"\\(?:url|href)\{([^}]*)\}(?:\{([^}]*)\})?")
EMPH_COMMAND_RE = re.compile(r"\\(?:emph|textit|textsl|mkbibemph)\s*\{|\{\\(?:em|it|sl)\s")
MD_LINK_RE = re.compile(r"\[([^\]]{0,500})\]\((https?://[^)\s]+)\)")
MD_EMPHASIS_RE = re.compile(r"(?<![\w*])\*([^*\n]{2,400})\*(?![\w*])|(?<![\w_])_([^_\n]{2,400})_(?![\w_])")
QUOTED_TITLE_RE = re.compile(r"\u201c([^\u201d]{3,400})\u201d|``(.{3,400}?)''|\"([^\"]{3,400})\"")
YEAR_PAREN_RE = re.compile(r"\(\s*(1[5-9]\d{2}|20\d{2})[a-z]?\s*\)|\(\s*(n\.\s?d\.)\s*\)")
YEAR_ANY_RE = re.compile(r"(?<![\d.])(1[5-9]\d{2}|20\d{2})[a-z]?(?![\d.]?\d)")


def _strip_comment_keep_urls(line: str) -> str:
    spans = [m.span() for m in URL_COMMAND_RE.finditer(line)]
    for match in UNESCAPED_PERCENT_RE.finditer(line):
        if not any(start <= match.start() < end for start, end in spans):
            return line[:match.start()]
    return line


def _unescape_url(url: str) -> str:
    for escaped, plain in (("\\%", "%"), ("\\#", "#"), ("\\_", "_"), ("\\&", "&"),
                           ("\\~{}", "~"), ("\\~", "~"), ("\\textasciitilde{}", "~")):
        url = url.replace(escaped, plain)
    return url.strip()


def _trim_identifier(value: str) -> str:
    value = value.strip().rstrip(".,;:")
    for opener, closer in (("(", ")"), ("[", "]")):
        while value.endswith(closer) and value.count(closer) > value.count(opener):
            value = value[:-1].rstrip(".,;:")
    return value


def _braced(text: str, start: int) -> tuple[str, int] | None:
    """Return the content of the brace group opening at text[start] and the index after it."""
    depth = 0
    index = start
    limit = min(len(text), start + 2000)
    while index < limit:
        char = text[index]
        if char == "\\":
            index += 2
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1:index], index + 1
        index += 1
    return None


VANCOUVER_AUTHOR_RE = re.compile(r"[A-Z][\w'\u2019-]*(?:\s+[A-Za-z][\w'\u2019-]*){0,3}\s+[A-Z]{1,4}")


def _vancouver_title(body: str) -> tuple[int, str] | None:
    """Vancouver/NLM style, "Surname AB, Surname C. Title. Journal. 2015;521:436-44.": when
    every comma-separated item before the first period is a surname with initials (or "et
    al"), the next sentence is the title. Returns (start, title) or None."""
    first = re.search(r"\.\s+", body)
    if not first:
        return None
    authors = body[:first.start()].strip()
    items = [item.strip() for item in authors.split(",")]
    if not items or not all(VANCOUVER_AUTHOR_RE.fullmatch(item) or item.lower() == "et al"
                            for item in items):
        return None
    second = re.search(r"[.?!]\s+", body[first.end():])
    title = body[first.end():first.end() + second.start() + 1 if second else len(body)].strip()
    return (first.end(), title.rstrip(".")) if len(title.split()) >= 2 else None


def parse_reference_text(raw: str, latex: bool) -> dict[str, str]:
    """Split one free-form reference into authors, year, title, DOI, arXiv id and URLs."""
    fields: dict[str, str] = {}
    urls: list[str] = []
    if latex:
        for match in URL_COMMAND_RE.finditer(raw):
            urls.append(_unescape_url(match.group(1)))
        body = URL_COMMAND_RE.sub(lambda m: " " + (m.group(2) or "") + " ", raw)
    else:
        for match in MD_LINK_RE.finditer(raw):
            urls.append(match.group(2))
        body = MD_LINK_RE.sub(lambda m: m.group(1), raw)
        urls += re.findall(r"<(https?://[^>\s]+)>", body)
        body = re.sub(r"<(https?://[^>\s]+)>", " ", body)
    for match in LINK_RE.finditer(body):
        urls.append(_trim_identifier(match.group(0)))
    body = LINK_RE.sub(" ", body)
    urls = [_trim_identifier(url) for url in dict.fromkeys(urls) if url]

    emphasized: list[tuple[int, str]] = []
    if latex:
        for match in EMPH_COMMAND_RE.finditer(body):
            brace = match.end() - 1 if match.group(0).endswith("{") else match.start()
            group = _braced(body, brace)
            if group:
                emphasized.append((match.start(), group[0]))
    else:
        for match in MD_EMPHASIS_RE.finditer(body):
            emphasized.append((match.start(), match.group(1) or match.group(2)))
    quoted = [(m.start(), next(g for g in m.groups() if g)) for m in QUOTED_TITLE_RE.finditer(body)]
    first_mark = min([start for start, _ in emphasized + quoted], default=len(body))
    year_match = YEAR_PAREN_RE.search(body)
    if not year_match:
        candidates = [m for m in YEAR_ANY_RE.finditer(body)]
        year_match = next((m for m in candidates if m.start() < first_mark), None) or (
            candidates[0] if candidates else None)
    after_year = year_match.end() if year_match else 0

    def gap(position: int) -> str:
        return body[after_year:position].strip(" .,;:") if position >= after_year else "x"

    title = ""
    title_start = None
    following = [item for item in emphasized if item[0] >= after_year]
    if year_match and following and not gap(following[0][0]):
        title_start, title = following[0]             # "Authors (2021). \emph{Title}."
    else:
        near = [item for item in quoted
                if not year_match or item[0] < year_match.start() or len(gap(item[0])) <= 3]
        if near:
            title_start, title = near[0]               # Authors, "Title," Journal, 2021.
        elif year_match and body[after_year:].strip(" .,;:") and (following or not emphasized):
            # APA-like "Authors (2021). Title. *Venue*": the sentence after the year.
            rest = body[after_year:].lstrip(" .,;:")
            sentence = re.split(r"(?<=[^A-Z])\.\s", rest, maxsplit=1)[0]
            if len(sentence.split()) >= 2:
                title_start, title = after_year, sentence
        if not title and not YEAR_PAREN_RE.search(body):
            vancouver = _vancouver_title(body)       # LeCun Y, Bengio Y. Title. Journal. 2015;
            if vancouver:
                title_start, title = vancouver
        if not title and emphasized:
            title_start, title = emphasized[0]         # Author, *Title*, Publisher, 2020.
    plain = (lambda value: latex_to_plain(value)) if latex else (
        lambda value: " ".join(re.sub(r"[*_]{1,3}", "", value).split()))
    if title:
        fields["title"] = plain(title).strip(" .,;:")
    if year_match and year_match.group(1):
        fields["year"] = year_match.group(1)
    ends = [position for position in (year_match.start() if year_match else None, title_start)
            if position is not None]
    authors = plain(body[:min(ends)]).strip(" .,;:(") if ends else ""
    if authors:
        fields["author"] = authors

    text_ids = latex_to_plain(body) if latex else body
    for url in urls:
        doi_url = DOI_URL_RE.match(url)
        arxiv_url = ARXIV_URL_RE.search(url)
        if doi_url and "doi" not in fields:
            fields["doi"] = urllib.parse.unquote(_trim_identifier(doi_url.group(1)))
        elif arxiv_url and "arxiv" not in fields:
            fields["arxiv"] = re.sub(r"\.pdf$", "", _trim_identifier(arxiv_url.group(1))).rstrip("/")
        elif "doi_inferred" not in fields and DOI_IN_URL_RE.search(url):
            found = urllib.parse.unquote(DOI_IN_URL_RE.search(url).group(1))
            found = re.sub(r"/(?:full|abstract|pdf|epdf|html|meta|references)/?$", "", found)
            fields["doi_inferred"] = _trim_identifier(found)
        elif "url" not in fields:
            fields["url"] = url
    if "doi" not in fields:
        explicit = DOI_TEXT_RE.search(text_ids) or BARE_DOI_RE.search(text_ids)
        if explicit:
            fields["doi"] = _trim_identifier(explicit.group(1))
    if "arxiv" not in fields:
        explicit = ARXIV_TEXT_RE.search(text_ids)
        if explicit:
            fields["arxiv"] = _trim_identifier(explicit.group(1))
    if urls:
        fields["urls"] = " ".join(urls)
    return fields


def parse_reference_list(path: Path, text: str) -> list[dict[str, object]]:
    latex = path.suffix.lower() in LATEX_SUFFIXES
    lines = text.splitlines()
    items: list[tuple[int, list[str], str]] = []   # first line, text lines, \bibitem key
    if latex:
        clean = [_strip_comment_keep_urls(line) for line in lines]
        has_bibliography = any("\\begin{thebibliography}" in line for line in clean)
        heading = next((i for i, line in enumerate(clean) if LATEX_REF_HEADING_RE.search(line)), None)
        start = 0 if heading is None or has_bibliography else heading
        current: tuple[int, list[str], str] | None = None
        inside = not has_bibliography
        for number in range(start, len(clean)):
            line = clean[number]
            if has_bibliography:
                if "\\begin{thebibliography}" in line:
                    inside = True
                if not inside:
                    continue
            if not line.strip() or LATEX_LIST_END_RE.search(line):
                if current:
                    items.append(current)
                    current = None
                if LATEX_LIST_END_RE.search(line) and has_bibliography and "thebibliography" in line:
                    inside = False
                continue
            position = 0
            for match in LATEX_LIST_ITEM_RE.finditer(line):
                if has_bibliography and not match.group(0).startswith("\\bibitem"):
                    continue
                if current:
                    current[1].append(line[position:match.start()])
                    items.append(current)
                current = (number + 1, [], match.group(1) or "")
                position = match.end()
            if current:
                current[1].append(line[position:])
        if current:
            items.append(current)
    else:
        start, stop, level = 0, len(lines), 0
        for index, line in enumerate(lines):
            heading = MD_HEADING_RE.match(line)
            plain_heading = re.fullmatch(r"\s*" + REF_HEADING_WORDS + r"\s*:?\s*", line, re.IGNORECASE)
            if (heading and re.search(REF_HEADING_WORDS, heading.group(2), re.IGNORECASE)) or plain_heading:
                start, level = index + 1, len(heading.group(1)) if heading else 0
                for later in range(start, len(lines)):
                    other = MD_HEADING_RE.match(lines[later])
                    if other and level and len(other.group(1)) <= level:
                        stop = later
                        break
                break
        current = None
        in_fence = False
        paragraphs: list[tuple[int, list[str], str]] = []
        paragraph: tuple[int, list[str], str] | None = None
        for number in range(start, stop):
            line = lines[number]
            if line.strip().startswith(("```", "~~~")):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            item = MD_REF_ITEM_RE.match(line)
            if not line.strip() or MD_HEADING_RE.match(line):
                if current:
                    items.append(current)
                    current = None
                if paragraph:
                    paragraphs.append(paragraph)
                    paragraph = None
                continue
            if item:
                if current:
                    items.append(current)
                current = (number + 1, [item.group(1)], "")
            elif current:
                current[1].append(line.strip())
            if paragraph is None:
                paragraph = (number + 1, [line.strip()], "")
            else:
                paragraph[1].append(line.strip())
        if current:
            items.append(current)
        if paragraph:
            paragraphs.append(paragraph)
        if not items and start > 0:
            items = paragraphs   # a References section written as one paragraph per entry
    entries: list[dict[str, object]] = []
    for ordinal, (line, parts, bibkey) in enumerate(items, start=1):
        raw = " ".join(part.strip() for part in parts if part.strip())
        if not raw:
            continue
        fields = parse_reference_text(raw, latex)
        title = fields.get("title", "")
        short = title if len(title) <= 50 else title[:47] + "..."
        name = f'entry {ordinal}' + (f' ("{short}")' if short else "")
        entries.append({"key": bibkey or f"entry {ordinal}", "type": "reference", "fields": fields,
                        "line": line, "source": path, "name": name, "bibitem": bibkey})
    return entries


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


def normalize_doi(value: str) -> str:
    normalized = value.strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "https://dx.doi.org/",
                   "http://dx.doi.org/", "doi:"):
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix):]
            break
    return normalized.strip().rstrip(".,;")


def normalize_title(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", latex_to_plain(value)).casefold()
    return " ".join(re.findall(r"[a-z0-9]+", decomposed))


def valid_isbn(value: str) -> bool:
    digits = re.sub(r"[^0-9Xx]", "", value)
    if len(digits) == 10 and re.fullmatch(r"[0-9]{9}[0-9Xx]", digits):
        total = sum((10 - i) * (10 if c in "xX" else int(c)) for i, c in enumerate(digits))
        return total % 11 == 0
    if len(digits) == 13 and digits.isdigit():
        return sum(int(c) * (1 if i % 2 == 0 else 3) for i, c in enumerate(digits)) % 10 == 0
    return False


def valid_arxiv(value: str) -> bool:
    """New form YYMM.NNNN(N) (four digits until 2014, five from 2015), optional version; old
    form archive(.SC)/YYMMNNN, 1991 to 2007."""
    match = NEW_ARXIV_RE.fullmatch(value)
    if match:
        year, month, number = int(match.group(1)), int(match.group(2)), match.group(3)
        if not 1 <= month <= 12 or (year, month) < (7, 4):
            return False
        return len(number) == (4 if year < 15 else 5)
    match = OLD_ARXIV_RE.fullmatch(value)
    if match:
        year, month = int(match.group(3)), int(match.group(4))
        return 1 <= month <= 12 and (year >= 91 or year <= 7)
    return False


def arxiv_base(value: str) -> str:
    return re.sub(r"v\d+$", "", value.strip())


def entry_identifiers(entry: dict[str, object]) -> dict[str, object]:
    """Collect the identifiers of a bibliography or reference-list entry."""
    fields: dict[str, str] = entry["fields"]  # type: ignore[assignment]
    ids: dict[str, object] = {"doi": "", "doi_inferred": False, "arxiv": "", "urls": []}
    urls: list[str] = []
    for name in ("url",):
        if fields.get(name):
            urls.append(fields[name].strip())
    for name in ("howpublished", "note"):
        for match in LINK_RE.finditer(fields.get(name, "").replace("\\url", " ")):
            urls.append(_trim_identifier(match.group(0)))
    urls += [url for url in fields.get("urls", "").split() if url]
    urls = list(dict.fromkeys(urls))
    ids["urls"] = urls
    doi = fields.get("doi", "")
    if doi:
        ids["doi"] = normalize_doi(doi)
    else:
        for url in urls:
            found = DOI_URL_RE.match(url)
            if found:
                ids["doi"] = normalize_doi(urllib.parse.unquote(found.group(1)))
                break
        else:
            inferred = fields.get("doi_inferred", "")
            if not inferred:
                for url in urls:
                    match = DOI_IN_URL_RE.search(url)
                    if match and "arxiv.org" not in url.lower():
                        inferred = re.sub(r"/(?:full|abstract|pdf|epdf|html|meta)/?$", "",
                                          urllib.parse.unquote(match.group(1)))
                        break
            if inferred:
                ids["doi"], ids["doi_inferred"] = normalize_doi(inferred), True
    arxiv = fields.get("arxiv", "") or fields.get("arxivid", "")
    eprint = fields.get("eprint", "")
    prefix = (fields.get("archiveprefix", "") or fields.get("eprinttype", "")).lower()
    if not arxiv and eprint and (prefix == "arxiv" or (not prefix and (
            re.match(r"\d{4}\.\d", eprint) or re.match(r"[a-z-]+(?:\.[A-Z]{2})?/\d", eprint)))):
        arxiv = eprint
    if not arxiv:
        for name in ("journal", "journaltitle", "note", "howpublished", "number", "archive_location"):
            match = ARXIV_TEXT_RE.search(fields.get(name, ""))
            if match:
                arxiv = _trim_identifier(match.group(1))
                break
    if not arxiv:
        for url in urls:
            match = ARXIV_URL_RE.search(url)
            if match:
                arxiv = re.sub(r"\.pdf$", "", _trim_identifier(match.group(1))).rstrip("/")
                break
    doi_value = str(ids["doi"])
    arxiv_doi = ARXIV_DOI_RE.match(doi_value)
    if arxiv_doi and not arxiv:
        arxiv = arxiv_doi.group(1)
    ids["arxiv"] = re.sub(r"^arxiv:\s*", "", arxiv.strip(), flags=re.IGNORECASE)
    return ids


def entry_name(entry: dict[str, object]) -> str:
    return str(entry.get("name") or f'"{entry["key"]}"')


def check_entries(entries: list[dict[str, object]], report: Report) -> dict[str, dict[str, object]]:
    """Format checks for bibliography or reference-list entries. Returns entries by key."""
    by_key: dict[str, dict[str, object]] = {}
    seen_doi: dict[str, str] = {}
    seen_title: dict[str, str] = {}
    seen_arxiv: dict[str, str] = {}
    this_year = datetime.date.today().year
    for entry in entries:
        key, line, source = str(entry["key"]), int(entry["line"]), entry["source"]
        name = entry_name(entry)
        fields: dict[str, str] = entry["fields"]  # type: ignore[assignment]
        reference = entry["type"] == "reference"
        if not reference:
            if key in by_key:
                report.add(source, line, "error", "DUPLICATE_KEY", f'"{key}" is defined more than once')
                continue
            by_key[key] = entry
        else:
            by_key[f"{source}:{line}:{key}"] = entry
        ids = entry_identifiers(entry)
        entry["ids"] = ids
        if "crossref" in fields or "xdata" in fields:
            continue
        if not fields.get("title") and not fields.get("booktitle"):
            report.add(source, line, "warning", "MISSING_FIELD", f'{name} has no title')
        if not any(fields.get(field) for field in ("author", "editor", "organization", "institution")):
            report.add(source, line, "warning", "MISSING_FIELD", f'{name} has no author or editor')
        year_text = fields.get("year") or fields.get("date") or ""
        years = [int(y) for y in YEAR_RE.findall(year_text)]
        if not year_text:
            if entry["type"] not in NO_YEAR_TYPES:
                report.add(source, line, "warning", "MISSING_FIELD", f'{name} has no year or date')
        elif years and (years[0] > this_year + 1 or years[0] < 1500):
            report.add(source, line, "warning", "IMPLAUSIBLE_YEAR", f'{name} has year {years[0]}')
        for alternatives in VENUE_FIELDS.get(str(entry["type"]), ()):
            if not any(fields.get(field) for field in alternatives):
                report.add(source, line, "warning", "MISSING_FIELD",
                           f'{name} (@{entry["type"]}) has no {" or ".join(alternatives)}')
        title = normalize_title(fields.get("title", ""))
        if title:
            if title in seen_title:
                report.add(source, line, "warning", "POSSIBLE_DUPLICATE_TITLE",
                           f'{name} has the same title as {seen_title[title]}')
            else:
                seen_title[title] = name
        doi = str(ids["doi"])
        if doi:
            if not DOI_RE.fullmatch(doi):
                report.add(source, line, "error", "MALFORMED_DOI", f'{name}: DOI does not look like 10.xxxx/...')
                ids["doi"] = ""
            elif doi in seen_doi:
                report.add(source, line, "warning", "DUPLICATE_DOI",
                           f'{name} has the same DOI as {seen_doi[doi]}')
            else:
                seen_doi[doi] = name
        arxiv = str(ids["arxiv"])
        if arxiv:
            if not valid_arxiv(arxiv):
                report.add(source, line, "warning", "MALFORMED_ARXIV_ID",
                           f'{name}: arXiv identifier "{arxiv}" is neither YYMM.NNNNN nor '
                           "archive/YYMMNNN")
                ids["arxiv"] = ""
            elif arxiv_base(arxiv) in seen_arxiv:
                report.add(source, line, "warning", "DUPLICATE_ARXIV",
                           f'{name} has the same arXiv identifier as {seen_arxiv[arxiv_base(arxiv)]}')
            else:
                seen_arxiv[arxiv_base(arxiv)] = name
        isbn = fields.get("isbn", "")
        if isbn and not all(valid_isbn(part) for part in re.split(r"[,;]|\s{2,}", isbn) if part.strip()):
            report.add(source, line, "warning", "MALFORMED_ISBN", f'{name}: ISBN fails its checksum')
        url = fields.get("url", "")
        if url and not URL_RE.fullmatch(url.strip()):
            report.add(source, line, "warning", "MALFORMED_URL", f'{name}: URL is not http(s)')
        if not (ids["doi"] or ids["arxiv"] or ids["urls"] or isbn or fields.get("pmid")
                or fields.get("eprint")):
            report.add(source, line, "warning", "NO_IDENTIFIER",
                       f"{name} has no DOI, arXiv identifier, ISBN or URL: it cannot be checked "
                       "mechanically; verify it by search")
    return by_key


def read_ledger(path_value: str) -> tuple[Path, list[dict[str, str]]]:
    path, text = read_text(path_value, {".csv"})
    reader = csv.DictReader(io.StringIO(text, newline=""))
    names = {(name or "").strip().lower(): name for name in (reader.fieldnames or [])}
    key_column = next((names[n] for n in ("key", "citekey", "source_id", "id") if n in names), None)
    status_column = next((names[n] for n in ("status", "verification_status") if n in names), None)
    if key_column is None or status_column is None:
        raise InputError(f"{path}: the ledger needs the columns key and status")
    rows: list[dict[str, str]] = []
    for number, row in enumerate(reader, start=2):
        rows.append({
            "key": (row.get(key_column) or "").strip(),
            "status": (row.get(status_column) or "").strip().lower(),
            "locator": (row.get(names.get("locator", "")) or "").strip() if "locator" in names else "",
            "has_locator_column": "yes" if "locator" in names else "",
            "line": str(number),
        })
    return path, rows


def check_ledger(path: Path, rows: list[dict[str, str]], cited: dict[str, tuple[Path, int]],
                 bibliography: dict[str, dict[str, object]] | None, report: Report) -> None:
    ledger: dict[str, dict[str, str]] = {}
    for row in rows:
        if not row["key"]:
            continue
        if row["key"] in ledger:
            report.add(path, int(row["line"]), "warning", "DUPLICATE_LEDGER_KEY",
                       f'"{row["key"]}" appears more than once')
            continue
        ledger[row["key"]] = row
        if bibliography is not None and row["key"] not in bibliography:
            report.add(path, int(row["line"]), "info", "LEDGER_KEY_NOT_IN_BIBLIOGRAPHY",
                       f'"{row["key"]}" is in the ledger but not in the bibliography')
    for key, (source, line) in cited.items():
        row = ledger.get(key)
        if row is None:
            report.add(source, line, "warning", "CITED_SOURCE_NOT_IN_LEDGER",
                       f'"{key}" has no ledger row, so nothing records that it was opened and checked')
        elif not row["status"].startswith("verified"):
            report.add(source, line, "warning", "CITED_SOURCE_NOT_VERIFIED",
                       f'"{key}" has ledger status "{row["status"] or "empty"}"')
        elif row["has_locator_column"] and not row["locator"]:
            report.add(path, int(row["line"]), "info", "LEDGER_ROW_WITHOUT_LOCATOR",
                       f'"{key}" is marked verified but has no page, section or table locator')


# ---------------------------------------------------------------------------
# Online verification
# ---------------------------------------------------------------------------


def compare_title(value: str) -> str:
    """Lowercase, strip accents, LaTeX, HTML tags, HTML entities and punctuation."""
    value = html.unescape(re.sub(r"<[^>]{1,100}>", " ", value))
    decomposed = unicodedata.normalize("NFKD", latex_to_plain(value))
    decomposed = "".join(c for c in decomposed if not unicodedata.combining(c)).casefold()
    return " ".join(re.findall(r"[a-z0-9]+", decomposed))[:300]


def _ratio(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b).ratio() if a and b else 0.0


def title_similarity(entry_title: str, record_titles: list[str]) -> tuple[float, float]:
    """Return (full, main): the best SequenceMatcher ratio of the entry's full title against
    each record title and its main title (before a colon, question mark or semicolon), and
    the best ratio of the entry's main title against the record titles.

    Only the full ratio can confirm a reference: an entry may leave out a subtitle the record
    has, but an entry whose subtitle the record lacks ("Deep learning: <invented subtitle>")
    must not match on the shared main title. The main ratio only tells a differing subtitle
    from an unrelated title."""
    mine = compare_title(entry_title)
    mine_main = compare_title(re.split(r"[:?;]\s", entry_title, maxsplit=1)[0])
    full = main = 0.0
    for title in record_titles:
        if not title:
            continue
        theirs = {compare_title(title), compare_title(re.split(r"[:?;]\s", title, maxsplit=1)[0])}
        for b in theirs:
            full = max(full, _ratio(mine, b))
            main = max(main, _ratio(mine_main, b))
    return full, max(full, main)


def surname_tokens(value: str) -> list[str]:
    decomposed = unicodedata.normalize("NFKD", latex_to_plain(value))
    decomposed = "".join(c for c in decomposed if not unicodedata.combining(c)).casefold()
    return re.findall(r"[a-z]+", decomposed)


SUFFIXES_OF_NAMES = {"jr", "sr", "ii", "iii", "iv"}


INITIALS_RE = re.compile(r"^(?:[A-Z]\.?(?:-[A-Z]\.?)?\s*)+(?:,|$)")


def first_surname(authors: str, bibtex: bool) -> str:
    """The first author's surname, from BibTeX ("Lee, Ana and Osei, Kofi"), CSL ("Lee; Osei")
    or free-form author strings ("Rao Surapaneni, Miku Jha and ...", "Kingma, D. P., & Ba,
    J.", "Kingma, Ba", "Mnih et al.")."""
    text = latex_to_plain(authors).strip()
    separators = r"\s+and\s+|;" if bibtex else r"\bet\s+al\b|;|\s+and\s+|\s*&\s*|\s+/\s+"
    first = re.split(separators, text, maxsplit=1, flags=re.IGNORECASE)[0].strip(" .,")
    vancouver = re.match(r"(.+?)\s+[A-Z]{1,4}$", first.split(",", 1)[0].strip())
    if not bibtex and vancouver and re.search(r"[a-z]", vancouver.group(1)):
        return vancouver.group(1)   # Vancouver/NLM: "LeCun Y, Bengio Y" or "Hochreiter S"
    if "," in first:
        head, tail = (part.strip() for part in first.split(",", 1))
        if bibtex or not tail or INITIALS_RE.match(tail) or len(head.split()) == 1:
            return head   # "Family, Given" or "Family, F." (a family name may be two words)
        first = head      # "Given Family, Given Family": the first full name
    words = [w for w in first.split() if w.lower().strip(".") not in SUFFIXES_OF_NAMES]
    return words[-1] if words else ""


def surname_matches(entry_surname: str, record_first: str) -> bool:
    mine, theirs = surname_tokens(entry_surname), surname_tokens(record_first)
    if not mine or not theirs:
        return False
    return mine[-1] in theirs or theirs[-1] in mine


class Online:
    """HTTP access with a rate limit, a response cache and a network-failure fuse."""

    def __init__(self, cache_path: Path | None, mailto: str | None) -> None:
        self.cache_path = cache_path
        self.mailto = mailto
        self.cache: dict[str, dict[str, object]] = {}
        self.records: dict[str, object] = {}
        self.cache_hits = 0
        self.requests = 0
        self.last = 0.0
        self.last_by_kind: dict[str, float] = {}
        self.failures_in_row = 0
        self.offline_reason = ""
        if cache_path and cache_path.is_file():
            try:
                data = json.loads(cache_path.read_text(encoding="utf-8"))
                self.cache = dict(data.get("responses", {}))
                self.records = dict(data.get("records", {}))
            except (OSError, ValueError, AttributeError) as exc:
                print(f"{TOOL}: ignoring unreadable cache {cache_path}: {exc}", file=sys.stderr)

    def save(self) -> None:
        if not self.cache_path:
            return
        data = {"tool": TOOL, "saved": datetime.datetime.now(datetime.timezone.utc).isoformat(
            timespec="seconds"), "responses": self.cache, "records": self.records}
        directory = self.cache_path.resolve().parent
        handle, temporary = tempfile.mkstemp(prefix=".refcache-", dir=directory)
        try:
            with os.fdopen(handle, "w", encoding="utf-8") as stream:
                json.dump(data, stream, ensure_ascii=False)
            os.replace(temporary, self.cache_path)
        except OSError as exc:
            print(f"{TOOL}: could not write the cache {self.cache_path}: {exc}", file=sys.stderr)
            try:
                os.unlink(temporary)
            except OSError:
                pass

    def _wait(self, kind: str) -> None:
        """At most one request per MIN_INTERVAL overall, and per service interval for arXiv
        and for Crossref search queries."""
        interval = {"arxiv": ARXIV_INTERVAL, "search": SEARCH_INTERVAL}.get(kind, 0.0)
        now = time.monotonic()
        delay = max(self.last + MIN_INTERVAL - now, self.last_by_kind.get(kind, -1e9) + interval - now)
        if delay > 0:
            time.sleep(delay)
        self.last = time.monotonic()
        self.last_by_kind[kind] = self.last

    def get(self, url: str, method: str = "GET", api: bool = True, read: bool = True,
            cache: bool = True) -> tuple[int | None, str, str]:
        """Return (HTTP status or None, body, error). api=True requests count toward the
        network-failure fuse; checks of arbitrary reference URLs do not."""
        key = f"{method} {url}"
        if key in self.cache:
            self.cache_hits += 1
            cached = self.cache[key]
            return int(cached["status"]), str(cached.get("body", "")), ""   # type: ignore[arg-type]
        if api and self.offline_reason:
            return None, "", self.offline_reason
        full = url
        if self.mailto and "api.crossref.org" in url:
            full += ("&" if "?" in url else "?") + "mailto=" + urllib.parse.quote(self.mailto)
        kind = ("arxiv" if "arxiv.org" in urllib.parse.urlsplit(url).netloc else
                "search" if url.startswith("https://api.crossref.org/works?") else "other")
        status: int | None = None
        body = b""
        for attempt in range(3):
            self._wait(kind)
            self.requests += 1
            try:
                request = urllib.request.Request(full, method=method, headers={
                    "User-Agent": USER_AGENT, "Accept": "*/*"})
                with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                    status = response.status
                    body = response.read(MAX_RESPONSE_BYTES if read else 0) if method != "HEAD" else b""
            except urllib.error.HTTPError as exc:
                status = exc.code
                try:
                    body = exc.read(65536) if read else b""
                except OSError:
                    body = b""
                if status in (429, 500, 502, 503, 504) and attempt < 2:
                    retry = exc.headers.get("Retry-After", "") if exc.headers else ""
                    time.sleep(min(10.0, float(retry)) if retry.isdigit() else 2.0 * (attempt + 1))
                    continue
            except (urllib.error.URLError, TimeoutError, OSError, ValueError,
                    http.client.HTTPException) as exc:
                reason = getattr(exc, "reason", None) or exc
                if api:
                    self.failures_in_row += 1
                    if self.failures_in_row >= 3:
                        self.offline_reason = f"skipped after repeated network failures ({reason})"
                return None, "", f"network failure ({reason})"
            break
        if api:
            self.failures_in_row = 0
        text = body.decode("utf-8", errors="replace")
        if cache and status is not None and (
                status in (200, 404, 410) or (not api and status < 500 and status != 429)):
            self.cache[key] = {"status": status, "body": text if read else ""}
        return status, text, ""


def display_title(value: str) -> str:
    """A record title for display: HTML tags removed, entities decoded, whitespace collapsed."""
    return " ".join(html.unescape(re.sub(r"<[^>]{1,100}>", "", value)).split())


def crossref_record(message: dict[str, object]) -> dict[str, object]:
    titles = [display_title(str(t)) for t in (message.get("title") or [])]   # type: ignore[union-attr]
    subtitles = [display_title(str(t)) for t in (message.get("subtitle") or [])]   # type: ignore[union-attr]
    variants = list(titles)
    if titles and subtitles:
        variants.append(f"{titles[0]}: {subtitles[0]}")
    for extra in ("short-title", "original-title"):
        variants += [str(t) for t in (message.get(extra) or [])]   # type: ignore[union-attr]
    people = message.get("author") or message.get("editor") or []
    authors = [str(p.get("family") or p.get("name") or "") for p in people if isinstance(p, dict)]  # type: ignore[union-attr]
    years: list[int] = []
    for field in ("issued", "published-print", "published-online", "published"):
        parts = (message.get(field) or {}).get("date-parts") or []   # type: ignore[union-attr]
        if parts and parts[0] and parts[0][0]:
            years.append(int(parts[0][0]))
    return {"title": titles[0] if titles else "", "titles": variants, "authors": authors,
            "years": sorted(set(years)), "doi": str(message.get("DOI", "")), "source": "Crossref"}


def datacite_record(data: dict[str, object]) -> dict[str, object]:
    attributes = (data.get("data") or {}).get("attributes") or {}   # type: ignore[union-attr]
    titles = [display_title(str(t.get("title", ""))) for t in attributes.get("titles", [])
              if isinstance(t, dict)]
    authors = [str(c.get("familyName") or c.get("name") or "") for c in attributes.get("creators", [])
               if isinstance(c, dict)]
    year = attributes.get("publicationYear")
    return {"title": titles[0] if titles else "", "titles": titles, "authors": authors,
            "years": [int(year)] if str(year or "").isdigit() else [],
            "doi": str(attributes.get("doi", "")), "source": "DataCite"}


ATOM = "{http://www.w3.org/2005/Atom}"


def arxiv_records(text: str) -> dict[str, dict[str, object]]:
    records: dict[str, dict[str, object]] = {}
    root = ET.fromstring(text)
    for item in root.findall(f"{ATOM}entry"):
        title = " ".join((item.findtext(f"{ATOM}title") or "").split())
        identifier = item.findtext(f"{ATOM}id") or ""
        if title == "Error" or "/abs/" not in identifier:
            continue
        base = arxiv_base(identifier.split("/abs/", 1)[1])
        published = item.findtext(f"{ATOM}published") or ""
        authors = [" ".join((a.findtext(f"{ATOM}name") or "").split()) for a in item.findall(f"{ATOM}author")]
        records[base] = {"title": title, "titles": [title], "authors": authors,
                         "years": [int(published[:4])] if published[:4].isdigit() else [],
                         "arxiv": base, "source": "arXiv"}
    return records


def public_http_url(url: str) -> bool:
    try:
        parts = urllib.parse.urlsplit(url)
    except ValueError:
        return False
    if parts.scheme not in ("http", "https") or not parts.hostname or len(url) > 2000:
        return False
    host = parts.hostname.lower()
    if host == "localhost" or host.endswith((".local", ".localhost", ".internal")):
        return False
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        return True
    return address.is_global


class Verifier:
    def __init__(self, online: Online, report: Report) -> None:
        self.online = online
        self.report = report
        self.counts = {name: 0 for name in ONLINE_CLASSES}
        self.examples: dict[str, list[str]] = {name: [] for name in ONLINE_CLASSES}

    def emit(self, entry: dict[str, object], kind: str, severity: str, detail: str) -> None:
        self.counts[kind] += 1
        name = entry_name(entry)
        self.report.add(entry["source"], int(entry["line"]), severity, kind, f"{name}: {detail}")

    @staticmethod
    def meta(entry: dict[str, object]) -> tuple[str, str, int | None]:
        fields: dict[str, str] = entry["fields"]  # type: ignore[assignment]
        title = fields.get("title", "") or fields.get("booktitle", "")
        people = fields.get("author") or fields.get("editor") or ""
        surname = first_surname(people, bibtex=entry["type"] != "reference") if people else ""
        years = [int(y) for y in YEAR_RE.findall(fields.get("year") or fields.get("date") or "")]
        return title, surname, (years[0] if years else None)

    def judge(self, entry: dict[str, object], record: dict[str, object], via: str,
              search: bool = False) -> bool:
        """Compare an entry with a record and emit a finding. Returns False when a search
        result is not a confident match (nothing emitted)."""
        title, surname, year = self.meta(entry)
        ratio, main_ratio = (title_similarity(title, list(record["titles"]))  # type: ignore[arg-type]
                             if title else (0.0, 0.0))
        subtitle_only = bool(title) and ratio < TITLE_MATCH and main_ratio >= TITLE_MATCH
        authors: list[str] = list(record["authors"])  # type: ignore[arg-type]
        years: list[int] = list(record["years"])  # type: ignore[arg-type]
        author_ok = surname_matches(surname, authors[0]) if surname and authors else None
        year_ok = any(abs(year - y) <= 1 for y in years) if year and years else None
        shown = record.get("title") or "(no title)"
        if search and ((ratio < SEARCH_MATCH and main_ratio < SEARCH_MATCH)
                       or (author_ok is False and year_ok is False)):
            return False   # not confidently the same work: a different author and year
        problems = []
        if subtitle_only:
            problems.append(f'title "{shown}": the main titles match, but the entry\'s subtitle '
                            f"is not in the record (full-title similarity {ratio:.2f})")
        elif title and ratio < TITLE_MATCH:
            problems.append(f'title "{shown}" (similarity {ratio:.2f})')
        if author_ok is False:
            problems.append(f'first author {authors[0]} (entry: {surname})')
        if year_ok is False:
            problems.append(f"year {'/'.join(map(str, years))} (entry: {year})")
        if problems:
            severity = "error" if title and ratio < TITLE_MATCH and not subtitle_only else "warning"
            self.emit(entry, "METADATA_MISMATCH", severity,
                      f"{via} has a different " + "; ".join(problems)
                      + ("; check that the identifier belongs to this work" if severity == "error"
                         else "; check the subtitle against the source" if subtitle_only
                         else "; check the edition, version or author order"))
            return True
        if not title:
            self.emit(entry, "UNVERIFIED", "warning",
                      f'{via} resolves to "{shown}", but the entry has no title to compare')
            return True
        if author_ok is None and year_ok is None:
            self.emit(entry, "UNVERIFIED", "warning",
                      f'{via} matches the title (similarity {ratio:.2f}), but the entry has no '
                      "author or year to compare")
            return True
        checked = [f"title {ratio:.2f}"]
        if author_ok:
            checked.append(f"first author {surname}")
        if year_ok:
            checked.append(f"year {year}")
        self.emit(entry, "VERIFIED", "info", f"{via} matches ({', '.join(checked)})")
        return True

    def check_doi(self, entry: dict[str, object], doi: str, inferred: bool) -> None:
        url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/")
        status, text, error = self.online.get(url)
        label = f"DOI {doi}" + (" (taken from the URL)" if inferred else "")
        if error:
            self.emit(entry, "UNVERIFIED", "warning", f"{label} could not be looked up: {error}")
            return
        if status == 200:
            try:
                record = crossref_record(json.loads(text)["message"])
            except (ValueError, KeyError, TypeError):
                self.emit(entry, "UNVERIFIED", "warning", f"{label}: Crossref answered with unreadable data")
                return
            self.judge(entry, record, f"Crossref record for {label}")
            return
        if status not in (404, 410):
            self.emit(entry, "UNVERIFIED", "warning", f"{label}: Crossref answered HTTP {status}")
            return
        # Crossref has no record: ask doi.org which agency registered the DOI, if any.
        status, text, error = self.online.get("https://doi.org/ra/" + urllib.parse.quote(doi, safe="/"))
        if error or status != 200:
            self.emit(entry, "UNVERIFIED", "warning",
                      f"{label} is not in Crossref, and doi.org could not be asked "
                      f"({error or f'HTTP {status}'})")
            return
        try:
            answer = json.loads(text)[0]
        except (ValueError, IndexError, KeyError, TypeError):
            answer = {}
        agency = str(answer.get("RA", "")) if isinstance(answer, dict) else ""
        if not agency:
            state = str(answer.get("status", "unknown")) if isinstance(answer, dict) else "unknown"
            if inferred:
                self.emit(entry, "UNVERIFIED", "warning",
                          f"{label} does not exist (doi.org: {state}); the link may still work, "
                          "so verify the work by search")
            else:
                self.emit(entry, "NOT_FOUND", "error",
                          f"{label} does not resolve (Crossref: no record; doi.org: {state})")
            return
        if agency == "DataCite":
            status, text, error = self.online.get(
                "https://api.datacite.org/dois/" + urllib.parse.quote(doi, safe="/"))
            if status == 200 and not error:
                try:
                    self.judge(entry, datacite_record(json.loads(text)), f"DataCite record for {label}")
                    return
                except (ValueError, TypeError, AttributeError):
                    pass
            self.emit(entry, "UNVERIFIED", "warning",
                      f"{label} is registered with DataCite, but its record could not be read "
                      f"({error or f'HTTP {status}'})")
            return
        self.emit(entry, "UNVERIFIED", "warning",
                  f"{label} is registered with {agency}; this checker compares Crossref, DataCite "
                  "and arXiv metadata only, so verify it by hand")

    def lookup_arxiv(self, identifiers: list[str]) -> dict[str, str]:
        """Fetch arXiv records into the cache; return an error per identifier that failed."""
        errors: dict[str, str] = {}
        wanted = [i for i in dict.fromkeys(arxiv_base(i) for i in identifiers)
                  if f"arxiv:{i}" not in self.online.records]
        for start in range(0, len(wanted), ARXIV_BATCH):
            batch = wanted[start:start + ARXIV_BATCH]
            url = ("https://export.arxiv.org/api/query?id_list=" + ",".join(batch)
                   + f"&max_results={len(batch)}")
            status, text, error = self.online.get(url, cache=False)   # records are cached
            if error or status != 200:
                for identifier in batch:
                    errors[identifier] = error or f"arXiv answered HTTP {status}"
                continue
            try:
                found = arxiv_records(text)
            except ET.ParseError:
                for identifier in batch:
                    errors[identifier] = "arXiv answered with unreadable XML"
                continue
            for identifier in batch:
                if identifier in found:
                    self.online.records[f"arxiv:{identifier}"] = found[identifier]
                elif len(batch) == 1:
                    self.online.records[f"arxiv:{identifier}"] = None
            missing = [identifier for identifier in batch if identifier not in found]
            if len(batch) > 1:
                for identifier in missing:   # confirm one by one before calling it missing
                    errors.update(self.lookup_arxiv([identifier]))
        return errors

    def check_arxiv(self, entry: dict[str, object], identifier: str, error: str) -> None:
        base = arxiv_base(identifier)
        if error:
            self.emit(entry, "UNVERIFIED", "warning", f"arXiv:{identifier} could not be looked up: {error}")
            return
        record = self.online.records.get(f"arxiv:{base}")
        if record is None:
            self.emit(entry, "NOT_FOUND", "error", f"arXiv:{identifier} does not exist (arXiv API: no record)")
            return
        self.judge(entry, record, f"arXiv record {base}")  # type: ignore[arg-type]

    def search(self, entry: dict[str, object]) -> bool:
        """Crossref bibliographic search; True when a finding was emitted."""
        title, surname, _ = self.meta(entry)
        if not title:
            return False
        query = urllib.parse.quote_plus(f"{title} {surname}".strip()[:300])
        url = ("https://api.crossref.org/works?query.bibliographic=" + query + "&rows=3"
               "&select=DOI,title,subtitle,author,editor,issued,published-print,published-online,type")
        status, text, error = self.online.get(url)
        if error or status != 200:
            entry["search_error"] = error or f"Crossref search answered HTTP {status}"
            return False
        try:
            items = json.loads(text)["message"]["items"]
        except (ValueError, KeyError, TypeError):
            entry["search_error"] = "Crossref search answered with unreadable data"
            return False
        records = [crossref_record(item) for item in items if isinstance(item, dict)]
        if not records:
            entry["search_best"] = "no candidates"
            return False
        _, surname, year = self.meta(entry)

        def rank(record: dict[str, object]) -> tuple[bool, bool, bool, float]:
            ratio = max(title_similarity(title, list(record["titles"])))  # type: ignore[arg-type]
            authors: list[str] = list(record["authors"])  # type: ignore[arg-type]
            years: list[int] = list(record["years"])  # type: ignore[arg-type]
            return (ratio >= SEARCH_MATCH,
                    bool(year and any(abs(year - y) <= 1 for y in years)),
                    bool(surname and authors and surname_matches(surname, authors[0])), ratio)

        best = max(records, key=rank)
        ratio = rank(best)[3]
        entry["search_best"] = f'best candidate "{best["title"]}", similarity {ratio:.2f}'
        return self.judge(entry, best, f"Crossref search (DOI {best['doi']})", search=True)

    @staticmethod
    def search_outcome(entry: dict[str, object]) -> str:
        if entry.get("search_error"):
            return f"the Crossref search failed: {entry['search_error']}"
        if entry.get("search_best"):
            return f"no confident Crossref match ({entry['search_best']})"
        return "no title to search for"

    def check_url(self, entry: dict[str, object], url: str) -> None:
        if not public_http_url(url):
            self.emit(entry, "UNVERIFIED", "warning",
                      f"{url} was not requested (not a public http or https address)")
            return
        status, _, error = self.online.get(url, method="HEAD", api=False, read=False)
        if status is None or status >= 400:
            status, _, error = self.online.get(url, method="GET", api=False, read=False)
        searched = self.search_outcome(entry)
        if status is not None and status < 400:
            self.emit(entry, "URL_ONLY", "warning",
                      f"{url} resolves (HTTP {status}), but there is no DOI or arXiv identifier "
                      f"and {searched}; a person must verify the work and its metadata")
        else:
            if status in (401, 403, 429):
                state = (f"refuses automated access (HTTP {status}; the site or a proxy may block "
                         "it), so check it in a browser")
            elif status in (404, 410):
                state = f"was not found (HTTP {status})"
            else:
                state = f"does not resolve ({error or f'HTTP {status}'})"
            self.emit(entry, "UNVERIFIED", "warning",
                      f"no DOI or arXiv identifier, {searched}, and {url} {state}")

    def run(self, entries: list[dict[str, object]], limit: int | None) -> dict[str, int]:
        chosen: list[dict[str, object]] = []
        skipped = 0
        for entry in entries:
            ids: dict[str, object] = entry.get("ids", {})  # type: ignore[assignment]
            fields: dict[str, str] = entry["fields"]  # type: ignore[assignment]
            if not (ids.get("doi") or ids.get("arxiv") or ids.get("urls") or fields.get("title")):
                self.emit(entry, "UNVERIFIED", "warning",
                          "no DOI, arXiv identifier, URL or readable title to look up; verify "
                          "it by search")
                continue
            if limit is not None and len(chosen) >= limit:
                skipped += 1
                continue
            chosen.append(entry)
        arxiv_errors = self.lookup_arxiv([str(e["ids"]["arxiv"]) for e in chosen  # type: ignore[index]
                                          if e["ids"]["arxiv"] and not e["ids"]["doi"]])  # type: ignore[index]
        for entry in chosen:
            ids = entry["ids"]  # type: ignore[assignment]
            if ids["doi"]:
                self.check_doi(entry, str(ids["doi"]), bool(ids["doi_inferred"]))
            elif ids["arxiv"]:
                self.check_arxiv(entry, str(ids["arxiv"]), arxiv_errors.get(arxiv_base(str(ids["arxiv"])), ""))
            elif self.search(entry):
                pass
            elif ids["urls"]:
                self.check_url(entry, str(ids["urls"][0]))  # type: ignore[index]
            else:
                self.emit(entry, "UNVERIFIED", "warning",
                          f"no DOI, arXiv identifier or URL, and {self.search_outcome(entry)}; "
                          "verify it by search")
        self.online.save()
        return {"looked_up": len(chosen), "not_looked_up": skipped,
                "requests": self.online.requests, "from_cache": self.online.cache_hits, **self.counts}


# ---------------------------------------------------------------------------
# Command line
# ---------------------------------------------------------------------------


def rule_table() -> str:
    width = max(len(rule[0]) for rule in RULES)
    return "\n".join(f"  {code:<{width}}  {severity.replace('info', 'note'):<13}  {text}"
                     for code, severity, text in RULES)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit citation keys against a bibliography (.bib or CSL .json), check "
        "bibliography entries and free-form reference lists, and with --online look each "
        "reference up at Crossref, arXiv and DataCite. A clean report does not show that a "
        "reference supports the sentence that cites it.",
        epilog="modes (they combine):\n"
        "  citation keys   manuscripts are scanned for natbib and biblatex \\cite commands "
        "(starred,\n                  several keys, pre- and postnotes, multicite) and Pandoc "
        "[@key] groups\n"
        "  bibliography    every .bib or .json file (positional or --bib) is checked and "
        "compared\n                  with the cited keys; an uncited entry is a note unless "
        "\\nocite{*}\n"
        "  reference list  --reference-list parses free-form \\item, \\bibitem, numbered or "
        "bulleted\n                  entries (after a References/Bibliography/Sources heading "
        "when present)\n"
        "  ledger          --ledger compares cited keys with a verification ledger\n"
        "  online          --online looks entries up (Crossref, arXiv, doi.org, DataCite; "
        "HEAD/GET for\n                  bare URLs), 20 s timeout, about 5 requests/s (searches "
        "1/s, arXiv 1/3 s),\n                  generic User-Agent; --cache, --max-online and --mailto "
        "apply only with --online\n\n"
        "exit status: 0 no error-level finding, 1 at least one, 2 input rejected or "
        "invalid option. Network failures are warnings.\n\nrules (id, severity, description):\n"
        + rule_table(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("files", nargs="*", metavar="FILE",
                        help="manuscripts (.tex, .texview, .md, .markdown, .txt) and "
                        "bibliographies (.bib, .json)")
    parser.add_argument("--bib", action="append", default=[], metavar="FILE",
                        help="bibliography file (.bib or CSL .json); repeat for several")
    parser.add_argument("--reference-list", action="append", default=[], metavar="FILE",
                        help="a free-form reference list (LaTeX \\item or \\bibitem list, or a "
                        "Markdown or text list) to parse and check; repeatable")
    parser.add_argument("--ledger", metavar="CSV", help="source ledger with key and status columns")
    parser.add_argument("--skip-missing", action="store_true",
                        help="skip manuscript and reference-list files that do not exist yet, with "
                        "a notice on standard error, instead of rejecting the run (exit 1 if every "
                        "file is missing)")
    parser.add_argument("--no-bare-keys", action="store_true",
                        help="ignore @key outside [ ] in Markdown (for text with handles)")
    parser.add_argument("--online", action="store_true",
                        help="look references up at Crossref, arXiv, doi.org and DataCite, and "
                        "request URLs that have no DOI or arXiv identifier (off by default)")
    parser.add_argument("--max-online", type=int, metavar="N",
                        help="look up at most N references (default: all)")
    parser.add_argument("--cache", metavar="FILE",
                        help="JSON file that keeps online responses between runs")
    parser.add_argument("--mailto", metavar="ADDRESS",
                        help="e-mail address sent to Crossref for its polite pool (not sent "
                        "unless given)")
    parser.add_argument("--min-severity", choices=SEVERITIES + ("note",), default="info",
                        help="lowest severity to print (default: info, the same as note)")
    parser.add_argument("--json", action="store_true", help="print a JSON report")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_intermixed_args(argv)
    manuscripts = [name for name in args.files if Path(name).suffix.lower() not in BIB_SUFFIXES]
    bib_files = [name for name in args.files if Path(name).suffix.lower() in BIB_SUFFIXES] + args.bib
    if not (manuscripts or bib_files or args.reference_list):
        parser.error("give at least one manuscript, bibliography or --reference-list file")
    if args.max_online is not None and args.max_online < 0:
        parser.error("--max-online must be zero or more")
    if args.mailto and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", args.mailto):
        parser.error("--mailto needs an e-mail address")
    min_severity = SEVERITY_ALIASES.get(args.min_severity, args.min_severity)
    if args.skip_missing:
        absent = [n for n in manuscripts + args.reference_list if not os.path.lexists(n)]
        if absent:
            print(f"{TOOL}: skipped missing file(s): {', '.join(absent)}", file=sys.stderr)
        manuscripts = [n for n in manuscripts if n not in absent]
        args.reference_list = [n for n in args.reference_list if n not in absent]
        if not (manuscripts or bib_files or args.reference_list):
            print(f"{TOOL}: nothing checked: every file given is missing (check the paths)", file=sys.stderr)
            return 1
    report = Report()
    cited: Uses = {}
    bare: Uses = {}
    bibitems: set[str] = set()
    cite_all = False
    references: list[dict[str, object]] = []
    try:
        for name in manuscripts:
            path, text = read_text(name, MANUSCRIPT_SUFFIXES)
            found, found_bare, items, everything = scan_manuscript(
                path, text, report, bare_keys=not args.no_bare_keys)
            for key, where in found.items():
                cited.setdefault(key, where)
            for key, where in found_bare.items():
                bare.setdefault(key, where)
            bibitems |= items
            cite_all = cite_all or everything
        entries: list[dict[str, object]] = []
        for name in bib_files:
            path, text = read_text(name, BIB_SUFFIXES)
            if path.suffix.lower() == ".bib":
                entries.extend(parse_bibtex(path, text, report))
            else:
                entries.extend(parse_csl_json(path, text))
        for name in args.reference_list:
            path, text = read_text(name, MANUSCRIPT_SUFFIXES)
            parsed = parse_reference_list(path, text)
            if not parsed:
                report.add(path, 1, "warning", "REFERENCE_LIST_EMPTY",
                           "no reference entries found (expected a \\bibitem or \\item list, or "
                           "a numbered or bulleted list)")
            references.extend(parsed)
            bibitems |= {str(entry["bibitem"]) for entry in parsed if entry.get("bibitem")}
        ledger = read_ledger(args.ledger) if args.ledger else None
        cache_path = Path(args.cache) if args.cache and args.online else None
        if cache_path:
            inputs = {Path(n).resolve() for n in manuscripts + bib_files + args.reference_list
                      + ([args.ledger] if args.ledger else [])}
            if cache_path.resolve() in inputs:
                raise InputError(f"{cache_path}: the cache file must not be one of the inputs")
            if cache_path.is_symlink() or (cache_path.exists() and not cache_path.is_file()):
                raise InputError(f"{cache_path}: the cache must be a regular file")
    except (InputError, OSError) as exc:
        print(f"{TOOL}: {exc}", file=sys.stderr)
        return 2

    bibliography: dict[str, dict[str, object]] | None = None
    known: set[str] | None = None
    if bib_files:
        bibliography = check_entries(entries, report)
        known = set(bibliography) | bibitems
    elif bibitems:
        known = set(bibitems)
    if references:
        check_entries(references, report)
    # A bare @key counts as a citation when it matches a known key; otherwise it may be a
    # handle or similar text, so it is a warning and is left out of the later checks.
    lookup = known if known is not None else (
        {row["key"] for row in ledger[1]} if ledger is not None else None)
    for key, (source, line) in bare.items():
        if key in cited:
            continue
        if lookup is None or key in lookup:
            cited[key] = (source, line)
        else:
            where = "bibliography entry" if known is not None else "ledger row"
            report.add(source, line, "warning", "BARE_KEY_NOT_IN_BIBLIOGRAPHY",
                       f'"@{key}" outside [ ] matches no {where}; if it is a citation, add '
                       "the entry; if it is a handle or other text, ignore this")
    if manuscripts:
        if known is None:
            report.add(manuscripts[0], 1, "info", "NO_BIBLIOGRAPHY_GIVEN",
                       "pass --bib to compare citation keys with a bibliography")
        else:
            for key, (source, line) in cited.items():
                if key not in known:
                    report.add(source, line, "error", "CITED_KEY_NOT_IN_BIBLIOGRAPHY",
                               f'"{key}" is cited but has no bibliography entry')
            if bibliography is not None and not cite_all:
                for key, entry in bibliography.items():
                    if key not in cited:
                        report.add(entry["source"], int(entry["line"]), "info", "ENTRY_NEVER_CITED",
                                   f'"{key}" is in the bibliography but is not cited in the files checked')
    if ledger is not None:
        check_ledger(ledger[0], ledger[1], cited, bibliography, report)

    online_summary: dict[str, int] | None = None
    if args.online:
        verifier = Verifier(Online(cache_path, args.mailto), report)
        to_check = list((bibliography or {}).values()) + references
        online_summary = verifier.run(to_check, args.max_online)

    findings = sorted(
        report.findings,
        key=lambda f: (SEVERITY_RANK[str(f["severity"])], str(f["file"]), f["line"], f["code"]),
    )
    totals = {name: sum(f["severity"] == name for f in findings) for name in SEVERITIES}
    shown = [f for f in findings
             if SEVERITY_RANK[str(f["severity"])] <= SEVERITY_RANK[min_severity]]
    summary: dict[str, object] = {
        "keys_cited": len(cited),
        "bibliography_entries": len(bibliography) if bibliography is not None else len(bibitems),
        "network_used": bool(args.online),
        **totals,
    }
    if args.reference_list:
        summary["reference_list_entries"] = len(references)
    if online_summary is not None:
        summary["online"] = online_summary
    if args.json:
        print(json.dumps({"tool": TOOL, "summary": summary, "findings": shown},
                         indent=2, ensure_ascii=False))
    else:
        for f in shown:
            print(f'{f["file"]}:{f["line"]}: {f["severity"]}: {f["code"]}: {f["detail"]}')
        listed = (f' {len(references)} reference-list entries.' if args.reference_list else "")
        if online_summary is not None:
            classes = ", ".join(f"{name} {online_summary[name]}" for name in ONLINE_CLASSES)
            print(f"{TOOL}: online: {online_summary['looked_up']} references looked up "
                  f"({online_summary['requests']} requests, {online_summary['from_cache']} answers "
                  f"from the cache): {classes}; {online_summary['not_looked_up']} not looked up "
                  "(--max-online).")
            tail = ("A VERIFIED reference exists with that metadata; open it to confirm that it "
                    "supports the claim." if online_summary.get("VERIFIED") else
                    "No reference was VERIFIED: open each source to confirm that it exists and "
                    "supports the claim.")
        else:
            tail = ("No identifier was resolved: open each source to confirm that it exists and "
                    "supports the claim.")
        print(f'{TOOL}: {totals["error"]} error(s), {totals["warning"]} warning(s), '
              f'{totals["info"]} note(s); {summary["keys_cited"]} keys cited, '
              f'{summary["bibliography_entries"]} bibliography entries.{listed} {tail}')
    return 1 if totals["error"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
