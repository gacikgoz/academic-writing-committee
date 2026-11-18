# Academic Writing Committee

**Academic writing for Claude that holds every sentence to the standard of a careful editor, and can put a whole committee of readers, reviewers and editors behind it when it matters.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Version 2.0.0](https://img.shields.io/badge/version-2.0.0-informational)
![Claude Code plugin](https://img.shields.io/badge/Claude%20Code-plugin%20%2B%20skill-8A63D2)
![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-3776AB)

`academic-writing-committee` is a Claude Code plugin and a standalone skill for planning, drafting, revising, reviewing and checking academic documents: journal articles, conference papers, surveys, theses, books and book chapters, lecture notes, technical reports and grant proposals.

It works in two ways:

- **Without a committee**, it is a single-session writing assistant with a complete writing guide and two checkers. Use it to draft a section, tighten a paragraph, calibrate a claim, or audit a reference list.
- **With the committee**, it divides a document into units and runs a multi-agent workflow. Tiered writers revise each unit, reader personas and reviewer lenses judge every revision, a chair decides, and editors polish. An editor-in-chief signs off on the whole. The cycle repeats until everything is approved.

---

## Contents

- [Quick Start](#quick-start)
- [With or Without the Committee](#with-or-without-the-committee)
- [Commands](#commands)
- [What It Enforces](#what-it-enforces)
- [How the Committee Works](#how-the-committee-works)
- [Publication Types](#publication-types)
- [The Checkers](#the-checkers)
- [Setting Up a Project](#setting-up-a-project)
- [Models and Cost](#models-and-cost)
- [Installation Options](#installation-options)
- [Requirements](#requirements)
- [Status](#status)
- [Repository Layout](#repository-layout)
- [Sources and License](#sources-and-license)

---

## Quick Start

Install the plugin in Claude Code. This repository is both the plugin and its marketplace:

```
/plugin marketplace add gacikgoz/academic-writing-committee
/plugin install academic-writing-committee@academic-writing-committee
```

Then ask for what you need. The skill loads by itself whenever a task involves academic writing:

```text
Revise the introduction of paper.tex for a NeurIPS submission, no committee.
Check every reference in thesis/chapter3.tex against refs.bib.
Review proposal.md as an NSF panel would, without a committee.
Run the committee on paper.tex as a conference paper until everything is approved.
```

Or start a mode directly with one of the [commands](#commands), for example:

```text
/academic-writing-committee:no-committee revise chapters/02-methods.tex thesis
```

---

## With or Without the Committee

| | No committee | Committee |
|---|---|---|
| **How to choose it** | `--no-committee`, "no committee" in the request, or the `no-committee` command; automatic when the Workflow tool is not available | the `committee` or `review` command, or a request for a committee run |
| **Who does the work** | Claude, in your session | a Workflow of specialized agents |
| **Best for** | a section, a paper you are actively editing, a quick review, a citation audit | a whole paper, thesis or book brought up to a set of guidelines |
| **Review** | one careful review by severity, no edits | parallel reader personas and reviewer lenses, consolidated by a chair |
| **Revision of a whole document** | unit by unit in reading order, with both checkers and the build after each unit | tiered writers, independent judgment each round, escalation, editors, a regression check |
| **Cost** | one session | about 18 to 35 agent calls per unit (see [Models and Cost](#models-and-cost)) |

The writing guide, the standards and the checkers are the same in both. The committee adds independent judgment, escalation and memory across runs.

---

## Commands

The plugin adds five commands. The standalone skill does everything they do when you ask in plain words.

| Command | What it does |
|---|---|
| `/academic-writing-committee:write [file or topic] [type] [instructions]` | Writes or revises text to the standard of the guide, then runs both checkers on what changed. Always a single session. |
| `/academic-writing-committee:review [--no-committee] [main file] [type] [venue]` | Reviews a document without changing it. Readers and reviewer lenses work in parallel and a chair writes a prioritized report. With `--no-committee`, Claude reviews it alone. |
| `/academic-writing-committee:committee [--no-committee] [configuration] [stages or units]` | Runs the committee until every unit and the whole document are approved, or until a unit needs your decision. With `--no-committee`, Claude revises the document unit by unit in one session. |
| `/academic-writing-committee:check [files] [bibliography]` | Runs the manuscript and citation checkers and proposes fixes. Always a single session. |
| `/academic-writing-committee:no-committee [write \| review \| check \| revise] [file or topic] [type] [instructions]` | Plain academic writing in any mode, in one session, with no subagents. |

A committee run is a multi-agent run, so invoking `review` or `committee` without `--no-committee` counts as your agreement to one. Claude states the plan and the expected number of agents before it launches anything.

---

## What It Enforces

The guide rests on twelve principles and four standards that reviewers raise again and again. In short:

- **Accuracy before fluency.** Observation, estimate, interpretation and speculation stay distinct. A fluent sentence is not evidence.
- **Nothing invented.** No guessed citations, numbers, quotations, dates or methods. A missing fact becomes a visible `[[TODO: ...]]`, never plausible filler.
- **Calibrated claims.** Verbs match the evidence: association is not cause, and "the first" needs a documented search. Overclaiming and underselling are both errors. The contributions, experiments, results, discussion and conclusion must agree with one another.
- **Real references.** Every cited work exists, has been opened, and supports the sentence that cites it. A real work cited for something it does not say counts as seriously as a fake one.
- **Clean language.** Hyphens, en dashes and em dashes are used correctly. Chains of *and*, repeated words and openings, formulaic transitions and stacked hedges go.
- **The author's voice.** Text is edited, not replaced. Terminology and claims stay unless they are the problem, and every substantive change comes with its reason.
- **Project rules first.** The venue's instructions and the project's own guidelines outrank the field's conventions, which outrank the skill.

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
- **The committee learns.** Recurring problems become lessons and lint rules that every later agent reads. Gaps in your guidelines become proposals for you. The committee never edits the guidelines itself.
- **Edits stay safe.** Editors only reword, and a regression check after acceptance rejects any new or changed claim.
- **Runs resume.** A ledger records every unit's state. An interrupted run picks up from the open actions, and long documents can be split into shards that run side by side.

The full procedure is in [`committee/procedure.md`](skills/academic-writing-committee/committee/procedure.md). The role contracts are in [`committee/roles.md`](skills/academic-writing-committee/committee/roles.md), and the severity scale and acceptance gates in [`committee/quality-gates.md`](skills/academic-writing-committee/committee/quality-gates.md).

---

## Publication Types

Each type has a profile that sets how the document is divided and who judges it.

| Type | Unit of work | Readers | Reviewer lenses |
|---|---|---|---|
| Journal article | whole document | expert, adjacent-field reader | technical, claims, experiments, significance, references, presentation, language, venue |
| Conference paper | whole document | program-committee reviewer, expert, skimmer | technical, claims, experiments, significance, references, presentation, language, venue |
| Survey | whole document | newcomer, expert, practitioner | coverage, claims, references, technical, presentation, language, venue |
| Thesis | chapter | examiner, expert, generalist | guidelines, technical, claims, experiments, references, presentation, language |
| Book | chapter | newcomer, expert, chapter skimmer | guidelines, technical, claims, pedagogy, presentation, references, language |
| Book chapter | whole document | newcomer, expert | guidelines, technical, claims, references, presentation, language |
| Lecture notes | chapter | newcomer, chapter skimmer | technical, pedagogy, presentation, language, references |
| Technical report | whole document | practitioner, expert | technical, claims, references, presentation, language |
| Grant proposal | whole document | panel generalist, specialist | venue, significance, feasibility, claims, references, language |

Every type also gets a developmental editor, a committee chair, line and consistency editors, a regression checker, an integration editor and an editor-in-chief. A document with several units also gets a cross-unit claims review in every global round. A project can add or drop any reader or lens by its key in [`committee/catalog.json`](skills/academic-writing-committee/committee/catalog.json).

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

- **`check_manuscript.py`** flags dash and hyphen misuse, chains of *and*, repeated words, phrases and sentence openings, stacked hedges, overclaiming and underselling words, formulaic phrasing, very long sentences, and references to unknown labels. Run `--list-rules` to see every rule.
- **`check_citations.py`** finds missing and unused keys, duplicates, missing fields and malformed identifiers. With `--online` it looks every reference up at Crossref, arXiv, doi.org and DataCite. It reports identifiers that do not exist (`NOT_FOUND`) and records whose metadata do not match (`METADATA_MISMATCH`). With `--ledger sources.csv` it compares the cited keys with a source ledger.

Both reports list candidates for a person to judge. A clean report proves nothing, and the checker cannot tell whether a work supports the sentence that cites it, so open each reference.

---

## Setting Up a Project

The committee reads `writing-committee.json` at the root of your project. A conference paper needs little more than this:

```json
{
  "name": "Robust Retrieval Under Distribution Shift",
  "publicationType": "conference-paper",
  "goal": "Make the paper ready for submission.",
  "guidelines": ["venue-rules.md"],
  "documents": ["paper.tex"]
}
```

A book or thesis lists `stages` whose `unitsFrom` globs make one unit per chapter, with the commands that build and check it. If your project has no configuration, the `committee` command writes one with you and asks only for what it cannot infer.

- Complete examples: [`templates/`](skills/academic-writing-committee/templates/) (a book and a conference paper)
- Every field: [`committee/config.md`](skills/academic-writing-committee/committee/config.md)

---

## Models and Cost

The committee gives each task enough capability and no more. The defaults:

| Work | Model |
|---|---|
| Mechanical checks, commits, skimming reader | Haiku |
| Most readers and reviewer lenses, standard writers, line and consistency editors | Sonnet |
| Briefs, hard writers, the chair, the technical and claims lenses, the integration editor | Opus |
| Critical units, escalated writers, the editor-in-chief | Fable |

A unit costs about 25 to 35 agent calls with the default roster, and a run is capped at about 900. For a lean run, drop readers or lenses, lower `limits.maxRounds`, or cap every role at one model with `modelCeiling`. One book project ran at about 18 calls per unit with one reader, three lenses and one editor. `prepare_run.py` prints its estimate before anything starts.

Defaults, escalation paths and the reasoning behind them are in [`committee/models.md`](skills/academic-writing-committee/committee/models.md).

---

## Installation Options

### Plugin (Claude Code, with Commands)

```
/plugin marketplace add gacikgoz/academic-writing-committee
/plugin install academic-writing-committee@academic-writing-committee
```

- **Update:** `/plugin marketplace update academic-writing-committee`
- **Local clone:** `claude --plugin-dir path/to/academic-writing-committee`
- **Earlier installs:** if you installed `academic-writing` or `academic-writing-committee@gacikgoz-plugins` from the `gacikgoz/aibook` marketplace, uninstall it first, so that only one copy of the skill competes for selection.

### Standalone Skill (No Plugin)

The folder [`skills/academic-writing-committee/`](skills/academic-writing-committee/) works on its own. Every path in it is relative to the folder, and its scripts need only Python.

| Where | How |
|---|---|
| Claude Code, every project | copy the folder to `~/.claude/skills/academic-writing-committee/` |
| Claude Code, one project | copy it to `<project>/.claude/skills/academic-writing-committee/` |
| claude.ai and other hosts that accept skill uploads | run `./package-skill.sh` and upload `dist/academic-writing-committee.zip` |
| Other agents that read `SKILL.md` skills | place the folder where the agent looks for skills, or point it at `SKILL.md` |

The standalone skill has every mode; only the slash commands come with the plugin.

---

## Requirements

- **Claude Code**, or any agent that loads `SKILL.md` skills. The committee runs as a Workflow, so it needs the Workflow tool; without it, the skill uses the no-committee option.
- **Python 3.9 or later** for the scripts, and network access for `check_citations.py --online`.
- **For the committee:** the models of the roster (Fable, Opus, Sonnet, Haiku), or overrides in your configuration for any you lack; `git`, because the committee commits after each wave; and your project's own build tools for its checks.

---

## Status

Version 2.0.0. The writing guide, the checkers and the no-committee option are complete. The committee has run end to end on a small sample project. It is also being used, with a lean roster, to revise a textbook of more than 4,000 pages; that revision is still in progress. Expect the committee's procedure and defaults to keep changing as that work teaches them.

---

## Repository Layout

```
.claude-plugin/
  plugin.json                  plugin manifest
  marketplace.json             this repository as a one-plugin marketplace
commands/                      write, review, committee, check, no-committee
package-skill.sh               builds dist/academic-writing-committee.zip
skills/academic-writing-committee/
  SKILL.md                     the guide: principles, standards, process, modes, no-committee option
  references/                  detailed guidance, read on demand
  profiles/                    one JSON profile per publication type
  committee/                   procedure, roles, quality gates, models, configuration, catalog
  workflow/committee.js        the committee workflow
  scripts/                     prepare_run.py, check_manuscript.py, check_citations.py
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
