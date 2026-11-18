# Project Configuration

A project describes itself in a JSON file (by convention `writing-committee.json` at the repository root). `scripts/prepare_run.py` reads it, expands units and writes the workflow arguments. Paths are relative to the configuration file unless `root` says otherwise.

## Fields

| Field | Type | Meaning |
|---|---|---|
| `name` | string | Name of the document, used in prompts and commit messages. |
| `publicationType` | string | **Required.** A profile in `profiles/` (book, book-chapter, journal-article, conference-paper, survey, thesis, technical-report, grant-proposal, lecture-notes). It supplies default readers, reviewer lenses, editors, limits and the goal; anything set in the configuration overrides it. Pick the nearest type and adjust it with the fields below. |
| `documents` | string[] | Shortcut for documents judged as a whole: each main file becomes one unit (with the files only it includes, and the bibliography it names unless that is shared). Used when `stages` is absent. |
| `goal` | string | What this whole effort must achieve. Every agent reads it. |
| `language` | string | Language of the document. |
| `root` | string | Project root relative to the configuration file (default `.`). |
| `stateDir` | string | Committee state directory (default `.writing-committee`). |
| `guidelines` | string[] | Guideline files; they are the authority. Default `guidelines.md`, if it exists; a file listed here must exist. Without any, the skill's writing guide and the publication-type section serve as the guidelines (prepare_run.py prints a notice). |
| `context` | string[] | Other files every agent should know: roadmap, glossary, notation table, issue list. |
| `writingSkills` | string[] | Additional writing references every agent consults, such as a publisher's style guide or a lab's writing rules, subordinate to the guidelines. The skill's own writing guide (`SKILL.md` and its references) is always given to every agent, so this field lists only extras. |
| `sharedFiles` | string[] | Files no unit may own (main file, preamble, a bibliography several units cite, indices); a path ending in `/` means every file under it. Do not also list them in a unit's `files`, except for a stage whose units are meant to set up shared files (a design-system stage, say): `prepare_run.py` prints a note for each such overlap and for a file owned in several stages. Shared prose files are part of the whole-document checks: a main file with `\begin{document}` first, the others last. |
| `bibliography` | string or string[] | The bibliography file(s) (`.bib` or CSL JSON). Default: the files that the `documents` name with `\bibliography` or `\addbibresource`. The citation checker runs against them in every round and in every global round. |
| `assetDir` | string | Where a unit may create new files, with `{unit}` for the unit id (for example `figures/{unit}`). |
| `checks.unit` | string | Command run per unit; `{files}` becomes the unit's files, `{main}` its main (first) file, `{unit}` its id, `{bib}` the bibliography and `{skill}` the skill directory. Must be safe to run in parallel (build into a directory named after `{unit}`). |
| `checks.global` | string[] | Commands run once per global round (full build, link check, size budget); `{bib}` and `{skill}` are filled in. |
| `checks.notes` | string | Anything checkers should know about the commands' output. |
| `referenceList` | string or string[] | Free-form reference lists (a LaTeX `\item` or `\bibitem` list, or a Markdown list) for documents without a bibliography database. Every global round checks them with `check_citations.py --reference-list`; a list that a unit owns joins the global checks once that unit has run. |
| `onlineCitations` | boolean | Verify references online in every global round (`check_citations.py --online`, cached in `<stateDir>/citations-cache.json`, which is git-ignored). Default true; set false when the network is unavailable: every agent is then told not to pass `--online`, and the references lens verifies every reference by search instead. |
| `stages` | object[] | Ordered stages; see below. |
| `readers` | object[] | Reader personas: `{key, persona, model, effort}`. Replaces the profile's list. |
| `reviewers` | object[] | Reviewer lenses: `{key, focus, model, effort, critical?: {model, effort}}`. Replaces the profile's list. |
| `editors` | object[] | Editors run in order: `{key, focus, model, effort}`. Replaces the profile's list. |
| `addReaders`, `addReviewers`, `addEditors` | string[] | Keys from `committee/catalog.json` to add to the profile's (or configured) list, for example `["pedagogy"]`. |
| `dropReaders`, `dropReviewers`, `dropEditors` | string[] | Keys to remove from the list, for example `["experiments"]` for a paper without experiments. |
| `readBeforeBrief` | boolean | Readers also read the original text before the developmental brief, so the brief and the first writer start from reader feedback (default true; adds one reader pass per unit). |
| `roster` | object | Overrides for role models (see `models.md`): `scout`, `brief`, `briefCritical`, `writerTiers`, `checker`, `chair`, `chairCritical`, `regression`, `integration`, `globalChair`, `retrospective`, `committer`. |
| `limits` | object | `maxRounds`, `maxGlobalRounds` (2), `waveSize`, `maxRepairs` (2), `maxAgents` (900), `shards` (1; the default for `prepare_run.py --shards`, the number of workflows that revise disjoint units at the same time), and `laterRoundRounds` (2.5), the average number of rounds per unit used only to estimate how many units fit in a run. The defaults come from the profile: whole-document types use `maxRounds` 6 and `waveSize` 4, chapter types 5 and 6 (the workflow's own fallback is 5 and 6). |
| `commit` | object | `perWave` (true), `push` (false), `branch`: the remote branch to push to (`git push origin HEAD:<branch>`; the current branch's name when empty). |
| `adaptRoster` | boolean | Let the retrospective adjust the roster (default true). Its changes are saved by `prepare_run.py --record` to `<stateDir>/roster.json` and applied to later runs: above the profile, below the configuration's `roster` entries, and replacing the model and effort of listed readers, reviewers, editors and writer tiers. Delete the file to discard them. |
| `modelCeiling` | string or object | The most capable model any role may use, for example `"opus"`, or `{ "model": "opus", "except": ["globalChair"] }` to exempt roles (role names as in roster adjustments: `chair`, `globalChair`, `writerTier:2`, `reviewer:technical`). A role above the ceiling runs on the ceiling model with its own effort; this covers the defaults, the configuration, learned changes and the retrospective's adjustments during a run. Use it to keep a run off a model (cost, availability) without listing every role. |
| `reviewOnly` | boolean | Always prepare review-only runs (the same as `--review-only`). |

The committee always adds `scripts/check_manuscript.py` and `scripts/check_citations.py --bib <bibliography>` to the unit check (on the unit's `.tex`, `.texview`, `.md`, `.markdown` and `.txt` files, and with `--reference-list` for a `referenceList` file the unit owns) and to the global check (in reading order on the units of the run, the units accepted in earlier runs and the shared files, with `--online` unless `onlineCitations` is false, plus `--reference-list` for each `referenceList`), so the configured commands need not repeat them; a global `check_citations.py` command on the main file alone would miss the keys of the files it includes. Both scripts get `--skip-missing`, so a file that a unit has yet to create is skipped with a notice instead of failing the check.

## Stages

A stage is a set of units processed before the next stage starts. Give a stage either explicit `units`, or `unitsFrom` (expanded by `prepare_run.py`), or only a `scope` (the Scout agent divides it). The Scout is told which units already exist and never reuses their ids or files; the units it creates are recorded in the ledger, so later runs resume them, with their open actions and tier, instead of scouting again (`prepare_run.py --rescout` scouts the scope afresh).

```json
{
  "id": "chapters",
  "goal": "Bring every chapter up to the guidelines.",
  "unitsFrom": {
    "glob": "chapters/*.tex",
    "exclude": ["chapters/draft-*.tex"],
    "idTemplate": "{stem}",
    "idPattern": "ch(?P<num>\\d+)",
    "companions": ["figures/{stem}/*", "exercises/ex{num_int}.tex"],
    "inputsAsCompanions": true,
    "orderFrom": "main.tex",
    "difficulty": "standard",
    "difficultyOverrides": {"ch03": "hard"},
    "goal": "Unit-level goal shared by every unit of the stage."
  }
}
```

- `idPattern` named groups are available in `idTemplate` and `companions`; numeric groups also appear as `<name>_int` without leading zeros. `idPrefix` is prepended to every id. When `idTemplate` uses a group, every file the glob matches must match `idPattern`; `prepare_run.py` skips any other file with a warning, so list helper files under `exclude`. Unit ids must be unique across the configuration; `prepare_run.py` stops on a duplicate.
- `difficulty` defaults to the profile's `defaultDifficulty`. The configured difficulty is a floor: the developmental editor may raise it, never lower it.
- `inputsAsCompanions` gives a unit every file that only it includes with `\input`/`\include`.
- `orderFrom` orders units by where their main file first appears in that file (so the reading order is preserved).
- An explicit unit is `{id, title?, files, difficulty?, goal?, tier?, check?}`; `tier` (0 to 3) starts its writer at a given tier, and `check` replaces `checks.unit` for that unit (with the same placeholders; an empty string runs none), for example a full build for a unit that owns the main file. Files that do not exist yet are created by the unit; a path ending in `/` owns every file under that directory.
- For a book or thesis, put the introduction, preface and conclusion in a final stage, so that they describe the chapters as revised.

## Example

See `templates/` for complete configurations (a LaTeX book and a conference paper).
