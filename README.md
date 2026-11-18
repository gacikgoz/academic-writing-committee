# Academic Writing Committee: Plugin and Skill

`academic-writing-committee` is one skill for every stage of academic writing: planning, drafting, revising, reviewing, and checking books, book chapters, journal articles, conference papers, surveys, theses, technical reports, grant proposals, and lecture notes. The skill combines:

- **A writing guide.** It covers structure, style, evidence and citations, figures and tables, mathematics and notation, integrity and AI disclosure, review and revision, and publishing and grants. Two references give a focused standard for points reviewers often raise: language mechanics (hyphens and dashes, chains of *and*, repetition, and fluency) and claims and coherence (no overclaiming or underselling; contributions, experiments, discussion, and conclusion that agree; real references only).
- **Publication-type profiles.** Each type sets how the document is divided, which reader personas and reviewer lenses judge it, and what its readers expect.
- **Checkers.** `check_manuscript.py` lints prose mechanics and claim wording. `check_citations.py` audits citation keys, bibliography entries, and free-form reference lists (duplicates, missing fields, identifier syntax, and the source ledger). With `--online` it looks each reference up at Crossref, arXiv, doi.org and DataCite: it reports DOIs and arXiv identifiers that do not exist (NOT_FOUND) and records whose metadata do not match, and marks the references it cannot confirm as UNVERIFIED or URL_ONLY, which must be checked by search. With `--ledger sources.csv` it compares the cited keys with a source ledger (the columns `key` and `status`, `status` starting with `verified` once the source was opened, and an optional `locator`). Agents still open each reference to confirm that it supports the sentence citing it.
- **An optional writing committee.** This multi-agent workflow assigns units to tiered writers (Sonnet, then Opus, then Fable). It puts every revision in front of reader personas, a reviewer committee, a committee chair, and an editor committee, and iterates with escalation until every unit and the whole document are approved. Haiku runs the mechanical checks, the skimming reader, and the commits; Opus and Fable take the briefs, the chair, the hardest lenses, and the editor-in-chief. The committee learns as it runs: recurring problems become lessons, lint rules, and roster changes for later agents and later runs.
- **A no-committee option.** With `--no-committee` (or "no committee" in a request, or the `no-committee` command) the skill works as plain academic writing in a single session: no subagents and no workflow. Writing, review, checking, and a unit-by-unit revision of a whole document all run that way. The same applies automatically when the Workflow tool is missing.

The skill is packaged twice from the same folder: as a Claude Code **plugin** (with commands) and as a **standalone skill** that can be copied or uploaded directly.

## Requirements

- Claude Code (or any agent that loads `SKILL.md` skills). The review and committee modes run as a Workflow, so they need the Workflow tool; without it, the skill falls back to the no-committee option.
- Python 3.9 or later for the scripts (standard library only), and network access for `check_citations.py --online`.
- The models `fable`, `opus`, `sonnet`, and `haiku` for the default roster. An account without one of them overrides the roles that use it with the configuration's `roster` and the `model` of each reader, reviewer, and editor (`committee/models.md`).
- `git` for the committee's commits; the project's own build tools for its checks.

The committee has run end to end on a small sample project (a smoke test), not yet on a full book or paper.

## Installation

### As a Plugin (Claude Code, with Commands)

This repository is both the plugin and its marketplace. In Claude Code:

```
/plugin marketplace add gacikgoz/academic-writing-committee
/plugin install academic-writing-committee@academic-writing-committee
```

The marketplace command reads the repository's default branch, and a private repository also needs GitHub access on the machine that runs it. For a local clone, start Claude Code with `claude --plugin-dir path/to/academic-writing-committee`. To update an installed copy, run `/plugin marketplace update academic-writing-committee`. An earlier install from the `gacikgoz/aibook` marketplace (`academic-writing` or `academic-writing-committee@gacikgoz-plugins`) should be uninstalled first, so that only one copy of the skill competes for selection.

### As a Standalone Skill (No Plugin)

The folder `skills/academic-writing-committee/` is complete on its own: every path in it is relative to the folder, and the scripts use only the Python standard library. To use it directly:

- **Claude Code, personal:** copy the folder to `~/.claude/skills/academic-writing-committee/`.
- **Claude Code, one project:** copy it to `<project>/.claude/skills/academic-writing-committee/`.
- **Upload (claude.ai and other skill hosts):** build a zip with `./package-skill.sh` (it writes `dist/academic-writing-committee.zip`, with the skill folder at the top of the archive) and upload that file.
- **Other agents** that read `SKILL.md` skills (for example Codex): put the folder where that agent looks for skills, or point it at `SKILL.md`.

The standalone skill has every mode; only the slash commands below come with the plugin. Without them, ask in plain words, for example "Use academic-writing-committee with no committee to revise section 3."


## Use

The skill loads automatically when a task involves academic writing. The commands start each mode explicitly:

| Command | What it does |
|---|---|
| `/academic-writing-committee:write [file or topic] [type] [instructions]` | Writes or revises text to the standard of the guide, then runs both checkers on what changed. Single session. |
| `/academic-writing-committee:review [--no-committee] [main file] [type] [venue]` | Runs an independent committee review that edits nothing: the type's readers and reviewer lenses work in parallel, and the chair consolidates their findings into a prioritized report. With `--no-committee`, a single-session review. |
| `/academic-writing-committee:committee [--no-committee] [configuration] [stages or units]` | Runs the self-improving writing committee until everything is approved or a decision needs a person. With `--no-committee`, a single-session revision, unit by unit. |
| `/academic-writing-committee:check [files] [bibliography]` | Runs the manuscript and citation checkers and proposes fixes. Single session. |
| `/academic-writing-committee:no-committee [write \| review \| check \| revise] [file or topic] [type] [instructions]` | Plain academic writing without the committee: any mode, in one session, with no subagents. |

The review and committee modes run as a Workflow, so invoking them without `--no-committee` is your explicit agreement to a multi-agent run. Before launching, Claude states the plan and the expected number of agents. A request in plain words works too, for example: "Run the academic-writing-committee skill on paper.tex as a conference paper until everything is approved," or "Review paper.tex with academic-writing-committee, no committee."

## Publication Types and Committee Sizes

| Type | Unit of work | Readers | Reviewer lenses |
|---|---|---|---|
| Book | chapter | newcomer, expert, chapter skimmer | guidelines, technical, claims, pedagogy, presentation, references, language |
| Book chapter | whole document | newcomer, expert | guidelines, technical, claims, references, presentation, language |
| Journal article | whole document | expert, adjacent-field reader | technical, claims, experiments, significance, references, presentation, language, venue |
| Conference paper | whole document | program-committee reviewer, expert, skimmer | technical, claims, experiments, significance, references, presentation, language, venue |
| Survey | whole document | newcomer, expert, practitioner | coverage, claims, references, technical, presentation, language, venue |
| Thesis | chapter | examiner, expert, generalist | guidelines, technical, claims, experiments, references, presentation, language |
| Technical report | whole document | practitioner, expert | technical, claims, references, presentation, language |
| Grant proposal | whole document | panel generalist, specialist | venue, significance, feasibility, claims, references, language |
| Lecture notes | chapter | newcomer, chapter skimmer | technical, pedagogy, presentation, language, references |

Every type also gets a developmental editor, a committee chair, line and consistency editors, a regression checker, an integration editor, and an editor-in-chief; documents with several units also get a cross-unit claims review in every global round. A document judged as a whole is a single unit, so it can afford more lenses per round. A long document has many units, so each unit gets a focused set and the integration editor and editor-in-chief look after the whole. The models and effort levels of each role are in `skills/academic-writing-committee/committee/models.md`; a project configuration can override any of them.

## Setting Up the Committee for a Project

The committee reads `writing-committee.json` at the root of the project. A conference paper needs little more than this:

```json
{
  "name": "Robust Retrieval Under Distribution Shift",
  "publicationType": "conference-paper",
  "goal": "Make the paper ready for submission.",
  "guidelines": ["venue-rules.md"],
  "documents": ["paper.tex"]
}
```

A book or thesis lists stages whose `unitsFrom` globs make one unit per chapter. `skills/academic-writing-committee/templates/` has complete examples, and `committee/config.md` documents every field. If the project has no configuration, the committee command writes one with you, asking only for what it cannot infer.

## What the Committee Enforces

- **Guidelines first.** The project's guidelines and the venue's rules come first, then the writing guide. The committee never edits the guidelines; it proposes changes to their owner.
- **Calibrated claims.** Overclaiming and underselling a central claim are major findings (an overclaim in the abstract or conclusion is a blocker). Contributions, experiments, results, discussion, and conclusion must agree with one another, within each unit and across units.
- **Real references.** A reference that cannot be found is a blocker, and a real work cited for something it does not say is a major finding. Agents run the citation checker and verify every reference by search; nobody invents a citation, number, date or quotation.
- **Clean language.** Hyphens, en dashes, and em dashes are used correctly. Chains of *and*, repeated words and sentence openings, formulaic transitions, and stacked hedges are removed.
- **Safe edits.** Units processed in parallel never share a file, editors only reword, and a regression check after acceptance rejects any new or changed claim.

A workflow runs only a few agents at a time (two on a 4-CPU machine). For a long document, `prepare_run.py --shards K` divides the units among K workflows that run side by side, each committing only its own files; the global rounds follow once every shard has ended (`committee/procedure.md`, "Running More Agents at Once").

## Layout

```
.claude-plugin/plugin.json      plugin manifest
commands/                       write, review, committee, check, no-committee
package-skill.sh                builds dist/academic-writing-committee.zip (the standalone skill)
skills/academic-writing-committee/
  SKILL.md                      the writing guide, the no-committee option and the entry point for every mode
  references/                   detailed guidance, read on demand
  profiles/                     one JSON profile per publication type
  committee/                    procedure, roles, quality gates, models, configuration, catalog
  workflow/committee.js         the committee workflow
  scripts/                      prepare_run.py, check_manuscript.py, check_citations.py
  templates/                    example project configurations
  SOURCES.md, LICENSES/         the skills this one draws on and their licenses
```

## Sources and License

The writing guide is a synthesis, in new wording, of several MIT-licensed academic-writing skills, with original additions. `skills/academic-writing-committee/SOURCES.md` lists them and what was taken from each, and `skills/academic-writing-committee/LICENSES/` holds their license texts.
