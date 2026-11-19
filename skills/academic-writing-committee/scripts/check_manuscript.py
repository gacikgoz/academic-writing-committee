#!/usr/bin/env python3
# check_manuscript.py - read-only lint for academic manuscripts (Markdown, LaTeX, plain text).
#
# ADAPTED WORK. This file is not an unchanged copy of any source script. It combines and
# rewrites ideas from two MIT-licensed scripts:
#
#   1. K-Dense-AI/claude-scientific-skills
#      skills/scientific-writing/scripts/lint_manuscript.py and scripts/_common.py
#      MIT License, Copyright (c) 2025 K-Dense Inc.
#      Taken from it: the placeholder, overstatement, causal-language and sensitive-content
#      rules; bounded UTF-8 input; symbolic-link rejection; line-numbered rule codes; exit
#      status 1 only for errors.
#   2. vishalsachdev/claude-code-skills
#      skills/paper-writing/scripts/check_paper.py
#      MIT License, Copyright (c) 2026 Claude Code Community (skill LICENSE.txt);
#      repository MIT License, Copyright (c) 2026 Vishal Sachdev
#      Taken from it: the wordy-phrase, hedge and sentence-length checks.
#
# Main changes: LaTeX and plain-text support (the K-Dense script accepted Markdown only);
# no dependency on claim or evidence markers or on a manifest file; code, mathematics,
# comments and citations are masked before prose rules run; a sentence splitter that keeps
# decimals and abbreviations intact; new rules (unsupported attribution, priority claims,
# absence claims, "significant" without a statistic, acronyms, float references, repeated
# words); no hedge or passive percentages and no overall score, because such numbers invite
# optimizing the number instead of the text. Written for this skill and not taken from the
# sources: the hyphen and dash rules, the coordination and repetition rules, the generic-
# phrase lexicon, the underselling, certainty and state-of-the-art rules, the house rules
# (dashes in prose and tables, predicative hyphens, commas after conjunctions, paragraphs
# opening with "To", acronyms in the abstract, internal identifiers of the studied software),
# the title-style rules (abbreviations in the title, title length), --disable, --allow-terms
# and --list-rules.
#
# The license texts are in ../LICENSES/ (K-Dense-Inc-MIT.md, Claude-Code-Community-MIT.txt,
# Vishal-Sachdev-MIT.txt). Standard library only. No network access. Input
# files are opened read-only and nothing is written except the report on standard output.
"""Lint academic manuscripts for placeholders, risky claims, punctuation and prose clutter.

Usage:
    python3 check_manuscript.py paper.md
    python3 check_manuscript.py chapters/*.tex --min-severity warning
    python3 check_manuscript.py paper.tex --observational --json
    python3 check_manuscript.py book.tex --disable AND_CHAIN,HYPE_WORD --allow-terms "boosting,residual"
    python3 check_manuscript.py paper.tex --disable DASH_IN_PROSE   # a venue that allows dashes
    python3 check_manuscript.py --list-rules

Inputs: .md, .markdown, .tex, .texview (read as LaTeX) and .txt files, in reading order.
Mathematics, code, citations, cross-references, URLs and comments are masked before the
prose rules run. Rule groups: housekeeping (placeholders, floats, labels), mechanics
(hyphens, dashes, minus signs, repeated words), claims (overstatement, priority, absence,
attribution, statistics, certainty, hype, underselling, causal wording with
--observational) and style (wording, coordination with "and", repetition, sentence length,
paragraph openings, acronyms, the document title). --list-rules prints every rule id with its severity and a
one-line description; --disable switches rules off; --no-style switches off the whole style
group.

House rules (references/language-mechanics.md, "House Rules"). The default style has no en
or em dash in prose, captions or table text (DASH_IN_PROSE, which also reads the cells of
tabular environments and Markdown tables), no hyphen in a compound after a linking verb
(PREDICATIVE_COMPOUND_HYPHEN, with LY_ADVERB_HYPHEN), no comma right after a conjunction or a
sentence-initial connective (COMMA_AFTER_CONJUNCTION), no paragraph that begins with "To"
(PARAGRAPH_STARTS_WITH_TO), and every acronym expanded in the body before it is used alone,
with an abstract that uses none (ACRONYM_NOT_DEFINED, ACRONYM_USED_BEFORE_DEFINITION). While
DASH_IN_PROSE is on, the older dash rules it subsumes (DOUBLE_HYPHEN, SPACED_EN_DASH,
SPACED_EM_DASH, EM_DASH_DENSITY) and the rules that recommend an en dash (EPONYM_HYPHEN,
EQUAL_PAIR_HYPHEN) stay silent, and HYPHEN_IN_RANGE and SPACED_HYPHEN advise "to" or a comma
instead of a dash. A project whose guidelines relax the dash rule runs with
--disable DASH_IN_PROSE and gets the earlier dash conventions back.

House rule R6, no internal identifiers (INTERNAL_IDENTIFIER, a warning). In prose, headings,
captions, table cells, the node text of TikZ pictures and the text of algorithmic
environments (not in comments, mathematics, the arguments of \\cite, \\ref, \\label and \\url,
or the bibliography) it reports every \\texttt, \\verb, \\lstinline or \\code argument (inline
code in Markdown) and every bare token that looks like an identifier of the studied software:
camelCase with an internal capital and at least three lower-case letters
(createUserAccount), snake_case (retry_on_timeout, int4_q), a dotted namespaced path
of three or more parts (pkg.orders.findOrderById), a file name with a code or data extension
(config.yaml), a version string (2.6.0, v1.2.3, "version 3.0", "release 4.2.1"; not a section
number such as "Section 3.2.1"), and a hexadecimal token of 7 to 40 characters with both
letters a-f and digits (a commit or report hash such as 9f3c2ab1). Names given with
--allow-terms and common names of public software with internal capitals (GitHub, JavaScript,
PyTorch, LaTeX, BibTeX, McNemar, iPhone, macOS, OpenAI, DeepSeek and a few more) are not
reported, nor is a name with an internal capital that the run cites right after it
("ToolSandbox \\cite{...}") or defines with an abbreviation ("NormalFloat (NF4)"), nor a key
value in options (draw=cBlue). In Markdown an underscore inside a word is not taken for
emphasis, so snake_case stays one token for every rule. The writer describes the thing in
plain words; versions, hashes and run identifiers go to the data or code availability
statement, a supplement or the evidence record.

Title style (references/structure.md, "Titles"). The document title is \title{...} in LaTeX
(preamble or body; notes such as \thanks and \tnoteref and mathematics are removed), the YAML
front-matter "title:" in Markdown or, when no file of the run has either, the first "# "
heading of the first Markdown or text file. TITLE_ABBREVIATION reports a token of two or more
capitals (GNN, LLMs, GPT-4) or a listed mixed-case acronym (IoT, LiDAR) in it; roman numerals,
names given with --allow-terms, and a one-word system name that forms the whole part before
the first colon of a title whose subtitle has at least three words ("ImageNet: A Large-Scale Hierarchical Image Database
...") are not reported. TITLE_TOO_LONG is a note above 15 words and a warning above 20. Only
the author approves a title; the checker does not judge whether a subtitle explains a name.

Severities: error (clearly broken: placeholders, an empty file), warning (a mechanical error
or a claim that needs evidence), info, printed as a note (a stylistic pattern). Every
finding is a prompt for human judgment. A clean report does not show that a manuscript is
correct, complete or ready to submit. Findings quote short fragments of the input, so treat
the report as being as confidential as the manuscript.

Exit status: 0 without error-level findings, 1 with at least one, 2 when an input is
rejected (symbolic link, unsupported extension, not UTF-8, over 5 MB, missing) or an option
is invalid (for example an unknown rule id in --disable).
"""

from __future__ import annotations

import argparse
import bisect
import functools
import json
import re
import sys
from collections import deque
from pathlib import Path

TOOL = "check_manuscript"
MAX_FILE_BYTES = 5_000_000
LATEX_SUFFIXES = {".tex", ".texview"}
PLAIN_SUFFIXES = {".md", ".markdown", ".txt"}
SUFFIXES = LATEX_SUFFIXES | PLAIN_SUFFIXES
SEVERITIES = ("error", "warning", "info")
SEVERITY_RANK = {name: rank for rank, name in enumerate(SEVERITIES)}
SEVERITY_ALIASES = {"note": "info"}

CITE = "\u2039cite\u203a"
REF = "\u2039ref\u203a"
MATH = "\u2039math\u203a"
CODE = "\u2039code\u203a"
URL = "\u2039url\u203a"
MARKER_RE = re.compile("\u2039[a-z]+\u203a")

# ---------------------------------------------------------------------------
# Rule catalogue: id, severity, group, one-line description. --no-style switches off the
# "style" group. "info/warning" means the severity depends on a threshold.
# ---------------------------------------------------------------------------

RULES = (
    ("UNRESOLVED_PLACEHOLDER", "error", "housekeeping",
     "TODO, TBD, FIXME, XXX, [insert ...], \\todo, empty \\cite{}, ?? and similar"),
    ("EMPTY_MANUSCRIPT", "error", "housekeeping",
     "a file with no prose (a note when other files of the run have prose)"),
    ("INCLUDES_ONLY", "info", "housekeeping",
     "a LaTeX file whose only content is \\input or \\include: pass the included files"),
    ("POSSIBLE_PERSONAL_DATA", "warning", "housekeeping",
     "an identifier field (MRN, SSN, date of birth, patient name)"),
    ("INTERNAL_IDENTIFIER", "warning", "housekeeping",
     "house rule: code in \\texttt or backticks, or a function name, code identifier, file "
     "name, version or hash in prose, captions, tables or figure labels"),
    ("FLOAT_NEVER_REFERENCED", "warning", "housekeeping",
     "a labeled figure or table (or Markdown caption) the text never refers to"),
    ("REFERENCE_TO_UNKNOWN_LABEL", "warning", "housekeeping",
     "a \\ref to a label not defined in the files checked"),
    ("FLOAT_MENTION_WITHOUT_CAPTION", "info", "housekeeping",
     "Markdown: \"Figure N\" is mentioned but no caption line starts with it"),
    ("HYPHEN_IN_RANGE", "warning", "mechanics",
     "a hyphen in a numeric range in prose (12-15, 2019-2023, 0.1-0.5)"),
    ("RANGE_AFTER_FROM_BETWEEN", "warning", "mechanics",
     "a dash range after \"from\" or \"between\" (from 2019-2023, between 5-10)"),
    ("SPACED_HYPHEN", "warning", "mechanics", "a spaced hyphen \" - \" used as a dash"),
    ("DASH_IN_PROSE", "warning", "mechanics",
     "house rule: an en or em dash (--, ---, \u2013, \u2014) in prose, captions or tables; "
     "use a comma, colon, parentheses or \"to\""),
    ("DOUBLE_HYPHEN", "warning", "mechanics",
     ".md and .txt only: -- or --- typed for a dash in prose (only with DASH_IN_PROSE off)"),
    ("SPACED_EN_DASH", "info", "mechanics",
     "a spaced en dash between words (\" -- \" in LaTeX, \" \u2013 \") used as a break "
     "(only with DASH_IN_PROSE off)"),
    ("SPACED_EM_DASH", "info", "mechanics",
     "a spaced em dash (\" --- \" in LaTeX, or \" \u2014 \"); set closed (only with "
     "DASH_IN_PROSE off)"),
    ("EPONYM_HYPHEN", "warning", "mechanics",
     "an eponymous pair joined by a hyphen (Kullback-Leibler); use an en dash (only with "
     "DASH_IN_PROSE off: the house style keeps the hyphen)"),
    ("EQUAL_PAIR_HYPHEN", "info", "mechanics",
     "two equal terms joined by a hyphen (encoder-decoder, input-output); en dash (only "
     "with DASH_IN_PROSE off)"),
    ("LY_ADVERB_HYPHEN", "warning", "mechanics",
     "a hyphen after an -ly adverb (widely-used, highly-accurate)"),
    ("PREDICATIVE_COMPOUND_HYPHEN", "warning", "mechanics",
     "house rule: a hyphenated compound after its noun and a linking verb (is well-known)"),
    ("COMMA_AFTER_CONJUNCTION", "warning", "mechanics",
     "house rule: a comma right after a sentence-initial connective (However, Thus,) or a "
     "conjunction (, and, ; but,)"),
    ("HYPHEN_AS_MINUS", "info", "mechanics",
     "a hyphen-minus typed as a minus sign before a number in prose (-0.3)"),
    ("REPEATED_WORD", "warning", "mechanics", "the same word twice in a row (the the)"),
    ("POSSIBLE_OVERSTATEMENT", "warning", "claims",
     "definitive or certainty wording; prove outside a theorem or proof context"),
    ("SOTA_WITHOUT_EVIDENCE", "warning", "claims",
     "state of the art, outperforms all, best-performing with no citation or number"),
    ("PRIORITY_OR_GAP_CLAIM", "warning", "claims",
     "the first to, we show for the first time, unprecedented, never been studied"),
    ("ABSENCE_CLAIM", "warning", "claims", "no effect / no difference stated as a finding"),
    ("ATTRIBUTION_WITHOUT_CITATION", "warning", "claims",
     "several studies have shown ..., it is well known ... with no citation"),
    ("SIGNIFICANT_WITHOUT_STATISTIC", "warning", "claims",
     "significant(ly) with no statistic in the same or the next sentence"),
    ("CAUSAL_LANGUAGE", "warning", "claims",
     "with --observational only: causes, leads to, results in, the effect of"),
    ("CERTAINTY_WORD", "info", "claims",
     "clearly, always, never, we solve: state the tested cases or the guarantee"),
    ("HYPE_WORD", "info", "claims",
     "novel, revolutionary, groundbreaking, cutting-edge, paradigm shift"),
    ("UNDERSELLING", "info", "claims",
     "merely, just a, only slightly, somewhat, a bit, we try to, simple trick"),
    ("STACKED_HEDGES", "info", "style",
     "two or more hedges in one clause, or three in one sentence (may possibly)"),
    ("WORDY_PHRASE", "info", "style", "a wordy phrase with a plainer equivalent (in order to)"),
    ("GENERIC_PHRASE", "info", "style",
     "a stock generic phrase (delve, plays a crucial role, paving the way, tapestry)"),
    ("EMPTY_OPENER", "info", "style",
     "an empty opener (it is important to note that, it can be seen that)"),
    ("LONG_SENTENCE", "info/warning", "style",
     "over --max-sentence-words (note) or --very-long-sentence-words (warning) words"),
    ("AND_CHAIN", "info/warning", "style",
     "three (note) or four or more (warning) coordinating \"and\" in one sentence"),
    ("AND_ALSO", "info", "style", "and also, and additionally, as well as also"),
    ("AND_OR", "info", "style", "and/or"),
    ("AMPERSAND_IN_PROSE", "info", "style", "an ampersand in running prose"),
    ("SENTENCE_STARTS_WITH_AND", "info", "style", "a sentence that begins with \"And\""),
    ("REPEATED_OPENING", "info", "style",
     "three or more consecutive sentences starting with the same word"),
    ("STACKED_TRANSITIONS", "info", "style",
     "additive transitions (Moreover, Furthermore, Also ...) opening 2 of 3 sentences"),
    ("REPEATED_CONTENT_WORD", "info", "style",
     "a content word (5+ letters) used three times within 40 words"),
    ("REPEATED_PHRASE", "info", "style",
     "a phrase of three or more words repeated within one paragraph"),
    ("EM_DASH_DENSITY", "info", "style",
     "more than two em dashes in one paragraph (only with DASH_IN_PROSE off)"),
    ("PARAGRAPH_STARTS_WITH_TO", "warning", "style",
     "house rule: a paragraph whose first word is \"To\" (To compare X, we ...)"),
    ("ACRONYM_NOT_DEFINED", "warning", "style",
     "house rule: an acronym never expanded in the body, or any acronym in the abstract"),
    ("ACRONYM_USED_BEFORE_DEFINITION", "warning", "style",
     "house rule: an acronym used alone before the place where the body expands it"),
    ("TITLE_ABBREVIATION", "warning", "style",
     "title style: an abbreviation or acronym in the document title (GNN, LLM, IoT); a "
     "system name before the colon of a title with a subtitle is allowed"),
    ("TITLE_TOO_LONG", "info/warning", "style",
     "title style: a document title of more than 15 words (note) or 20 words (warning)"),
)
RULE_IDS = {rule[0] for rule in RULES}
STYLE_RULES = {rule[0] for rule in RULES if rule[2] == "style"}

# ---------------------------------------------------------------------------
# Housekeeping rules
# ---------------------------------------------------------------------------

PLACEHOLDER_PATTERNS = (
    re.compile(r"\[\[\s*TODO\b", re.IGNORECASE),
    re.compile(r"\b(?:TODO|TBD|FIXME)\b"),
    re.compile(r"(?<![{}@|>A-Za-z])\bX{3,}\b(?![{}@|])"),   # not tabularx columns such as {lXXX@{}}
    re.compile(
        r"\[\s*(?:(?:insert|add|describe|replace|cite|citation needed|ref|reference)\b[^\]]{0,200}"
        r"|(?:citations?|refs?|references?|sources?)(?:\s+needed)?\s*)\](?![({:\[])",
        re.IGNORECASE,
    ),
    re.compile(r"\blorem ipsum\b", re.IGNORECASE),
    re.compile(r"\\(?:todo|fixme|missingfigure)\b"),
    re.compile(r"\(\s*Author,?\s+Year\s*\)"),
    re.compile(r"\\[A-Za-z]*[Cc]ite[A-Za-z]*\*?(?:\[[^\]]{0,200}\])*\{\s*\}"),
    re.compile(r"\(\?\?\)|\[\?+\]|(?<![?\w])\?{2,}(?![?\w])"),
)
# The bracket rule, run again on whole paragraphs to catch "[insert" / "citation]".
BRACKET_PLACEHOLDER_RE = PLACEHOLDER_PATTERNS[3]
# LaTeX optional arguments such as \cite[Ref.~3]{x} or \item[Add] are removed before the
# placeholder rules run, so that they are not taken for "[Ref ...]" or "[Add ...]".
LATEX_OPTIONAL_ARG_RE = re.compile(r"(\\[A-Za-z]+\*?)\s*(?:\[[^\]\n]{0,200}\]\s*)+")
# Code in LaTeX (\verb|# TODO|, \lstinline, \texttt{FIXME}) is masked before the placeholder
# rules, so that a paper about TODO comments can pass.
LATEX_CODE_RE = re.compile(
    r"\\(?:verb|lstinline)\*?([^\sA-Za-z{])[^\n]*?\1|\\(?:lstinline|texttt|code)\{[^{}\n]{0,400}\}")
# Front-matter commands in the LaTeX preamble whose arguments are checked for placeholders.
PREAMBLE_META_RE = re.compile(r"\\(?:title|subtitle|author|date|thanks|keywords|subject)\b")

PERSONAL_DATA_RE = re.compile(
    r"\b(?:MRN|medical record number|SSN|social security number|DOB|date of birth)\s*[:#]"
    r"|\b(?:patient|participant)\s+name\s*:",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Claim rules
# ---------------------------------------------------------------------------

OVERSTATEMENT_RE = re.compile(
    r"\b(?:definitively|undoubtedly|unquestionably|indisputabl[ey]|conclusively|"
    r"definitely|undeniabl[ey]|irrefutabl[ey]|"
    r"guarantees?|no\s+limitations|universally|obviously|beyond\s+(?:any\s+)?doubt|"
    r"(?:highly|very|extremely)\s+significant|"
    r"clearly\s+(?:shows?|demonstrates?|proves?|establish(?:es)?))\b",
    re.IGNORECASE,
)
# "prove" outside a theorem or proof context; "proved useful" and "proves to be" mean
# "turned out" and are not proof claims.
PROOF_VERB_RE = re.compile(
    r"\b(?:prove|proves|proved|proven)\b(?!\s+(?:to\s+be|useful|effective|successful|"
    r"valuable|helpful|difficult|hard|popular|essential|fruitful|beneficial|worthwhile|"
    r"elusive|challenging|instrumental|influential|durable)\b)",
    re.IGNORECASE,
)
# "Our experiments prove": an empirical subject before a proof verb.
EMPIRICAL_SUBJECT_RE = re.compile(
    r"\b(?:experiments?|experimental\s+\w+|results?|data|findings?|evaluations?|stud(?:y|ies)|"
    r"analys[ie]s|simulations?|observations?|benchmarks?|measurements?|trials?|surveys?|"
    r"evidence|work|papers?|literature|research|ablations?)\s+(?:\w+\s+){0,3}?"
    r"(?:prove|proves|proved|proven)\b",
    re.IGNORECASE,
)
NEGATION_BEFORE_RE = re.compile(
    r"(?:\b(?:not|cannot|never|no|nor|without)|n't)\s+(?:\w+\s+){0,2}$", re.IGNORECASE)
AUXILIARY_BEFORE_RE = re.compile(
    r"\b(?:is|are|was|were|be|been|being|has|have|had)\s+(?:\w+\s+)?$", re.IGNORECASE)
MATH_CONTEXT_RE = re.compile(
    r"\b(?:theorem|lemma|proposition|corollary|claim|proof|inequality|identity|bound|"
    r"induction|contradiction)\b",
    re.IGNORECASE,
)
# "guarantees convergence", "universally consistent": technical vocabulary, not overstatement.
TECHNICAL_GUARANTEE_RE = re.compile(
    r"\s+(?:convergence|termination|stability|feasibility|optimality|correctness|uniqueness|"
    r"existence|consistency|monotonicity|privacy|safety|completeness|soundness)\b"
    r"|\s+(?:consistent|quantified|valid|approximat\w*)\b",
    re.IGNORECASE,
)
SECTION_POINTER_RE = re.compile(r"\b(?:Section|Sec\.|Appendix|Chapter|Ch\.|Supplement\w*)\s")
CAUSAL_RE = re.compile(
    r"\b(?:causes?|caused|causing|leads?\s+to|led\s+to|results?\s+in|resulted\s+in|"
    r"the\s+(?:effect|impact)\s+of|"
    r"(?:increases?|increased|reduces?|reduced|lowers?|lowered|raises?|raised)\s+the\s+"
    r"(?:risk|odds|likelihood|probability|incidence)\s+of)\b",
    re.IGNORECASE,
)
ABSENCE_RE = re.compile(
    r"\bno\s+(?:significant\s+)?(?:effect|difference|association|relationship|impact)s?\b"
    r"|\bno\s+(?:statistically\s+)?significant\s+changes?\b"
    r"|\b(?:did|does|do)\s+not\s+differ\b|\bnot\s+(?:statistically\s+)?significantly\s+different\b"
    r"|\b(?:was|were|is|are)\s+not\s+(?:significantly\s+)?associated\s+with\b",
    re.IGNORECASE,
)
# "were equivalent" is an absence claim only about groups, conditions or outcomes; "the two
# formulations are equivalent" is a mathematical statement.
EQUIVALENT_RE = re.compile(r"\b(?:was|were|is|are)\s+(?:statistically\s+)?equivalent\b", re.IGNORECASE)
STATISTICAL_CUE_RE = re.compile(
    r"\b(?:groups?|conditions?|arms?|outcomes?|treatments?|cohorts?|samples?|participants|"
    r"patients|subjects|scores|means|performance|accuracy|placebo|control)\b",
    re.IGNORECASE,
)
# A priority claim needs a claim frame: "the first to", "is the first study", "we show for the
# first time". Ordinal enumeration ("the first method uses ..., the second ...", "In the first
# study") and "saw it for the first time" are not claims.
NOVELTY_RE = re.compile(
    r"\bthe\s+first\s+to\b|\bthe\s+first\s+such\b"
    r"|\b(?:is|are|was|were|be|being|been|represents?|presents?|constitutes?|provides?|offers?|"
    r"introduces?|reports?|describes?)\s+(?:the|a|our)\s+(?:very\s+)?first\s+(?:[\w-]+\s+)?"
    r"(?:study|work|paper|method|approach|attempt|framework|demonstration|investigation|"
    r"analysis|application|evaluation|benchmark|dataset|algorithm|system|model|technique)\b"
    r"|\b(?:we|is|are|was|were|been|be|here)\s+(?:\w+\s+){0,3}for\s+the\s+first\s+time\b"
    r"|\bto\s+(?:the\s+best\s+of\s+)?our\s+knowledge\b[^.;]{0,120}?\bfirst\b"
    r"|\bfirst[-\s]ever\b|\blittle\s+is\s+known\b"
    r"|\bunprecedented\b"
    r"|\b(?:has|have)\s+(?:never|not)\s+been\s+(?:studied|explored|investigated|addressed|examined)\b"
    r"|\bno\s+(?:prior|previous|existing)\s+(?:work|study|studies|research)\b",
    re.IGNORECASE,
)
ATTRIBUTION_RE = re.compile(
    r"\b(?:several|many|some|numerous|recent|previous|prior|most|various)\s+"
    r"(?:studies|researchers|authors|papers|scholars|works|investigations|experiments)"
    r"(?:\s+\w+)?\s+(?:have|has|had|show|shows|showed|suggest|suggests|suggested|find|finds|"
    r"found|report|reports|reported|argue|argues|argued|indicate|indicates|indicated|"
    r"demonstrate|demonstrates|demonstrated|claim|claims|claimed|propose|proposes|proposed|"
    r"agree|agrees|believe|believes|confirm|confirms|confirmed)\b"
    r"|\b(?:studies|research)\s+(?:have|has)\s+(?:shown|demonstrated|found|suggested|established)\b"
    r"|^\W{0,3}(?:studies|research|evidence|experts?)\s+(?:show|shows|suggest|suggests|indicate|"
    r"indicates|agree|agrees|confirm|confirms)\b"
    r"|\bit\s+(?:has\s+been|is)\s+(?:shown|well\s+known|well\s+established|"
    r"widely\s+(?:accepted|known|believed|recognized))\b",
    re.IGNORECASE,
)
SIGNIFICANT_RE = re.compile(r"\bsignifican(?:t|tly)\b", re.IGNORECASE)
# A statistic: a comparison with a number (t(28) = 2.1, p = .03, d = 0.4, OR = 1.5), a
# percentage, an interval or a named statistic. A bare count ("in 3 of 5 sites") is not one.
STATISTIC_HINT_RE = re.compile(
    r"[=<>\u2264\u2265]\s*[-\u2212]?\.?\d|\d\s*%|\b[tFzr]\s*\(\s*\d|\bCI\b|\d\s+level\b"
    r"|[(\[]\s{0,3}[-\u2212]?\d{0,9}\.?\d{1,9}\s{0,3},\s{0,3}[-\u2212]?\d{0,9}\.?\d{1,9}\s{0,3}[)\]]"
    r"|\bp\s*[<=>]|\u00b1|\\pm|\u03c7|\bchi\b|\beffect\s+sizes?\b|\bodds\s+ratios?\b"
    r"|\bconfidence\s+intervals?\b|\bstandard\s+errors?\b|\bp[-\s]values?\b|\bCohen",
    re.IGNORECASE,
)
SOTA_RE = re.compile(
    r"\bstate[-\s]of[-\s]the[-\s]art\b|\bSOTA\b"
    r"|\boutperform(?:s|ed|ing)?\s+(?:all|every|any|existing|prior|previous|current|other|competing)\b"
    r"|\bsuperior\s+to\s+(?:all|every|any|existing|prior|previous|current|other)\b"
    r"|\bbest[-\s]performing\b(?!\s+(?:\w+\s+)?(?:configuration|setting|hyperparameters?|"
    r"checkpoint|run|seed|variant|learning\s+rate)s?\b)",
    re.IGNORECASE,
)
CLEARLY_START_RE = re.compile(r"^[\W\u2039\u203a]{0,3}clearly\b", re.IGNORECASE)
# The lookahead lists the possible first letters, so that the scanner skips other words fast.
CERTAINTY_RE = re.compile(
    r"\b(?=[abcefimnorstwABCEFIMNORSTW])(?:(?:is|are|was|were|be|been)\s+clearly\b"
    r"|\bclearly\s+(?:outperform\w*|better|superior|worse|indicat\w*|reveal\w*|confirm\w*|"
    r"suggest\w*|the\s+best|more|less|higher|lower)\b"
    r"|\b(?:always|never)\s+(?:outperform|improve|beat|exceed|work|succeed|fail|help|hurt|win|"
    r"produce|yield|achieve|generali[sz]e|transfer|scale|recover|detect|find)\w*"
    r"|\b(?:method|model|approach|algorithm|system|technique|framework|results?|estimator)\s+"
    r"(?:\w+\s+)?(?:always|never)\b"
    r"|\bin\s+(?:all|every)\s+cases?\b"
    r"|\b(?:we|our\s+\w+|(?:this|the\s+proposed)\s+\w+)\s+(?:\w+ly\s+)?solve[sd]?\b"
    r"|\b(?:completely|fully|entirely)\s+solve[sd]?\b)",
    re.IGNORECASE,
)
HYPE_RE = re.compile(
    r"\b(?:novel|revolutionary|revolutioni[sz](?:e|es|ed|ing)|ground-?breaking|"
    r"game[-\s]chang(?:ing|ers?)|cutting[-\s]edge|paradigm[-\s]shift(?:s|ing)?|"
    r"unparalleled|unrivall?ed|transformative)\b",
    re.IGNORECASE,
)
UNDERSELLING_RE = re.compile(
    r"\b(?:is|are|was|were|be|been|only|just)\s+merely\b"
    r"|\bmerely\s+(?:a|an|one|slightly|marginally|incremental|heuristic|preliminary)\b"
    r"|\bjust\s+(?:a|an|one|slightly|marginally|a\s+few)\b"
    r"|\bonly\s+(?:slightly|marginally|modestly)\b|\bsomewhat\b"
    r"|\ba\s+(?:little\s+)?bit\b(?!\s+(?:vectors?|flips?|width|strings?|masks?|per\b|in\s|"
    r"of\s+(?:memory|storage|information)))"
    r"|\b(?:we|this\s+(?:paper|work|study|article|chapter))\s+(?:try|tries|tried|attempt|"
    r"attempts|attempted)\s+to\b|\bsimple\s+trick\b",
    re.IGNORECASE,
)
HEDGE_RE = re.compile(
    r"\b(?:may|might|could|possibly|perhaps|potentially|presumably|arguably|somewhat|"
    r"seems?|appears?|suggests?|likely)\b",
    re.IGNORECASE,
)
ADJACENT_HEDGES_RE = re.compile(
    r"\b(?:may|might|could)\s+(?:possibly|perhaps|potentially|conceivably)\b"
    r"|\b(?:possibly|perhaps|potentially)\s+(?:suggests?|indicates?|may|might|could)\b"
    r"|\b(?:seems?|appears?)\s+to\s+(?:possibly|perhaps|potentially|suggest)\b",
    re.IGNORECASE,
)
CLAUSE_SPLIT_RE = re.compile(
    r"[,;:()\[\]\u2013\u2014]|\s-{1,3}\s"
    r"|\b(?:that|which|because|although|though|whereas|while|but|if|when|since|and|or)\b",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Style rules: wording lexicon, coordination, repetition
# ---------------------------------------------------------------------------

EMPTY_OPENER_RE = re.compile(
    r"\bit\s+(?:is|was)\s+(?:important|interesting|worth|noteworthy|notable)\s+(?:to\s+)?"
    r"(?:note|noting|mention|mentioning|point\s+out|emphasize)(?:\s+that)?\b"
    r"|\bit\s+should\s+be\s+(?:noted|mentioned|pointed\s+out|emphasized)\s+that\b"
    r"|\bit\s+(?:was|has\s+been|is)\s+(?:found|observed|shown|seen|demonstrated)\s+that\b"
    r"|\bit\s+can\s+be\s+(?:seen|observed|shown)\s+that\b",
    re.IGNORECASE,
)
# "in in-context", "on on-policy": a preposition before a hyphenated compound is not a repeat.
REPEATED_WORD_RE = re.compile(r"\b([A-Za-z]{2,})\s+\1\b(?![-\u2010\u2011])", re.IGNORECASE)
REPEATED_WORD_OK = {"that", "had", "is", "very", "blah"}

WORDY = {
    "due to the fact that": "because",
    "in spite of the fact that": "although",
    "in order to": "to",
    "at this point in time": "now",
    "at the present time": "now",
    "in the event that": "if",
    "for the purpose of": "to, for",
    "with regard to": "about",
    "in regard to": "about",
    "a majority of": "most",
    "a large number of": "many",
    "a number of": "several, many (or the count)",
    "has the ability to": "can",
    "is able to": "can",
    "are able to": "can",
    "prior to": "before",
    "subsequent to": "after",
    "in the near future": "soon (or a date)",
    "take into consideration": "consider",
    "make an assumption": "assume",
    "make a decision": "decide",
    "reach a conclusion": "conclude",
    "give an explanation": "explain",
    "provide assistance": "help",
    "perform an analysis": "analyze",
    "conduct an investigation": "investigate",
    "utilization": "use",
    "utilize": "use",
    "utilizes": "uses",
    "utilized": "used",
    "utilizing": "using",
    "end result": "result",
    "past history": "history",
    "completely eliminate": "eliminate",
    "very unique": "unique",
    "close proximity": "near",
    "basic fundamentals": "fundamentals",
    "future plans": "plans",
    "whether or not": "whether (if the alternative is implied)",
    "as a matter of fact": "(delete)",
    "needless to say": "(delete)",
}
# Stock generic phrases (language-mechanics.md, "Words That Make Text Read as Generic").
# They share one lexicon and one regular expression with WORDY; "it is important to note"
# and "it is worth noting" are EMPTY_OPENER and are not repeated here.
GENERIC = (
    (r"in\s+today['\u2019]s", "name the specific problem and why it matters now"),
    (r"rapidly\s+(?:evolving|changing|growing|advancing|developing)",
     "give the specific change, with a fact"),
    (r"(?:ever-?)?evolving\s+landscape|the\s+landscape\s+of", "name the literal subject"),
    (r"delv(?:e|es|ed|ing)(?:\s+(?:deep(?:er|ly)?\s+)?into)?",
     "study, measure, analyze, or name the actual action"),
    (r"div(?:e|es|ing)\s+(?:deep(?:er)?\s+)?into", "study, measure, analyze, or name the action"),
    (r"a\s+testament\s+to", "state the conclusion and its evidence"),
    (r"navigat(?:e|es|ed|ing)\s+the\s+(?:complexities|intricacies|challenges|landscape)",
     "name the problem and what is done about it"),
    (r"tapestr(?:y|ies)", "name the literal subject"),
    (r"underscor(?:e|es|ed|ing)\s+(?:the|that|how|why|its|their|this|these|our|a|an)",
     "state the conclusion and its evidence"),
    (r"showcas(?:e|es|ed|ing)", "show, present, or give the specific result"),
    (r"seamless(?:ly)?", "name the property and the conditions under which it holds"),
    (r"harness(?:es|ed|ing)?\s+the\s+(?:full\s+)?(?:power|potential)", "use"),
    (r"unlock(?:s|ed|ing)?\s+the\s+(?:full\s+)?potential", "say what the result lets someone do"),
    (r"pav(?:e|es|ed|ing)\s+the\s+way", "say what the result lets someone do"),
    (r"in\s+the\s+realm\s+of", "in"),
    (r"play(?:s|ed|ing)?\s+an?\s+(?:crucial|pivotal|vital|key|critical|instrumental|paramount)"
     r"\s+role", "state the specific effect (\"accounts for 40% of latency\")"),
    (r"sh(?:ed|eds|edding)\s+(?:new\s+)?light\s+on", "say what the result shows"),
    (r"(?:intricate|complex)\s+interplay", "name the relation"),
    (r"(?:a\s+)?myriad\s+of", "many, or the number"),
    (r"leverag(?:es|ing)|leveraged?\s+(?:the|our|this|these|a|an|its|their|existing|recent)",
     "use"),
    (r"(?:has|have)\s+(?:gained|garnered|attracted|received)\s+(?:significant|considerable|"
     r"increasing|growing|much|great|widespread|tremendous)\s+(?:attention|interest|traction)",
     "the specific development, with a fact"),
    (r"embark(?:s|ed|ing)?\s+on", "begin, or name the action"),
    (r"multifaceted", "name the facets"),
    (r"holistic(?:ally)?", "name the coverage"),
)
GENERIC_COMPILED = tuple((re.compile(p, re.IGNORECASE), advice) for p, advice in GENERIC)
GENERIC_FIRST_LETTERS = "acdehilmnprstu"
LEXICON_FIRST = "".join(sorted(set(GENERIC_FIRST_LETTERS) | {key[0] for key in WORDY}))
LEXICON_RE = re.compile(
    r"\b(?=[" + LEXICON_FIRST + LEXICON_FIRST.upper() + r"])(?:"
    + "|".join(re.escape(p).replace(r"\ ", r"\s+") for p in sorted(WORDY, key=len, reverse=True))
    + "|" + "|".join(p for p, _ in GENERIC)
    + r")\b",
    re.IGNORECASE,
)

AND_RE = re.compile(r"\band\b(?!\s*/)", re.IGNORECASE)
AND_PAIR_END_RE = re.compile(r"\s+[\w'\u2019-]{1,40}\s*[,;:.!?)\]]")
AND_EXEMPT_BEFORE_RE = re.compile(r"\b(?:between|both)\s+(?:\S+\s+){0,4}$", re.IGNORECASE)
AND_FIXED_RE = re.compile(
    r"\b(?:trial\s+and\s+error|pros\s+and\s+cons|back\s+and\s+forth|more\s+and\s+more|"
    r"over\s+and\s+over|again\s+and\s+again|and\s+so\s+(?:on|forth)|and\s+the\s+like)\b",
    re.IGNORECASE)
AND_ALSO_RE = re.compile(r"\band\s+(?:also|additionally)\b|\bas\s+well\s+as\s+also\b", re.IGNORECASE)
AND_OR_RE = re.compile(r"\band\s*/\s*or\b", re.IGNORECASE)
AMPERSAND_RE = re.compile(r"&(?!(?:[A-Za-z]{2,8}|#\d{1,7}|#x[0-9A-Fa-f]{1,6});)")
AND_START_RE = re.compile(r"^[\"'(\[\u201c\u2018]{0,3}And\b")
TRANSITION_OPENER_RE = re.compile(
    r"^[\"'(\[\u201c\u2018]{0,3}(Moreover|Furthermore|Additionally|In\s+addition|Also|"
    r"Besides|Further(?=,))\b"
)
OPENER_TOKEN_RE = re.compile("\u2039[a-z]+\u203a|[A-Za-z0-9][A-Za-z0-9'\u2019-]*")
WORD_TOKEN_RE = re.compile("\u2039[a-z]+\u203a|[A-Za-z][A-Za-z'\u2019]*")
PHRASE_TOKEN_RE = re.compile(
    "\u2039[a-z]+\u203a|[A-Za-z][A-Za-z'\u2019]*(?:-[A-Za-z][A-Za-z'\u2019]*){0,4}|[^\\sA-Za-z]"
)
STOPWORDS = set("""
a about above across after again against all almost along already also although always am
among an and another any anyone anything are around as at be because been before being below
between beyond both but by can cannot could did do does doing done down during each either else
enough even ever every few for from further had has have having he her here hers herself him
himself his how however i if in into is it its itself just least less like may me might more
most much must my myself neither never no nor not now of off often on once one only onto or other
others otherwise our ours ourselves out over own per perhaps rather same several shall she should
since so some such than that the their theirs them themselves then there therefore these they
this those though three through throughout thus to too toward towards two under until up upon us
very via was we well were what whatever when where whereas whether which while who whom whose why
will with within without would yet you your yours yourself yourselves
first second third using used uses given based shown thing things section sections chapter
chapters figure figures table tables equation equations appendix following respectively
""".split())
REPETITION_WINDOW = 40
PHRASE_WINDOW = 300   # a repeated phrase counts when its occurrences are this close (tokens)

# ---------------------------------------------------------------------------
# Mechanics rules: hyphens, dashes, minus signs
# ---------------------------------------------------------------------------

NUMBER = r"\d{1,9}(?:[.,]\d{1,9}){0,3}"
HYPHEN_RANGE_RE = re.compile(
    r"(?<![\w.,\-\u2013\u2212/])(" + NUMBER + r")-(" + NUMBER + r")(?![\w\-\u2013/]|[.,]\d)"
)
# Numbering and identifiers such as "Figure 3-2" or "ISO 8601-1" are not ranges.
RANGE_LABEL_BEFORE_RE = re.compile(
    r"(?:Figure|Fig\.|Table|Tab\.|Equation|Eq\.|Section|Sec\.|Chapter|Ch\.|Algorithm|Alg\.|"
    r"Listing|Exercise|Example|Problem|Theorem|Lemma|Definition|Proposition|Corollary|"
    r"Appendix|No\.|Number|ISO|RFC|ISBN|ISSN|IEEE|ANSI|DIN|IEC|EN|"
    r"[Gg]rant|[Aa]ward|[Pp]roject|[Pp]rotocol|[Cc]ontract|[Cc]ase|[Aa]pproval|[Pp]ermit|no\.)\s{0,2}$"
)
FROM_BETWEEN_RANGE_RE = re.compile(
    r"\b([Ff]rom|[Bb]etween)\s{1,3}"
    r"(?:(?!(?:[Tt]he|[Aa]n?|[Tt]his|[Tt]hat|[Tt]hese|[Tt]hose|[Ee]ach|[Ee]very|[Oo]ur|[Tt]heir)\s)"
    r"[A-Za-z.]{1,12}\s{1,3}){0,2}[$\u20ac\u00a3]?" + NUMBER
    + r"\s{0,2}%?\s{0,2}(?:\u2013|\u2014|-{1,3})\s{0,2}[$\u20ac\u00a3\u2212-]?" + NUMBER
)
SPACED_HYPHEN_RE = re.compile(
    r"(?<=[A-Za-z0-9)\]\"'\u201d\u2019%.,]) {1,2}-(?= {1,2}[A-Za-z0-9(\[\"'\u201c\u2018$])"
)
DOUBLE_HYPHEN_RE = re.compile(r"(?<![-<!])-{2,3}(?![->])")
# A spaced en dash between words used as a parenthetical break: "The model -- a small one --".
SPACED_EN_DASH_TEX_RE = re.compile(r"(?<=[A-Za-z)\]'\u2019]) {1,2}--(?!-) {1,2}(?=[A-Za-z(\[])")
SPACED_EN_DASH_RE = re.compile(r"(?<=[A-Za-z)\]'\u2019]) {1,2}\u2013 {1,2}(?=[A-Za-z(\[])")
SPACED_EM_DASH_TEX_RE = re.compile(r"(?<=[^\s-]) {1,2}---(?!-) {1,2}(?=\S)")
SPACED_EM_DASH_RE = re.compile(r"(?<=\S) {1,2}\u2014 {1,2}(?=\S)")
EM_DASH_RE = re.compile(r"\u2014|(?<!-)---(?!-)")
# House rule R1: any en or em dash (and the figure dash and horizontal bar). In LaTeX, -- and
# --- outside mathematics, code, comments, citations, references and URLs, which are masked;
# in Markdown and text files, -- or --- typed for a dash, as DOUBLE_HYPHEN reads them.
TEX_DASH_RE = re.compile(r"(?<!-)-{2,3}(?!-)|[\u2012-\u2015]")
PLAIN_DASH_RE = re.compile(r"(?<![-<!])-{2,3}(?![->])|[\u2012-\u2015]")
DASH_RANGE_RE = re.compile(r"(\d[\d.,]*)\s?$")
MD_TABLE_RULE_RE = re.compile(r"^\s*\|?[\s:|-]+\|?\s*$")
# House rule R2: a hyphenated compound placed after its noun and a linking verb ("the result
# is well-known") is open. The prefixes are those whose compounds are open after the noun;
# -ly adverbs are LY_ADVERB_HYPHEN. A noun after the compound ("is a well-known result" has an
# article, "is well-known work" a noun) is not matched: the compound must end the clause.
PREDICATIVE_HYPHEN_RE = re.compile(
    r"\b(?:is|are|was|were|be|been|being|remains?|remained|seems?|seemed|appears?|appeared|"
    r"becomes?|became)\s+(?:not\s+|still\s+|also\s+)?"
    r"((?:well|ill|better|best|little|lesser)-[a-z]+)\b(?![-\u2010\u2011])"
    r"(?=\s*(?:[.,;:)\u2039]|$|\s(?:and|or|but|in|for|to|by|with|when|if|as|than|because|since|"
    r"under|on|at|from|only|here|there)\b))",
    re.IGNORECASE,
)
# House rule R3: no comma right after a conjunction or a sentence-initial connective. A comma
# that closes a parenthetical or an introductory subordinate clause is not matched.
CONNECTIVES = (
    "On the other hand", "As a result", "In addition", "In contrast", "By contrast", "In turn",
    "However", "Thus", "Therefore", "Hence", "Moreover", "Furthermore", "Additionally",
    "Consequently", "Accordingly", "Nevertheless", "Nonetheless", "Conversely", "Similarly",
    "Likewise", "Meanwhile", "Besides", "Otherwise", "Instead", "Further", "Also", "And",
    "But", "So", "Yet", "Then", "Still", "Next", "First", "Second", "Third", "Fourth",
    "Finally", "Lastly",
)
OPENING_CONNECTIVE_COMMA_RE = re.compile(
    r"^[\"'(\[\u201c\u2018]{0,3}(" + "|".join(c.replace(" ", r"\s+") for c in CONNECTIVES)
    + r")\s*,"
)
# The same connectives opening a clause after a semicolon or colon ("; however, the").
CLAUSE_CONNECTIVE_COMMA_RE = re.compile(
    r"[;:]\s+(" + "|".join(c.lower().replace(" ", r"\s+") for c in CONNECTIVES
                          if c not in {"And", "But", "So", "Yet", "Then", "Still", "Next",
                                       "First", "Second", "Third", "Fourth", "Also"})
    + r")\s*,"
)
# ", and, " / ", but, " / " and, ": a comma right after a coordinating conjunction.
CONJUNCTION_COMMA_RE = re.compile(r"(?<![\w/\u2039-])(and|but|or|nor)\s*,(?=\s|$)", re.IGNORECASE)
# House rule R4: the first word of a paragraph is "To" ("To compare X, we ...").
PARAGRAPH_TO_RE = re.compile(r"^[\s\"'(\[\u201c\u2018]{0,4}To\b(?![-\u2019'])")
# A run-in heading: the text after \paragraph{...} on the same line is prose.
RUNIN_HEADING_RE = re.compile(r"\\(?:sub)?paragraph\*?\s*(?:\[[^\]\n]{0,200}\])?\{[^{}\n]*\}")
HYPHEN_MINUS_RE = re.compile(r"(?:(?<=[\s(\[=:;,])|^)-(\d{1,9}(?:\.\d{1,9})?)(?![\w\-]|[.,]\d)")
LY_HYPHEN_RE = re.compile(r"(?<![\w-])([A-Za-z]{2,20}ly)-(?=[a-z])")
NOT_LY_ADVERBS = set("""
ally anomaly apply assembly belly bodily bully burly chilly comely comply costly cowardly
curly daily dally deadly early elderly emily family fly folly friendly ghastly ghostly godly
golly gully hilly holly holy homely hourly imply italy jelly jolly july kelly kindly likely
lily lively lonely lovely lowly manly melancholy molly monopoly monthly multiply neighborly
nightly oily only orderly poly quarterly rally reilly rely reply sally scholarly silly sully
supply surly tally timely ugly unlikely unruly weekly wily wooly woolly worldly yearly
butterfly firefly dragonfly apply underbelly
""".split())

EPONYMS = (
    "Kullback-Leibler", "Runge-Kutta", "Cauchy-Schwarz", "Eckart-Young-Mirsky", "Eckart-Young",
    "Karush-Kuhn-Tucker", "Gauss-Newton", "Gauss-Seidel", "Gauss-Markov", "Metropolis-Hastings",
    "Robbins-Monro", "Bradley-Terry", "Lotka-Volterra", "Navier-Stokes", "Fokker-Planck",
    "Ornstein-Uhlenbeck", "Hamilton-Jacobi-Bellman", "Hamilton-Jacobi", "Rao-Blackwell",
    "Cramér-Rao", "Neyman-Pearson", "Benjamini-Hochberg", "Kolmogorov-Smirnov", "Mann-Whitney",
    "Nadaraya-Watson", "Sherman-Morrison-Woodbury", "Sherman-Morrison", "Gram-Schmidt",
    "Hodgkin-Huxley", "Lucas-Kanade", "Levenberg-Marquardt", "Davidon-Fletcher-Powell",
    "Broyden-Fletcher-Goldfarb-Shanno", "Marchenko-Pastur", "Johnson-Lindenstrauss",
    "Erdős-Rényi", "Barabási-Albert", "Hammersley-Clifford", "Baum-Welch", "Kaplan-Meier",
    "Hosmer-Lemeshow", "Box-Muller", "Box-Cox", "Box-Jenkins", "Floyd-Warshall", "Bellman-Ford",
    "Ford-Fulkerson", "Needleman-Wunsch", "Smith-Waterman", "Rauch-Tung-Striebel",
    "Dvoretzky-Kiefer-Wolfowitz", "Kiefer-Wolfowitz", "Jensen-Shannon", "Vapnik-Chervonenkis",
    "Moore-Penrose", "Newton-Raphson", "Nelder-Mead", "Perron-Frobenius", "Euler-Lagrange",
    "Watts-Strogatz", "Plackett-Luce", "Glivenko-Cantelli", "Radon-Nikodym", "Wiener-Khinchin",
)
ACCENT_CLASSES = {"é": "[eé]", "ő": "[oőö]", "á": "[aá]"}


def _eponym_pattern(name: str) -> str:
    parts = []
    for part in name.split("-"):
        parts.append("".join(ACCENT_CLASSES.get(ch, re.escape(ch)) for ch in part))
    return r"(?:--|\u2013|-)".join(parts)


EPONYM_RE = re.compile(
    r"(?<![\w-])(?=[A-Z])(?:"
    + "|".join(_eponym_pattern(n) for n in sorted(EPONYMS, key=len, reverse=True))
    + r")(?![\w])"
)
EQUAL_PAIRS = (
    "query-key-value", "encoder-decoder", "input-output", "teacher-student", "student-teacher",
    "actor-critic", "query-key", "key-value", "generator-discriminator", "bias-variance",
    "precision-recall", "exploration-exploitation", "speed-accuracy", "accuracy-efficiency",
    "price-performance", "cost-benefit", "risk-benefit", "mean-variance", "risk-return",
    "state-action", "question-answer", "image-text", "text-image", "vision-language",
    "image-caption", "query-document", "user-item", "source-target", "sender-receiver",
    "client-server", "producer-consumer", "predator-prey", "parent-child", "prompt-response",
    "time-frequency",
)
EQUAL_PAIR_RE = re.compile(
    r"(?<![\w-])(?:" + "|".join(re.escape(p) for p in sorted(EQUAL_PAIRS, key=len, reverse=True))
    + r")(?![A-Za-z])"
)

ACRONYM_RE = re.compile(r"\b([A-Z]{2,6}[0-9]{0,2})s?\b")
# Capitals that are not abbreviations a reader needs expanded: roman numerals, to-do
# markers, units of storage, era and clock abbreviations, the logical OR, and a few country
# and organisation names. The house rule (R5) expands every other abbreviation at first use in
# the body, common ones included (artificial intelligence (AI), application programming
# interface (API), graphics processing unit (GPU), confidence interval (CI)); a proper name of
# a work, system or format gets a descriptive noun instead ("the BERT encoder"), and
# --allow-terms names it so that it is not reported.
ACRONYM_OK = {
    "USA", "US", "UK", "EU", "UN", "IEEE", "ACM", "ISO", "NVIDIA",
    "OK", "OR", "AM", "PM", "BC", "AD", "CE", "BCE", "II", "III", "IV", "VI", "VII",
    "VIII", "IX", "XI", "XII", "XIII", "XIV", "XV", "XX", "TODO", "TBD", "FIXME", "XXX",
    "KB", "MB", "GB", "TB", "PB",
}

# House rule R6: no internal identifiers of the studied software in the text. A candidate
# token is a run of letters, digits and underscores, possibly joined by dots or slashes.
IDENT_TOKEN_RE = re.compile(r"(?<![\w\u2039])[A-Za-z0-9_]+(?:[./][A-Za-z0-9_]+)*")
IDENT_CAMEL_RE = re.compile(r"[a-z][A-Z]")
IDENT_SNAKE_RE = re.compile(r"[A-Za-z0-9]_[A-Za-z0-9]")
IDENT_VERSION_RE = re.compile(r"v?\d+(?:\.\d+){2,}")
IDENT_HEX_RE = re.compile(r"[0-9a-f]{7,40}|[0-9A-F]{7,40}")
IDENT_VERSION_PHRASE_RE = re.compile(
    r"\b(?:[Vv]ersions?|[Bb]undles?|[Rr]eleases?)\s+v?\d+(?:\.\d+)+(?![\w.]*\d)")
# A number such as 3.2.1 after one of these words is a section or item number, not a version.
IDENT_NUMBERING_RE = re.compile(
    r"(?:\b(?:sections?|secs?|chapters?|ch|appendix|appendices|figures?|figs?|tables?|tabs?|"
    r"eqs?|equations?|theorems?|lemmas?|definitions?|propositions?|corollar(?:y|ies)|remarks?|"
    r"examples?|exercises?|problems?|steps?|items?|parts?|clauses?|paragraphs?|algorithms?|"
    r"lines?|listings?|annex)\.?|\u00a7)\s*$", re.IGNORECASE)
# A name with an internal capital that is cited right after it ("ToolSandbox \cite{...}", "the
# ToolLLM framework \cite{...}") or defined with an abbreviation ("NormalFloat (NF4)") names a
# published work or a public term, not the studied software; it is then known for the whole run.
IDENT_CITED_AFTER_RE = re.compile(
    r"[\w\u2019'-]*(?:\s+[a-z][a-z-]{1,20}){0,2}\s*(?:\u2039cite\u203a|\([A-Z][A-Za-z0-9-]{1,10}\))")
IDENT_FILE_EXTENSIONS = {
    "py", "ipynb", "js", "mjs", "ts", "tsx", "jsx", "java", "rs", "go", "rb", "sh", "bash",
    "ps1", "json", "jsonl", "yaml", "yml", "toml", "ini", "cfg", "conf", "env", "csv", "tsv",
    "parquet", "sqlite", "db", "sql", "log", "xml", "html", "md", "tex", "bib", "txt", "lock",
    "gguf", "onnx", "pt", "pth", "ckpt", "safetensors", "bin", "npz", "npy", "pkl", "zip", "tar",
    "gz", "tgz", "whl", "dockerfile",
}
# Names of public software, companies and people with an internal capital, which R6 keeps.
# Lower case; --allow-terms adds more.
PUBLIC_MIXED_CASE_NAMES = {
    "github", "gitlab", "javascript", "typescript", "pytorch", "tensorflow", "latex", "tikz",
    "bibtex", "biblatex", "mcnemar", "mccabe", "mcdonald", "mcgraw", "macmillan", "mckinsey",
    "iphone", "ipad", "ios", "macos", "macbook", "openai", "deepseek", "deepmind", "youtube",
    "linkedin", "postgresql", "mongodb", "numpy", "scipy", "opencv", "openmp", "fastapi",
    "graphql", "websocket", "powerpoint", "jupyterlab", "chatgpt", "huggingface", "langchain",
    "llamaindex", "lightgbm", "catboost", "openreview", "researchgate", "arxiv", "biorxiv",
    "medrxiv", "pubmed", "openstreetmap", "ardupilot", "qgroundcontrol", "airsim", "autocad",
    "imagenet", "wordnet", "resnet", "alexnet", "googlenet", "mobilenet", "efficientnet",
    "densenet", "pointnet", "convnet", "sentencepiece", "wordpiece", "fasttext", "glove",
    "spacy", "biobert", "scibert", "codebert", "distilbert", "starcoder", "deepspeed",
    "humaneval", "hotpotqa", "triviaqa", "toolbench", "agentbench", "webarena",
    "node.js", "vue.js", "next.js", "d3.js", "three.js", "chart.js", "llama.cpp", "whisper.cpp",
}

# Title style (references/structure.md, "Titles"). The document title is \title{...} in LaTeX
# (preamble or body, with an optional [short] argument and \thanks or \tnoteref notes
# removed), the YAML front-matter "title:" in Markdown, or, when no file of the run has either,
# the first level-1 "# " heading of the first Markdown or text file.
LATEX_TITLE_RE = re.compile(r"\\title\*?\s*(?:\[[^\]]{0,400}\]\s*)?\{")
LATEX_TITLE_NOTE_RE = re.compile(
    r"\\(?:thanks|tnoteref|tnotetext|fnref|footnote|footnotemark|corref|label|texorpdfstring)\b")
YAML_TITLE_RE = re.compile(r"^title\s*:\s*(.*?)\s*$")
MD_TITLE_RE = re.compile(r"^#\s+(\S.*?)\s*#*\s*$")
# An abbreviation in a title: a token of two or more capitals (digits allowed, a plural "s"
# allowed: GNN, LLMs, GPT-4, 3D is not one) or a mixed-case acronym from the list below.
TITLE_CAPS_RE = re.compile(
    r"(?<![A-Za-z0-9])([A-Z0-9]*[A-Z][A-Z0-9]*[A-Z][A-Z0-9]*)(s?)(?![A-Za-z0-9])")
TITLE_MIXED_ACRONYMS = {
    "IoT", "IIoT", "LiDAR", "eVTOL", "mmWave", "GenAI", "PhD", "MSc", "BSc", "AutoML", "DevOps",
    "MLOps", "LLMOps", "RoBERTa", "ConvNet", "ConvNets", "XGBoost",
}
TITLE_MIXED_RE = re.compile(
    r"(?<![A-Za-z0-9])(" + "|".join(sorted(TITLE_MIXED_ACRONYMS, key=len, reverse=True))
    + r")(?![A-Za-z0-9])")
# Roman numerals up to 39 (Part II, Volume XIV) are not abbreviations.
ROMAN_RE = re.compile(r"X{0,3}(?:IX|IV|V?I{0,3})")
TITLE_NOTE_WORDS = 15      # more words than this: a note
TITLE_WARNING_WORDS = 20   # more words than this: a warning

# A proper name introduced with a descriptive noun ("the ImageNet dataset", "the BERT encoder",
# "the HDF5 file format"): the house rule's form for names, which a reader confirms.
DESCRIPTIVE_NOUN_RE = re.compile(
    r"^\s*(?:\u2039cite\u203a\s*)?(?:[a-z]+\s+){0,2}(?:framework|benchmark|dataset|corpus|"
    r"encoder|decoder|model|method|algorithm|pipeline|library|toolkit|tool|format|protocol|"
    r"standard|system|ranking|suite|metric|score|language|architecture|server|engine|platform|"
    r"package|project|simulator|software|specification|function)s?\b"
)
ABBREVIATION_RE = re.compile(
    r"\b(?:e\.g|i\.e|et\s+al|etc|vs|cf|Figs?|Eqs?|Secs?|Refs?|No|Dr|Prof|Mr|Ms|Mrs|approx|"
    r"resp|viz|ca|Vol|Ch|Thm|Def|Tab|Alg|App)\.|\bpp?\.(?=\s*\d)|\b[A-Z]\.(?=\s+[A-Z])"
)
SENTENCE_END_RE = re.compile(r"[.!?][\"')\]\u201d\u2019]*\s+(?=[\"'(\[\u201c\u2018]?[A-Z\u2039])")
WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'\u2019-]*")

# ---------------------------------------------------------------------------
# Input handling and masking
# ---------------------------------------------------------------------------

LATEX_SKIP_ENVS = {
    "verbatim", "lstlisting", "minted", "comment", "equation", "align", "alignat", "gather",
    "multline", "eqnarray", "displaymath", "flalign", "tikzpicture", "tabular", "tabularx",
    "array", "algorithmic", "thebibliography", "filecontents", "longtable", "tabulary",
    "supertabular", "xltabular", "tblr", "longtblr", "NiceTabular", "algorithm2e", "Verbatim",
    "pgfpicture", "math",
}
MATH_DISPLAY_ENVS = {
    "equation", "align", "alignat", "gather", "multline", "eqnarray", "displaymath", "flalign",
}
LATEX_VERBATIM_ENVS = {"verbatim", "lstlisting", "minted", "comment", "filecontents", "Verbatim"}
# Skipped environments whose labels or steps are text: INTERNAL_IDENTIFIER reads the node text
# of a picture and the text of an algorithm (house rule R6).
LATEX_PICTURE_ENVS = {"tikzpicture", "pgfpicture"}
LATEX_ALGORITHM_ENVS = {"algorithmic", "algorithm2e"}
TIKZ_NODE_TEXT_RE = re.compile(
    r"\b(?:node|label\s*=\s*(?:[a-z ]{1,20}:)?)(?:\s*(?:\[[^\]\n]{0,300}\]|\([^()\n]{0,100}\)|at\b))*"
    r"\s*\{")
LATEX_CODE_ARG_RE = re.compile(
    r"\\(?:verb|lstinline)\*?([^\sA-Za-z{])([^\n]*?)\1|\\(?:lstinline|texttt|code)\{([^{}\n]{0,400})\}")
MD_CODE_SPAN_RE = re.compile(r"`([^`\n]+)`")
# Skipped environments whose cells are text: DASH_IN_PROSE reads them (house rule R1).
LATEX_TABLE_ENVS = {
    "tabular", "tabularx", "longtable", "tabulary", "supertabular", "xltabular", "tblr",
    "longtblr", "NiceTabular",
}
LATEX_FLOAT_ENVS = {
    "figure", "table", "algorithm", "wrapfigure", "subfigure", "longtable", "sidewaysfigure",
    "sidewaystable", "listing",
}
# Environments whose prose is a theorem or a proof: "prove" is expected there.
THEOREM_ENVS = {
    "theorem", "lemma", "proposition", "corollary", "proof", "definition", "claim",
    "conjecture", "remark", "assumption", "axiom", "fact", "observation", "property", "thm",
    "lem", "prop", "cor", "defn", "dfn", "rem", "rmk",
}
LATEX_HEADING_RE = re.compile(
    r"\\(?:part|chapter|section|subsection|subsubsection|paragraph|title|caption)\*?\b"
)
LATEX_BEGIN_RE = re.compile(r"\\begin\{([A-Za-z0-9]+)\*?\}")
LATEX_END_RE = re.compile(r"\\end\{([A-Za-z0-9]+)\*?\}")
LATEX_ENV_TOKEN_RE = re.compile(r"\\(begin|end)\{([A-Za-z0-9]+)\*?\}")
LATEX_ITEM_RE = re.compile(r"\\item(?![A-Za-z])")
LATEX_LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REF_COMMANDS = (
    r"ref|eqref|autoref|autopageref|cref|Cref|cpageref|Cpageref|labelcref|namecref|nameCref|"
    r"lcnamecref|pageref|vref|Vref|vpageref|nameref|subref|zcref"
)
LATEX_REF_RE = re.compile(
    r"\\(?:" + REF_COMMANDS + r"|crefrange|Crefrange|cpagerefrange)\*?(?:\[[^\]\n]{0,200}\]){0,2}"
    r"\{([^}]+)\}(?:\{([^}]+)\})?|\\hyperref\[([^\]]+)\]"
)
LATEX_CITE_RE = re.compile(r"\\[A-Za-z]*[Cc]ite[A-Za-z]*\*?(?:\[[^\]]{0,200}\])*\{[^}]*\}")
LATEX_REF_MASK_RE = re.compile(
    r"\\(?:" + REF_COMMANDS + r")\*?(?:\[[^\]\n]{0,200}\]){0,2}\{[^}]*\}"
)
LATEX_COMMENT_RE = re.compile(r"(?<!\\)%.*")
# Inline mathematics delimiters, tracked across lines in LaTeX: $, $$, \( \), \[ \].
INLINE_MATH_TOKEN_RE = re.compile(r"(?<!\\)\$\$?|\\\(|\\\)|(?<!\\)\\\[|(?<!\\)\\\]")
LATEX_ACCENT_RE = re.compile(
    r"\\['`^\"~=.]\{?([A-Za-z])\}?|\\[Hcvudbtkr](?:\{([A-Za-z])\}|\s([A-Za-z]))"
    r"|\\(i|j|o|O|l|L|ss|ae|AE|oe|OE|aa|AA)(?![A-Za-z])"
)
LATEX_DROP_RE = re.compile(
    r"\\(?:label|input|include|includegraphics|bibliography|bibliographystyle|"
    r"usepackage|documentclass|vspace|hspace|setlength|newcommand|renewcommand|"
    r"setcounter|addtocounter|addtolength|definecolor|captionsetup|hypersetup|newtheorem|"
    r"newenvironment|renewenvironment|DeclareMathOperator|pagenumbering|pagestyle|"
    r"thispagestyle|numberwithin|graphicspath|colorlet|tikzset|pgfplotsset|lstset|algtext|"
    r"algrenewtext|algnotext|algnewcommand|algrenewcommand|algdef|algblock|algblockdefx|"
    r"algcblock|algcblockdefx)"
    r"\*?(?:\[[^\]]{0,200}\])*(?:\{[^}]*\})*"
)
# Quoted text is someone else's words or a mention of a phrase ("the the"), not the author's
# prose; it is masked, keeping its length, before the prose rules run.
QUOTED_RE = re.compile(
    "\"[^\"\\n]{1,300}\"|\u201c[^\u201d]{1,300}\u201d|``.{1,300}?''")
QUOTE = "\u2039quote\u203a"
PAREN_SPAN_RE = re.compile(r"\([^()]{0,400}\)")
MD_LIST_ITEM_RE = re.compile(r"^(\s*)(?:[-*+]|\d{1,3}[.)])\s+")
MD_CAPTION_RE = re.compile(r"^\s*(?:[*_]{1,2})?(Figure|Fig\.|Table)\s+(\d+)\s*[.:]", re.IGNORECASE)
MD_MENTION_RE = re.compile(r"\b(Figure|Fig\.|Table)s?\s+(\d+)", re.IGNORECASE)
# Author-year citations. A parenthetical one, "(Lee and Osei, 2021; Kim 2019a)", is found by
# testing each innermost "( ... )" group in linear time: a capital letter and no digit before
# the year, a space just before it, and only further citations after it. (One backtracking
# regex for this took quadratic time on long lines.)
PAREN_GROUP_RE = re.compile(r"\(([^()]+)\)")
CAPITAL_RE = re.compile(r"[A-Z]")
DIGIT_RE = re.compile(r"\d")
YEAR_TAIL_RE = re.compile(r"(?:1[5-9]|20)\d{2}[a-z]?(?:\s*[;,][^()]*)?")
NARRATIVE_CITE_RE = re.compile(
    r"\b[A-Z][A-Za-z\u2019'-]{1,40}(?:\s+et\s+al\.?|\s+(?:and|&)\s+[A-Z][A-Za-z\u2019'-]{1,40})?"
    r"\s+\((?:1[5-9]|20)\d{2}[a-z]?(?:,[^()]*)?\)"
)
NUMERIC_CITE_RE = re.compile(r"\[\d+(?:\s*[,\u2013-]\s*\d+)*\]")
URL_RE = re.compile(r"https?://\S+")


class InputError(ValueError):
    """Raised when an input file fails a safety check."""


def read_manuscript(path_value: str) -> tuple[Path, str]:
    path = Path(path_value)
    if path.is_symlink():
        raise InputError(f"{path}: symbolic links are not accepted")
    if not path.is_file():
        raise InputError(f"{path}: not an existing regular file")
    if path.suffix.lower() not in SUFFIXES:
        raise InputError(f"{path}: extension must be one of {', '.join(sorted(SUFFIXES))}")
    if path.stat().st_size > MAX_FILE_BYTES:
        raise InputError(f"{path}: larger than {MAX_FILE_BYTES} bytes")
    try:
        return path, path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise InputError(f"{path}: not UTF-8 text") from exc


def mask_inline_math(line: str, open_: bool) -> tuple[str, bool]:
    """Mask LaTeX inline mathematics, which may start on one line and end on a later one.

    Returns the line with each math span replaced by a marker, and whether a span is still
    open at the end of the line."""
    out: list[str] = []
    position = 0
    inside = open_
    for match in INLINE_MATH_TOKEN_RE.finditer(line):
        token = match.group(0)
        if not inside:
            if token in ("\\)", "\\]"):
                continue
            out.append(line[position:match.start()])
            inside = True
        else:
            if token in ("\\(", "\\["):
                continue
            out.append(f" {MATH} ")
            position = match.end()
            inside = False
    if inside:
        out.append(f" {MATH} ")
        return "".join(out), True
    out.append(line[position:])
    return "".join(out), False


def _mask_quote(match: re.Match[str]) -> str:
    text = match.group(0)
    opener = 2 if text.startswith("``") else 1
    inner = text[opener:len(text) - opener]
    body = inner.rstrip(".,;:!?")
    tail = inner[len(body):]
    filler = QUOTE + " " * (len(body) - len(QUOTE)) if len(body) >= len(QUOTE) else " " * len(body)
    return text[:opener] + filler + tail + text[len(text) - opener:]


def mask_quotes(text: str) -> str:
    """Mask quoted passages without changing the length of the text."""
    return QUOTED_RE.sub(_mask_quote, text)


def _accent(match: re.Match[str]) -> str:
    return match.group(1) or match.group(2) or match.group(3) or match.group(4) or ""


def mask_latex(line: str) -> str:
    line = LATEX_CITE_RE.sub(f" {CITE} ", line)
    line = LATEX_REF_MASK_RE.sub(f" {REF} ", line)
    line = re.sub(r"\\\(.*?\\\)|(?<!\\)\$[^$]*\$", f" {MATH} ", line)
    line = re.sub(r"\\(?:verb|lstinline)(\W).*?\1", f" {CODE} ", line)
    line = re.sub(r"\\(?:url|href)\{[^}]*\}", f" {URL} ", line)
    line = re.sub(r"\\(?:begin|end)\{[^}]*\}(?:\[[^\]]{0,200}\])*(?:\{[^}]*\})*", " ", line)
    line = LATEX_DROP_RE.sub(" ", line)
    line = LATEX_EMPHASIS_RE.sub(_mask_mention, line)
    line = re.sub(r"\\textendash(?![A-Za-z])\s?", "--", line)
    line = re.sub(r"\\textemdash(?![A-Za-z])\s?", "---", line)
    line = LATEX_ACCENT_RE.sub(_accent, line)
    line = re.sub(r"\\[-@/]", "", line)
    # A bare & is an alignment tab; \& is an ampersand in the text.
    line = line.replace("\\&", "\x00").replace("&", " ").replace("\x00", "&")
    line = line.replace("\\%", "%").replace("\\_", "_").replace("\\$", "$")
    line = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]{0,200}\])?", " ", line)
    line = re.sub(r"\\.", " ", line)
    return line.replace("{", "").replace("}", "").replace("~", " ")


MENTION_WORDS = {"and", "or", "but", "nor", "the", "a", "an", "of", "to", "is", "not", "and/or"}


def _is_mention(inner: str) -> bool:
    """An italic word list ("*may, might, could*") or an italic function word ("*and*") is
    a mention of words, as in a style guide, not prose."""
    items = [item.strip() for item in inner.split(",")]
    if len(items) >= 3 and all(0 < len(item.split()) <= 4 for item in items):
        return True
    return inner.strip().lower() in MENTION_WORDS


def _mask_mention(match: re.Match[str]) -> str:
    inner = next(group for group in match.groups() if group is not None)
    return f" {QUOTE} " if _is_mention(inner) else match.group(0)


MD_EMPHASIS_RE = re.compile(r"(?<![\w*])\*([^*\n]{1,400})\*(?![\w*])|(?<![\w_])_([^_\n]{1,400})_(?![\w_])")
LATEX_EMPHASIS_RE = re.compile(r"\\(?:emph|textit)\{([^{}]{1,400})\}")


def mask_markdown(line: str) -> str:
    line = re.sub(r"`[^`]*`", f" {CODE} ", line)
    line = re.sub(r"(?<!\\)\$[^$]+\$", f" {MATH} ", line)
    line = MD_EMPHASIS_RE.sub(_mask_mention, line)
    # Bounded classes keep these linear on long lines with unmatched "(" or "<".
    line = re.sub(r"!\[([^\]]{0,500})\]\([^()\n]{0,2000}\)", r"\1", line)
    line = re.sub(r"\[([^\]]{0,500})\]\([^()\n]{0,2000}\)", r"\1", line)
    line = re.sub(r"\[(?=[^\]]{0,500}\])[^\]@]*@[^\]]*\]", f" {CITE} ", line)
    line = re.sub(r"(?<![\w.])@[A-Za-z0-9_][\w:.-]*", f" {CITE} ", line)
    line = re.sub(r"\[\^[^\]]+\]", " ", line)
    line = re.sub(r"</?[A-Za-z][^<>\n]{0,200}>", " ", line)
    # Emphasis marks go; an underscore inside a word (snake_case) is not emphasis and stays.
    return re.sub(r"\*{1,3}(?=\S)|(?<=\S)\*{1,3}|(?<![A-Za-z0-9])_{1,3}(?=\S)"
                  r"|(?<=\S)_{1,3}(?![A-Za-z0-9])", "", line)


def _mask_paren_citation(match: re.Match[str]) -> str:
    inner = match.group(1)
    digit = DIGIT_RE.search(inner)
    if digit:
        prefix = inner[: digit.start()]
        if (len(prefix) >= 2 and prefix[-1].isspace() and CAPITAL_RE.search(prefix)
                and YEAR_TAIL_RE.fullmatch(inner, digit.start())):
            return f" {CITE} "
    return match.group(0)


def mask_common(line: str) -> str:
    line = URL_RE.sub(f" {URL} ", line)
    line = NUMERIC_CITE_RE.sub(f" {CITE} ", line)
    line = PAREN_GROUP_RE.sub(_mask_paren_citation, line)
    return NARRATIVE_CITE_RE.sub(f" {CITE} ", line)


def _braced(text: str, start: int) -> int:
    """Index just past the brace group whose "{" is at text[start - 1]; -1 if unbalanced."""
    depth = 1
    position = start
    while position < len(text) and position - start < 4000:
        char = text[position]
        if char == "\\":
            position += 2
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return position + 1
        position += 1
    return -1


def clean_latex_title(title: str) -> str:
    """Plain text of a LaTeX title: notes, mathematics and markup removed."""
    out = []
    position = 0
    for match in LATEX_TITLE_NOTE_RE.finditer(title):
        if match.start() < position:
            continue
        out.append(title[position:match.start()])
        end = match.end()
        brace = re.match(r"\s*(?:\[[^\]]{0,200}\])?\s*\{", title[end:])
        if brace:
            stop = _braced(title, end + brace.end())
            end = stop if stop > 0 else len(title)
        position = end
    out.append(title[position:])
    text = re.sub(r"\\\\(?:\[[^\]]{0,20}\])?|\\newline\b", " ", "".join(out))
    text = mask_latex(text).replace(MATH, " ")
    return " ".join(MARKER_RE.sub(" ", text).split())


def extract_title(text: str, latex: bool) -> tuple[int, str, bool] | None:
    """The document title of one file: (line, plain text, explicit), or None."""
    lines = text.splitlines()
    if latex:
        stripped = "\n".join(LATEX_COMMENT_RE.sub("", line) for line in lines)
        for match in LATEX_TITLE_RE.finditer(stripped):
            if re.search(r"\\(?:re)?newcommand\*?\s*\{?\s*$",
                         stripped[max(0, match.start() - 30):match.start()]):
                continue   # \renewcommand{\title}: a definition, not the title
            end = _braced(stripped, match.end())
            if end < 0:
                return None
            title = clean_latex_title(stripped[match.end():end - 1])
            if title:
                return stripped.count("\n", 0, match.start()) + 1, title, True
        return None
    if lines and lines[0].strip() == "---":
        for number, line in enumerate(lines[1:], start=2):
            if line.strip() in {"---", "..."}:
                break
            found = YAML_TITLE_RE.match(line)
            if not found:
                continue
            value = found.group(1)
            if value in {"|", ">", "|-", ">-", ""}:   # a block scalar on the next lines
                block = []
                for follow in lines[number:]:
                    if not follow.startswith((" ", "\t")) or not follow.strip():
                        break
                    block.append(follow.strip())
                value = " ".join(block)
            value = value.strip().strip("\"'").strip()
            if value:
                return number, " ".join(mask_markdown(value).replace(MATH, " ").split()), True
    in_fence = False
    for number, line in enumerate(lines, start=1):
        if line.strip().startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        found = None if in_fence else MD_TITLE_RE.match(line)
        if found:
            title = " ".join(MARKER_RE.sub(" ", mask_markdown(found.group(1))).split())
            return (number, title, False) if title else None
    return None


class Document:
    """One input file split into raw lines, prose paragraphs and headings."""

    def __init__(self, path: Path, text: str) -> None:
        self.path = path
        self.latex = path.suffix.lower() in LATEX_SUFFIXES
        self.raw: list[tuple[int, str]] = []         # comment-stripped lines outside code
        self.paragraphs: list[list[tuple[int, str]]] = []
        self.paragraph_theorem: list[bool] = []       # paragraph lies in a theorem or proof
        self.paragraph_item: list[bool] = []          # paragraph is a list item
        self.paragraph_abstract: list[bool] = []      # paragraph lies in the abstract
        self.table_lines: list[tuple[int, str]] = []  # masked text of table cells
        # Masked node text of pictures and text of algorithms, with where it was found.
        self.figure_lines: list[tuple[int, str, str]] = []
        self.code_spans: list[tuple[int, str]] = []   # \texttt, \verb or `code` arguments
        self.headings: list[tuple[int, str]] = []
        # Document title: (line, text, explicit), explicit for \title or YAML "title:".
        self.title: tuple[int, str, bool] | None = None
        self.labels: list[tuple[str, int, bool]] = []  # name, line, defined inside a float
        self.refs: list[tuple[str, int]] = []
        self.display_blocks = 0
        self.includes = 0   # line of the first \input, \include or \subfile in a LaTeX file
        self._parse(text)
        self.title = extract_title(text, self.latex)
        with_math = sum(any(MATH in t for _, t in p) for p in self.paragraphs)
        # Mostly mathematics: "this proves" there is a derivation, not an empirical claim.
        self.math_heavy = (self.display_blocks + with_math) >= max(5, 0.2 * len(self.paragraphs))

    def _parse(self, text: str) -> None:
        current: list[tuple[int, str]] = []
        current_theorem = False
        current_item = False
        current_abstract = False
        skip_env: str | None = None
        float_depth = 0
        theorem_depth = 0
        abstract_depth = 0
        md_abstract = False
        inline_open = False
        in_fence = in_display = in_comment = in_front_matter = in_list = False
        lines = text.splitlines()
        body_start = 0
        if self.latex:
            for number, original in enumerate(lines, start=1):
                if "\\begin{document}" in LATEX_COMMENT_RE.sub("", original):
                    body_start = number
                    break

        def flush() -> None:
            nonlocal current, current_theorem, current_item, current_abstract
            if current:
                self.paragraphs.append(current)
                self.paragraph_theorem.append(current_theorem)
                self.paragraph_item.append(current_item)
                self.paragraph_abstract.append(current_abstract)
                current = []
            current_theorem = False
            current_item = False
            current_abstract = False

        def add_table_line(number: int, line: str) -> None:
            # Column separators and row ends become a visible mark, so that a cell holding
            # only a dash can be told from a dash between words.
            line = re.sub(r"(?<!\\)&|\\\\", " \u2502 ", mask_inline_math(line, False)[0])
            masked = mask_common(mask_latex(line))
            if MARKER_RE.sub("", masked).strip():
                self.table_lines.append((number, masked))
            self._scan_code(line, number)

        def add_figure_line(number: int, line: str, env: str) -> None:
            if env in LATEX_ALGORITHM_ENVS:
                parts = [line]
                where = " in an algorithm"
            else:
                parts = []
                for match in TIKZ_NODE_TEXT_RE.finditer(line):
                    end = _braced(line, match.end())
                    parts.append(line[match.end():end - 1 if end > 0 else len(line)])
                where = " in a figure label"
            for part in parts:
                part = mask_inline_math(part, False)[0]
                self._scan_code(part, number)
                masked = mask_common(mask_latex(part))
                if MARKER_RE.sub("", masked).strip():
                    self.figure_lines.append((number, masked, where))

        def track_envs(line: str) -> None:
            nonlocal float_depth, theorem_depth, abstract_depth
            for kind, name in LATEX_ENV_TOKEN_RE.findall(line):
                if kind == "begin":
                    float_depth += name in LATEX_FLOAT_ENVS
                    theorem_depth += name in THEOREM_ENVS
                    abstract_depth += name == "abstract"
                else:
                    if name in LATEX_FLOAT_ENVS and float_depth:
                        float_depth -= 1
                    if name in THEOREM_ENVS and theorem_depth:
                        theorem_depth -= 1
                    if name == "abstract" and abstract_depth:
                        abstract_depth -= 1

        for number, original in enumerate(lines, start=1):
            line = original
            stripped = line.strip()
            if self.latex:
                if number < body_start:
                    meta = LATEX_COMMENT_RE.sub("", line)
                    if PREAMBLE_META_RE.search(meta):
                        self.raw.append((number, meta))   # \title{TODO}: placeholder rules only
                    continue
                line = LATEX_COMMENT_RE.sub("", line)
                stripped = line.strip()
                if skip_env:
                    end = re.search(r"\\end\{" + re.escape(skip_env) + r"\*?\}", line)
                    if skip_env in LATEX_TABLE_ENVS:
                        add_table_line(number, line[:end.start()] if end else line)
                    elif skip_env in LATEX_PICTURE_ENVS | LATEX_ALGORITHM_ENVS:
                        add_figure_line(number, line[:end.start()] if end else line, skip_env)
                    if end:
                        skip_env = None
                        track_envs(line[end.start():])
                    elif skip_env not in LATEX_VERBATIM_ENVS:
                        self.raw.append((number, line))
                        self._scan_labels(line, number, float_depth > 0)
                    continue
                begun = LATEX_BEGIN_RE.findall(line)
                if not self.includes and re.search(r"\\(?:input|include|subfile)\{", line):
                    self.includes = number
                track_envs(line)
                self.raw.append((number, line))
                self._scan_labels(line, number, float_depth > 0)
                skipped = [name for name in begun if name in LATEX_SKIP_ENVS]
                self.display_blocks += sum(name in MATH_DISPLAY_ENVS for name in begun)
                if skipped:
                    if skipped[-1] in LATEX_TABLE_ENVS:
                        add_table_line(number, line)
                    elif skipped[-1] in LATEX_PICTURE_ENVS | LATEX_ALGORITHM_ENVS:
                        add_figure_line(number, line, skipped[-1])
                    if not re.search(r"\\end\{" + re.escape(skipped[-1]) + r"\*?\}", line):
                        skip_env = skipped[-1]
                    flush()
                    inline_open = False
                    continue
                if in_display:
                    if "\\]" in line or "$$" in line:
                        in_display = False
                    continue
                if stripped.startswith("\\["):
                    self.display_blocks += 1
                    in_display = "\\]" not in stripped
                    flush()
                    inline_open = False
                    continue
                if stripped.startswith("$$"):
                    self.display_blocks += 1
                    in_display = stripped.count("$$") < 2
                    flush()
                    inline_open = False
                    continue
                if not stripped:
                    flush()
                    inline_open = False
                    continue
                if LATEX_ITEM_RE.match(stripped):
                    flush()   # each list item is its own paragraph
                    current_item = True
                line, inline_open = mask_inline_math(line, inline_open)
                self._scan_code(line, number)
                masked = mask_common(mask_latex(line))
                if LATEX_HEADING_RE.match(stripped):
                    flush()
                    runin = RUNIN_HEADING_RE.match(line.lstrip())
                    rest = line.lstrip()[runin.end():] if runin else ""
                    if runin and re.search(r"[A-Za-z]{2}", rest):
                        # \paragraph{Title.} Text ...: the text is the paragraph's first line.
                        title = line.lstrip()[:runin.end()]
                        self.headings.append((number, mask_common(mask_latex(title))))
                        current.append((number, mask_common(mask_latex(rest))))
                        current_theorem = theorem_depth > 0
                        current_abstract = abstract_depth > 0
                        continue
                    self.headings.append((number, masked))
                    continue
                if not re.search(r"[A-Za-z]{2}", MARKER_RE.sub("", masked)):
                    if not MARKER_RE.search(masked):
                        flush()   # structural line such as \\begin{itemize} or \\maketitle
                    continue
                current.append((number, masked))
                current_theorem = current_theorem or theorem_depth > 0
                current_abstract = current_abstract or abstract_depth > 0
                continue

            # Markdown and plain text
            if number == 1 and stripped == "---":
                in_front_matter = True
                continue
            if in_front_matter:
                if stripped in {"---", "..."}:
                    in_front_matter = False
                continue
            if stripped.startswith(("```", "~~~")):
                in_fence = not in_fence
                flush()
                continue
            if in_fence:
                continue
            if in_comment:
                if "-->" in line:
                    in_comment = False
                continue
            line = re.sub(r"<!--.*?-->", "", line)
            if "<!--" in line:
                in_comment = True
                line = line.split("<!--", 1)[0]
            stripped = line.strip()
            if stripped == "$$":
                self.display_blocks += not in_display
                in_display = not in_display
                flush()
                continue
            if in_display:
                continue
            item = MD_LIST_ITEM_RE.match(line)
            is_item = bool(item and (len(item.group(1).expandtabs(4)) <= 3 or in_list))
            if stripped and not is_item and line.startswith(("    ", "\t")) and not current \
                    and not in_list:
                continue   # indented code block: not prose, and not checked for placeholders
            self.raw.append((number, re.sub(r"`[^`]*`", " ", line)))
            self._scan_code(line, number)
            if not stripped:
                flush()
                continue
            if stripped.startswith("#"):
                flush()
                in_list = False
                heading = stripped.lstrip("# ")
                md_abstract = heading.strip(" *_:.").lower() == "abstract"
                self.headings.append((number, mask_common(mask_markdown(heading))))
                continue
            if stripped.startswith("|") or re.fullmatch(r"[-=*_\s]{3,}", stripped):
                flush()
                if stripped.startswith("|") and not MD_TABLE_RULE_RE.match(stripped):
                    self.table_lines.append((number, mask_common(mask_markdown(line))))
                continue
            if is_item:
                flush()   # each list item is its own paragraph
                in_list = True
                current_item = True
            elif not line.startswith((" ", "\t")) and not current:
                in_list = False
            masked = mask_common(mask_markdown(line))
            masked = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", masked)
            masked = re.sub(r"^\s*\[[ xX]\]\s+", "", masked)   # task-list checkbox
            masked = re.sub(r"^\s*>+\s?", "", masked)
            current.append((number, masked))
            current_abstract = current_abstract or md_abstract
        flush()

    def _scan_code(self, line: str, number: int) -> None:
        """Collect the arguments of \\texttt, \\verb, \\lstinline and \\code, or Markdown
        inline code, for house rule R6. Comments and mathematics are already removed."""
        if self.latex:
            for match in LATEX_CODE_ARG_RE.finditer(line):
                text = match.group(2) if match.group(2) is not None else match.group(3)
                text = re.sub(r"\\[-/@,]|\\(?:allowbreak|linebreak|break|hspace\{[^}]*\})", "", text)
                text = re.sub(r"\\([_&%$#{}~^])", r"\1", text)
                text = re.sub(r"\\[A-Za-z]+\*?\s*", "", text).replace("{", "").replace("}", "")
                self.code_spans.append((number, text.strip()))
        else:
            for match in MD_CODE_SPAN_RE.finditer(line):
                self.code_spans.append((number, match.group(1).strip()))

    def _scan_labels(self, line: str, number: int, in_float: bool) -> None:
        for name in LATEX_LABEL_RE.findall(line):
            self.labels.append((name.strip(), number, in_float))
        for match in LATEX_REF_RE.finditer(line):
            for group in match.groups():
                if group:
                    for name in group.split(","):
                        self.refs.append((name.strip(), number))


def join_paragraph(paragraph: list[tuple[int, str]]) -> tuple[str, list[tuple[int, int]]]:
    """Join a paragraph's lines with spaces; return the text and (offset, line) starts."""
    starts: list[tuple[int, int]] = []
    offset = 0
    for number, text in paragraph:
        starts.append((offset, number))
        offset += len(text) + 1
    return " ".join(text for _, text in paragraph), starts


def line_at(starts: list[tuple[int, int]], position: int) -> int:
    index = bisect.bisect_right(starts, (position, float("inf"))) - 1
    return starts[max(index, 0)][1]


def sentences_of(paragraph: list[tuple[int, str]], joined: str | None = None,
                 starts: list[tuple[int, int]] | None = None) -> list[tuple[int, str]]:
    """Return (line number of first character, sentence text) pairs for one paragraph."""
    if joined is None or starts is None:
        joined, starts = join_paragraph(paragraph)
    protected = ABBREVIATION_RE.sub(lambda m: m.group(0).replace(".", "\u2024"), joined)

    result: list[tuple[int, str]] = []
    begin = 0
    for match in SENTENCE_END_RE.finditer(protected):
        end = match.end()
        chunk = joined[begin:end]
        if chunk.strip():
            lead = len(chunk) - len(chunk.lstrip())
            result.append((line_at(starts, begin + lead), chunk.strip()))
        begin = end
    tail = joined[begin:]
    if tail.strip():
        lead = len(tail) - len(tail.lstrip())
        result.append((line_at(starts, begin + lead), tail.strip()))
    return result


def count_words(sentence: str) -> int:
    """Words in a sentence, not counting masked mathematics, code, citations or URLs."""
    return len(WORD_RE.findall(MARKER_RE.sub(" ", sentence)))


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


class Report:
    def __init__(self, disabled: set[str] | None = None) -> None:
        self.findings: list[dict[str, object]] = []
        self.disabled = disabled or set()

    def add(self, path: Path, line: int, severity: str, code: str, detail: str) -> None:
        if code in self.disabled:
            return
        self.findings.append(
            {"file": str(path), "line": line, "severity": severity, "code": code, "detail": detail}
        )


def quote(text: str) -> str:
    text = " ".join(text.split())
    return text if len(text) <= 60 else text[:57] + "..."


def check_raw_lines(doc: Document, report: Report) -> None:
    for number, line in doc.raw:
        scan = LATEX_OPTIONAL_ARG_RE.sub(r"\1", LATEX_CODE_RE.sub(" ", line)) if doc.latex else line
        taken: list[tuple[int, int]] = []
        for pattern in PLACEHOLDER_PATTERNS:
            for match in pattern.finditer(scan):
                if any(match.start() < end and start < match.end() for start, end in taken):
                    continue   # the same placeholder, already matched by an earlier rule
                taken.append(match.span())
                report.add(doc.path, number, "error", "UNRESOLVED_PLACEHOLDER",
                           f'"{quote(match.group(0))}" is still in the text')
        if PERSONAL_DATA_RE.search(line):
            report.add(doc.path, number, "warning", "POSSIBLE_PERSONAL_DATA",
                       "looks like an identifier field; confirm it may appear in this document")


def check_split_placeholders(doc: Document, report: Report) -> None:
    """Report bracket placeholders broken across lines, such as "[insert" / "citation]"."""
    for paragraph in doc.paragraphs:
        if len(paragraph) < 2:
            continue
        joined, starts = join_paragraph(paragraph)
        for match in BRACKET_PLACEHOLDER_RE.finditer(joined):
            first = line_at(starts, match.start())
            if first != line_at(starts, match.end() - 1):
                report.add(doc.path, first, "error", "UNRESOLVED_PLACEHOLDER",
                           f'"{quote(match.group(0))}" is still in the text')


def check_dashes(doc: Document, text: str, starts: list[tuple[int, int]], report: Report,
                 where: str = "") -> None:
    """House rule R1: every en or em dash in masked prose, a caption or a table cell."""
    pattern = TEX_DASH_RE if doc.latex else PLAIN_DASH_RE
    for match in pattern.finditer(text):
        dash = match.group(0)
        before = text[match.start() - 1] if match.start() else " "
        after = text[match.end():match.end() + 1]
        if dash.startswith("-") and len(dash) == 2 and before.isspace() and after.isalpha():
            continue   # a command-line option such as --json
        kind = "em dash" if dash in {"---", "\u2014", "\u2015"} else "en dash"
        context = text[max(0, match.start() - 20):match.end() + 20]
        number = DASH_RANGE_RE.search(text[max(0, match.start() - 12):match.start()])
        later = re.match(r"\s?([\u2212-]?\d[\d.,]*)", text[match.end():match.end() + 12])
        if number and later:
            advice = f'write "{number.group(1)} to {later.group(1)}"'
        elif kind == "en dash" and before.isalpha() and after.isalpha():
            advice = ("join a pair of names or equal terms with a hyphen (Kullback-Leibler) or "
                      "rewrite it; otherwise use a comma, a colon or parentheses")
        elif where and re.search(r"(?:^|[|\u2502])\s*$", text[:match.start()]) and re.match(
                r"\s*(?:$|[|\u2502])", text[match.end():]):
            advice = ("a cell holding only a dash: leave it empty, or write a word (none, not "
                      "applicable) and explain it in the table note")
        else:
            advice = "use a comma, a colon, parentheses or a new sentence"
        report.add(doc.path, line_at(starts, match.start()), "warning", "DASH_IN_PROSE",
                   f'"{quote(context.strip())}": {kind}{where}; {advice}')


IDENT_ADVICE = ("describe the thing in plain words; versions and hashes go to the availability "
                "statement or the evidence record")


def _identifier_kind(token: str) -> str:
    """What an identifier-like token looks like, or "" if it looks like an ordinary word."""
    if IDENT_VERSION_RE.fullmatch(token):
        return "a version number"
    if IDENT_HEX_RE.fullmatch(token) and re.search(r"\d", token) and re.search(r"[A-Fa-f]", token):
        return "a hash or hash prefix"
    path_parts = token.split("/")
    name_parts = path_parts[-1].split(".")
    if (len(name_parts) >= 2 and name_parts[-1].lower() in IDENT_FILE_EXTENSIONS
            and re.search(r"[A-Za-z]", ".".join(name_parts[:-1]))):
        return "a file name"
    for part in path_parts:
        dotted = part.split(".")
        if (len(dotted) >= 3 and all(re.match(r"[A-Za-z_]", piece) for piece in dotted)
                and sum(len(piece) >= 2 for piece in dotted) >= 2):
            return "a namespaced code path"
        for piece in dotted:
            if IDENT_SNAKE_RE.search(piece) and re.search(r"[A-Za-z]", piece):
                return "a code identifier (snake_case)"
            if IDENT_CAMEL_RE.search(piece) and sum(c.islower() for c in piece) >= 3:
                return "a function or method name (camelCase)"
    return ""


def identifier_tokens(text: str, known: set[str]) -> list[tuple[int, str, str]]:
    """House rule R6: (offset, token, kind) for every identifier-like token in masked text."""
    found: list[tuple[int, str, str]] = []
    taken: list[tuple[int, int]] = []
    for match in IDENT_VERSION_PHRASE_RE.finditer(text):
        found.append((match.start(), match.group(0), "a version number"))
        taken.append(match.span())
    for match in IDENT_TOKEN_RE.finditer(text):
        if any(start <= match.start() < end for start, end in taken):
            continue
        token = match.group(0).rstrip("._/")
        if token.lower() in known:
            continue
        if re.search(r"=\s*$", text[max(0, match.start() - 3):match.start()]) or \
                text.startswith("!", match.end()):
            continue   # a key value in options (draw=cBlue, fill=cBlue!7), not prose
        kind = _identifier_kind(token)
        if kind == "a version number" and IDENT_NUMBERING_RE.search(text[:match.start()]):
            continue   # Section 3.2.1, Table 4.1.2
        if kind:
            found.append((match.start(), token, kind))
    return found


def _identifier_sources(doc: Document) -> list[tuple[str, list[tuple[int, int]], str]]:
    """Masked text that R6 reads: (text, line starts, where) for headings and captions,
    paragraphs, table cells, picture node text and algorithm text."""
    sources: list[tuple[str, list[tuple[int, int]], str]] = []
    for number, heading in doc.headings:
        sources.append((heading, [(0, number)], ""))
    for paragraph in doc.paragraphs:
        joined, starts = join_paragraph(paragraph)
        sources.append((joined, starts, ""))
    for number, cells in doc.table_lines:
        sources.append((cells, [(0, number)], " in a table cell"))
    for number, text, where in doc.figure_lines:
        sources.append((text, [(0, number)], where))
    return sources


def cited_names(docs: list[Document]) -> set[str]:
    """Names with an internal capital that the run cites or defines with an abbreviation
    (published works, public terms); R6 does not report them anywhere in the run."""
    names: set[str] = set()
    for doc in docs:
        for text, _, _ in _identifier_sources(doc):
            for match in IDENT_TOKEN_RE.finditer(text):
                token = match.group(0)
                if IDENT_CAMEL_RE.search(token) and IDENT_CITED_AFTER_RE.match(
                        text, match.end(), match.end() + 80):
                    names.add(token.lower())
    return names


def check_internal_identifiers(doc: Document, report: Report, allow: set[str]) -> None:
    """House rule R6: no names of functions, operations or endpoints, code identifiers, file
    names, versions or hashes of the studied software in prose, captions, tables, figure
    labels or algorithms. Code set in \\texttt (or Markdown backticks) is reported as a whole;
    bare tokens are reported by shape. Names in --allow-terms (passed in as allow, together with
    the names the run cites, see cited_names) and public names with internal capitals
    (PUBLIC_MIXED_CASE_NAMES) are not reported."""
    known = allow | PUBLIC_MIXED_CASE_NAMES
    seen: set[tuple[int, str]] = set()
    for number, text in doc.code_spans:
        if not re.search(r"[A-Za-z]", text) or text.lower() in known:
            continue
        if (number, text.lower()) in seen:
            continue
        seen.add((number, text.lower()))
        for match in IDENT_TOKEN_RE.finditer(text):
            seen.add((number, match.group(0).rstrip("._/").lower()))
        report.add(doc.path, number, "warning", "INTERNAL_IDENTIFIER",
                   f'"{quote(text)}" is set as code (house rule R6): {IDENT_ADVICE}; the name '
                   "of a public tool may stay (--allow-terms)")
    for text, starts, where in _identifier_sources(doc):
        for offset, token, kind in identifier_tokens(text, known):
            number = line_at(starts, offset)
            if (number, token.lower()) in seen:
                continue
            seen.add((number, token.lower()))
            report.add(doc.path, number, "warning", "INTERNAL_IDENTIFIER",
                       f'"{quote(token)}" looks like {kind}{where} (house rule R6): {IDENT_ADVICE}')


def check_mechanics(doc: Document, text: str, starts: list[tuple[int, int]], report: Report,
                    allow: set[str]) -> None:
    """Hyphen, dash and minus rules, on one masked paragraph or heading."""
    path = doc.path
    house = "DASH_IN_PROSE" not in report.disabled
    en_dash = "--" if doc.latex else "\u2013"
    minus = "$-$ in math mode" if doc.latex else "\u2212"

    def at(position: int) -> int:
        return line_at(starts, position)

    taken: list[tuple[int, int]] = []
    for match in FROM_BETWEEN_RANGE_RE.finditer(text):
        tail = text[match.end():match.end() + 30]
        word = match.group(1).lower()
        if (word == "from" and re.search(r"\bto\b", tail)) or (
                word == "between" and re.search(r"\band\b", tail)):
            continue   # "from 3-5 s to 1 s": the range is a value, not the construction
        taken.append(match.span())
        report.add(path, at(match.start()), "warning", "RANGE_AFTER_FROM_BETWEEN",
                   f'"{quote(match.group(0))}": write "from X to Y" or "between X and Y"')
    for match in HYPHEN_RANGE_RE.finditer(text):
        if any(start <= match.start() < end for start, end in taken):
            continue
        first, second = match.group(1), match.group(2)
        if first == second or RANGE_LABEL_BEFORE_RE.search(text[max(0, match.start() - 16):match.start()]):
            continue
        if (len(first) == 4 and first.isdigit() and 1500 <= int(first) <= 2100
                and len(second) == 2 and second.isdigit() and int(second) <= 12):
            continue   # a year and month, 2024-05
        if house:
            report.add(path, at(match.start()), "warning", "HYPHEN_IN_RANGE",
                       f'"{match.group(0)}": write "{first} to {second}" (house rule: no dash '
                       "in a range)")
        else:
            report.add(path, at(match.start()), "warning", "HYPHEN_IN_RANGE",
                       f'"{match.group(0)}": use an en dash ({en_dash}) '
                       'for a range, or "to" in running prose')
    for match in SPACED_HYPHEN_RE.finditer(text):
        context = text[max(0, match.start() - 20):match.end() + 20]
        marks = "a comma, a colon, parentheses or a new sentence" if house else \
            "an em dash, a colon, commas or parentheses"
        report.add(path, at(match.start()), "warning", "SPACED_HYPHEN",
                   f'"{quote(context.strip())}": a spaced hyphen is not a dash; use {marks}')
    for match in PREDICATIVE_HYPHEN_RE.finditer(text):
        compound = match.group(1)
        if compound.lower() in allow:
            continue
        report.add(path, at(match.start(1)), "warning", "PREDICATIVE_COMPOUND_HYPHEN",
                   f'"{quote(match.group(0))}": a compound after its noun is open '
                   f'("{compound.replace("-", " ", 1)}"); keep the hyphen only before a noun')
    if house:
        # DASH_IN_PROSE subsumes DOUBLE_HYPHEN, SPACED_EN_DASH, SPACED_EM_DASH and
        # EM_DASH_DENSITY; EPONYM_HYPHEN and EQUAL_PAIR_HYPHEN would advise an en dash.
        check_dashes(doc, text, starts, report)
    else:
        check_dash_conventions(doc, text, starts, report, allow)
    for match in LY_HYPHEN_RE.finditer(text):
        word = match.group(1)
        if word.lower() in NOT_LY_ADVERBS or word[0].isupper() and (
                match.start() == 0 or not text[:match.start()].rstrip().endswith((".", "!", "?"))):
            continue   # a proper noun such as Plotly-based (a sentence-initial adverb is checked)
        compound = text[match.start():match.end() + 25].split()[0].rstrip(".,;:)")
        if compound.lower() in allow:
            continue
        report.add(path, at(match.start()), "warning", "LY_ADVERB_HYPHEN",
                   f'"{quote(compound)}": no hyphen after an -ly adverb '
                   f'("{compound.replace("-", " ", 1)}")')
    for match in HYPHEN_MINUS_RE.finditer(text):
        report.add(path, at(match.start()), "info", "HYPHEN_AS_MINUS",
                   f'"{match.group(0)}": use a minus sign ({minus}), '
                   "not a hyphen")


def check_dash_conventions(doc: Document, text: str, starts: list[tuple[int, int]],
                           report: Report, allow: set[str]) -> None:
    """The dash conventions for a project that relaxes the house rule (DASH_IN_PROSE off):
    dashes typed as hyphens, spaced dashes, em-dash density, en dashes in name pairs."""
    path = doc.path
    en_dash = "--" if doc.latex else "\u2013"

    def at(position: int) -> int:
        return line_at(starts, position)

    if doc.path.suffix.lower() in PLAIN_SUFFIXES:
        for match in DOUBLE_HYPHEN_RE.finditer(text):
            before = text[match.start() - 1] if match.start() else " "
            after = text[match.end():match.end() + 1]
            if len(match.group(0)) == 2 and before.isspace() and after.isalpha():
                continue   # a command-line option such as --json
            context = text[max(0, match.start() - 15):match.end() + 15]
            report.add(path, at(match.start()), "warning", "DOUBLE_HYPHEN",
                       f'"{quote(context.strip())}": type the dash itself (\u2013 for ranges, '
                       "\u2014 for a break) unless the toolchain converts it")
    en_spaced = SPACED_EN_DASH_TEX_RE if doc.latex else SPACED_EN_DASH_RE
    match = en_spaced.search(text)
    if match:
        context = text[max(0, match.start() - 15):match.end() + 15]
        report.add(path, at(match.start()), "info", "SPACED_EN_DASH",
                   f'"{quote(context.strip())}": in American style an en dash joins ranges and '
                   "pairs; for a break use a closed em dash, commas or parentheses, unless the "
                   "venue sets spaced en dashes")
    spaced = list(SPACED_EM_DASH_RE.finditer(text))
    if doc.latex:
        spaced += list(SPACED_EM_DASH_TEX_RE.finditer(text))
    if spaced:
        match = min(spaced, key=lambda m: m.start())
        context = text[max(0, match.start() - 15):match.end() + 15]
        more = f" ({len(spaced)} in this paragraph)" if len(spaced) > 1 else ""
        report.add(path, at(match.start()), "info", "SPACED_EM_DASH",
                   f'"{quote(context.strip())}": set em dashes closed{more}')
    seen: set[str] = set()
    for match in EPONYM_RE.finditer(text):
        name = match.group(0)
        if "-" not in name.replace("--", ""):
            continue   # already en dashes
        if name in seen:
            continue
        seen.add(name)
        fixed = name.replace("--", "-").replace("-", en_dash)
        report.add(path, at(match.start()), "warning", "EPONYM_HYPHEN",
                   f'"{name}": names of two people take an en dash: {fixed}')
    for match in EQUAL_PAIR_RE.finditer(text):
        name = match.group(0)
        if name in seen or name in allow:
            continue
        seen.add(name)
        fixed = name.replace("-", en_dash)
        report.add(path, at(match.start()), "info", "EQUAL_PAIR_HYPHEN",
                   f'"{name}": a relation between equal terms takes an en dash ({fixed}) in '
                   "Chicago style; many venues accept the hyphen, so follow the house style")
    dashes = list(EM_DASH_RE.finditer(text))
    if len(dashes) > 2:
        report.add(path, at(dashes[2].start()), "info", "EM_DASH_DENSITY",
                   f"{len(dashes)} em dashes in one paragraph; keep at most one pair and use "
                   "commas, a colon, parentheses or a new sentence for the rest")


def _negated(sentence: str, position: int) -> bool:
    return bool(NEGATION_BEFORE_RE.search(sentence[max(0, position - 40):position]))


def _proof_claim(doc: Document, sentence: str, math_context: bool,
                 paragraph_math: bool) -> re.Match[str] | None:
    """A proof verb used for an empirical claim: "our experiments prove", or "prove" in text
    that is not a derivation. Negated uses ("does not prove"), exercise imperatives ("Prove
    that ...") and adjectival "proven" are left alone."""
    empirical = EMPIRICAL_SUBJECT_RE.search(sentence)
    for match in PROOF_VERB_RE.finditer(sentence):
        word = match.group(0).lower()
        before = sentence[max(0, match.start() - 40):match.start()]
        if _negated(sentence, match.start()):
            continue
        if word == "prove" and match.start() <= 3:
            continue
        if empirical and empirical.start() <= match.start() < empirical.end():
            return match
        if math_context or paragraph_math or doc.math_heavy:
            continue
        if REF in sentence or SECTION_POINTER_RE.search(sentence):
            continue   # "In Section 4 we prove ...": a pointer to a derivation
        if word in {"proved", "proven"} and not (
                AUXILIARY_BEFORE_RE.search(before)
                or sentence[match.end():match.end() + 20].lstrip().lower().startswith("that")):
            continue
        return match
    return None


def coordinating_ands(sentence: str) -> int:
    """Count "and" outside parentheses, serial lists ("A, B, and C"), "between/both ... and"
    and fixed pairs such as "trial and error"."""
    skip = sorted([m.span() for m in PAREN_SPAN_RE.finditer(sentence)]
                  + [m.span() for m in AND_FIXED_RE.finditer(sentence)])
    skip_starts = [start for start, _ in skip]
    count = 0
    for match in AND_RE.finditer(sentence):
        position = match.start()
        index = bisect.bisect_right(skip_starts, position) - 1
        if index >= 0 and position < skip[index][1]:
            continue   # inside parentheses or a fixed pair
        before = sentence[max(0, position - 80):position]
        stripped = before.rstrip()
        if stripped.endswith(",") and ("," in stripped[:-1] or ";" in stripped[:-1]):
            continue   # the last item of a serial list
        lowered = before.lower()
        if ("betw" in lowered or "both" in lowered) and AND_EXEMPT_BEFORE_RE.search(before):
            continue   # between ... and, both ... and
        if AND_PAIR_END_RE.match(sentence, match.end()):
            continue   # a pair of words closing a phrase: "clean and fluent:"
        count += 1
    return count


class Context:
    """What a sentence check needs to know about the sentence's surroundings."""

    def __init__(self, previous: str, following: str, theorem: bool, paragraph_math: bool):
        self.previous = previous
        self.following = following
        self.theorem = theorem
        self.paragraph_math = paragraph_math


def _overlaps(match: re.Match[str], spans: list[tuple[int, int]]) -> bool:
    return any(match.start() < end and start < match.end() for start, end in spans)


def check_sentence(doc: Document, line: int, sentence: str, context: Context,
                   args: argparse.Namespace, report: Report) -> None:
    path = doc.path
    has_cite = CITE in sentence
    math_context = bool(
        context.theorem or MATH in sentence or MATH_CONTEXT_RE.search(sentence)
        or MATH_CONTEXT_RE.search(context.previous)
    )

    technical = math_context or context.paragraph_math or doc.math_heavy
    claimed: list[tuple[int, int]] = []
    match = next((m for m in OVERSTATEMENT_RE.finditer(sentence)
                  if not _negated(sentence, m.start())
                  and not (m.group(0).lower() in {"guarantee", "guarantees", "universally"}
                           and (technical or TECHNICAL_GUARANTEE_RE.match(sentence, m.end())))),
                 None)
    if match is None and not context.theorem:
        match = _proof_claim(doc, sentence, math_context, context.paragraph_math)
    if match:
        claimed.append(match.span())
        report.add(path, line, "warning", "POSSIBLE_OVERSTATEMENT",
                   f'"{quote(match.group(0))}": match the verb to the design and the evidence')
    match = SOTA_RE.search(sentence)
    if match and not has_cite and REF not in sentence and not DIGIT_RE.search(sentence):
        report.add(path, line, "warning", "SOTA_WITHOUT_EVIDENCE",
                   f'"{quote(match.group(0))}": name the benchmark, the comparison set, the '
                   "date and the numbers, with sources")
    sentence_math = bool(context.theorem or MATH in sentence or MATH_CONTEXT_RE.search(sentence))
    match = ABSENCE_RE.search(sentence)
    if match is None:
        match = EQUIVALENT_RE.search(sentence)
        if match and not STATISTICAL_CUE_RE.search(sentence):
            match = None
    if match and not sentence_math:
        report.add(path, line, "warning", "ABSENCE_CLAIM",
                   f'"{quote(match.group(0))}": a nonsignificant result is not evidence of '
                   "absence; give the estimate and interval, or an equivalence test")
    match = NOVELTY_RE.search(sentence)
    if match and "first" in match.group(0).lower() and re.search(
            r"\b(?:second|latter)\b", sentence[match.end():], re.IGNORECASE):
        match = None   # "presents the first method, and Section 4 the second": enumeration
    if match:
        claimed.append(match.span())
        report.add(path, line, "warning", "PRIORITY_OR_GAP_CLAIM",
                   f'"{quote(match.group(0))}": support with a documented search or narrow the claim')
    match = ATTRIBUTION_RE.search(sentence)
    if match and not has_cite:
        report.add(path, line, "warning", "ATTRIBUTION_WITHOUT_CITATION",
                   f'"{quote(match.group(0))}": name and cite the sources')
    match = SIGNIFICANT_RE.search(sentence)
    if (match and not STATISTIC_HINT_RE.search(sentence) and MATH not in sentence
            and not STATISTIC_HINT_RE.search(context.following) and MATH not in context.following):
        report.add(path, line, "warning", "SIGNIFICANT_WITHOUT_STATISTIC",
                   f'"{match.group(0)}": report the estimate, interval and test, or use another '
                   "word if the meaning is not statistical")
    if args.observational:
        match = CAUSAL_RE.search(sentence)
        if match:
            report.add(path, line, "warning", "CAUSAL_LANGUAGE",
                       f'"{quote(match.group(0))}": causal wording in an observational design')
    clearly = CLEARLY_START_RE.match(sentence)
    for match in ([clearly] if clearly else []) + list(CERTAINTY_RE.finditer(sentence)):
        if _overlaps(match, claimed):
            continue
        if re.search(r"\b(?:always|never|all|every)\b", match.group(0), re.IGNORECASE):
            if math_context or context.paragraph_math or doc.math_heavy:
                continue   # a mathematical statement: "the residual is always orthogonal"
        report.add(path, line, "info", "CERTAINTY_WORD",
                   f'"{quote(match.group(0).strip())}": state the tested cases, the guarantee '
                   "and its assumptions, or delete")
        break
    match = HYPE_RE.search(sentence)
    if match:
        report.add(path, line, "info", "HYPE_WORD",
                   f'"{match.group(0)}": say what is new and against what, with evidence')
    match = next((m for m in UNDERSELLING_RE.finditer(sentence)
                  if not _negated(sentence, m.start())), None)
    if match:
        report.add(path, line, "info", "UNDERSELLING",
                   f'"{quote(match.group(0))}": state what was done or found at the strength '
                   "the evidence supports")

    # House rule R3: no comma right after a conjunction or a sentence-initial connective.
    commas = [m for m in (OPENING_CONNECTIVE_COMMA_RE.match(sentence),) if m]
    commas += list(CLAUSE_CONNECTIVE_COMMA_RE.finditer(sentence))
    commas += list(CONJUNCTION_COMMA_RE.finditer(sentence))
    for match in sorted(commas, key=lambda m: m.start(1)):
        word = " ".join(match.group(1).split())
        report.add(path, line, "warning", "COMMA_AFTER_CONJUNCTION",
                   f'"{word},": no comma right after a conjunction or connective; write '
                   f'"{word} ..." (a comma that closes a parenthetical or an introductory '
                   "clause stays)")

    # Style
    for match in LEXICON_RE.finditer(sentence):
        phrase = match.group(0)
        for pattern, advice in GENERIC_COMPILED:
            if pattern.fullmatch(phrase):
                report.add(path, line, "info", "GENERIC_PHRASE", f'"{quote(phrase)}": {advice}')
                break
        else:
            report.add(path, line, "info", "WORDY_PHRASE",
                       f'"{phrase}" -> {WORDY[" ".join(phrase.lower().split())]}')
    match = EMPTY_OPENER_RE.search(sentence)
    if match:
        report.add(path, line, "info", "EMPTY_OPENER",
                   f'"{quote(match.group(0))}": state the point, or name the agent or the exhibit')
    adjacent = ADJACENT_HEDGES_RE.search(sentence)
    hedges = HEDGE_RE.findall(sentence)
    clause_hedges: list[str] = []
    if not adjacent and len(hedges) >= 2:
        for clause in CLAUSE_SPLIT_RE.split(sentence):
            found = HEDGE_RE.findall(clause or "")
            if len(found) >= 2:
                clause_hedges = found
                break
    if adjacent or clause_hedges or len(hedges) >= 3:
        shown = adjacent.group(0) if adjacent else ", ".join((clause_hedges or hedges)[:4])
        report.add(path, line, "info", "STACKED_HEDGES",
                   f'"{quote(shown)}": one hedge per claim, placed on the uncertain part')
    words = count_words(sentence)
    if words > args.max_sentence_words or words > args.very_long_sentence_words:
        severity = "warning" if words > args.very_long_sentence_words else "info"
        report.add(path, line, severity, "LONG_SENTENCE",
                   f"{words} words; check that it carries one idea")
    for match in REPEATED_WORD_RE.finditer(sentence):
        if match.group(1).lower() not in REPEATED_WORD_OK:
            report.add(path, line, "warning", "REPEATED_WORD", f'"{match.group(0)}"')
    ands = coordinating_ands(sentence)
    if ands >= 3:
        report.add(path, line, "warning" if ands >= 4 else "info", "AND_CHAIN",
                   f'{ands} coordinating "and" in one sentence; split it, subordinate a clause '
                   "or make a list")
    match = AND_ALSO_RE.search(sentence)
    if match:
        report.add(path, line, "info", "AND_ALSO", f'"{match.group(0)}": use one of the two words')
    match = AND_OR_RE.search(sentence)
    if match:
        report.add(path, line, "info", "AND_OR",
                   '"and/or": write "A or B or both", or "or" when inclusion is obvious')
    for match in AMPERSAND_RE.finditer(sentence):
        before = sentence[match.start() - 1:match.start()]
        after = sentence[match.end():match.end() + 1]
        if before.isupper() and after.isupper():
            continue   # R&D, AT&T, Q&A
        report.add(path, line, "info", "AMPERSAND_IN_PROSE", '"&" in running prose: write "and"')
        break
    if AND_START_RE.match(sentence):
        report.add(path, line, "info", "SENTENCE_STARTS_WITH_AND",
                   'the sentence begins with "And"; use rarely, never as a habit')


PREPOSITION_OPENERS = {
    "in", "on", "for", "with", "at", "by", "from", "to", "of", "under", "after", "before",
    "during", "as", "if", "when", "while", "since", "across", "between", "within", "without",
}


def _opener(sentence: str) -> tuple[str, str] | None:
    tokens = OPENER_TOKEN_RE.findall(sentence[:200])
    if tokens and tokens[0].lower() in {"the", "a", "an"}:
        tokens = tokens[1:]
    if not tokens or tokens[0].startswith("\u2039"):
        return None
    if tokens[0].lower() in PREPOSITION_OPENERS:
        return None   # parallel "In a thesis, ... In a book, ..." is deliberate
    return tokens[0].lower(), tokens[0]


@functools.lru_cache(maxsize=65536)
def _normalize_word(token: str) -> str:
    word = token.lower().replace("\u2019", "'")
    if word.endswith("'s"):
        word = word[:-2]
    word = word.rstrip("'")
    if len(word) > 5 and word.endswith(("shes", "ches", "xes", "sses")):
        word = word[:-2]
    elif len(word) > 4 and word.endswith("s") and not word.endswith(("ss", "us", "is")):
        word = word[:-1]
    return word


# Ordinary vague words stay subject to REPEATED_CONTENT_WORD however often they occur.
ALWAYS_CHECK = {
    "important", "approach", "significant", "significantly", "various", "different",
    "interesting", "crucial", "essential", "novel", "robust", "effective", "efficient",
    "overall", "particular", "specific", "numerous", "notably", "simply", "really",
    "actually", "basically", "clearly", "highly", "great", "large", "small", "good",
}


def document_terms(docs: list[Document]) -> set[str]:
    """Words that recur throughout the files: at least 8 times and 2 per 1,000 words. In a
    textbook or paper these are the fixed technical terms, which should repeat."""
    counts: dict[str, int] = {}
    total = 0
    for doc in docs:
        for paragraph in doc.paragraphs:
            for _, text in paragraph:
                for token in WORD_TOKEN_RE.findall(text):
                    if token.startswith("\u2039"):
                        continue
                    total += 1
                    word = _normalize_word(token)
                    if len(word) >= 5:
                        counts[word] = counts.get(word, 0) + 1
    threshold = max(8, 2 * total / 1000)
    return {word for word, n in counts.items() if n >= threshold and word not in ALWAYS_CHECK}


def heading_terms(docs: list[Document]) -> set[str]:
    """Content words of the titles and headings: the topic's fixed terms, which may repeat."""
    terms: set[str] = set()
    for doc in docs:
        for _, heading in doc.headings:
            for token in WORD_TOKEN_RE.findall(heading):
                if not token.startswith("\u2039"):
                    terms.add(_normalize_word(token))
    return terms


def check_paragraph_style(doc: Document, text: str, starts: list[tuple[int, int]],
                          sentences: list[tuple[int, str]], report: Report,
                          allow: set[str], terms: set[str]) -> None:
    path = doc.path

    # Runs of sentences with the same opening word.
    run: list[tuple[int, str]] = []
    run_key: str | None = None
    for line, sentence in sentences + [(0, "")]:
        found = _opener(sentence) if sentence else None
        if found and found[0] == run_key:
            run.append((line, found[1]))
            continue
        if len(run) >= 3:
            report.add(path, run[0][0], "info", "REPEATED_OPENING",
                       f'{len(run)} consecutive sentences start with "{run[0][1]}"; vary the '
                       "openings or merge sentences")
        run = [(line, found[1])] if found else []
        run_key = found[0] if found else None

    # Additive transitions opening two of any three consecutive sentences.
    hits = [(index, line, m.group(1)) for index, (line, sentence) in enumerate(sentences)
            if (m := TRANSITION_OPENER_RE.match(sentence))]
    cluster: list[tuple[int, int, str]] = []
    for hit in hits + [(10**9, 0, "")]:
        if cluster and hit[0] - cluster[-1][0] <= 2:
            cluster.append(hit)
            continue
        if len(cluster) >= 2:
            names = ", ".join(dict.fromkeys(" ".join(h[2].split()) for h in cluster))
            report.add(path, cluster[0][1], "info", "STACKED_TRANSITIONS",
                       f"{len(cluster)} nearby sentences open with additive transitions "
                       f"({names}); state the relation (because, however, therefore) or merge")
        cluster = [hit]

    # A content word three times within REPETITION_WINDOW words.
    positions: dict[str, deque[int]] = {}
    reported: set[str] = set()
    index = 0
    for match in WORD_TOKEN_RE.finditer(text):
        token = match.group(0)
        if token.startswith("\u2039"):
            continue
        index += 1
        if len(token) < 5 or not token[1:].islower():
            continue   # short words, acronyms and names such as XGBoost
        word = _normalize_word(token)
        if (len(word) < 5 or word in STOPWORDS or word in allow or word in terms
                or word in reported):
            continue
        queue = positions.setdefault(word, deque())
        while queue and queue[0] <= index - REPETITION_WINDOW:
            queue.popleft()
        queue.append(index)
        if len(queue) >= 3:
            reported.add(word)
            report.add(path, line_at(starts, match.start()), "info", "REPEATED_CONTENT_WORD",
                       f'"{token.lower()}" {len(queue)} times within {REPETITION_WINDOW} words; '
                       "vary the ordinary word or merge sentences (fixed terms: --allow-terms)")

    # A phrase of three or more words repeated in the paragraph.
    words: list[str | None] = []
    offsets: list[int] = []
    for match in PHRASE_TOKEN_RE.finditer(text):
        token = match.group(0)
        words.append(token.lower() if token[0].isalpha() else None)
        offsets.append(match.start())
    # A word that can start or end a phrase: not a stopword, at least three letters.
    edge = [w is not None and len(w) >= 3 and w not in STOPWORDS for w in words]
    trigrams: dict[tuple[str, str, str], list[int]] = {}
    for i in range(len(words) - 2):
        if edge[i] and edge[i + 2] and words[i + 1] is not None:
            trigrams.setdefault((words[i], words[i + 1], words[i + 2]), []).append(i)  # type: ignore[arg-type]
    covered: set[int] = set()
    allowed_phrases = [term for term in allow if " " in term]
    for key, indices in sorted(trigrams.items(), key=lambda item: item[1][0]):
        occurrences: list[int] = []
        for i in indices:
            if not occurrences or i >= occurrences[-1] + 3:
                if occurrences and i - occurrences[-1] > PHRASE_WINDOW:
                    if len(occurrences) >= 2:
                        break   # report the first close repeat only
                    occurrences = []
                occurrences.append(i)
        if len(occurrences) < 2:
            continue
        if occurrences[0] in covered and occurrences[0] + 1 in covered:
            covered.update(j for i in occurrences for j in range(i, i + 3))
            continue   # the tail of a longer repeated phrase, already reported
        covered.update(j for i in occurrences for j in range(i, i + 3))
        phrase = " ".join(key)
        if any(word in allow for word in key) or any(phrase in term for term in allowed_phrases):
            continue
        if _normalize_word(key[0]) in terms and _normalize_word(key[2]) in terms:
            continue   # a phrase made of the document's own terms
        report.add(path, line_at(starts, offsets[occurrences[1]]), "info", "REPEATED_PHRASE",
                   f'"{phrase}" {len(occurrences)} times in one paragraph; refer back or '
                   "rephrase (fixed terms: --allow-terms)")


def check_acronyms(docs: list[Document], report: Report, allow: set[str] | None = None) -> None:
    """House rule R5: every acronym is expanded at its first use in the body, before it is
    used alone, and the abstract uses none (an expansion there does not count for the body).
    Names given with --allow-terms (proper names of works, systems and formats, which take a
    descriptive noun instead) are not reported."""
    allow = allow or set()
    first_use: dict[str, tuple[tuple[int, int], Document, int]] = {}
    first_definition: dict[str, tuple[int, int]] = {}
    counts: dict[str, int] = {}
    in_abstract: dict[str, tuple[Document, int]] = {}
    named: dict[str, str] = {}   # acronym -> descriptive noun phrase at its first use
    order = 0
    glossary = False
    for doc in docs:
        if any("\\newacronym" in line or "\\gls{" in line or "\\acro{" in line
               for _, line in doc.raw):
            glossary = True
        entries = [(n, t, doc.paragraph_abstract[i])
                   for i, para in enumerate(doc.paragraphs) for n, t in para]
        entries += [(n, t, False) for n, t in doc.headings]
        for number, text, abstract in sorted(entries, key=lambda e: (e[0], e[1])):
            order += 1   # position key: (order, offset), so a use and a definition on one line compare
            letters = [c for c in text if c.isalpha()]
            if letters and sum(c.isupper() for c in letters) > 0.6 * len(letters):
                continue
            for match in ACRONYM_RE.finditer(text):
                name = match.group(1)
                if name in ACRONYM_OK or name.lower() in allow or re.match(
                        r"-[A-Z0-9]", text[match.end():match.end() + 2]) or re.search(
                        r"[A-Za-z0-9]-$", text[max(0, match.start() - 2):match.start()]):
                    continue   # a name such as GPT-4, T5-11B, SMART-LLM or APIGen-MT
                if abstract:
                    in_abstract.setdefault(name, (doc, number))
                    continue
                counts[name] = counts.get(name, 0) + 1
                if name not in first_use:
                    first_use[name] = ((order, match.start()), doc, number)
                    noun = DESCRIPTIVE_NOUN_RE.match(text[match.end():match.end() + 60])
                    if noun:
                        named[name] = " ".join(f"{name} {MARKER_RE.sub('', noun.group(0))}".split())
                before = text[max(0, match.start() - 20):match.start()].rstrip()
                after = text[match.end():match.end() + 40].lstrip()
                # "the BERT encoder (Bidirectional Encoder ...)": a descriptive noun of up to
                # three words, then a parenthetical expansion that starts with the acronym's
                # first letter.
                noun_expansion = re.match(r"(?:[a-z][\w-]*\s+){0,3}\(([A-Z][^()]{3,160})\)",
                                          text[match.end():match.end() + 220].lstrip())
                defined = (
                    (before.endswith("(") and after[:1] in {")", ";", ","})
                    or bool(re.match(r"\((?=[a-z])", after))
                    or bool(re.match(r"(?:stands|is short) for\b", after))
                    or bool(noun_expansion and noun_expansion.group(1)[0] == name[0])
                )
                if defined:
                    first_definition.setdefault(name, (order, match.start()))
    if glossary:
        return
    for name, (doc, number) in in_abstract.items():
        report.add(doc.path, number, "warning", "ACRONYM_NOT_DEFINED",
                   f"{name} is in the abstract, which uses no abbreviations: write the words, "
                   "or a descriptive noun with a proper name (house rule)")
    for name, (used_at, doc, number) in sorted(first_use.items(), key=lambda item: item[1][0]):
        times = counts[name]
        if name not in first_definition and name in named:
            report.add(doc.path, number, "warning", "ACRONYM_NOT_DEFINED",
                       f"{name} (used {times} time{'s' if times != 1 else ''}) is not expanded "
                       f"but is introduced with a descriptive noun (\"{named[name]}\"): "
                       "enough for the proper name of a work, system or format (then list it "
                       "with --allow-terms); expand any other abbreviation")
        elif name not in first_definition:
            report.add(doc.path, number, "warning", "ACRONYM_NOT_DEFINED",
                       f"{name} (used {times} time{'s' if times != 1 else ''}) is never "
                       "expanded in the body of the files checked: write the words with the "
                       f"abbreviation in parentheses at first use (\"... ({name})\"), or, for "
                       "the name of a work, system or format, a descriptive noun and "
                       "--allow-terms")
        elif first_definition[name] > used_at:
            report.add(doc.path, number, "warning", "ACRONYM_USED_BEFORE_DEFINITION",
                       f"{name} appears before the place where it is expanded; move the "
                       "expansion to the first use in the body")


def check_title(docs: list[Document], report: Report, allow: set[str]) -> None:
    """Title style (references/structure.md, "Titles"): no abbreviation in the document title,
    and a short title. Checked on every explicit title (\\title, YAML "title:") in the run, or,
    when there is none, on the first "# " heading of the first Markdown or text file. A system
    name that forms the whole part before the first colon is allowed when a subtitle of at least
    three words follows: the subtitle is taken to say what the name is (whether it does is
    checked by reading). Names given with --allow-terms are not reported."""
    titles = [(doc, doc.title) for doc in docs if doc.title and doc.title[2]]
    if not titles:
        titles = [(doc, doc.title) for doc in docs if doc.title and not doc.latex][:1]
    for doc, (line, title, _) in titles:
        words = [w for w in title.split() if re.search(r"[A-Za-z0-9]", w)]
        letters = [c for c in title if c.isalpha()]
        shouting = bool(letters) and sum(c.isupper() for c in letters) > 0.6 * len(letters)
        name = ""
        head, colon, subtitle = title.partition(":")
        if colon and len(head.split()) == 1 and len(subtitle.split()) >= 3:
            name = head.strip()
        found: list[str] = []
        if not shouting:
            hits = [(m.start(), m.group(1) + m.group(2), m.group(1))
                    for m in TITLE_CAPS_RE.finditer(title)]
            hits += [(m.start(), m.group(1), m.group(1)) for m in TITLE_MIXED_RE.finditer(title)]
            for _, token, stem in sorted(hits):
                if token == name or ROMAN_RE.fullmatch(stem):
                    continue   # the system name before the colon, or a roman numeral
                if token.lower() in allow or stem.lower() in allow:
                    continue
                if token not in found:
                    found.append(token)
        if found:
            report.add(doc.path, line, "warning", "TITLE_ABBREVIATION",
                       f"title uses {', '.join(found)}: write the words in a title "
                       "(\"Graph Neural Network,\" not \"GNN\"); a system name is allowed "
                       "as \"Name: what it does for whom\" (references/structure.md, Titles)")
        if len(words) > TITLE_NOTE_WORDS:
            severity = "warning" if len(words) > TITLE_WARNING_WORDS else "info"
            report.add(doc.path, line, severity, "TITLE_TOO_LONG",
                       f"title has {len(words)} words (\"{quote(title)}\"): a title is a short "
                       "name, not a descriptive sentence; propose shorter candidates to the "
                       "author, who approves the title")


def check_floats(docs: list[Document], report: Report) -> None:
    labels: dict[str, tuple[Document, int, bool]] = {}
    referenced: set[str] = set()
    for doc in docs:
        for name, number, in_float in doc.labels:
            labels.setdefault(name, (doc, number, in_float))
        referenced.update(name for name, _ in doc.refs)
    for name, (doc, number, in_float) in labels.items():
        if in_float and name not in referenced:
            report.add(doc.path, number, "warning", "FLOAT_NEVER_REFERENCED",
                       f'label "{name}" is not referenced in the files checked')
    for doc in docs:
        seen: set[str] = set()
        for name, number in doc.refs:
            if name not in labels and name not in seen:
                seen.add(name)
                report.add(doc.path, number, "warning", "REFERENCE_TO_UNKNOWN_LABEL",
                           f'"{name}" is not defined in the files checked')
        if doc.latex:
            continue
        captions: dict[tuple[str, str], int] = {}
        mentions: dict[tuple[str, str], int] = {}
        for number, line in doc.raw:
            caption = MD_CAPTION_RE.match(line)
            rest = line
            if caption:
                key = ("table" if caption.group(1).lower() == "table" else "figure", caption.group(2))
                captions.setdefault(key, number)
                rest = line[caption.end():]
            for kind, digits in MD_MENTION_RE.findall(rest):
                key = ("table" if kind.lower() == "table" else "figure", digits)
                mentions.setdefault(key, number)
        for key, number in captions.items():
            if key not in mentions:
                report.add(doc.path, number, "warning", "FLOAT_NEVER_REFERENCED",
                           f"{key[0].capitalize()} {key[1]} is not mentioned in the text")
        if captions:
            for key, number in mentions.items():
                if key not in captions:
                    report.add(doc.path, number, "info", "FLOAT_MENTION_WITHOUT_CAPTION",
                               f"{key[0].capitalize()} {key[1]} is mentioned but no caption "
                               "line starts with that label")


def run_checks(docs: list[Document], args: argparse.Namespace) -> tuple[Report, dict[str, object]]:
    disabled = set(args.disabled)
    if args.no_style:
        disabled |= STYLE_RULES
    report = Report(disabled)
    allow = set(args.allowed_terms)
    identifier_allow = allow | cited_names(docs) if "INTERNAL_IDENTIFIER" not in disabled else allow
    topic = heading_terms(docs)
    lengths: list[int] = []
    empty: list = []
    for doc in docs:
        terms = topic | document_terms([doc])
        check_raw_lines(doc, report)
        check_split_placeholders(doc, report)
        if "INTERNAL_IDENTIFIER" not in disabled:
            check_internal_identifiers(doc, report, identifier_allow)
        for number, heading in doc.headings:
            check_mechanics(doc, heading, [(0, number)], report, allow)
        if "DASH_IN_PROSE" not in disabled:
            for number, cells in doc.table_lines:
                check_dashes(doc, cells, [(0, number)], report, " in a table cell")
        for index, paragraph in enumerate(doc.paragraphs):
            joined, starts = join_paragraph(paragraph)
            joined = mask_quotes(joined)
            sentences = sentences_of(paragraph, joined, starts)
            check_mechanics(doc, joined, starts, report, allow)
            if not doc.paragraph_item[index] and PARAGRAPH_TO_RE.match(joined):
                report.add(doc.path, paragraph[0][0], "warning", "PARAGRAPH_STARTS_WITH_TO",
                           f'"{quote(joined.strip()[:60])}": begin with the subject and its '
                           'verb ("We compare X by ..."), not with "To"')
            theorem = doc.paragraph_theorem[index]
            paragraph_math = MATH in joined
            for position, (line, sentence) in enumerate(sentences):
                lengths.append(count_words(sentence))
                context = Context(
                    sentences[position - 1][1] if position else "",
                    sentences[position + 1][1] if position + 1 < len(sentences) else "",
                    theorem, paragraph_math)
                check_sentence(doc, line, sentence, context, args, report)
            if not STYLE_RULES <= disabled:
                check_paragraph_style(doc, joined, starts, sentences, report, allow, terms)
        if not doc.paragraphs and not doc.headings:
            if doc.includes:
                report.add(doc.path, doc.includes, "info", "INCLUDES_ONLY",
                           "no prose of its own; it only includes other files, so pass those "
                           "files as well, in reading order")
            else:
                empty.append(doc)
    # A file without prose is an error when nothing in the run has prose, and a note when it
    # accompanies files that do (a table-only or macro-only companion file).
    any_prose = any(doc.paragraphs or doc.headings for doc in docs)
    for doc in empty:
        if any_prose:
            report.add(doc.path, 1, "info", "EMPTY_MANUSCRIPT",
                       "no prose found in this file (the other files of the run have prose)")
        else:
            report.add(doc.path, 1, "error", "EMPTY_MANUSCRIPT", "no prose found")
    check_acronyms(docs, report, allow)
    check_title(docs, report, allow)
    check_floats(docs, report)
    lengths.sort()
    stats: dict[str, object] = {
        "files_checked": len(docs),
        "sentences": len(lengths),
        "median_sentence_words": lengths[len(lengths) // 2] if lengths else 0,
    }
    return report, stats


# ---------------------------------------------------------------------------
# Command line
# ---------------------------------------------------------------------------


def rule_table() -> str:
    width = max(len(rule[0]) for rule in RULES)
    lines = []
    for code, severity, group, description in RULES:
        shown = severity.replace("info", "note")
        lines.append(f"  {code:<{width}}  {shown:<12}  {group:<12}  {description}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read-only lint for academic manuscripts (.md, .markdown, .tex, .texview, "
        ".txt). Findings are prompts for human judgment; a clean report proves nothing.",
        epilog="severities: error = clearly broken; warning = mechanical error or claim needing "
        "evidence; note (printed as info in findings) = stylistic pattern.\n"
        "exit status: 0 no error-level finding, 1 at least one, 2 input rejected or invalid "
        "option.\n\nrules (id, severity, group, description):\n" + rule_table(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("files", nargs="*", help="manuscript files, in reading order")
    parser.add_argument("--observational", action="store_true",
                        help="also flag causal wording (use for observational designs)")
    parser.add_argument("--max-sentence-words", type=int, default=40,
                        help="report sentences longer than this as a note (default: 40)")
    parser.add_argument("--very-long-sentence-words", type=int, default=60,
                        help="report sentences longer than this as a warning (default: 60)")
    parser.add_argument("--allow-terms", action="append", default=[], metavar="TERMS",
                        help="comma-separated fixed technical terms that may repeat or keep "
                        "their hyphen (REPEATED_CONTENT_WORD, REPEATED_PHRASE, "
                        "EQUAL_PAIR_HYPHEN, LY_ADVERB_HYPHEN, PREDICATIVE_COMPOUND_HYPHEN), and "
                        "names of works, systems, formats or public tools that need no "
                        "expansion or may be set as code (ACRONYM_NOT_DEFINED, "
                        "TITLE_ABBREVIATION, INTERNAL_IDENTIFIER); repeatable")
    parser.add_argument("--disable", action="append", default=[], metavar="RULE[,RULE...]",
                        help="switch off these rule ids; repeatable (see --list-rules)")
    parser.add_argument("--no-style", action="store_true",
                        help="switch off the style group (wording, coordination, repetition, "
                        "sentence length, em-dash density, paragraph openings, acronyms, title)")
    parser.add_argument("--min-severity", choices=SEVERITIES + ("note",), default="info",
                        help="lowest severity to print (default: info, the same as note)")
    parser.add_argument("--json", action="store_true", help="print a JSON report")
    parser.add_argument("--skip-missing", action="store_true",
                        help="skip files that do not exist yet, with a notice on standard error, "
                        "instead of rejecting the run (exit 1 if every file is missing)")
    parser.add_argument("--list-rules", action="store_true",
                        help="print every rule id with its severity and description, then exit")
    return parser


def _split_list(values: list[str]) -> list[str]:
    return [item.strip() for value in values for item in value.split(",") if item.strip()]


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_intermixed_args(argv)
    if args.list_rules:
        print(rule_table())
        return 0
    if not args.files:
        parser.error("at least one manuscript file is required")
    if args.max_sentence_words < 1 or args.very_long_sentence_words < 1:
        parser.error("--max-sentence-words and --very-long-sentence-words must be at least 1")
    if args.very_long_sentence_words < args.max_sentence_words:
        parser.error("--very-long-sentence-words must not be smaller than --max-sentence-words")
    args.disabled = [code.upper() for code in _split_list(args.disable)]
    unknown = sorted(set(args.disabled) - RULE_IDS)
    if unknown:
        parser.error(f"unknown rule id(s) in --disable: {', '.join(unknown)} (see --list-rules)")
    args.allowed_terms = [term.lower() for term in _split_list(args.allow_terms)]
    min_severity = SEVERITY_ALIASES.get(args.min_severity, args.min_severity)
    if args.skip_missing:
        absent = [name for name in args.files if not Path(name).is_symlink() and not Path(name).exists()]
        if absent:
            print(f"{TOOL}: skipped missing file(s): {', '.join(absent)}", file=sys.stderr)
            args.files = [name for name in args.files if name not in absent]
        if not args.files:
            print(f"{TOOL}: nothing checked: every file given is missing (check the paths)", file=sys.stderr)
            return 1
    try:
        docs = [Document(*read_manuscript(name)) for name in args.files]
    except (InputError, OSError) as exc:
        print(f"{TOOL}: {exc}", file=sys.stderr)
        return 2
    report, stats = run_checks(docs, args)
    order = {str(doc.path): index for index, doc in enumerate(docs)}
    findings = sorted(
        report.findings,
        key=lambda f: (order[str(f["file"])], f["line"], SEVERITY_RANK[str(f["severity"])], f["code"]),
    )
    totals = {name: sum(f["severity"] == name for f in findings) for name in SEVERITIES}
    shown = [f for f in findings
             if SEVERITY_RANK[str(f["severity"])] <= SEVERITY_RANK[min_severity]]
    if args.json:
        print(json.dumps({"tool": TOOL, "summary": {**stats, **totals}, "findings": shown},
                         indent=2, ensure_ascii=False))
    else:
        for f in shown:
            print(f'{f["file"]}:{f["line"]}: {f["severity"]}: {f["code"]}: {f["detail"]}')
        print(f'{TOOL}: {totals["error"]} error(s), {totals["warning"]} warning(s), '
              f'{totals["info"]} note(s) in {stats["files_checked"]} file(s); '
              f'{stats["sentences"]} sentences, median {stats["median_sentence_words"]} words. '
              "Findings are prompts for review, not verdicts.")
    return 1 if totals["error"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
