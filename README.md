# Academic Writing Committee

**Academic writing for Claude that holds every sentence to the standard of a careful editor, and can put a whole committee of readers, reviewers and editors behind it when it matters.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Version 2.5.0](https://img.shields.io/badge/version-2.5.0-informational)
![Claude Code plugin](https://img.shields.io/badge/Claude%20Code-plugin%20%2B%20skill-8A63D2)
![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-3776AB)

`academic-writing-committee` is a Claude Code plugin and a standalone skill for planning, drafting, revising, reviewing and checking academic documents. It covers journal articles, conference papers, surveys, theses, books and book chapters, lecture notes, technical reports and grant proposals.

It works in two ways:

- **Without a committee**, it is a single-session writing assistant with a complete writing guide and two checkers. Use it to draft a section, tighten a paragraph, calibrate a claim, or audit a reference list.
- **With the committee**, it divides a document into units and runs a multi-agent workflow. Tiered writers revise each unit, reader personas and reviewer lenses judge every revision, a chair decides, and editors polish. An editor-in-chief signs off on the whole. The cycle repeats until everything is approved.

---

## Contents

- [Quick Start](#quick-start)
- [With or Without the Committee](#with-or-without-the-committee)
- [Commands](#commands)
- [Setup](#setup)
  - [1. Requirements](#1-requirements)
  - [2. Install](#2-install)
  - [3. Check the Installation](#3-check-the-installation)
  - [4. Set Up a Project for the Committee](#4-set-up-a-project-for-the-committee)
  - [5. Run the Committee Step by Step](#5-run-the-committee-step-by-step)
  - [6. What the Committee Keeps on Disk](#6-what-the-committee-keeps-on-disk)
  - [7. Long Documents, Cost and Troubleshooting](#7-long-documents-cost-and-troubleshooting)
- [What It Enforces](#what-it-enforces)
- [Recent Work from the Target Journal](#recent-work-from-the-target-journal)
- [How the Committee Works](#how-the-committee-works)
- [Publication Types and Committee Size](#publication-types-and-committee-size)
  - [Committee Modes: Low, Medium, High, Full](#committee-modes-low-medium-high-full)
  - [Effort](#effort)
- [The Checkers](#the-checkers)
- [Models and Cost](#models-and-cost)
- [Status](#status)
- [Repository Layout](#repository-layout)
- [Sources and License](#sources-and-license)

---

## Quick Start

**1. Install** the plugin in Claude Code. This repository is both the plugin and its marketplace:

```
/plugin marketplace add gacikgoz/academic-writing-committee
/plugin install academic-writing-committee@academic-writing-committee
```

**2. Start** from the root of your project:

```
/academic-writing-committee:start
```

or just say what you want ("help me get my paper ready for NeurIPS"). That is all you need to know. The skill looks at your project first and asks only what the project cannot tell it.

**What happens next:**

1. **It looks.** It finds the main document, its class and venue, whether it is a paper, a thesis or a book, the chapters, the bibliography, any guideline or venue-rules file, the build command, and a committee run already under way.
2. **It tells you what it found**, in a line or two: *"A NeurIPS paper, main.tex, refs.bib, built with latexmk; no guidelines file."*
3. **It asks the rest in one go**, as multiple-choice questions with a recommended answer:

   | Question | Asked when |
   |---|---|
   | What should I do: revise with a committee, revise here without one, review only, or check references and language? | the request does not say |
   | What kind of document is this? | the type is uncertain |
   | Which journal is it for? | a journal article whose source does not name the journal |
   | What should the revision achieve? | always, for a whole document |
   | Are there rules the text must follow? | no guidelines file was found |
   | How large should the committee be, and at what effort? | for a committee |

4. **It does the work.** It edits, reviews or checks in your session, or writes the committee's configuration, checks that the build works, tells you the plan in three lines and launches the committee.

For a journal article it also adds **two or three related works the target journal published in the last six months** ([Recent Work from the Target Journal](#recent-work-from-the-target-journal)).

A sentence, a paragraph or a section needs none of this: ask, and it is done at once. Run `/academic-writing-committee:start` again later and it continues the run already under way instead of starting over.

---

## With or Without the Committee

| | No committee | Committee |
|---|---|---|
| **How to choose it** | answer "revise here" when `start` asks; or `--no-committee`, "no committee" in the request, or the `no-committee` command; automatic when the Workflow tool is not available | answer "revise with a committee" when `start` asks; or the `committee` or `review` command |
| **Who does the work** | Claude, in your session | a Workflow of specialized agents |
| **Best for** | a section, a paper you are actively editing, a quick review, a citation audit | a whole paper, thesis or book brought up to a set of guidelines |
| **Review** | one careful review by severity, no edits | parallel reader personas and reviewer lenses, consolidated by a chair |
| **Revision of a whole document** | unit by unit in reading order, with both checkers and the build after each unit | tiered writers, independent judgment each round, escalation, editors, a regression check |
| **Setup** | none | written for you by `start` from the project and your answers ([Setup](#setup)) |
| **Cost** | one session | about 14 to 28 agent calls per unit, by [mode](#committee-modes-low-medium-high-full) and type |

The writing guide, the standards and the checkers are the same in both. The committee adds independent judgment, escalation and memory across runs.

---

## Commands

You rarely need more than `start`. The other commands go straight to one mode. The standalone skill does everything they do when you ask in plain words.

| Command | What it does |
|---|---|
| `/academic-writing-committee:start [what you want] [file or folder]` | **Start here.** Looks at the project, asks only what it cannot find out, and runs the right mode. Continues a committee run already under way. |
| `/academic-writing-committee:write [file or topic] [type] [instructions]` | Writes or revises text to the standard of the guide, then runs both checkers on what changed. Always a single session. |
| `/academic-writing-committee:review [--no-committee \| --size low\|medium\|high\|full] [--effort low\|medium\|high\|xhigh\|max] [main file] [type] [venue]` | Reviews a document without changing it. Readers and reviewer lenses work in parallel and a chair writes a prioritized report. With `--no-committee`, Claude reviews it alone. |
| `/academic-writing-committee:committee [--no-committee \| --size low\|medium\|high\|full] [--effort low\|medium\|high\|xhigh\|max] [configuration] [stages or units]` | Runs the committee until every unit and the whole document are approved, or until a unit needs your decision. `--size` picks the [committee mode](#committee-modes-low-medium-high-full) and `--effort` the [effort](#effort); Claude asks for the effort if you give none. With `--no-committee`, Claude revises the document unit by unit in one session. |
| `/academic-writing-committee:check [files] [bibliography]` | Runs the manuscript and citation checkers and proposes fixes. Always a single session. |
| `/academic-writing-committee:no-committee [write \| review \| check \| revise] [file or topic] [type] [instructions]` | Plain academic writing in any mode, in one session, with no subagents. |

A committee run is a multi-agent run, so invoking `review` or `committee` without `--no-committee` counts as your agreement to one. Claude states the plan and the expected number of agents before it launches anything.

---

## Setup

### 1. Requirements

| You need | For |
|---|---|
| **Claude Code**, or another agent that loads `SKILL.md` skills | everything |
| **Python 3.9 or later** (standard library only, nothing to `pip install`) | the checkers and `prepare_run.py` |
| **The Workflow tool** in Claude Code | committee runs and committee reviews; without it the skill switches to the no-committee option |
| **The models** Fable, Opus, Sonnet and Haiku, or overrides for any you lack ([§7](#7-long-documents-cost-and-troubleshooting)) | committee runs |
| **git**, with the project in a repository | committee runs, which commit after each wave |
| **Your build tools** (for example `latexmk` or `pandoc`) | the build checks you configure |
| **Network access** to `api.crossref.org`, `export.arxiv.org`, `doi.org` and `api.datacite.org` | online reference verification (optional) |

### 2. Install

**As a plugin (Claude Code, with the commands):**

```
/plugin marketplace add gacikgoz/academic-writing-committee
/plugin install academic-writing-committee@academic-writing-committee
```

- **Update:** `/plugin marketplace update academic-writing-committee`
- **From a local clone:** `claude --plugin-dir path/to/academic-writing-committee`
- **Earlier installs:** if you installed `academic-writing` or `academic-writing-committee@gacikgoz-plugins` from the `gacikgoz/aibook` marketplace, uninstall it first, so that only one copy of the skill competes for selection.

**As a standalone skill (no plugin):** the folder [`skills/academic-writing-committee/`](skills/academic-writing-committee/) works on its own. Every path in it is relative to the folder.

| Where | How |
|---|---|
| Claude Code, every project | `cp -r skills/academic-writing-committee ~/.claude/skills/` |
| Claude Code, one project | `cp -r skills/academic-writing-committee <project>/.claude/skills/` |
| claude.ai and other hosts that accept skill uploads | run `./package-skill.sh` and upload `dist/academic-writing-committee.zip` |
| Other agents that read `SKILL.md` skills | place the folder where the agent looks for skills, or point it at `SKILL.md` |

The standalone skill has every mode; only the slash commands come with the plugin.

### 3. Check the Installation

With the plugin, `/plugin` should show `academic-writing-committee` as installed, and typing `/academic-writing-committee:` should offer the six commands. With the standalone skill, ask Claude "Which skills can you use?" and look for `academic-writing-committee`.

The scripts run without Claude, so they are a quick test of Python and of the network:

```bash
S=skills/academic-writing-committee/scripts   # or ~/.claude/skills/academic-writing-committee/scripts
python3 $S/check_manuscript.py --list-rules
python3 $S/check_manuscript.py your-draft.md
python3 $S/check_citations.py your-draft.tex --bib refs.bib --online
```

If `--online` reports network errors, the checker still runs offline without the flag; for committee runs, set `"onlineCitations": false` (see [§7](#7-long-documents-cost-and-troubleshooting)).

### 4. Set Up a Project for the Committee

**You do not have to do this by hand.** `/academic-writing-committee:start` detects what it can, asks you the rest and writes the configuration. This section is for when you want to see, check or adjust what it does.

The committee needs a git repository, a configuration file and, ideally, a guidelines file. The detection and the configuration come from one script, which you can also run yourself:

```bash
S=skills/academic-writing-committee/scripts
python3 $S/project_setup.py detect            # what the project says, and what is still open
python3 $S/project_setup.py init --type conference-paper --size high --effort high \
  --goal "Ready for submission to NeurIPS"    # writes writing-committee.json
```

`detect` changes nothing. It finds:
- the main document, its class, title and venue;
- the publication type, with its confidence;
- the chapters, the bibliography or reference list, and the guideline and context files (earlier reviews, a notation table, a roadmap);
- the build command and the installed tools;
- the git state, and an existing configuration with its ledger.

`init` writes the configuration from what was detected and your answers. It never overwrites an existing one without `--force`.

To write or adjust the files yourself:

**a. Write the guidelines.** The guidelines are the committee's authority: the venue's author instructions, a house style, or your own rules (page limit, citation style, required sections, terms to use). Put them in a Markdown file such as `guidelines.md` or `venue-rules.md`. Number the rules if you can, so that reviews can cite them. Without a guidelines file, the skill's writing guide serves as the guidelines.

**b. Write `writing-committee.json`** at the root of the project. For a paper judged as a whole:

```json
{
  "name": "Robust Retrieval Under Distribution Shift",
  "publicationType": "conference-paper",
  "committeeSize": "high",
  "effort": "high",
  "goal": "Make the paper ready for submission.",
  "guidelines": ["venue-rules.md"],
  "documents": ["paper.tex"],
  "bibliography": "references.bib",
  "checks": {
    "unit": "latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=.writing-committee/build/{unit} {main}",
    "global": ["latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=.writing-committee/build/full paper.tex"]
  },
  "commit": { "perWave": true, "push": false }
}
```

For a book, thesis or lecture notes, use `stages` instead of `documents`. Each stage's `unitsFrom` glob makes one unit per chapter, for example `"glob": "chapters/*.tex"` with `"orderFrom": "main.tex"`. [`templates/book.example.json`](skills/academic-writing-committee/templates/book.example.json) is a complete example.

The fields you will use most:

| Field | What it sets |
|---|---|
| `publicationType` | **Required.** One of the [nine profiles](#choosing-the-type); it chooses the readers, reviewer lenses, editors and limits. |
| `committeeSize` | `low`, `medium`, `high` or `full` (default): how large the committee is ([Committee Modes](#committee-modes-low-medium-high-full)). `--size` overrides it for one run. |
| `effort` | `low`, `medium`, `high`, `xhigh`, `max` or `default`: the effort of every role ([Effort](#effort)). Claude asks for it if it is missing; `--effort` overrides it for one run. |
| `recentWork` | the target journal, for [recent related work](#recent-work-from-the-target-journal); set for you when the journal is known. |
| `goal` | What the whole effort must achieve. Every agent reads it, so state your priorities here (for example "keep the author's text; change a paragraph only where a rule requires it"). |
| `guidelines`, `context` | Your rule files, and other files every agent should know (notation table, roadmap, earlier reviews). |
| `documents` or `stages` | What is revised, as whole documents or as units per stage. |
| `bibliography`, `referenceList` | A `.bib` or CSL JSON file, or a free-form reference list, checked in every round. |
| `sharedFiles` | Files no unit may own (main file, preamble, shared bibliography); only the Integration Editor changes them. |
| `checks.unit`, `checks.global` | Your build commands. `{unit}`, `{main}`, `{files}`, `{bib}` and `{skill}` are filled in. A unit check must be safe to run in parallel, so build into a directory named after `{unit}`. |
| `dropReaders`, `dropReviewers`, `addReviewers` | Remove or add personas and lenses by key, for example `"dropReviewers": ["experiments"]` for a paper without experiments. |
| `roster`, `modelCeiling` | Models and efforts per role, or one model as the ceiling for every role. |
| `limits` | `maxRounds`, `maxGlobalRounds`, `waveSize`, `maxAgents` and `shards`. |
| `commit` | `perWave`, `push`, and the remote `branch` to push to. |

Every field is documented in [`committee/config.md`](skills/academic-writing-committee/committee/config.md). The committee adds both checkers to your unit and global checks by itself, so do not list them.

**c. Run the preflight yourself once.** Commit or stash your own changes, so that the committee starts from a clean working tree. Run your unit check on one unit and your global check once; with LaTeX, a full build first also lets unit checks resolve references to the rest of the document. Fix a broken check command before any agent runs: every round depends on it.

### 5. Run the Committee Step by Step

The `start` and `committee` commands do all of this for you. These are the steps it takes, for when you want to drive or inspect a run yourself (`S` is the skill's `scripts/` folder):

1. **Preview the plan.** This writes the workflow arguments to `.writing-committee/run-args.json` and prints the units, their order and the estimated number of agent calls:
   ```bash
   python3 $S/prepare_run.py writing-committee.json
   python3 $S/prepare_run.py writing-committee.json --stages chapters --units ch03,ch04
   ```
2. **Launch.** Ask Claude to run the committee, or to launch `workflow/committee.js` with the Workflow tool and the arguments in `run-args.json`. Watch the run with `/workflows`. It runs in the background, and Claude is notified when it ends.
3. **Record the result.** Claude saves the workflow's result and merges it into the ledger:
   ```bash
   python3 $S/prepare_run.py writing-committee.json --record .writing-committee/result-1.json
   ```
4. **Check the state** at any time:
   ```bash
   python3 $S/prepare_run.py writing-committee.json --status
   ```
5. **Continue.** Run `prepare_run.py` again; it plans only what is still open. Unresolved units resume from their open actions, one writer tier higher. When every unit is accepted, a `--global-only` run judges the whole document, and the Editor-in-Chief approves it or reopens units.
6. **Decide where needed.** A unit that stays unresolved at the strongest tier, or fails twice, is listed under "NEEDS A HUMAN DECISION". Read its open actions, decide, then plan it again with `--include-stalled`.
7. **Read the proposals.** `.writing-committee/guideline_proposals.md` collects gaps the committee found in your guidelines. The committee never edits the guidelines; you decide.

Other useful options:

| Option | Use |
|---|---|
| `--review-only` | One round of independent review with a report, and no edits. |
| `--plan-only` | Only the first reading and the developmental briefs; it edits nothing, so it can run beside other work. |
| `--shards K` | Divide the units among K workflows that run side by side ([§7](#7-long-documents-cost-and-troubleshooting)). |
| `--no-global`, `--global-only` | Leave the whole-document rounds to a later run, or run only those rounds. |
| `--max-units N` | Plan at most N units in this run. |

### 6. What the Committee Keeps on Disk

Everything lives in the state directory, `.writing-committee/` by default (`stateDir` in the configuration). `prepare_run.py` adds the working files to `.gitignore` on its first run.

| Path | What it holds | In git |
|---|---|---|
| `ledger.json` | the state of every unit: accepted, open actions, writer tier, rounds | yes |
| `lessons.md`, `lint_rules.md` | what the committee learned; every later agent reads them | yes |
| `guideline_proposals.md` | proposed changes to your guidelines, for you to decide | yes |
| `roster.json` | learned model changes (only when `adaptRoster` is on) | yes |
| `units/<unit>/` | briefs, reader, reviewer and chair reports, writer change reports | no |
| `build/` | private build directories for unit and global checks | no |
| `run-args*.json`, `result-*.json` | the arguments and results of runs | no |
| `citations-cache.json` | the cache of online reference lookups | no |

Keep the ledger and the lessons in git: they are how the next run, or the next person, continues. The reports in `units/` can be large; archive them if you need to keep them.

### 7. Long Documents, Cost and Troubleshooting

**More agents at once.** A single workflow runs only a few agents at a time: min(16, CPUs − 2), which is 2 on a 4-CPU machine. For a long document, `--shards K` divides the units among K workflows, each committing only its own files. Record every shard when it ends, then prepare once more for the units still open and for the global rounds. Builds set the limit, not agents: give a full-document build a CPU of its own.

**Many parallel LaTeX builds.** Each XeLaTeX or LuaLaTeX run can take a few hundred megabytes. With many shards, cap the concurrent runs with a small wrapper in front of the real binary, for example:

```bash
#!/bin/bash
# /usr/local/bin/xelatex: at most N XeLaTeX runs at a time
N=${XELATEX_SLOTS:-8}; REAL=/usr/bin/xelatex
while true; do
  for i in $(seq 1 "$N"); do
    exec 9>"/tmp/xelatex-slot-$i.lock"
    if flock -n 9; then "$REAL" "$@"; exit $?; fi
    exec 9>&-
  done
  sleep 2
done
```

**A cheaper run.** Choose a smaller [committee mode](#committee-modes-low-medium-high-full): `"committeeSize": "medium"` in the configuration, or `--size medium` for one run. Medium keeps one reader, three lenses and the line editor, caps the rounds at 3 and keeps every role at Opus or below, the Editor-in-Chief included. That is about 18 agent calls per unit, against 24 to 28 with `full`. `low` goes down to about 14. A lower [effort](#effort) cuts the tokens each call uses.

**Troubleshooting:**

| Symptom | What to do |
|---|---|
| The committee does not start, or Claude revises alone | The Workflow tool is not available in this session, so the skill fell back to the no-committee option. Use a Claude Code session with the Workflow tool, or keep working without a committee. |
| A model of the roster is not available | Set `modelCeiling`, or override the roles in `roster` and the `model` of each reader, reviewer and editor ([`committee/models.md`](skills/academic-writing-committee/committee/models.md)). |
| `prepare_run.py` exits with status 2 | There is nothing to do: every unit in scope is accepted. Use `--global-only` for the whole-document rounds, or `--include-accepted` to revise again. |
| A run stopped part-way | Relaunch it with the same arguments and `resumeFromRunId`, so that finished agents replay from the cache. If the session itself was lost, `prepare_run.py` rebuilds the plan from the ledger and the committed files. |
| No network, or online lookups time out | Set `"onlineCitations": false`. The references lens then verifies by search and reports what it cannot confirm. |
| Unit checks fail on references to other units | Run a full build first, so that unit builds can resolve those references, or say in `checks.notes` how your build resolves them. |
| Memory runs out during builds | Fewer shards, or a wrapper that caps concurrent builds (above). |

The full procedure is in [`committee/procedure.md`](skills/academic-writing-committee/committee/procedure.md).

---

## What It Enforces

The guide rests on twelve principles and four standards that reviewers raise again and again. In short:

- **Accuracy before fluency.** Observation, estimate, interpretation and speculation stay distinct. A fluent sentence is not evidence.
- **Nothing invented.** No guessed citations, numbers, quotations, dates or methods. A missing fact becomes a visible `[[TODO: ...]]`, never plausible filler.
- **Calibrated claims.** Verbs match the evidence: association is not cause, and "the first" needs a documented search. Overclaiming and underselling are both errors. The contributions, experiments, results, discussion and conclusion must agree with one another.
- **Real references.** Every cited work exists, has been opened, and supports the sentence that cites it. A real work cited for something it does not say counts as seriously as a fake one.
- **Clean language.** By default no en or em dash in prose, captions or tables, only the hyphens that are needed, no comma right after a conjunction or connective, no paragraph that opens with *To*, and every abbreviation written out at first use in the body and none in the abstract; a project's guidelines may relax these house rules. Chains of *and*, repeated words and openings, formulaic transitions and stacked hedges go.
- **Titles the author approves.** A title is short and striking (*Name: what it does for whom*), leads with the method and the contribution, names the domain, uses no abbreviations, and claims nothing the evidence does not carry. The committee proposes three to five candidates and writes none into any file until the author approves one.
- **The author's voice.** Text is edited, not replaced. Terminology and claims stay unless they are the problem, and every substantive change comes with its reason.
- **Project rules first.** The venue's instructions and the project's own guidelines outrank the field's conventions, which outrank the skill.

---

## Recent Work from the Target Journal

Editors and reviewers expect a submission to know what their journal has published lately. For a journal article, the skill adds **two or three related works that the target journal published in the last six months** to the related-work section, with or without a committee.

- **The journal** is read from the source (`\journal{...}` in `elsarticle`, `\journalname{...}` in Springer's class, `journal:` in Markdown front matter), or asked once when it is missing.
- **The candidates** come from Crossref: the journal's articles of the last six months, ranked by how well they match the manuscript's title and abstract.
- **Each one is read before it is cited.** Only works on the same problem, method or data are kept. Their BibTeX comes from doi.org, never from memory. Each gets one or two sentences that say what it does and how the manuscript relates to it.
- **Nothing is padded.** If fewer than two are really related, only those are added, and the report says why.

You can run the search yourself:

```bash
python3 skills/academic-writing-committee/scripts/venue_recent.py --venue "Pattern Recognition" --from main.tex
python3 skills/academic-writing-committee/scripts/venue_recent.py --bibtex 10.1016/j.patcog.2025.113013
```

In the configuration, this is the `recentWork` field: `{"venue": "Pattern Recognition", "months": 6, "count": [2, 3]}`. Set `months` to look further back, `issn` when the journal's name is ambiguous, or leave the field out (`project_setup.py init --no-recent`) to skip the step. Conference proceedings are not covered by the script; for a conference paper, ask for it and the skill searches the venue's recent proceedings instead.

---

## How the Committee Works

```
           guidelines + venue rules + writing guide + lessons learned
                                   │
  Scout ─► units ─► Readers ─► Developmental Editor ─► brief for each unit
                                   │
        ┌──────────────── each round, up to a limit ─────────────────┐
        │  Writer (tiered: Sonnet → Opus → Fable)                     │
        │    ├─► Mechanical Checker: build, manuscript, citations     │
        │    ├─► Reader personas, in parallel                         │
        │    ├─► Reviewer lenses, in parallel                         │
        │    └─► Committee Chair: verify, decide, escalate, learn     │
        └──── revise ◄── actions                    accept ───────────┘
                                                      │
                 Line and Consistency Editors ─► Regression Checker
                                                      │
   whole document: global checks ─► Integration Editor ─► cross-unit claims review
                                ─► Editor-in-Chief: approve, or reopen units
```

- **Units never collide.** Units that run in parallel never share a file. Shared files change only through the Integration Editor, who works alone.
- **Writers escalate.** A unit that keeps failing moves to a stronger writer. A unit still unresolved at the strongest tier stops and asks you.
- **The committee learns.** Recurring problems become lessons and lint rules that every later agent reads. Gaps in your guidelines become proposals for you.
- **Edits stay safe.** Editors only reword, and a regression check after acceptance rejects any new or changed claim.
- **Runs resume.** The ledger records every unit's state, so an interrupted run picks up from the open actions.

The role contracts are in [`committee/roles.md`](skills/academic-writing-committee/committee/roles.md), and the severity scale and acceptance gates in [`committee/quality-gates.md`](skills/academic-writing-committee/committee/quality-gates.md).

---

## Publication Types and Committee Size

Set the type with `publicationType` in the configuration. The type decides who judges the document, how it is divided into units, and how large the committee is. Choose the nearest type and adjust it with `addReviewers`, `dropReviewers` and the like.

### Choosing the Type

| Type (`publicationType`) | Also use it for | Judged by | Central question |
|---|---|---|---|
| Journal article (`journal-article`) | research articles, letters | editor and reviewers | Is it sound, new and complete? |
| Conference paper (`conference-paper`) | full, short and workshop papers | program committee | Is the contribution clear and convincing within the page limit? |
| Survey (`survey`) | systematic reviews, tutorials | editor and reviewers | Is the coverage complete, organized and accurate? |
| Thesis (`thesis`) | dissertations | examiners | Is it original, substantiated and coherent? |
| Book (`book`) | textbooks, monographs | publisher, reviewers, adopters | Does it teach or argue cumulatively? |
| Book chapter (`book-chapter`) | chapters in edited volumes | volume editors | Is it self-contained and authoritative? |
| Lecture notes (`lecture-notes`) | course notes | students and instructor | Can a student learn from them alone? |
| Technical report (`technical-report`) | white papers | practitioners | Is it accurate and actionable? |
| Grant proposal (`grant-proposal`) | resubmissions | review panel | Is it significant, new and feasible? |

[`references/publication-types.md`](skills/academic-writing-committee/references/publication-types.md) gives each type's readers, structure, length, typical failures and committee setup.

### Who Sits on the Committee

| Type | Unit of work | Writer starts at | Readers | Reviewer lenses |
|---|---|---|---|---|
| Journal article | whole document | hard (Opus) | expert, adjacent-field reader | technical, claims, experiments, significance, references, presentation, language, venue |
| Conference paper | whole document | hard (Opus) | program-committee reviewer, expert, skimmer | technical, claims, experiments, significance, references, presentation, language, venue |
| Survey | whole document | hard (Opus) | newcomer, expert, practitioner | coverage, claims, references, technical, presentation, language, venue |
| Thesis | chapter | hard (Opus) | examiner, expert, generalist | guidelines, technical, claims, experiments, references, presentation, language |
| Book | chapter | standard (Sonnet) | newcomer, expert, chapter skimmer | guidelines, technical, claims, pedagogy, presentation, references, language |
| Book chapter | whole document | hard (Opus) | newcomer, expert | guidelines, technical, claims, references, presentation, language |
| Lecture notes | chapter | standard (Sonnet) | newcomer, chapter skimmer | technical, pedagogy, presentation, language, references |
| Technical report | whole document | standard (Sonnet) | practitioner, expert | technical, claims, references, presentation, language |
| Grant proposal | whole document | hard (Opus) | panel generalist, specialist | venue, significance, feasibility, claims, references, language |

Every committee also has these roles, whatever the type:

- **For each unit:** a developmental editor, who writes the brief; the writer; a mechanical checker; the committee chair; the line and consistency editors; and a regression checker.
- **For the whole document:** an integration editor, an editor-in-chief, a retrospective analyst and a committer. A document with several units also gets a cross-unit claims review in every global round, and a stage without fixed units gets a scout to divide it.

A unit can be marked `standard`, `hard` or `critical` in the configuration. Critical units start their writer, brief, chair and technical lens on Fable.

### Committee Modes: Low, Medium, High, Full

The committee runs in four sizes. Choose one with `committeeSize` in the configuration, with `--size` on the `committee` and `review` commands, or in words ("run a medium committee on paper.tex"). The default is `full`.

| Mode | Readers | Lenses | Editors | Writer ladder | Rounds per unit (max) | Global rounds | Models | Agent calls per unit | Review only | Use it for |
|---|---|---|---|---|---|---|---|---|---|---|
| `low` | 1 | 2 | line | 2 tiers: Sonnet → Sonnet⁺ | 2 | 1 | every role on Sonnet or below | ~14 | ~6 | drafts, quick passes, many units on a tight budget |
| `medium` | 1 | 3 | line | 3 tiers: Sonnet → Opus → Opus⁺ | 3 | 1 | every role on Opus or below, the Editor-in-Chief included | ~18 | ~7 | long documents where writing comes first |
| `high` | 2 | 5 | line, consistency | 4 tiers: Sonnet → Opus → Fable → Fable⁺ | 4 | 2 | default roster | ~24 | ~10 | most final revisions |
| `full` | all of the profile | all of the profile | line, consistency | 4 tiers: Sonnet → Opus → Fable → Fable⁺ | 5 or 6 | 2 | default roster | ~24 to 28 | ~10 to 14 | submissions and defenses where every lens counts |

⁺ The last tier runs one effort level higher than the others, so escalating to it still adds effort when the model stays the same.

**Writers.** Each unit has one writer per round, so a unit makes at most as many writer calls as its round limit (plus a repair if a check fails after acceptance). The writer starts on the tier the unit's difficulty sets: `standard` on the first, `hard` on the second, `critical` on the third, never past the last. It climbs one tier when the chair asks for it or the same problems repeat for two rounds. A unit still unresolved on the last tier stops and asks you. How many writers work at the same moment depends on the wave size of the type (4 units for whole-document types, 6 for chapter types) and on how many agents the machine runs at once ([§7](#7-long-documents-cost-and-troubleshooting)).

- **Readers** are kept in the profile's order, so `low` and `medium` keep the type's main reader: the newcomer for a book, the program-committee reviewer for a conference paper, the examiner for a thesis.
- **Lenses** are kept in order of how expensive the errors they catch are: technical, guidelines, references, claims, experiments, venue, and then the rest. A survey starts with coverage, a grant proposal with significance and feasibility, lecture notes with technical and pedagogy.
- **The smaller modes** skip the readers' first reading before the brief (`readBeforeBrief` off), so readers start with the first revision, and they keep the roster fixed (`adaptRoster` off).
- **Lecture notes and technical reports** have only two readers and five lenses, so `high` gives them the same committee as `full`, with a lower round limit.
- **Anything you set explicitly wins.** A `medium` committee with `"addReviewers": ["language"]` has four lenses, `"limits": {"maxRounds": 5}` gives it five rounds, and `roster.writerTiers` replaces its writer ladder.

Which personas and lenses each mode keeps, for every type:

| Type | `low` | `medium` | `high` |
|---|---|---|---|
| Journal article | expert · technical, references | expert · technical, references, claims | expert, adjacent · technical, references, claims, experiments, venue |
| Conference paper | PC reviewer · technical, references | PC reviewer · technical, references, claims | PC reviewer, expert · technical, references, claims, experiments, venue |
| Survey | newcomer · coverage, references | newcomer · coverage, references, claims | newcomer, expert · coverage, references, claims, technical, venue |
| Thesis | examiner · technical, guidelines | examiner · technical, guidelines, references | examiner, expert · technical, guidelines, references, claims, experiments |
| Book | newcomer · technical, guidelines | newcomer · technical, guidelines, references | newcomer, expert · technical, guidelines, references, claims, pedagogy |
| Book chapter | newcomer · technical, guidelines | newcomer · technical, guidelines, references | newcomer, expert · technical, guidelines, references, claims, presentation |
| Lecture notes | newcomer · technical, pedagogy | newcomer · technical, pedagogy, references | newcomer, chapter skimmer · technical, pedagogy, references, presentation, language |
| Technical report | practitioner · technical, references | practitioner · technical, references, claims | practitioner, expert · technical, references, claims, presentation, language |
| Grant proposal | generalist · significance, feasibility | generalist · significance, feasibility, venue | generalist, specialist · significance, feasibility, venue, claims, references |

The modes are defined in [`committee/sizes.json`](skills/academic-writing-committee/committee/sizes.json); edit it to change them for every project.

### Effort

Before the first committee run, Claude asks you which **effort level** the committee should work at, unless you already gave one. Answer in words, pass `--effort` to the `committee` or `review` command, or set `effort` in the configuration. Claude never picks one for you.

| Effort | What it means |
|---|---|
| `low` | quick, shallow passes; cheapest |
| `medium` | careful enough for drafts and routine sections |
| `high` | careful work on every role; recommended for most revisions |
| `xhigh` | deeper reasoning on every role, for hard mathematics, proofs and dense arguments |
| `max` | the most thorough and the most expensive; for a short, critical document |
| `default` | each role keeps its own effort from the profile (for example the chair at high, the line editor at high, the consistency editor at medium) |

- The level applies to every role except the mechanical checker and the committer, which stay at `low`: running a build and reading its log needs no deliberation.
- The last writer tier runs one level higher (`high` gives the last writer `xhigh`).
- Effort and mode are independent: a `medium` committee at `xhigh` has few members who think hard, and a `full` committee at `medium` has many members who work quickly. More effort means more tokens and slower runs, not more agent calls.

### Committee Size

These are the sizes of the `full` mode, the default. The [smaller modes](#committee-modes-low-medium-high-full) scale them down.

| Type | Readers | Lenses | Editors | Members per unit | Rounds per unit (max) | Units at once (wave) | Agent calls per unit | Review only |
|---|---|---|---|---|---|---|---|---|
| Journal article | 2 | 8 | 2 | 17 | 6 | 4 | ~26 | ~13 |
| Conference paper | 3 | 8 | 2 | 18 | 6 | 4 | ~28 | ~14 |
| Survey | 3 | 7 | 2 | 17 | 6 | 4 | ~28 | ~13 |
| Thesis | 3 | 7 | 2 | 17 | 5 | 6 | ~28 | ~13 |
| Book | 3 | 7 | 2 | 17 | 5 | 6 | ~28 | ~13 |
| Book chapter | 2 | 6 | 2 | 15 | 6 | 4 | ~24 | ~11 |
| Lecture notes | 2 | 5 | 2 | 14 | 5 | 6 | ~24 | ~10 |
| Technical report | 2 | 5 | 2 | 14 | 6 | 4 | ~24 | ~10 |
| Grant proposal | 2 | 6 | 2 | 15 | 6 | 4 | ~24 | ~11 |

- **Members per unit** counts the readers, the lenses, the two editors, and the five fixed roles of each unit (developmental editor, writer, mechanical checker, chair, regression checker).
- **Agent calls per unit** is the estimate `prepare_run.py` prints for each type with its default roster. It assumes 2.5 rounds on average, with only the readers and lenses whose concerns remain looking again after the first round. A unit that needs every round costs more, and the global rounds add a few calls for the whole document. A run stops planning new units at about 900 calls (`limits.maxAgents`) and leaves the rest to the next run.
- **Review only** is one round with no edits (`--review-only`): the readers, the lenses, the chair and the report.
- **Whole-document types** get more lenses because there is only one unit. **Chapter types** keep a focused set per chapter, and the integration editor and editor-in-chief look after the whole.

The full catalog of personas and lenses is [`committee/catalog.json`](skills/academic-writing-committee/committee/catalog.json), and the profiles are in [`profiles/`](skills/academic-writing-committee/profiles/).

---

## The Checkers

Two read-only Python scripts with no dependencies beyond the standard library. Both work without Claude, and both exit with status 1 when they report an error.

```bash
S=skills/academic-writing-committee/scripts

# Prose mechanics and claim wording in Markdown, LaTeX or plain text
python3 $S/check_manuscript.py paper.tex
python3 $S/check_manuscript.py chapters/*.tex --min-severity warning

# Citation keys and BibTeX or CSL JSON entries, verified online
python3 $S/check_citations.py paper.tex --bib refs.bib --online --cache refs-cache.json

# A free-form reference list, without a bibliography database
python3 $S/check_citations.py --reference-list references.tex --online
```

- **`check_manuscript.py`** flags the house rules (any en or em dash in prose, captions or tables; a comma right after a conjunction or connective; a paragraph that opens with *To*; an abbreviation used before it is written out, or used in the abstract), the title style (an abbreviation in the title, a title over 15 words), dash and hyphen misuse, chains of *and*, repeated words, phrases and sentence openings, stacked hedges, overclaiming and underselling words, formulaic phrasing, very long sentences, and references to unknown labels. Run `--list-rules` to see every rule, and `--disable RULE` or `--allow-terms` to tune it.
- **`check_citations.py`** finds cited keys missing from the bibliography, entries never cited, duplicates, missing fields and malformed identifiers. With `--online` it looks every reference up at Crossref, arXiv, doi.org and DataCite. It reports identifiers that do not exist (`NOT_FOUND`) and records whose metadata do not match (`METADATA_MISMATCH`). With `--ledger sources.csv` it compares the cited keys with a source ledger.

Both reports list candidates for a person to judge. A clean report proves nothing, and the checker cannot tell whether a work supports the sentence that cites it, so open each reference.

---

## Models and Cost

The committee gives each task enough capability and no more. The defaults:

| Work | Model |
|---|---|
| Mechanical checks, commits, skimming reader | Haiku |
| Most readers and reviewer lenses, standard writers, line and consistency editors | Sonnet |
| Briefs, hard writers, the chair, the technical and claims lenses, the integration editor | Opus |
| Critical units, escalated writers, the editor-in-chief (in the `high` and `full` modes) | Fable |

A unit costs about 24 to 28 agent calls in the default `full` mode, depending on the type ([Committee Size](#committee-size)), and a run is capped at about 900. The smaller [modes](#committee-modes-low-medium-high-full) bring it to about 24 (`high`), 18 (`medium`) or 14 (`low`). `prepare_run.py` prints its estimate before anything starts. Defaults, escalation paths and the reasoning behind them are in [`committee/models.md`](skills/academic-writing-committee/committee/models.md).

---

## Status

Version 2.5.0. The writing guide, the checkers, the guided start, the recent-work search, the no-committee option, the four committee modes and the effort setting are complete. The committee has run end to end on a small sample project. It is also being used, with a lean roster close to the `medium` mode, to revise a textbook of more than 4,000 pages; that revision is still in progress. Expect the committee's procedure and defaults to keep changing as that work teaches them.

**New in 2.5.0.** House rules on dashes, hyphens, conjunction commas, paragraph openings and abbreviations (`references/language-mechanics.md`); title style and the title approval procedure (`references/structure.md`, Titles, and Shared Rule 10 in `committee/roles.md`); and new checker rules for both: `DASH_IN_PROSE`, `PREDICATIVE_COMPOUND_HYPHEN`, `COMMA_AFTER_CONJUNCTION`, `PARAGRAPH_STARTS_WITH_TO`, `TITLE_ABBREVIATION` and `TITLE_TOO_LONG`, with the acronym rules raised to warnings. A project whose venue allows dashes runs the checker with `--disable DASH_IN_PROSE`.

---

## Repository Layout

```
.claude-plugin/
  plugin.json                  plugin manifest
  marketplace.json             this repository as a one-plugin marketplace
commands/                      start, write, review, committee, check, no-committee
package-skill.sh               builds dist/academic-writing-committee.zip
skills/academic-writing-committee/
  SKILL.md                     the guide: principles, standards, process, modes, no-committee option
  references/                  detailed guidance, read on demand
  profiles/                    one JSON profile per publication type
  committee/                   procedure, roles, quality gates, models, configuration, catalog
  workflow/committee.js        the committee workflow
  scripts/                     project_setup.py, venue_recent.py, prepare_run.py, check_manuscript.py, check_citations.py
  templates/                   example project configurations
  SOURCES.md, LICENSES/        the works this skill draws on, and their licenses
```

| Reference | Covers |
|---|---|
| `language-mechanics.md` | hyphens and dashes, chains of *and*, repetition, fluency |
| `claims-and-coherence.md` | the calibration ladder, the claim-evidence matrix, whole-document coherence |
| `style.md` | sentences, word choice, paragraphs, voice and tense |
| `structure.md` | papers, reviews, theses, textbooks and lecture notes, technical reports |
| `evidence-and-citations.md` | searching, establishing a gap, verifying and citing sources |
| `figures-and-tables.md` | design, captions, image integrity, alt text, figures in teaching texts |
| `mathematics-and-notation.md` | notation, equations, proofs, algorithms, statistics |
| `review-and-revision.md` | revision passes, reviewing a manuscript, responding to reviewers |
| `integrity-and-ai.md` | AI use and disclosure, authorship, confidentiality, reporting guidelines |
| `publishing-and-grants.md` | venues, preprints, open access and funder mandates, grant proposals |
| `publication-types.md` | each type's readers, structure, length, judges and failure modes |

---

## Sources and License

MIT. See [LICENSE](LICENSE).

The writing guide is a synthesis, in new wording, of several MIT-licensed academic-writing skills, with original additions where they were silent. [`SOURCES.md`](skills/academic-writing-committee/SOURCES.md) lists them and what was drawn from each, and [`LICENSES/`](skills/academic-writing-committee/LICENSES/) keeps their license texts.
