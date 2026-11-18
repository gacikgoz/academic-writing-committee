#!/usr/bin/env python3
"""Find recent work in the target journal that is related to the manuscript, for its related-work section.

Journals and the editors who handle a submission expect it to know what the journal itself has
published lately. This script asks Crossref for the journal's articles of the last N months that
best match the manuscript's title and abstract, so that the writer can open the best two or three,
read them, and cite each one for what it actually says.

  venue_recent.py --venue "Journal of Machine Learning Research" --from paper.tex [--months 6] [--rows 10] [--json]
  venue_recent.py --issn 1532-4435 --query "retrieval under distribution shift"
  venue_recent.py --bibtex 10.xxxx/yyyy [10.xxxx/zzzz ...]      # BibTeX from doi.org for chosen works

--venue is resolved to an ISSN through Crossref's journal list (the closest title wins; pass --issn
when the name is ambiguous). --from reads the title and abstract of a LaTeX or Markdown file;
--query gives the search text directly. The results are candidates ranked by Crossref's relevance
score: open each one (its DOI) before citing it, and cite it only for what it says. Conference
proceedings are not covered; search the venue's site for those.

Only the Python standard library is used. Network access to api.crossref.org and doi.org is needed.
"""
import argparse
import datetime as dt
import difflib
import json
import re
import sys
import urllib.parse
import urllib.request

UA = "academic-writing-committee/2.4 (venue_recent.py; +https://github.com/gacikgoz/academic-writing-committee)"
API = "https://api.crossref.org"


def get(url, accept="application/json", timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read().decode("utf-8", errors="replace")
    return json.loads(data) if accept == "application/json" else data


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", re.sub(r"\s+", " ", (s or "").lower())).strip()


def resolve_issn(venue):
    """Return (issn, title, candidates) for the journal whose title best matches `venue`."""
    d = get(f"{API}/journals?query={urllib.parse.quote(venue)}&rows=10")
    items = d.get("message", {}).get("items", [])
    if not items:
        return None, None, []
    target = norm(venue)
    scored = []
    for it in items:
        t = it.get("title") or ""
        ratio = difflib.SequenceMatcher(None, target, norm(t)).ratio()
        if norm(t) == target:
            ratio = 2.0
        scored.append((ratio, t, (it.get("ISSN") or [None])[0]))
    scored.sort(key=lambda x: -x[0])
    best = scored[0]
    return best[2], best[1], [(t, i, round(r, 2)) for r, t, i in scored[:5]]


def strip_markup(s):
    s = re.sub(r"(?<!\\)%.*", "", s)
    s = re.sub(r"\\(cite|ref|label|eqref|url|href)\w*\*?(\[[^\]]*\])?\{[^}]*\}", " ", s)
    s = re.sub(r"\$[^$]*\$", " ", s)
    s = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", s)
    s = re.sub(r"[{}_^~\\#*`>|]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def query_from_file(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    title = re.search(r"\\title\s*(?:\[[^\]]*\])?\s*\{((?:[^{}]|\{[^{}]*\})*)\}", text) or \
        re.search(r"^title:\s*['\"]?(.+?)['\"]?\s*$", text, re.M) or re.search(r"^#\s+(.+)$", text, re.M)
    abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.S) or \
        re.search(r"^abstract:\s*[|>]?\s*\n?(.+?)(?:\n\S+:|\Z)", text, re.S | re.M) or \
        re.search(r"^#+\s*Abstract\s*\n(.+?)(?:\n#|\Z)", text, re.S | re.M | re.I)
    parts = [strip_markup(m.group(1)) for m in (title, abstract) if m]
    q = " ".join(parts)
    return " ".join(q.split()[:120])


def recent(issn, query, months, rows):
    since = (dt.date.today() - dt.timedelta(days=round(months * 30.44))).isoformat()
    params = {
        "query.bibliographic": query,
        "filter": f"from-pub-date:{since},type:journal-article",
        "rows": str(rows),
        "select": "DOI,title,author,published,published-online,published-print,container-title,abstract,URL,score",
    }
    d = get(f"{API}/journals/{urllib.parse.quote(issn)}/works?{urllib.parse.urlencode(params)}")
    out = []
    for it in d.get("message", {}).get("items", []):
        date = None
        for k in ("published-online", "published-print", "published"):
            parts = (it.get(k) or {}).get("date-parts") or [[None]]
            if parts[0] and parts[0][0]:
                date = "-".join(str(x).zfill(2) for x in parts[0])
                break
        authors = [" ".join(x for x in (a.get("given"), a.get("family")) if x) for a in it.get("author", [])]
        abstract = strip_markup(re.sub(r"<[^>]+>", " ", it.get("abstract") or ""))
        out.append({
            "doi": it.get("DOI"),
            "title": (it.get("title") or [""])[0],
            "authors": authors,
            "date": date,
            "journal": (it.get("container-title") or [""])[0],
            "score": round(it.get("score", 0), 1),
            "abstract": abstract[:600],
            "url": f"https://doi.org/{it.get('DOI')}",
        })
    return since, out


def bibtex(dois):
    for doi in dois:
        try:
            print(get(f"https://doi.org/{urllib.parse.quote(doi, safe='/')}", accept="application/x-bibtex").strip())
        except Exception as e:  # noqa: BLE001 - report and go on with the next DOI
            print(f"% {doi}: BibTeX not available ({e}); write the entry from the publisher's page", file=sys.stderr)
        print()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--venue", help="journal name, resolved to an ISSN through Crossref")
    ap.add_argument("--issn", help="the journal's ISSN (skips the name lookup)")
    ap.add_argument("--from", dest="src", help="LaTeX or Markdown file whose title and abstract form the query")
    ap.add_argument("--query", help="search text (instead of --from)")
    ap.add_argument("--months", type=float, default=6, help="how far back to look (default 6)")
    ap.add_argument("--rows", type=int, default=10, help="number of candidates (default 10)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--bibtex", nargs="+", metavar="DOI", help="print BibTeX for these DOIs and exit")
    a = ap.parse_args()
    if a.bibtex:
        bibtex(a.bibtex)
        return
    if not (a.venue or a.issn):
        ap.error("give --venue or --issn")
    query = a.query or (query_from_file(a.src) if a.src else None)
    if not query:
        ap.error("give --from FILE or --query TEXT")
    try:
        issn, title, cands = (a.issn, a.venue, []) if a.issn else resolve_issn(a.venue)
        if not issn:
            sys.exit(f"no journal found for '{a.venue}' at Crossref; pass --issn")
        since, items = recent(issn, query, a.months, a.rows)
    except OSError as e:
        sys.exit(f"Crossref could not be reached ({e}); search the journal's site for its recent issues instead")
    if a.json:
        print(json.dumps({"journal": title, "issn": issn, "since": since, "query": query, "journal_candidates": cands,
                          "works": items}, indent=2, ensure_ascii=False))
        return
    print(f"journal: {title} (ISSN {issn}); published since {since}; {len(items)} candidate(s)")
    if cands and len(cands) > 1 and cands[0][2] < 2.0:
        print("  other journals with similar names: " + "; ".join(f"{t} ({i})" for t, i, _ in cands[1:4]) + " - pass --issn if the match is wrong")
    print(f"query: {query[:160]}{'...' if len(query) > 160 else ''}\n")
    for n, w in enumerate(items, 1):
        au = ", ".join(w["authors"][:3]) + (" et al." if len(w["authors"]) > 3 else "")
        print(f"{n}. [{w['score']}] {w['title']}\n   {au} - {w['date']} - {w['url']}")
        if w["abstract"]:
            print(f"   {w['abstract'][:300]}{'...' if len(w['abstract']) > 300 else ''}")
    if not items:
        print("no article of this journal in that period matches; widen --months or change the query")


if __name__ == "__main__":
    main()
