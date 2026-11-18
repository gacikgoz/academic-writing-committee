#!/usr/bin/env python3
"""Prepare, record and report runs of the academic-writing committee.

  prepare_run.py CONFIG [--stages a,b] [--units id1,id2] [--include-accepted] [--include-stalled]
                 [--rescout] [--max-units N] [--review-only] [--plan-only] [--shards K] [--first-shard N] [--no-global]
                 [--global-only] [--out PATH]
      Expand the project configuration into concrete units and write the workflow
      arguments (default: <stateDir>/run-args.json). Prints a plan summary. Exits
      with status 2 when there is nothing to do. Units that stalled (unresolved twice at
      the strongest tier, or failed twice) are left out until a person decides
      (--include-stalled). A stage defined by a scope is scouted once; later runs resume
      its scouted units from the ledger (--rescout scouts it again).
      --shards K divides the units among K workflows that run at the same time
      (<stateDir>/run-args.shard-<i>.json): a workflow runs only a few agents at once, so
      shards are how a run gets more agents working. Units that share a file stay in one
      shard; shards run no global round, so record them all and prepare once more for it.
      --first-shard N numbers the shards from N: use it when shards of an earlier plan are still
      running, because each shard keeps its lessons in <stateDir>/*.shard-<i>.md.
      --plan-only runs the first reading and the developmental briefs and edits nothing;
      the run that revises those units later starts at the writer. --no-global ends a run
      after its units, and --global-only runs only the global rounds, over the units accepted
      so far (the step after a set of shards, or after runs prepared with --no-global).
  prepare_run.py CONFIG --record RESULT.json
      Merge a workflow result into <stateDir>/ledger.json (a result already
      recorded is skipped) and save learned roster changes to <stateDir>/roster.json.
  prepare_run.py CONFIG --status
      Print the ledger: accepted, reopened, unresolved, failed, deferred, reviewed
      and stalled units.

Only the Python standard library is used.
"""

import argparse
import glob
import hashlib
import json
import os
import re
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IGNORE_LINES = ["units/", "global/", "build/", "run-args.json", "last_result.json", "result-*.json",
                "citations-cache.json", "run-args.shard-*.json", "*.shard-*.md"]
RANK = {"standard": 0, "hard": 1, "critical": 2}
INPUT_RE = re.compile(r"\\(?:input|include|InputIfFileExists)\s*\{([^}#]+)\}")
BIB_RE = re.compile(r"\\(?:bibliography|addbibresource)\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}")
DEFAULT_TIERS = [{"model": "sonnet", "effort": "high"}, {"model": "opus", "effort": "high"},
                 {"model": "fable", "effort": "high"}, {"model": "fable", "effort": "xhigh"}]


def load_config(path):
    if not os.path.isfile(path) and os.path.isfile(os.path.join(".writing-committee", path)):
        path = os.path.join(".writing-committee", path)
    with open(path, encoding="utf-8") as fh:
        cfg = json.load(fh)
    cfg_dir = os.path.dirname(os.path.abspath(path))
    if os.path.basename(cfg_dir) == cfg.get("stateDir", ".writing-committee") and cfg.get("root", ".") == ".":
        root = os.path.dirname(cfg_dir)
    else:
        root = os.path.abspath(os.path.join(cfg_dir, cfg.get("root", ".")))
    state = os.path.join(root, cfg.get("stateDir", ".writing-committee"))
    return cfg, root, state


def strip_comments(text):
    return re.sub(r"(?<!\\)%.*", "", text)


def read(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8", errors="replace") as fh:
        return fh.read()


def resolve_input(root, target):
    for cand in (target, target + ".tex"):
        if os.path.isfile(os.path.join(root, cand)):
            return os.path.normpath(cand)
    return None


def groups_for(pattern, stem):
    if not pattern:
        return {}
    m = re.search(pattern, stem)
    if not m:
        return {}
    out = {}
    for k, v in m.groupdict().items():
        if v is None:
            continue
        out[k] = v
        if v.isdigit():
            out[k + "_int"] = str(int(v))
    return out


def expand_units(cfg, root, stage, profile=None):
    """Return concrete units for a stage (explicit units are passed through)."""
    profile = profile or {}
    if stage.get("units"):
        return [dict(u) for u in stage["units"]]  # keeps an optional "_inputs" flag
    spec = stage.get("unitsFrom")
    if not spec:
        return []  # the Scout agent will divide the scope
    files = sorted(os.path.relpath(p, root) for p in glob.glob(os.path.join(root, spec["glob"])))
    excluded = set()
    for pat in spec.get("exclude", []):
        excluded |= {os.path.relpath(p, root) for p in glob.glob(os.path.join(root, pat))}
    units = []
    for f in files:
        if f in excluded:
            continue
        stem = os.path.splitext(os.path.basename(f))[0]
        g = {"stem": stem, **groups_for(spec.get("idPattern"), stem)}
        try:
            uid = (spec.get("idPrefix", "") + spec.get("idTemplate", "{stem}").format(**g)).replace("_", "-").lower()
        except (KeyError, IndexError):
            print(f"warning: {f} matches the glob of stage {stage.get('id')} but not its idPattern; skipped "
                  "(list it under exclude)", file=sys.stderr)
            continue
        owned = [f]
        for tpl in spec.get("companions", []):
            for p in sorted(glob.glob(os.path.join(root, tpl.format(**g)))):
                rel = os.path.relpath(p, root)
                if rel not in owned:
                    owned.append(rel)
        units.append({
            "id": uid,
            "title": stem,
            "files": owned,
            "difficulty": spec.get("difficultyOverrides", {}).get(uid, spec.get("difficulty", profile.get("defaultDifficulty", "standard"))),
            "goal": spec.get("goal", ""),
            "_inputs": bool(spec.get("inputsAsCompanions")),
        })
    order_from = spec.get("orderFrom")
    if order_from and os.path.isfile(os.path.join(root, order_from)):
        text = strip_comments(read(root, order_from))

        def pos(u):
            primary = os.path.splitext(u["files"][0])[0]
            m = re.search(r"\\(?:input|include|InputIfFileExists)\s*\{" + re.escape(primary) + r"(?:\.[A-Za-z]+)?\}", text)
            if m:
                return m.start()
            i = text.find(primary)
            return i if i >= 0 else len(text) + 1
        units.sort(key=pos)
    return units


def add_input_companions(root, all_units):
    """Give each unit the files that only it \\input-s (LaTeX projects)."""
    refs = {}
    for u in all_units:
        if not u.get("_inputs"):
            continue
        for f in list(u["files"]):
            if not os.path.isfile(os.path.join(root, f)):
                continue
            for m in INPUT_RE.finditer(strip_comments(read(root, f))):
                tgt = resolve_input(root, m.group(1).strip())
                if tgt:
                    refs.setdefault(tgt, set()).add(u["id"])
    owned_anywhere = {f for u in all_units for f in u["files"]}
    for u in all_units:
        if not u.pop("_inputs", False):
            continue
        for tgt, owners in sorted(refs.items()):
            if owners == {u["id"]} and tgt not in owned_anywhere:
                u["files"].append(tgt)
                owned_anywhere.add(tgt)


def ensure_gitignore(root, state):
    rel = os.path.relpath(state, root).replace(os.sep, "/")
    if rel.startswith(".."):
        return   # the state directory is outside the project: nothing of it can be committed
    path = os.path.join(root, ".gitignore")
    existing = open(path, encoding="utf-8").read().splitlines() if os.path.isfile(path) else []
    wanted = [f"/{rel}/{x}" for x in IGNORE_LINES]
    missing = [w for w in wanted if w not in existing]
    if missing:
        nl = "\r\n" if os.path.isfile(path) and b"\r\n" in open(path, "rb").read() else "\n"
        present = [i for i, line in enumerate(existing) if line in wanted]
        if present:
            # Extend the committee's existing block instead of starting a second one.
            lines = existing[:present[-1] + 1] + missing + existing[present[-1] + 1:]
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(nl.join(lines) + nl)
            return
        with open(path, "a", encoding="utf-8", newline="") as fh:
            if existing and existing[-1] != "":
                fh.write(nl)
            fh.write(nl.join(["# academic-writing committee working files"] + missing) + nl)


STATE_FILES = {
    "lessons.md": "# Committee Lessons\n\nShort preventive instructions learned from earlier rounds, addressed to a role. The Retrospective Analyst maintains this file; it starts empty.\n",
    "lint_rules.md": "# Learned Lint Rules\n\nMechanical patterns the Mechanical Checker applies (pattern or command, what it detects, the guideline rule, severity). The Retrospective Analyst maintains this file; it starts empty.\n",
    "guideline_proposals.md": "# Guideline Proposals\n\nAmbiguities, gaps and contradictions in the guidelines, with proposed wording, for the human owner to decide. The committee never edits the guidelines; this file starts empty.\n",
}


def ensure_state_files(state):
    for name, text in STATE_FILES.items():
        path = os.path.join(state, name)
        if not os.path.isfile(path):
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)


def load_ledger(state):
    p = os.path.join(state, "ledger.json")
    return json.load(open(p, encoding="utf-8")) if os.path.isfile(p) else {}


def save_ledger(state, ledger):
    os.makedirs(state, exist_ok=True)
    with open(os.path.join(state, "ledger.json"), "w", encoding="utf-8") as fh:
        json.dump(ledger, fh, indent=1, sort_keys=True)


def writing_skills(cfg, root):
    """Extra writing references (the skill's own guide is always given to every agent)."""
    return [p if os.path.isabs(p) else os.path.join(root, p) for p in cfg.get("writingSkills", [])]


def load_profile(cfg):
    """Defaults for a publication type from profiles/<type>.json; the configuration overrides them."""
    known = sorted(os.path.splitext(f)[0] for f in os.listdir(os.path.join(SKILL_DIR, "profiles")) if f.endswith(".json"))
    ptype = cfg.get("publicationType")
    if not ptype:
        sys.exit(f"publicationType is required; known types: {', '.join(known)}")
    path = os.path.join(SKILL_DIR, "profiles", f"{ptype}.json")
    if not os.path.isfile(path):
        sys.exit(f"unknown publicationType '{ptype}'; known types: {', '.join(known)}")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def load_sizes():
    with open(os.path.join(SKILL_DIR, "committee", "sizes.json"), encoding="utf-8") as fh:
        return json.load(fh)


def apply_size(cfg, profile, size=None):
    """Scale the profile to a committee size (low, medium, high, full; committee/sizes.json).
    The size changes the profile and fills in settings the configuration leaves out, so anything the
    configuration states explicitly still wins. Returns the size name and the scaled profile."""
    table = load_sizes()
    name = size or cfg.get("committeeSize") or table.get("default", "full")
    spec = table["sizes"].get(name)
    if spec is None:
        sys.exit(f"committeeSize: unknown size '{name}'; use one of {', '.join(table['sizes'])}")
    profile = dict(profile)
    if "readers" in spec:
        profile["readers"] = (profile.get("readers") or [])[: spec["readers"]]
    if "reviewers" in spec:
        order = table["lensPriority"].get(cfg.get("publicationType"), table["lensPriority"]["default"])
        rank = {k: i for i, k in enumerate(order)}
        lenses = sorted(profile.get("reviewers") or [], key=lambda r: rank.get(r.get("key"), len(order)))
        profile["reviewers"] = lenses[: spec["reviewers"]]
    if "editors" in spec:
        profile["editors"] = [e for e in (profile.get("editors") or []) if e.get("key") in spec["editors"]]
    if "limits" in spec:
        profile["limits"] = {**profile.get("limits", {}), **spec["limits"]}
    if "writerTiers" in spec:
        models = spec["writerTiers"]
        tiers = [{"model": m, "effort": "high"} for m in models]
        if len(tiers) > 1:
            tiers[-1]["effort"] = "xhigh"  # the last tier escalates by effort
        profile["roster"] = {**profile.get("roster", {}), "writerTiers": tiers}
    for key in ("readBeforeBrief", "modelCeiling", "adaptRoster"):
        if key in spec and key not in cfg:
            cfg[key] = spec[key]
    return name, profile


EFFORTS = ["low", "medium", "high", "xhigh", "max"]


def recent_work(cfg, run_args):
    """The task text for `recentWork`: add a few related works that the target journal published recently.
    Returns None when the configuration has no recentWork."""
    rw = cfg.get("recentWork")
    if not rw:
        return None
    venue = rw.get("venue") or rw.get("journal")
    if not venue:
        sys.exit("recentWork: give the journal as recentWork.venue")
    months = rw.get("months", 6)
    lo, hi = (rw.get("count") or [2, 3]) if isinstance(rw.get("count"), list) else (rw.get("count", 2), rw.get("count", 3))
    issn = f' --issn {rw["issn"]}' if rw.get("issn") else ""
    script = f'python3 {SKILL_DIR}/scripts/venue_recent.py --venue "{venue}"{issn} --from <the main document> --months {months}'
    return (f"Recent work from the target journal: add {lo} to {hi} related works that {venue} published in the last "
            f"{months:g} months to the related-work discussion (the related-work section, or the introduction when there is "
            f"none). Find the candidates with `{script}`. Open each candidate's DOI and read at least its abstract; keep only "
            f"works that are genuinely related to this manuscript's problem or method. Add their entries to the bibliography "
            f"with `venue_recent.py --bibtex <DOI>`, and cite each one for what it actually says, in one or two sentences that "
            f"relate it to this work. If fewer than {lo} are genuinely related, add only those and report why; never pad the "
            f"list. The writer does this in the first round, and the references lens verifies each addition.")


def run_effort(cfg, effort=None):
    """The run's effort level (low, medium, high, xhigh, max), or None for each role's own default.
    The workflow gives it to every role except the mechanical checker and the committer; the last
    writer tier runs one level higher. --effort overrides the configuration's `effort`."""
    e = effort or cfg.get("effort")
    if e in (None, "", "default"):
        return None
    if e not in EFFORTS:
        sys.exit(f"effort: unknown level '{e}'; use one of {', '.join(EFFORTS)} or default")
    return e


def load_catalog():
    with open(os.path.join(SKILL_DIR, "committee", "catalog.json"), encoding="utf-8") as fh:
        return json.load(fh)


def roster_lists(cfg, profile):
    """Readers, reviewers and editors: the configuration's list, else the profile's, then add/drop by catalog key."""
    catalog = None
    out = {}
    for kind, cap in (("readers", "Readers"), ("reviewers", "Reviewers"), ("editors", "Editors")):
        items = [dict(x) for x in (cfg.get(kind) or profile.get(kind) or [])]
        drop = set(cfg.get("drop" + cap, []))
        items = [x for x in items if x.get("key") not in drop]
        for key in cfg.get("add" + cap, []):
            if any(x.get("key") == key for x in items):
                continue
            catalog = catalog or load_catalog()
            entry = catalog.get(kind, {}).get(key)
            if not entry:
                sys.exit(f"add{cap}: '{key}' is not in committee/catalog.json; known: {', '.join(sorted(catalog.get(kind, {})))}")
            items.append(dict(entry))
        if items:
            out[kind] = items
    return out


MODEL_ORDER = ["haiku", "sonnet", "opus", "fable"]


def model_ceiling(cfg):
    """The configuration's modelCeiling as {model, except}, or None. No role runs above the ceiling model
    except the roles listed in `except` (role names as in roster adjustments: chair, globalChair,
    writerTier:2, reviewer:technical). The workflow applies it to the whole roster, learned changes included."""
    c = cfg.get("modelCeiling")
    if not c:
        return None
    c = {"model": c, "except": []} if isinstance(c, str) else {"model": c.get("model"), "except": list(c.get("except", []))}
    if c["model"] not in MODEL_ORDER:
        sys.exit(f"modelCeiling: unknown model '{c['model']}'; use one of {', '.join(MODEL_ORDER)}")
    return c


def apply_learned_roster(state, run_args, cfg):
    """Merge <stateDir>/roster.json (model changes the retrospective made in earlier runs).

    Precedence for the role entries of `roster`: configuration > learned > profile. For readers, reviewers,
    editors and writer tiers the learned model and effort replace the listed ones (a list entry always names
    a model, so an explicit choice cannot be told apart); set adaptRoster to false or delete roster.json to
    discard what was learned."""
    path = os.path.join(state, "roster.json")
    if not run_args.get("adaptRoster", True) or not os.path.isfile(path):
        return []
    learned = json.load(open(path, encoding="utf-8"))
    applied = []
    for role, v in sorted(learned.items()):
        kind, _, key = role.partition(":")
        mv = {"model": v.get("model"), "effort": v.get("effort")}
        if kind in ("reader", "reviewer", "editor"):
            for x in run_args.get(kind + "s", []):
                if x.get("key") == key:
                    x.update(mv)
                    applied.append(role)
        elif kind == "writerTier" and key.isdigit():
            tiers = run_args["roster"].setdefault("writerTiers", [dict(t) for t in DEFAULT_TIERS])
            if int(key) < len(tiers):
                tiers[int(key)] = dict(tiers[int(key)], **mv)
                applied.append(role)
        elif kind not in cfg.get("roster", {}):
            run_args["roster"][kind] = mv
            applied.append(role)
    return applied


def bib_targets(root, main):
    """Bibliography files a LaTeX main file names with \\bibliography or \\addbibresource."""
    if not os.path.isfile(os.path.join(root, main)):
        return []
    base = os.path.dirname(main)
    out = []
    for m in BIB_RE.finditer(strip_comments(read(root, main))):
        for name in m.group(1).split(","):
            name = name.strip()
            if not name:
                continue
            if not name.endswith(".bib"):
                name += ".bib"
            for cand in (os.path.normpath(os.path.join(base, name)), os.path.normpath(name)):
                if os.path.isfile(os.path.join(root, cand)) and cand not in out:
                    out.append(cand)
                    break
    return out


def document_stage(cfg, profile, root):
    """`documents` shortcut: one unit per main file, for papers and other documents judged as a whole.

    The unit also owns the bibliography its main file names, unless the bibliography is a shared file or
    another document uses it too."""
    docs = cfg.get("documents") or []
    if not docs:
        return None
    bibs = {d: bib_targets(root, d) for d in docs}
    shared = set(cfg.get("sharedFiles", []))
    units = []
    for d in docs:
        stem = os.path.splitext(os.path.basename(d))[0]
        own = [b for b in bibs[d] if b not in shared and not any(b in bibs[o] for o in docs if o != d)]
        units.append({"id": re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-") or "document", "title": stem,
                      "files": [d] + own, "difficulty": profile.get("defaultDifficulty", "hard"), "goal": "", "_inputs": True})
    return {"id": "document", "goal": cfg.get("goal", profile.get("goal", "")), "units": units}


def bibliography(cfg, root):
    """The configured bibliography, or the files the documents' main files name."""
    b = cfg.get("bibliography")
    if b:
        return [b] if isinstance(b, str) else list(b)
    found = []
    for d in cfg.get("documents") or []:
        for x in bib_targets(root, d):
            if x not in found:
                found.append(x)
    return found


def fill_skill(checks):
    """Replace {skill} with the skill directory in the check commands and notes."""
    sub = lambda x: x.replace("{skill}", SKILL_DIR) if isinstance(x, str) else x
    out = dict(checks)
    for k in ("unit", "notes"):
        if k in out:
            out[k] = sub(out[k])
    if "global" in out:
        out["global"] = [sub(c) for c in out["global"]]
    return out


def agent_cap():
    """Agents one workflow runs at a time: the Workflow tool allows min(16, CPUs - 2)."""
    return max(1, min(16, (os.cpu_count() or 4) - 2))


def shard_units(stages, k):
    """Divide the units among at most k shards. Units that share a file (in any stage) stay
    together, a stage the Scout has yet to divide goes to the first shard, and each shard
    keeps the order of the stages and of the units. Returns one stage list per shard."""
    units = [(si, ui) for si, st in enumerate(stages) for ui in range(len(st["units"]))]
    parent = {x: x for x in units}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    owner = {}
    for x in units:
        for f in stages[x[0]]["units"][x[1]]["files"]:
            if f in owner:
                parent[find(x)] = find(owner[f])
            else:
                owner[f] = x
    groups = {}
    for x in units:
        groups.setdefault(find(x), []).append(x)
    # Largest groups first, each to the shard with the fewest units so far; ties keep the reading order.
    load = [0] * k
    where = {}
    for members in sorted(groups.values(), key=lambda m: (-len(m), m[0])):
        i = min(range(k), key=lambda j: (load[j], j))
        load[i] += len(members)
        for x in members:
            where[x] = i
    shards = []
    for i in range(k):
        mine = []
        for si, st in enumerate(stages):
            keep = [u for ui, u in enumerate(st["units"]) if where.get((si, ui)) == i]
            if keep or (i == 0 and st.get("scope") and not st["units"]):
                mine.append(dict(st, units=keep))
        if mine:
            shards.append(mine)
    return shards


def merge_shard_state(state, index):
    """Append a finished shard's lessons, lint rules and guideline proposals to the committee's
    files and remove the shard's own. The next retrospective merges and trims the result."""
    merged = []
    for name in STATE_FILES:
        stem, ext = os.path.splitext(name)
        path = os.path.join(state, f"{stem}.shard-{index}{ext}")
        if not os.path.isfile(path):
            continue
        lines = open(path, encoding="utf-8").read().splitlines()
        while lines and (not lines[0].strip() or lines[0].startswith("# ")):
            lines.pop(0)   # the shard file's own title
        body = "\n".join(lines).strip()
        if body:
            ensure_state_files(state)
            with open(os.path.join(state, name), "a", encoding="utf-8") as fh:
                fh.write(f"\n## From Parallel Shard {index}\n\n{body}\n")
            merged.append(name)
        os.remove(path)
    return merged


def per_unit_estimate(run_args):
    readers = len(run_args.get("readers") or [1, 2])
    reviewers = len(run_args.get("reviewers") or [1, 2, 3, 4, 5, 6])
    if run_args.get("planOnly"):
        return 1 + (readers if run_args.get("readBeforeBrief", True) else 0)
    if run_args.get("reviewOnly"):
        return 3 + readers + reviewers
    editors = len(run_args.get("editors") or [1, 2])
    limits = run_args.get("limits", {})
    later = min(limits.get("laterRoundRounds", 2.5), limits.get("maxRounds", 5))
    first_read = readers if run_args.get("readBeforeBrief", True) else 0
    return 1 + first_read + (3 + readers + reviewers) + max(0, later - 1) * 5 + editors + 1


def max_tier(run_args):
    return len(run_args.get("roster", {}).get("writerTiers") or DEFAULT_TIERS) - 1


def is_meta(key):
    return key.startswith("_")


def prepare(args):
    cfg, root, state = load_config(args.config)
    ledger = load_ledger(state)
    profile = load_profile(cfg)
    size, profile = apply_size(cfg, profile, args.size)
    unitization = profile.get("unitization", "")
    if unitization == "whole-document" and not cfg.get("stages") and not cfg.get("documents"):
        print(f"warning: a {cfg['publicationType']} is judged as a whole; list its main file(s) in `documents`", file=sys.stderr)
    if unitization == "chapters" and not cfg.get("stages"):
        print(f"warning: a {cfg['publicationType']} is divided into chapters; give `stages` with `unitsFrom` (see committee/config.md)", file=sys.stderr)
    if not cfg.get("stages") and cfg.get("documents"):
        cfg["stages"] = [document_stage(cfg, profile, root)]
    wanted_stages = set(args.stages.split(",")) if args.stages else None
    wanted_units = set(args.units.split(",")) if args.units else None
    all_stages = [{k: v for k, v in st.items() if k != "unitsFrom"} | {"units": expand_units(cfg, root, st, profile)}
                  for st in cfg.get("stages", [])]
    add_input_companions(root, [u for st in all_stages for u in st["units"]])
    ids = [u["id"] for st in all_stages for u in st["units"]]
    dups = sorted({i for i in ids if ids.count(i) > 1})
    if dups:
        sys.exit(f"duplicate unit id(s): {', '.join(dups)}; adjust idPattern/idTemplate or exclude the extra files")
    stage_owners = {}
    for st in all_stages:
        owners = {}
        for u in st["units"]:
            for f in u["files"]:
                owners.setdefault(f, []).append(u["id"])
                stage_owners.setdefault(f, {}).setdefault(st["id"], []).append(u["id"])
        for f, us in sorted(owners.items()):
            if len(us) > 1:
                print(f"warning: stage {st['id']}: {f} is owned by several units ({', '.join(us)}); they will run in different waves", file=sys.stderr)
    for f, by_stage in sorted(stage_owners.items()):
        if len(by_stage) > 1:
            print(f"note: {f} is owned in several stages ({', '.join(f'{k}: {chr(44).join(v)}' for k, v in by_stage.items())}); "
                  "each stage edits it in turn", file=sys.stderr)
    owned_shared = sorted(f for f in cfg.get("sharedFiles", []) if f in stage_owners)
    if owned_shared:
        print(f"note: shared file(s) also owned by a unit: {', '.join(owned_shared)}; the owning unit edits them "
              "in its stage, and the Integration Editor at other times", file=sys.stderr)
    # Reading order of the whole document, for the global checks.
    prose = re.compile(r"\.(tex|texview|md|markdown|txt)$", re.I)
    global_files = []
    for st in all_stages:
        for u in st["units"]:
            for f in u["files"]:
                if prose.search(f) and f not in global_files:
                    global_files.append(f)
    # Shared prose files (front matter, abstract, back matter) belong to the whole-document checks
    # too: a main file with \begin{document} comes first, the others last. The main files that stages
    # read their order from count even when the configuration does not list them as shared.
    order_files = [st.get("unitsFrom", {}).get("orderFrom") for st in cfg.get("stages", [])]
    for f in list(dict.fromkeys(list(cfg.get("sharedFiles", [])) + [x for x in order_files if x])):
        if not prose.search(f) or f in global_files or not os.path.isfile(os.path.join(root, f)):
            continue
        if "\\begin{document}" in strip_comments(read(root, f)):
            global_files.insert(0, f)
        else:
            global_files.append(f)
    top = max_tier({"roster": {**profile.get("roster", {}), **cfg.get("roster", {})}})
    stages, skipped, prior, stalled_out, briefed_out = [], [], [], [], []
    configured = set(ids)
    for st in all_stages:
        in_scope = (not wanted_stages or st["id"] in wanted_stages) and not args.global_only
        scouted_before = st.get("scope") and not st["units"] and any(
            not is_meta(uid) and e.get("stage") == st["id"] and uid not in configured for uid, e in ledger.items())
        if scouted_before and not args.rescout:
            # Resume the units scouted in an earlier run instead of scouting the scope again.
            st = {k: v for k, v in st.items() if k != "scope"}
            st["units"] = [{"id": uid, "files": e["files"], "scouted": True, "difficulty": e.get("difficulty", "standard"),
                            **({"goal": e["goal"]} if e.get("goal") else {})}
                           for uid, e in sorted(ledger.items())
                           if not is_meta(uid) and e.get("stage") == st["id"] and e.get("files") and uid not in configured]
        keep = []
        for u in st["units"]:
            prev = ledger.get(u["id"], {})
            if prev.get("status") == "accepted" and not args.include_accepted:
                prior.append({"id": u["id"], "files": u["files"], "tier": prev.get("tier_index")})
                if in_scope and (not wanted_units or u["id"] in wanted_units):
                    skipped.append(u["id"])
                continue
            if not in_scope or (wanted_units and u["id"] not in wanted_units):
                continue
            if is_stalled(prev) and not args.include_stalled and not (wanted_units and u["id"] in wanted_units):
                stalled_out.append(u["id"])
                continue
            missing = [f for f in u["files"] if not os.path.exists(os.path.join(root, f))]
            if missing:
                u["goal"] = (u.get("goal", "") + " " if u.get("goal") else "") + f"(New files to create: {', '.join(missing)})"
            resume_status = prev.get("resume_status") if prev.get("status") == "deferred" else prev.get("status")
            if prev.get("tier_index") is not None and resume_status in ("unresolved", "reopened", "failed", "not_run"):
                # Escalation across runs: an unresolved unit starts one tier higher; other carry-overs keep their tier.
                step = 1 if resume_status == "unresolved" else 0
                u["tier"] = min(top, prev["tier_index"] + step)
            if prev.get("actions") and resume_status in ("unresolved", "reopened", "failed"):
                u["actions"] = prev["actions"]  # resume from the open actions instead of a new brief
            brief = prev.get("briefed")
            has_brief = bool(brief) and os.path.isfile(os.path.join(state, "units", u["id"], "brief.md"))
            if args.plan_only and (has_brief or u.get("actions")):
                briefed_out.append(u["id"])   # nothing left to plan for this unit
                continue
            if has_brief and not u.get("actions"):
                # A plan-only run wrote this unit's brief: the revision starts at the writer.
                u["briefed"] = True
                u["readersR0"] = bool(brief.get("readers_r0"))
                if RANK.get(brief.get("difficulty"), 0) > RANK.get(u.get("difficulty", "standard"), 0):
                    u["difficulty"] = brief["difficulty"]
            keep.append(u)
        if in_scope and (keep or (st.get("scope") and not wanted_units)):
            stages.append(dict(st, units=keep))
    if briefed_out:
        print(f"left out of the plan-only run (brief already written, or resuming from open actions): {', '.join(briefed_out)}")
    if stalled_out:
        print(f"left out, NEEDS A HUMAN DECISION (stalled; see --status, then --include-stalled or --units): {', '.join(stalled_out)}")
    # Ledger entries for scouted units (not in the configuration) also count as earlier work.
    known = {p["id"] for p in prior} | set(ids)
    for uid, e in sorted(ledger.items()):
        if not is_meta(uid) and uid not in known and e.get("status") == "accepted" and e.get("files"):
            prior.append({"id": uid, "files": e["files"], "tier": e.get("tier_index")})
    if args.max_units:
        budget = args.max_units
        for st in stages:
            st["units"], budget = st["units"][:max(0, budget)], max(0, budget - len(st["units"]))
        stages = [st for st in stages if st["units"]]
    # The whole-document checks cover what the committee has taken on: the units of this run, the
    # units accepted in earlier runs, and the shared prose files, in reading order. Units that no
    # run has revised yet would only add their unrevised baseline to every global report.
    in_scope_files = {f for st in stages for u in st["units"] for f in u["files"]} | {f for p in prior for f in p["files"]}
    shared_prose = set(cfg.get("sharedFiles", [])) | {x for x in order_files if x}
    # A shared file that a unit of a later run owns waits for that unit as well.
    waiting = {f for st in all_stages for u in st["units"] for f in u["files"]} - in_scope_files
    global_files = [f for f in global_files if f in in_scope_files or (f in shared_prose and f not in waiting)]
    reference_lists = [cfg["referenceList"]] if isinstance(cfg.get("referenceList"), str) else list(cfg.get("referenceList") or [])
    held_back = [r for r in reference_lists if r in waiting]
    if held_back:
        print(f"note: reference list(s) checked globally once their unit has run: {', '.join(held_back)}", file=sys.stderr)
    reference_lists = [r for r in reference_lists if r not in waiting]
    run_args = {
        "root": root,
        "skillDir": SKILL_DIR,
        "stateDir": state,
        "name": cfg.get("name", os.path.basename(root)),
        "goal": cfg.get("goal") or profile.get("goal", ""),
        "publicationType": cfg.get("publicationType", ""),
        "committeeSize": size,
        "effort": run_effort(cfg, args.effort),
        "publicationSection": profile.get("section", ""),
        "profileNote": profile.get("note", ""),
        "language": cfg.get("language", ""),
        "guidelines": guidelines_for(cfg, root),
        "context": cfg.get("context", []),
        "writingSkills": writing_skills(cfg, root),
        "checks": fill_skill(cfg.get("checks", {})),
        "bibliography": bibliography(cfg, root),
        "referenceList": reference_lists,
        "onlineCitations": cfg.get("onlineCitations", True),
        "assetDir": cfg.get("assetDir", ""),
        "limits": {**profile.get("limits", {}), **cfg.get("limits", {})},
        "commit": cfg.get("commit", {}),
        "roster": {**profile.get("roster", {}), **cfg.get("roster", {})},
        "adaptRoster": cfg.get("adaptRoster", True),
        "modelCeiling": model_ceiling(cfg),
        "readBeforeBrief": cfg.get("readBeforeBrief", True),
        "reviewOnly": bool(args.review_only or cfg.get("reviewOnly", False)),
        "planOnly": bool(args.plan_only),
        "skipGlobal": bool(args.no_global),
        "stages": stages,
        "priorAccepted": [p for p in prior if not any(p["id"] == u["id"] for st in stages for u in st["units"])],
        "globalFiles": global_files,
    }
    run_args.update(roster_lists(cfg, profile))
    recent = recent_work(cfg, run_args)
    if recent:
        run_args["goal"] = (run_args["goal"] + "\n\n" + recent).strip()
    learned = apply_learned_roster(state, run_args, cfg)
    for g in run_args["guidelines"]:
        if not os.path.isfile(os.path.join(root, g)):
            sys.exit(f"guidelines file not found: {g}")
    n = sum(len(st["units"]) for st in stages)
    if not stages:
        pending = ledger.get("_global", {}).get("status") == "pending"
        if args.global_only and run_args["priorAccepted"]:
            run_args["globalOnly"] = True
            print(f"global-only run: the global rounds over the {len(run_args['priorAccepted'])} accepted unit(s)")
        elif args.global_only:
            sys.exit("--global-only: no unit has been accepted yet, so there is nothing for the global rounds to judge")
        elif pending and not run_args["reviewOnly"] and not run_args["planOnly"] and not wanted_units and run_args["priorAccepted"]:
            run_args["globalOnly"] = True
            print("no unit needs revision, but the last global round did not approve the document: preparing a global-only run")
        else:
            print("nothing to do: no unit in scope needs work" + (f" (already accepted: {', '.join(skipped)}; use --include-accepted to redo them)" if skipped else ""))
            if wanted_units:
                unknown = sorted(wanted_units - set(ids) - set(ledger))
                if unknown:
                    print(f"unknown unit id(s): {', '.join(unknown)}")
            sys.exit(2)
    os.makedirs(state, exist_ok=True)
    ensure_gitignore(root, state)
    ensure_state_files(state)
    out = args.out or os.path.join(state, "run-args.json")
    per = per_unit_estimate(run_args)
    cap = max(1, int((run_args["limits"].get("maxAgents", 900) - 12) // per))
    for old in glob.glob(os.path.join(state, "run-args.shard-*.json")):
        os.remove(old)   # arguments of an earlier sharded plan must not be launched again
    want = args.shards if args.shards is not None else int(run_args["limits"].get("shards", 1) or 1)
    shards = shard_units(stages, want) if want > 1 and n and not run_args.get("globalOnly") else []
    if want > 1 and len(shards) < 2:
        print(f"--shards {want}: the units of this plan cannot be divided (one unit, or all of them share files); planning one run")
    if len(shards) > 1:
        at_once = agent_cap()
        wave = max(1, min(int(run_args["limits"].get("waveSize", 6)), at_once + 1))
        print(f"sharded plan: {len(shards)} workflows to launch at the same time, each with its own arguments; "
              f"a workflow runs about {at_once} agent(s) at once on this machine ({os.cpu_count()} CPUs), "
              f"so about {at_once * len(shards)} agents work in parallel")
        last = args.first_shard + len(shards) - 1
        for i, mine in enumerate(shards, args.first_shard):
            sargs = dict(run_args, stages=mine, shard={"index": i, "of": last},
                         limits=dict(run_args["limits"], waveSize=wave))
            path = os.path.join(state, f"run-args.shard-{i}.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(sargs, fh, indent=1)
            sids = [u["id"] for st in mine for u in st["units"]]
            runs = max(1, -(-len(sids) // cap))
            print(f"  shard {i}: {path}: {len(sids)} unit(s){f' (needs {runs} runs)' if runs > 1 else ''}: "
                  f"{', '.join(sids[:10])}{' ...' if len(sids) > 10 else ''}")
        print("shards run no global round: record every shard's result, then run prepare_run.py again for the "
              "units still open and the global rounds")
    else:
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(run_args, fh, indent=1)
        print(f"workflow arguments: {out}")
    print(f"workflow: {SKILL_DIR}/workflow/committee.js")
    print(f"committee size: {run_args['committeeSize']}: {len(run_args.get('readers', []))} reader(s) "
          f"({', '.join(r['key'] for r in run_args.get('readers', []))}), {len(run_args.get('reviewers', []))} lens(es) "
          f"({', '.join(r['key'] for r in run_args.get('reviewers', []))}), editors: "
          f"{', '.join(e['key'] for e in run_args.get('editors', [])) or 'none'}; at most {run_args['limits'].get('maxRounds', 5)} round(s) per unit")
    ladder = run_args["roster"].get("writerTiers") or DEFAULT_TIERS
    print(f"writer ladder ({len(ladder)} tier(s), one writer per unit and round): "
          + " -> ".join(t["model"] for t in ladder)
          + f"; effort: {run_args['effort'] or 'each role its own default (ask the user, then pass --effort)'}")
    print(f"publication type: {run_args['publicationType']}; bibliography: {', '.join(run_args['bibliography']) or 'none found'}; extra writing references: {', '.join(run_args['writingSkills']) or 'none'}")
    for st in stages:
        sids = [u["id"] for u in st["units"]]
        print(f"stage {st['id']}: {len(sids)} unit(s){' (scout will divide the scope)' if not sids else ''}: {', '.join(sids[:12])}{' ...' if len(sids) > 12 else ''}")
    resumed = [u["id"] for st in stages for u in st["units"] if u.get("actions")]
    if resumed:
        print(f"resuming from open actions: {', '.join(resumed)}")
    briefed_now = [u["id"] for st in stages for u in st["units"] if u.get("briefed")]
    if briefed_now:
        print(f"brief already written (the revision starts at the writer): {', '.join(briefed_now)}")
    if run_args["planOnly"]:
        print("plan-only run: first reading and developmental briefs; no file of the document is edited")
    if n and len(shards) < 2:
        print(f"~{per:.0f} agent calls per unit; about {cap} units fit in one workflow run; {n} unit(s) planned -> {max(1, -(-n // cap))} run(s)")
    elif n:
        print(f"~{per:.0f} agent calls per unit; {n} unit(s) planned")
    if skipped:
        print(f"skipped {len(skipped)} unit(s) already accepted (use --include-accepted to redo them); the global rounds still judge them")
    if learned:
        print(f"learned roster changes applied: {', '.join(learned)}")
    if run_args.get("modelCeiling"):
        c = run_args["modelCeiling"]
        print(f"model ceiling: {c['model']}" + (f" (except {', '.join(c['except'])})" if c["except"] else ""))
    if cfg.get("sharedFiles"):
        print(f"shared files (integration editor only): {', '.join(cfg['sharedFiles'])}")


def is_stalled(entry):
    return entry.get("status") != "accepted" and (entry.get("stalls", 0) >= 2 or entry.get("failures", 0) >= 2)


def guidelines_for(cfg, root):
    """The configured guideline files; without any, guidelines.md if it exists. With neither,
    the skill's writing guide and the publication-type section are the authority (an empty
    list tells the workflow so)."""
    if "guidelines" in cfg:
        return cfg["guidelines"]
    if os.path.isfile(os.path.join(root, "guidelines.md")):
        return ["guidelines.md"]
    if os.path.isfile(os.path.join(root, ".writing-committee", "guidelines.md")):
        return [".writing-committee/guidelines.md"]
    print("note: no guidelines file is configured and guidelines.md does not exist; the skill's writing "
          "guide and the publication-type section serve as the guidelines. Write venue or project rules "
          "into guidelines.md to add to them.")
    return []


def tier_index(tier, tiers=None):
    names = [f"{t['model']}/{t['effort']}" for t in (tiers or DEFAULT_TIERS)]
    return names.index(tier) if tier in names else None


def record(args):
    cfg, root, state = load_config(args.config)
    ledger = load_ledger(state)
    raw = open(args.record, "rb").read()
    res = json.loads(raw.decode("utf-8"))
    res = res.get("result", res)
    # A canonical form, so that the same result saved with other formatting counts once.
    digest = hashlib.sha256(json.dumps(res, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    done = ledger.setdefault("_recorded", [])
    if digest in done or hashlib.sha256(raw).hexdigest() in done:
        print(f"{args.record} was already recorded; nothing changed")
        status(args)
        return
    tiers = {**load_profile(cfg).get("roster", {}), **cfg.get("roster", {})}.get("writerTiers") or DEFAULT_TIERS
    top = len(tiers) - 1
    rounds = res.get("rounds", {})

    def tidx(uid, item=None):
        r = rounds.get(uid, {})
        for v in ((item or {}).get("tier_index"), r.get("tier_index"), tier_index(r.get("tier"), tiers)):
            if v is not None:
                return v
        return ledger.get(uid, {}).get("tier_index")

    if res.get("status") == "planned":
        for b in res.get("briefed", []):
            e = ledger.setdefault(b["id"], {})
            e["briefed"] = {"difficulty": b.get("difficulty", "standard"), "readers_r0": bool(b.get("readers_r0"))}
            e.setdefault("files", b.get("files", []))
            print(f"{b['id']}: briefed ({e['briefed']['difficulty']}); its revision starts at the writer")
        for f in res.get("failed", []):
            print(f"{f['id']}: no brief was produced; it is planned again by the next run")
    shard = res.get("shard") or {}
    if shard.get("index"):
        merged = merge_shard_state(state, shard["index"])
        if merged:
            print(f"shard {shard['index']} of {shard.get('of', '?')}: merged its {', '.join(merged)} into the committee's files")
    if res.get("status") == "reviewed":
        for rep in res.get("reports", []):
            e = ledger.setdefault(rep["id"], {})
            e["review"] = {"status": rep.get("status"), "report": rep.get("report"), "open": rep.get("open", [])}
            print(f"{rep['id']}: {rep.get('status')}; report {rep.get('report')}; {len(rep.get('open', []))} open item(s)")
    for unit in res.get("scouted", []):
        # A unit the Scout created: the next run resumes it from the ledger instead of scouting again.
        e = ledger.setdefault(unit["id"], {"status": "not_run"})
        e.update(stage=unit.get("stage"), goal=unit.get("goal", ""), difficulty=unit.get("difficulty", "standard"))
        e.setdefault("files", unit.get("files", []))
    for uid in res.get("accepted", []):
        e = ledger.setdefault(uid, {})
        e.update(status="accepted", open=[], actions=[], runs=e.get("runs", 0) + 1, tier=rounds.get(uid, {}).get("tier"),
                 tier_index=tidx(uid), stalls=0, failures=0, files=rounds.get(uid, {}).get("files", e.get("files")))
        e.pop("resume_status", None)
    for item in res.get("unresolved", []):
        uid = item["id"]
        e = ledger.setdefault(uid, {})
        ti = tidx(uid, item)
        st = item.get("status", "unresolved")
        e.update(status=st, open=item.get("open", []), actions=item.get("actions", []) or e.get("actions", []) if st == "failed"
                 else item.get("actions", []), runs=e.get("runs", 0) + 1,
                 tier=rounds.get(uid, {}).get("tier"), tier_index=ti, files=rounds.get(uid, {}).get("files", e.get("files")))
        e.pop("resume_status", None)
        if st == "unresolved" and ti is not None and ti >= top:
            e["stalls"] = e.get("stalls", 0) + 1  # unresolved at the strongest tier
        if st in ("failed", "not_run"):
            e["failures"] = e.get("failures", 0) + 1
    for uid in res.get("deferred", []) if res.get("status") not in ("reviewed", "planned") else []:
        e = ledger.setdefault(uid, {})
        if e.get("status") in ("unresolved", "reopened", "failed", "not_run"):
            e["resume_status"] = e["status"]   # keeps its open actions and tier for the next run
        if e.get("status") != "accepted":
            e["status"] = "deferred"
    if res.get("status") not in ("reviewed", "planned"):
        if res.get("global_pending", res.get("status") != "complete"):
            ledger["_global"] = {"status": "pending", "issues": res.get("remaining_issues", [])}
        else:
            ledger["_global"] = {"status": "approved"}
    adj = res.get("roster_adjustments") or []
    if adj:
        path = os.path.join(state, "roster.json")
        learned = json.load(open(path, encoding="utf-8")) if os.path.isfile(path) else {}
        for a in adj:
            learned[a["role"]] = {"model": a["model"], "effort": a["effort"], "reason": a.get("reason", "")}
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(learned, fh, indent=1, sort_keys=True)
        print(f"learned roster changes saved to {path}: {', '.join(a['role'] for a in adj)}")
    done.append(digest)
    save_ledger(state, ledger)
    with open(os.path.join(state, "last_result.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
    status(args)


def status(args):
    cfg, root, state = load_config(args.config)
    ledger = load_ledger(state)
    by, reviewed = {}, {}
    for uid, e in sorted(ledger.items()):
        if is_meta(uid):
            continue
        by.setdefault(e.get("status", "?"), []).append(uid)
        if e.get("review"):
            reviewed.setdefault(e["review"].get("status", "?"), []).append(uid)
    for k in ("accepted", "reopened", "unresolved", "failed", "not_run", "deferred"):
        if by.get(k):
            print(f"{k}: {len(by[k])}: {', '.join(by[k])}")
    waiting = [u for u, e in sorted(ledger.items()) if not is_meta(u) and e.get("briefed") and not e.get("status")]
    if waiting:
        print(f"briefed, waiting for their revision: {len(waiting)}: {', '.join(waiting)}")
    for k in ("reviewed-ready", "reviewed-needs-work", "failed"):
        if reviewed.get(k):
            print(f"review {k}: {len(reviewed[k])}: {', '.join(reviewed[k])}")
    g = ledger.get("_global")
    if g:
        print(f"global review of the whole document: {g.get('status')}")
        for i in g.get("issues", [])[:5]:
            print(f"  {i}")
    stalled = [u for u, e in ledger.items() if not is_meta(u) and is_stalled(e)]
    if stalled:
        print("NEEDS A HUMAN DECISION (unresolved twice at the strongest tier, or failed twice): " + ", ".join(stalled))
        for u in stalled:
            for o in ledger[u].get("open", [])[:5]:
                print(f"  {u}: {o}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("config")
    ap.add_argument("--stages")
    ap.add_argument("--units")
    ap.add_argument("--include-accepted", action="store_true")
    ap.add_argument("--include-stalled", action="store_true", help="plan stalled units again (after a human decision)")
    ap.add_argument("--rescout", action="store_true", help="scout scope stages again instead of resuming their units")
    ap.add_argument("--max-units", type=int)
    ap.add_argument("--review-only", action="store_true", help="one round of independent review with a report; no edits")
    ap.add_argument("--plan-only", action="store_true", help="first reading and developmental briefs only; no edits")
    ap.add_argument("--shards", type=int, help="divide the units among this many workflows that run at the same time")
    ap.add_argument("--first-shard", type=int, default=1, metavar="N",
                    help="number the shards from N, so that they do not share state files with shards still running")
    ap.add_argument("--global-only", action="store_true", help="only the global rounds, over the units accepted so far")
    ap.add_argument("--no-global", action="store_true", help="end after the units; the global rounds run in a later run")
    ap.add_argument("--out")
    ap.add_argument("--record")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--size", choices=["low", "medium", "high", "full"],
                    help="committee size for this run (overrides committeeSize in the configuration; default full)")
    ap.add_argument("--effort", choices=EFFORTS + ["default"],
                    help="effort level of every role except the mechanical checker and the committer (overrides "
                         "effort in the configuration; default: each role's own effort)")
    args = ap.parse_args()
    if args.record:
        record(args)
    elif args.status:
        status(args)
    else:
        prepare(args)


if __name__ == "__main__":
    main()
