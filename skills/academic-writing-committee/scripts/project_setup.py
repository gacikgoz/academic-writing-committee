#!/usr/bin/env python3
"""Find out what a writing project already says about itself, so that the agent asks the user only
what the repository cannot answer, and write the committee configuration from the answers.

  project_setup.py detect [ROOT] [--json]
      Scan the project (read-only): main documents, document class and venue hints, publication-type
      guess, chapters, bibliography, guidelines and context files, build command, an existing
      committee configuration and its ledger, git state and installed tools. Prints a summary, a
      proposed configuration and the questions that remain open (--json: everything as JSON).

  project_setup.py init [ROOT] [--type T] [--size S] [--effort E] [--goal TEXT] [--guidelines F,...]
                        [--journal NAME] [--recent-months N] [--no-recent]
                        [--main F] [--bib F] [--name TEXT] [--out writing-committee.json] [--force]
      Write the configuration: the detected values, overridden by the answers given. Refuses to
      overwrite an existing file without --force. Prints the next command to run.

Only the Python standard library is used. Nothing is changed by `detect`.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

SKIP_DIRS = {".git", "node_modules", ".writing-committee", "build", "_build", "dist", "out", ".venv", "venv",
             "__pycache__", ".claude", ".github", "site-packages", ".cache", "target", "plugins", "skills"}
TEXT_EXT = (".tex", ".texview", ".md", ".markdown", ".qmd", ".rmd", ".txt")
NOT_DOCS = {"readme", "license", "licence", "changelog", "contributing", "code_of_conduct", "security",
            "claude", "agents", "todo", "notes", "requirements", "authors", "citation"}
TYPES = ["journal-article", "conference-paper", "survey", "thesis", "book", "book-chapter",
         "lecture-notes", "technical-report", "grant-proposal"]
SIZES = ["low", "medium", "high", "full"]
CHAPTER_TYPES = {"book", "thesis", "lecture-notes", None}  # profiles divided into chapters (None: not yet known)
EFFORTS = ["low", "medium", "high", "xhigh", "max", "default"]

# Venue and class hints: (regex on \documentclass or \usepackage names, publication type, venue label)
CLASS_HINTS = [
    (r"neurips|nips_", "conference-paper", "NeurIPS"), (r"icml", "conference-paper", "ICML"),
    (r"iclr", "conference-paper", "ICLR"), (r"\bacl\b|acl_natbib|naacl|emnlp|coling", "conference-paper", "ACL family"),
    (r"aaai", "conference-paper", "AAAI"), (r"ijcai", "conference-paper", "IJCAI"),
    (r"cvpr|iccv|eccv", "conference-paper", "computer vision conference"), (r"llncs", "conference-paper", "Springer LNCS"),
    (r"acmart", "conference-paper", "ACM"), (r"usenix", "conference-paper", "USENIX"),
    (r"elsarticle", "journal-article", "Elsevier"), (r"revtex", "journal-article", "APS/AIP (REVTeX)"),
    (r"svjour|sn-jnl", "journal-article", "Springer journal"), (r"jmlr", "journal-article", "JMLR"),
    (r"tmlr", "journal-article", "TMLR"), (r"ieeetran", "journal-article", "IEEE"),
    (r"thesis|dissertation|phd|msc", "thesis", None),
    (r"\bbook\b|scrbook|memoir|krantz|svmono", "book", None),
    (r"\breport\b|scrreprt", "technical-report", None),
    (r"\barticle\b|scrartcl|amsart", "journal-article", None),
]
NAME_HINTS = [
    (r"thesis|dissertation", "thesis"), (r"proposal|grant|specific[-_ ]aims|nsf|erc|horizon", "grant-proposal"),
    (r"survey|review|tutorial", "survey"), (r"lecture|course|syllabus|notes", "lecture-notes"),
    (r"chapter", "book-chapter"), (r"white[-_ ]?paper|tech(nical)?[-_ ]report", "technical-report"),
]
GUIDE_NAMES = re.compile(r"(guideline|style[-_ ]?guide|venue|author[-_ ]?instruction|call[-_ ]for|cfp|submission|formatting|house[-_ ]style|rules)", re.I)
CONTEXT_NAMES = re.compile(r"(notation|glossary|roadmap|outline|reviews|reviewer|rebuttal|response[-_ ]to|feedback|unresolved|open[-_ ]issues)", re.I)


def walk(root, max_depth=4):
    root_depth = root.rstrip(os.sep).count(os.sep)
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS and not x.startswith("."))
        if d.count(os.sep) - root_depth >= max_depth:
            dirs[:] = []
        for f in sorted(files):
            yield os.path.relpath(os.path.join(d, f), root)


def read(root, rel, limit=400_000):
    try:
        with open(os.path.join(root, rel), encoding="utf-8", errors="replace") as fh:
            return fh.read(limit)
    except OSError:
        return ""


def strip_tex_comments(s):
    return re.sub(r"(?<!\\)%.*", "", s)


def tex_info(root, rel):
    s = strip_tex_comments(read(root, rel))
    cls = re.search(r"\\documentclass\s*(?:\[([^\]]*)\])?\s*\{([^}]+)\}", s)
    pkgs = re.findall(r"\\usepackage\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}", s)
    title = re.search(r"\\title\s*(?:\[[^\]]*\])?\s*\{((?:[^{}]|\{[^{}]*\})*)\}", s)
    includes = re.findall(r"\\(?:input|include|subfile)\s*\{([^}]+)\}", s)
    bibs = []
    for b in re.findall(r"\\(?:bibliography|addbibresource)\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}", s):
        bibs += [x.strip() for x in b.split(",") if x.strip()]
    pre = s.split("\\begin{document}")[0] if "\\begin{document}" in s else ""
    return {
        "file": rel,
        "class": cls.group(2).strip() if cls else None,
        "class_options": cls.group(1) if cls and cls.group(1) else "",
        "packages": [p.strip() for x in pkgs for p in x.split(",")],
        "title": re.sub(r"\s+", " ", re.sub(r"\\\\|\\[a-zA-Z]+\*?|[{}]", " ", title.group(1))).strip() if title else None,
        "includes": includes,
        "preamble_includes": re.findall(r"\\(?:input|include)\s*\{([^}]+)\}", pre),
        "bibliography": bibs,
        "chapters": len(re.findall(r"\\chapter\*?\s*[\[{]", s)),
        "fontspec": bool(re.search(r"fontspec|unicode-math|polyglossia", " ".join(pkgs))),
        "abstract": "\\begin{abstract}" in s,
        "journal": (lambda m: re.sub(r"\s+", " ", m.group(1)).strip() if m else None)(
            re.search(r"\\(?:journal|journalname|jname)\s*\{([^{}]+)\}", s)),
    }


def resolve_tex(root, base_dir, name, exts=(".tex", ".texview", "")):
    for e in exts:
        cand = os.path.normpath(os.path.join(base_dir, name if name.endswith(e) else name + e)) if e else os.path.normpath(os.path.join(base_dir, name))
        if os.path.isfile(os.path.join(root, cand)):
            return cand
        cand = os.path.normpath(name + e) if e else os.path.normpath(name)
        if os.path.isfile(os.path.join(root, cand)):
            return cand
    return None


def guess_type(info, files, title, n_chapter_files=0):
    """Return (type, confidence, reasons)."""
    reasons, votes = [], {}
    hay = " ".join([info.get("class") or "", info.get("class_options") or "", " ".join(info.get("packages", []))]).lower() if info else ""
    venue = None
    for pat, t, v in CLASS_HINTS:
        if hay and re.search(pat, hay):
            votes[t] = votes.get(t, 0) + (3 if v or t == "thesis" else 1)  # a generic class is a weak hint
            reasons.append(f"class/package matches {pat.split('|')[0].strip(chr(92) + 'b')} -> {t}")
            if v and not venue:
                venue = v
            break
    if info and "ieeetran" in hay and "conference" in hay:
        votes["conference-paper"] = votes.get("conference-paper", 0) + 4
        reasons.append("IEEEtran with the conference option -> conference-paper")
    names = " ".join(files + [title or ""]).lower()
    for pat, t in NAME_HINTS:
        if re.search(pat, names):
            votes[t] = votes.get(t, 0) + 3
            reasons.append(f"file names or title mention '{pat.split('|')[0]}' -> {t}")
    if info and info.get("chapters", 0) >= 2 and not any(t in votes for t in ("thesis", "lecture-notes")):
        votes["book"] = votes.get("book", 0) + 2
        reasons.append(f"{info['chapters']} \\chapter commands -> book")
    if not info and n_chapter_files >= 2 and not any(t in votes for t in ("thesis", "lecture-notes")):
        votes["book"] = votes.get("book", 0) + 2
        reasons.append(f"{n_chapter_files} chapter files -> book")
    if not votes:
        return None, "none", ["no class, venue or name hint found"], venue
    best = max(votes, key=votes.get)
    ordered = sorted(votes.values(), reverse=True)
    conf = "high" if ordered[0] >= 3 and (len(ordered) == 1 or ordered[0] - ordered[1] >= 2) else "medium" if ordered[0] >= 2 else "low"
    return best, conf, reasons, venue


def tools():
    found = {t: bool(shutil.which(t)) for t in ("latexmk", "pdflatex", "xelatex", "lualatex", "pandoc", "git", "make", "quarto")}
    found["python"] = sys.version.split()[0]
    return found


def git_state(root):
    try:
        inside = subprocess.run(["git", "-C", root, "rev-parse", "--is-inside-work-tree"], capture_output=True, text=True, timeout=10)
        if inside.returncode != 0:
            return {"repository": False}
        st = subprocess.run(["git", "-C", root, "status", "--porcelain"], capture_output=True, text=True, timeout=30)
        br = subprocess.run(["git", "-C", root, "branch", "--show-current"], capture_output=True, text=True, timeout=10)
        dirty = [l for l in st.stdout.splitlines() if l.strip()]
        return {"repository": True, "branch": br.stdout.strip(), "uncommitted_files": len(dirty)}
    except (OSError, subprocess.SubprocessError):
        return {"repository": False}


def existing_configs(root):
    out = []
    for rel in walk(root, max_depth=2):
        b = os.path.basename(rel)
        if b.startswith("writing-committee") and b.endswith(".json"):
            out.append(rel)
    for rel in (".writing-committee/writing-committee.json", ".writing-committee/writing-committee-mini.json"):
        if os.path.isfile(os.path.join(root, rel)) and rel not in out:
            out.append(rel)
    return out


def ledger_summary(root, config_rel):
    state = ".writing-committee"
    try:
        cfg = json.loads(re.sub(r"^\s*//.*$", "", read(root, config_rel), flags=re.M))
        state = cfg.get("stateDir", state)
    except (ValueError, TypeError):
        cfg = {}
    base = os.path.dirname(config_rel)
    for cand in (os.path.join(base, state), state):
        path = os.path.join(root, cand, "ledger.json")
        if os.path.isfile(path):
            try:
                led = json.load(open(path, encoding="utf-8"))
            except ValueError:
                return None
            counts = {}
            for k, v in led.items():
                if k.startswith("_") or not isinstance(v, dict):
                    continue
                s = v.get("status", "unknown")
                counts[s] = counts.get(s, 0) + 1
            return {"ledger": os.path.relpath(path, root), "units": sum(counts.values()), "by_status": counts,
                    "config_type": cfg.get("publicationType"), "config_size": cfg.get("committeeSize"),
                    "config_effort": cfg.get("effort")}
    return {"ledger": None, "config_type": cfg.get("publicationType"), "config_size": cfg.get("committeeSize"),
            "config_effort": cfg.get("effort")}


def detect(root):
    root = os.path.abspath(root)
    files = list(walk(root))
    texts = [f for f in files if f.lower().endswith(TEXT_EXT)]
    tex = [f for f in texts if f.lower().endswith((".tex", ".texview"))]
    mains = []
    for f in tex:
        head = read(root, f, 200_000)
        if re.search(r"^[^%\n]*\\documentclass", head, re.M) and "\\begin{document}" in head:
            mains.append(f)
    infos = [tex_info(root, f) for f in mains]
    infos = [i for i in infos if (i["class"] or "").lower() not in ("standalone", "beamer", "tikz")]
    # The main document: the one that includes the most, then the shortest path.
    infos.sort(key=lambda i: (-len(i["includes"]), i["file"].count("/"), i["file"]))
    main = infos[0] if infos else None

    md_docs = []
    if not main:
        for f in texts:
            stem = os.path.splitext(os.path.basename(f))[0].lower()
            if f.lower().endswith((".md", ".markdown", ".qmd", ".rmd")) and stem not in NOT_DOCS and not GUIDE_NAMES.search(stem) and not CONTEXT_NAMES.search(stem):
                md_docs.append(f)

    included = []
    if main:
        base = os.path.dirname(main["file"])
        for name in main["includes"]:
            r = resolve_tex(root, base, name)
            if r and r not in main["preamble_includes"]:
                included.append(r)
    preamble = []
    if main:
        for name in main["preamble_includes"]:
            r = resolve_tex(root, os.path.dirname(main["file"]), name)
            if r:
                preamble.append(r)

    # Chapter units: included files that sit in a common directory (at least two), or Markdown chapters.
    chapter_glob, chapter_files = None, []
    dirs = {}
    for f in included:
        dirs.setdefault(os.path.dirname(f), []).append(f)
    if dirs:
        d, fs = max(dirs.items(), key=lambda kv: len(kv[1]))
        if len(fs) >= 2 and d:
            ext = os.path.splitext(fs[0])[1]
            chapter_glob, chapter_files = f"{d}/*{ext}", fs
    if not main and len(md_docs) >= 2:
        dirs = {}
        for f in md_docs:
            dirs.setdefault(os.path.dirname(f), []).append(f)
        d, fs = max(dirs.items(), key=lambda kv: len(kv[1]))
        if len(fs) >= 2:
            ext = os.path.splitext(fs[0])[1]
            chapter_glob, chapter_files = (f"{d}/*{ext}" if d else f"*{ext}"), fs

    bibs = []
    if main:
        for b in main["bibliography"]:
            r = resolve_tex(root, os.path.dirname(main["file"]), b, exts=(".bib", ""))
            if r:
                bibs.append(r)
    if not bibs:
        bibs = [f for f in files if f.lower().endswith(".bib")][:3]
    ref_lists = [f for f in texts if re.search(r"(primary[-_ ]?sources|references|bibliography)", os.path.basename(f), re.I)
                 and not f.lower().endswith(".bib") and f not in bibs][:3] if not bibs else []

    guidelines = [f for f in texts if GUIDE_NAMES.search(os.path.basename(f)) and f.lower().endswith((".md", ".markdown", ".txt", ".pdf"))]
    guidelines += [f for f in files if f.lower().endswith(".pdf") and GUIDE_NAMES.search(os.path.basename(f))]
    guidelines = sorted(set(guidelines))[:5]
    context = sorted({f for f in texts if CONTEXT_NAMES.search(os.path.basename(f)) and f not in guidelines and f.lower().endswith((".md", ".markdown", ".txt"))})[:6]

    title = main["title"] if main else None
    journal = main.get("journal") if main else None
    if not journal and md_docs:
        m = re.search(r"^journal:\s*['\"]?(.+?)['\"]?\s*$", read(root, md_docs[0], 20_000), re.M)
        journal = m.group(1).strip() if m else None
    if not title and md_docs:
        m = re.search(r"^#\s+(.+)$", read(root, md_docs[0], 20_000), re.M) or re.search(r"^title:\s*['\"]?(.+?)['\"]?$", read(root, md_docs[0], 20_000), re.M)
        title = m.group(1).strip() if m else None
    ptype, conf, reasons, venue = guess_type(main, ([main["file"]] if main else []) + (md_docs[:1] if len(md_docs) == 1 else []) + [os.path.basename(root)], title, len(chapter_files))
    if not main and md_docs and not ptype:
        ptype, conf, reasons = ("book" if chapter_files else "journal-article"), "low", ["Markdown documents without class or venue hints"]
    if journal and ptype in (None, "journal-article", "technical-report"):
        ptype, conf = "journal-article", "high"
        reasons = reasons + [f"the source names the journal ({journal})"]
    if ptype not in CHAPTER_TYPES:  # a paper, report or proposal is judged as a whole, never section by section
        chapter_glob, chapter_files = None, []

    t = tools()
    build = None
    if main:
        engine = "-xelatex" if main["fontspec"] else "-pdf"
        has_rc = any(os.path.isfile(os.path.join(root, x)) for x in ("latexmkrc", ".latexmkrc"))
        if True:
            unit_main = "{main}" if not chapter_glob else main["file"]
            build = {
                "unit": f"latexmk {engine} -interaction=nonstopmode -halt-on-error -outdir=.writing-committee/build/{{unit}} {unit_main}",
                "global": [f"latexmk {engine} -interaction=nonstopmode -halt-on-error -outdir=.writing-committee/build/full {main['file']}"],
                "note": ("Chapters are checked by building the whole document; replace checks.unit with a one-chapter build if one exists."
                         if chapter_glob else ""),
                "warning": None if t["latexmk"] else "latexmk is not installed on this machine: install a TeX distribution, or every build check fails",
            }
    elif md_docs and t["pandoc"]:
        build = {"unit": "pandoc {files} -o .writing-committee/build/{unit}.html", "global": [], "note": "Markdown checked with pandoc"}

    configs = existing_configs(root)
    state = ledger_summary(root, configs[0]) if configs else None
    git = git_state(root)

    proposed = {"name": title or os.path.basename(root), "publicationType": ptype}
    if main and not chapter_glob:
        proposed["documents"] = [main["file"]]
    elif main and chapter_glob:
        proposed["stages"] = [{"id": "chapters", "goal": "Revise every chapter.",
                               "unitsFrom": {"glob": chapter_glob, "inputsAsCompanions": True, "orderFrom": main["file"]}}]
        proposed["sharedFiles"] = sorted(set([main["file"]] + preamble + bibs))
    elif md_docs:
        if chapter_glob:
            proposed["stages"] = [{"id": "chapters", "goal": "Revise every chapter.", "unitsFrom": {"glob": chapter_glob}}]
        else:
            proposed["documents"] = md_docs[:1]
    if guidelines:
        proposed["guidelines"] = [g for g in guidelines if not g.lower().endswith(".pdf")][:3]
    if context:
        proposed["context"] = context
    if bibs:
        proposed["bibliography"] = bibs[0] if len(bibs) == 1 else bibs
    if ref_lists:
        proposed["referenceList"] = ref_lists
    if build:
        proposed["checks"] = {"unit": build["unit"], "global": build["global"]}
        if build["note"]:
            proposed["checks"]["notes"] = build["note"]
    if ptype == "journal-article" and journal:
        proposed["recentWork"] = {"venue": journal, "months": 6, "count": [2, 3]}
    proposed["commit"] = {"perWave": True, "push": False, "branch": ""}

    questions = []
    if not configs:
        if not (main or md_docs):
            questions.append({"id": "document", "question": "Which file is the document to work on?", "options": [], "why": "no main LaTeX or Markdown document was found"})
        if conf in ("none", "low", "medium"):
            common = ["journal-article", "conference-paper", "thesis", "book", "survey", "technical-report"]
            opts = [ptype] if ptype else []
            opts += [x for x in common if x not in opts][: 4 - len(opts)]
            questions.append({"id": "type", "question": "What kind of document is this?", "options": opts, "recommended": ptype,
                              "why": "; ".join(reasons)})
        if ptype in (None, "journal-article") and not journal:
            questions.append({"id": "journal", "question": "Which journal is it for? I will add 2-3 related works that journal published in the last 6 months.",
                              "options": ["Not for a specific journal: skip this", "Other (name the journal)"],
                              "recommended": None, "why": "the source does not name the journal"})
        questions.append({"id": "goal", "question": "What should the revision achieve?",
                          "options": ([f"Ready for submission to {journal or venue}"] if (journal or venue) else ["Ready for submission"]) +
                                     (["Meet the rules in " + guidelines[0]] if guidelines else []) +
                                     ["Clearer, tighter prose without changing the content", "Other (describe)"],
                          "recommended": None, "why": "the goal is what every agent works toward; the repository cannot state it"})
        if not guidelines:
            questions.append({"id": "guidelines", "question": "Are there rules the text must follow (venue instructions, a style guide, a page limit)?",
                              "options": ["No, use the skill's writing guide", "Yes, I will give a file or a link", "Yes, I will describe them"],
                              "recommended": "No, use the skill's writing guide", "why": "no guidelines or venue-instructions file was found"})
    questions.append({"id": "size", "question": "How large should the committee be?", "options": SIZES,
                      "recommended": "medium" if chapter_glob and len(chapter_files) > 8 else "high",
                      "why": "low ~14, medium ~18, high ~24, full ~24-28 agent calls per unit"})
    questions.append({"id": "effort", "question": "At what effort should the committee work?", "options": ["high", "medium", "xhigh", "low"],
                      "recommended": "high", "why": "more effort means more careful work, more tokens and slower runs; max and default (each role its own) are also accepted"})
    if state and state.get("config_size"):
        questions = [q for q in questions if q["id"] != "size"]
    if state and state.get("config_effort"):
        questions = [q for q in questions if q["id"] != "effort"]

    return {
        "root": root,
        "existing_config": configs,
        "state": state,
        "main_document": main["file"] if main else (md_docs[0] if md_docs else None),
        "document_class": (main or {}).get("class"),
        "title": title,
        "venue": venue,
        "journal": journal,
        "publication_type": {"guess": ptype, "confidence": conf, "reasons": reasons},
        "units": {"kind": "chapters" if chapter_glob else "whole document", "glob": chapter_glob, "count": len(chapter_files) or (1 if (main or md_docs) else 0),
                  "examples": chapter_files[:5]},
        "preamble_files": preamble,
        "bibliography": bibs,
        "reference_lists": ref_lists,
        "guidelines": guidelines,
        "context": context,
        "build": build,
        "tools": t,
        "git": git,
        "proposed_config": proposed,
        "questions": questions,
    }


def summary(d):
    L = []
    if d["existing_config"]:
        L.append(f"existing committee configuration: {', '.join(d['existing_config'])}")
        st = d.get("state") or {}
        if st.get("ledger"):
            L.append(f"ledger: {st['units']} unit(s) " + ", ".join(f"{k} {v}" for k, v in sorted(st["by_status"].items())))
        L.append("-> continue with it (prepare_run.py <config> --status); only the size and effort may still need asking")
    L.append(f"main document: {d['main_document'] or 'not found'}" + (f" (class {d['document_class']})" if d["document_class"] else ""))
    if d["title"]:
        L.append(f"title: {d['title']}")
    pt = d["publication_type"]
    L.append(f"publication type: {pt['guess'] or 'unknown'} (confidence {pt['confidence']})" + (f"; venue: {d['venue']}" if d["venue"] else "")
             + (f"; journal: {d['journal']} (2-3 recent related works will be looked up)" if d.get("journal") else ""))
    u = d["units"]
    L.append(f"units: {u['kind']}" + (f", {u['count']} file(s) matching {u['glob']}" if u["glob"] else ""))
    L.append(f"bibliography: {', '.join(d['bibliography']) or 'none'}" + (f"; reference lists: {', '.join(d['reference_lists'])}" if d["reference_lists"] else ""))
    L.append(f"guidelines: {', '.join(d['guidelines']) or 'none found'}")
    if d["context"]:
        L.append(f"context files: {', '.join(d['context'])}")
    L.append(f"build: {d['build']['global'][0] if d['build'] and d['build']['global'] else (d['build']['unit'] if d['build'] else 'none detected')}")
    if d["build"] and d["build"].get("warning"):
        L.append(f"warning: {d['build']['warning']}")
    g = d["git"]
    L.append("git: " + (f"branch {g['branch']}, {g['uncommitted_files']} uncommitted file(s)" if g.get("repository") else "not a repository (the committee needs one)"))
    missing = [k for k in ("latexmk", "pandoc") if not d["tools"].get(k)]
    L.append(f"tools: python {d['tools']['python']}" + (f"; missing: {', '.join(missing)}" if missing else ""))
    L.append("")
    L.append("questions still open:")
    for q in d["questions"]:
        rec = f" [recommended: {q['recommended']}]" if q.get("recommended") else ""
        L.append(f"  - {q['question']} {' / '.join(q['options'])}{rec}")
    return "\n".join(L)


def init(args):
    root = os.path.abspath(args.root)
    d = detect(root)
    cfg = dict(d["proposed_config"])
    if args.type:
        if args.type not in TYPES:
            sys.exit(f"--type: unknown type '{args.type}'; use one of {', '.join(TYPES)}")
        cfg["publicationType"] = args.type
    if not cfg.get("publicationType"):
        sys.exit("the publication type could not be detected; pass --type")
    if args.name:
        cfg["name"] = args.name
    if args.main:
        cfg.pop("stages", None)
        cfg["documents"] = [args.main]
    if args.bib:
        cfg["bibliography"] = args.bib
    if args.guidelines is not None:
        g = [x for x in args.guidelines.split(",") if x]
        if g:
            cfg["guidelines"] = g
        else:
            cfg.pop("guidelines", None)
    if args.goal:
        cfg["goal"] = args.goal
    if args.journal:
        cfg["recentWork"] = {"venue": args.journal, "months": args.recent_months, "count": [2, 3]}
    elif "recentWork" in cfg:
        cfg["recentWork"]["months"] = args.recent_months
    if args.no_recent or cfg.get("publicationType") not in ("journal-article", "conference-paper", "survey"):
        cfg.pop("recentWork", None)
    if args.size:
        cfg["committeeSize"] = args.size
    if args.effort and args.effort != "default":
        cfg["effort"] = args.effort
    order = ["name", "publicationType", "committeeSize", "effort", "goal", "guidelines", "context", "documents", "stages",
             "sharedFiles", "bibliography", "referenceList", "recentWork", "checks", "commit"]
    cfg = {k: cfg[k] for k in order if k in cfg} | {k: v for k, v in cfg.items() if k not in order}
    out = os.path.join(root, args.out)
    if os.path.exists(out) and not args.force:
        sys.exit(f"{args.out} exists; pass --force to replace it, or continue with it")
    for g in cfg.get("guidelines", []):
        if not os.path.isfile(os.path.join(root, g)):
            sys.exit(f"guidelines file not found: {g}")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(cfg, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    skill = os.path.dirname(os.path.abspath(__file__))
    print(f"wrote {args.out}")
    print(json.dumps(cfg, indent=2, ensure_ascii=False))
    print(f"\nnext: python3 {skill}/prepare_run.py {args.out}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("detect", help="scan the project and list what is known and what must be asked")
    p.add_argument("root", nargs="?", default=".")
    p.add_argument("--json", action="store_true")
    q = sub.add_parser("init", help="write the committee configuration from the detection and the answers")
    q.add_argument("root", nargs="?", default=".")
    q.add_argument("--type")
    q.add_argument("--size", choices=SIZES)
    q.add_argument("--effort", choices=EFFORTS)
    q.add_argument("--goal")
    q.add_argument("--guidelines", help="comma-separated guideline files; empty for none")
    q.add_argument("--main", help="the main document, if detection chose the wrong one")
    q.add_argument("--bib")
    q.add_argument("--journal", help="target journal: the committee adds 2-3 related works it published recently")
    q.add_argument("--recent-months", type=float, default=6, help="how far back to look in the journal (default 6)")
    q.add_argument("--no-recent", action="store_true", help="do not add recent work from the target journal")
    q.add_argument("--name")
    q.add_argument("--out", default="writing-committee.json")
    q.add_argument("--force", action="store_true")
    a = ap.parse_args()
    if a.cmd == "detect":
        d = detect(a.root)
        print(json.dumps(d, indent=2, ensure_ascii=False) if a.json else summary(d))
    else:
        init(a)


if __name__ == "__main__":
    main()
