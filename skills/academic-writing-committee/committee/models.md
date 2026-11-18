# Model Roster and Effort

The committee spreads work across four models so that each task gets enough intelligence and no more. The roster below is the default; a project overrides any entry in its configuration (`roster`, or `model`/`effort` on a reader, reviewer or editor), and the retrospective may adjust entries during a run when the evidence is clear. A configuration's `modelCeiling` caps every role at one model (for example Opus, with the Editor-in-Chief exempt); a capped role keeps its effort, so a project that gives up Fable usually raises the effort of the roles that would have used it (critical writers, briefs, chairs and the technical lens at Opus `xhigh`). Its adjustments are saved to `<stateDir>/roster.json` and carried into later runs (see `config.md`).

## The Models

| Model | Role in the committee | Effort guidance |
|---|---|---|
| **Claude Fable** (`fable`) | The most capable model, for the hardest reasoning and long-horizon work: critical units, the Editor-in-Chief, and writers escalated after repeated failure. | Start at `high`; use `xhigh` only where it measurably helps; reserve `max` for exceptional cases. |
| **Claude Opus** (`opus`) | The default strong model: developmental briefs, hard units (mathematics, figures, research depth), the technical, claims and experiments lenses, the committee chair and the integration editor. | Its default effort is `medium`, so the roster sets `high` explicitly for judgment-heavy roles. |
| **Claude Sonnet** (`sonnet`) | Fast and capable everyday work: writers for standard units, readers, most reviewer lenses, the line and consistency editors, the retrospective and the scout. | `medium` suits multistep tool use; `high` suits writing and close reading. |
| **Claude Haiku** (`haiku`) | Mechanical, high-volume work: the mechanical checker (unit and global checks), the skimming reader, the committer. | `low` for mechanical tasks, `medium` when it must read prose. |

The short names (`fable`, `opus`, `sonnet`, `haiku`) select the current version of each model. Prices, context windows and capabilities change; read the current model documentation before planning a very large run.

## Default Assignments

| Role | Model / effort | Escalation |
|---|---|---|
| Scout | sonnet / medium | |
| Developmental Editor | opus / high | fable / high for critical units |
| Writer | tier by difficulty: standard → sonnet / high, hard → opus / high, critical → fable / high | one tier up when the chair asks for it or problems repeat for two rounds: sonnet → opus → fable / high → fable / xhigh |
| Mechanical Checker | haiku / low | |
| Readers | sonnet / medium; the expert, program-committee, examiner and specialist personas sonnet / high; the skimmers haiku / medium | |
| Reviewer lenses: technical, claims, experiments, feasibility | opus / high (claims: sonnet / high in the book profile, which has many units) | technical: fable / high for critical units |
| Reviewer lenses: references, significance, coverage, pedagogy | sonnet / high | |
| Reviewer lenses: presentation, language, guidelines | sonnet / medium | |
| Reviewer lens: venue | sonnet / low | |
| Committee Chair | opus / high | fable / high for critical units |
| Editors: line, consistency | sonnet / high, sonnet / medium | |
| Regression Checker | sonnet / medium | |
| Integration Editor | opus / high | |
| Editor-in-Chief | fable / high | |
| Retrospective Analyst | sonnet / high | |
| Committer | haiku / low | |

## Committee Size by Publication Type

The profiles in `profiles/` set the readers, reviewer lenses and editors for each type; `committee/catalog.json` holds every persona and lens. Research documents get the lenses that catch the most expensive errors (technical, claims, experiments, references); a paper or article judged as a whole affords eight lenses per round. A book or thesis keeps seven lenses per chapter, because each chapter is a substantial document, while lecture notes get a lighter set of five; across many units, the integration editor and the editor-in-chief cover the whole.

| Type | Units | Readers | Reviewer lenses | Editors |
|---|---|---|---|---|
| book-chapter | whole-document | newcomer, expert | guidelines, technical, claims, references, presentation, language | line, consistency |
| book | chapters | newcomer, expert, chapter-skimmer | guidelines, technical, claims, pedagogy, presentation, references, language | line, consistency |
| conference-paper | whole-document | pc-reviewer, expert, skimmer | technical, claims, experiments, significance, references, presentation, language, venue | line, consistency |
| grant-proposal | whole-document | generalist, specialist | venue, significance, feasibility, claims, references, language | line, consistency |
| journal-article | whole-document | expert, adjacent | technical, claims, experiments, significance, references, presentation, language, venue | line, consistency |
| lecture-notes | chapters | newcomer, chapter-skimmer | technical, pedagogy, presentation, language, references | line, consistency |
| survey | whole-document | newcomer, expert, practitioner | coverage, claims, references, technical, presentation, language, venue | line, consistency |
| technical-report | whole-document | practitioner, expert | technical, claims, references, presentation, language | line, consistency |
| thesis | chapters | examiner, expert, generalist | guidelines, technical, claims, experiments, references, presentation, language | line, consistency |

Every type also has the developmental editor, the committee chair, the integration editor and the editor-in-chief; documents with several units also get a cross-unit claims review in each global round (on the claims lens's model, or Opus at high effort when the profile has no claims lens, as for lecture notes). Override any of these in the project configuration, or add and drop single lenses by catalog key (`addReviewers`, `dropReviewers` and the like).

## Why This Shape

- **Judgement concentrates where errors are expensive.** A wrong acceptance decision or a missed mathematical error costs more than any number of polished sentences, so the chair, the technical reviewer and the Editor-in-Chief get the strongest models.
- **Breadth is cheap.** Readers and most reviewer lenses run in parallel on Sonnet; diversity of perspective catches more than one expensive generalist.
- **Escalation beats over-provisioning.** Most units pass with a Sonnet or Opus writer. Only units that keep failing climb to Fable, so the expensive model is spent where it has been shown to be needed.
- **Mechanical work never gets a frontier model.** Running a build and reading its log is Haiku work.

## Cost Planning

A unit typically needs about 25 to 35 agent calls (a first reading by two or three readers and one brief; a first round with writer, checker, the readers again, five to eight lenses and the chair; one or two lighter rounds; two editors and a regression check). A workflow run is limited to 1,000 agent calls, so the configuration's `limits.maxAgents` (default 900) caps a run at roughly 30 units with the default rosters (25 to 35 depending on the calls per unit; `prepare_run.py` prints the exact figure), and the remaining units are deferred to the next run automatically. To reduce cost: fewer readers or lenses, `limits.maxRounds` lower, cheaper models for lenses that rarely find problems, or smaller stages. To increase quality on a hard project: raise the chair and technical reviewer to Fable, or start hard units one tier higher (`tier` on the unit).
