# Running the Writing Committee

The committee turns a set of rules into finished prose. It divides a document into units, gives each unit to a writer chosen for its difficulty, and puts every revision in front of independent readers, reviewers and editors until the unit satisfies the rules. It learns as it goes: recurring problems become lessons and lint rules that every later agent reads, stubborn units escalate to stronger models, and the roster adapts to the evidence. A run ends only when every unit and the document as a whole are approved, or it reports exactly what is still open.

Paths below are relative to the skill directory (the directory that holds `SKILL.md`); `<skill>` in a command stands for its absolute path.

## The Committee

```
              guidelines (+ venue rules)  +  writing guide  +  lessons.md  +  lint_rules.md
                                           │
 Scout ──► units ──► Readers (original text) ──► Developmental Editor ──► brief
                                           │
          ┌──────────────── round r (max N) ┴────────────────────────────┐
          │ Writer (tiered: sonnet → opus → fable → fable xhigh)          │
          │   └► Mechanical Checker (haiku): build, manuscript, citations │
          │   └► Readers ∥ personas chosen by publication type            │
          │   └► Reviewers ∥ lenses chosen by publication type            │
          │   └► Committee Chair: verify, merge, decide, escalate, learn  │
          └──── revise ◄── actions                         accept ────────┘
                                                             │
                     Editors (line ► consistency) ► Regression Checker ► accepted
                                                             │
     waves of units in parallel ─► Retrospective (lessons, lint rules, roster) ─► Commit
                                                             │
  global checks ► Integration Editor ► cross-unit claims review ► Editor-in-Chief: approve | reopen units
```

| Group | Roles | What they do |
|---|---|---|
| Planning | Scout, Developmental Editor | Divide the scope into units with disjoint files; diagnose each unit and write its revision brief. |
| Writing | Writer (four tiers) | Carry out the brief, then the chair's actions; dispute with evidence when they disagree. |
| Readers | Personas such as newcomer, expert, skimmer, program-committee reviewer, examiner, practitioner, panel generalist or specialist | Read the original text before the brief and the rendered unit in each round; report confusion, gaps, redundancy and what helped. Their feedback goes to the developmental editor, the writers, the reviewers and the chair. |
| Reviewer committee | Lenses such as technical, claims, experiments, references, significance, coverage, pedagogy, presentation, language, venue, feasibility, guidelines; Committee Chair | Judge each revision through one lens each; the chair verifies, merges and decides. |
| Editor committee | Developmental, Line, Consistency and Integration editors; Editor-in-Chief | Plan, polish and integrate; the Editor-in-Chief approves the whole or reopens units. |
| Support | Mechanical Checker, Regression Checker, Retrospective Analyst, Committer | Objective checks (the project's commands plus both checkers, per unit and on the whole document), edit safety, self-improvement, version control. |

The roles' contracts are in `committee/roles.md`, severity and acceptance gates in `committee/quality-gates.md`, the models and committee sizes in `committee/models.md`, the configuration format in `committee/config.md`, and the per-type defaults in `profiles/`.

## Procedure

Follow these steps in order. The orchestration runs as a Workflow (invoking this skill's committee mode is the user's explicit opt-in to multi-agent orchestration); you stay in the loop between runs.

### 1. Find or Write the Project Configuration

Follow the guided flow of `SKILL.md` ("Start Here"):

1. Run `python3 <skill>/scripts/project_setup.py detect --json`. If it finds a configuration (the one the user named, `writing-committee.json`, or one in the state directory), use it and continue from its ledger.
2. Otherwise ask the questions it lists (one batch with the question tool; the task, the type when uncertain, the goal, the guidelines when none were found, the size and the effort) and write the configuration with `project_setup.py init`. It fills in what was detected: the main document or the chapter glob, the shared files, the bibliography or reference list, guideline and context files, and the build commands.
3. Check what `init` could not know, and fix it in the file without asking: a chapter that cannot be built alone needs a unit check that builds it with the main preamble, and a missing build tool needs installing or a check that does not use it.

The fields, for reference:

- `publicationType`: one of the profiles in `profiles/` (book, book-chapter, journal-article, conference-paper, survey, thesis, technical-report, grant-proposal, lecture-notes). The profile chooses the readers, reviewer lenses, editors, limits and how the document is divided into units.
- `guidelines`: the project's rules (a style sheet, the venue's author instructions or the call's requirements). If there are none and the user described rules, write a short `guidelines.md` from their answer; otherwise the skill's writing guide covers everything general.
- For a paper, chapter, report or proposal: `documents` lists the main file(s); each becomes one unit judged as a whole. For a book, thesis or lecture notes: `stages` with `unitsFrom` globs make one unit per chapter.
- `checks`: the commands that build the document and check it (see `committee/config.md`). The committee adds `scripts/check_manuscript.py` and `scripts/check_citations.py` to every unit check and every global check by itself; give the `bibliography` if the documents do not name it.
- `committeeSize` and `effort`: from the user's answers.

Say which detected values and defaults you used, in one or two lines.

### 2. Preflight

1. Read the guidelines and the venue rules completely. If they are thin, say so: the committee can only be as good as the rules it enforces.
2. Make sure the working tree is clean (never commit or stash the user's work without asking; if there are uncommitted changes, ask or work on a branch).
3. Run each configured check once on a small unit and once globally, plus `scripts/check_manuscript.py` and `scripts/check_citations.py`, so that you know they work and what the baseline failures are. Fix broken check commands before launching agents.
4. For LaTeX projects, run a full build first so that unit checks can resolve references to the rest of the document.

### 3. Prepare the Run

```bash
python3 <skill>/scripts/prepare_run.py writing-committee.json [--size low|medium|high|full] [--stages a,b] [--units x,y] [--shards K]
```

The committee size (`committeeSize` in the configuration, or `--size` for one run) scales the profile's committee: `low` and `medium` for drafts, tight budgets or many units, `high` for most final revisions, `full` (the default) for the whole profile. If the user named a size ("a low committee", "medium committee"), pass it with `--size`; otherwise use the configuration's. Say the size in the plan you give the user.

**Ask the user for the effort before the first run.** Unless the request, the command (`--effort`) or the configuration (`effort`) already gives it, ask which effort level the committee should use: `low`, `medium`, `high` (recommended), `xhigh`, `max`, or `default` (each role keeps its own). Ask in one question, together with the size if that is open too, and pass the answer with `--effort` to this run and every later run of the same task. The effort applies to every role except the mechanical checker and the committer, and the last writer tier runs one level higher. Do not choose it for the user.

The script prepares everything the workflow needs:

- It applies the publication-type profile and any roster changes learned in earlier runs.
- It expands globs into units, with their companion files and the files that only one unit includes, and orders the units as the main file reads them.
- It skips units the ledger already marks as accepted (the global rounds still judge them and may reopen them), and carries over the open actions and tier of units the last run left open.
- It creates the committee's state files, writes `<stateDir>/run-args.json` and adds the working directories to `.gitignore`.
- It prints the plan: units per stage, estimated agents per unit, and how many workflow runs the scope needs.

It exits with status 2 and writes nothing when there is nothing to do. Tell the user the plan in two or three lines before launching.

With `--shards K` the script divides the units among K workflows and writes one argument file per shard (`<stateDir>/run-args.shard-<i>.json`); see "Running More Agents at Once" below.

### 4. Launch

Read `run-args.json` and call the Workflow tool with `scriptPath` set to `<skill>/workflow/committee.js` and `args` set to that JSON object (an object, not a string). The workflow runs in the background; tell the user what is running and how to watch it (`/workflows`). Do not poll; you are notified when it finishes.

For a sharded plan, launch one workflow per `run-args.shard-<i>.json`, all in the same message, and keep each run's id with its shard number.

### 5. Record, Verify, Continue

When the workflow finishes:

1. Save its result to `<stateDir>/result-<n>.json` and run `prepare_run.py <config> --record <that file>`; this updates the ledger, saves learned roster changes to `<stateDir>/roster.json`, and prints accepted, reopened, unresolved, failed, deferred and stalled units and the state of the global review. Recording the same file twice changes nothing.
2. Verify independently: run the global checks, the manuscript checker and the citation checker yourself, and look at a few rendered pages. Never report success the checks do not show.
3. Commit and push according to the configuration (the workflow commits after each wave and at the end when `commit.perWave` is true).
4. Continue automatically while there is progress to make:
   - status `continue` (units were deferred because of the agent budget): prepare and launch the next run;
   - units `unresolved`: launch a run for them; each resumes from its open actions, one writer tier higher than it ended (capped at the strongest tier);
   - units `reopened` (the Editor-in-Chief reopened them in the last global round, so no round was left to revise them): launch a run for them; each starts from the chief's actions at the tier it reached;
   - units `failed` or `not_run` (an agent returned nothing, or the run stopped early): launch a run for them once more, from their open actions if they had any; a unit that fails twice needs a person;
   - units `deferred` keep the state they had before (`resume_status` in the ledger), so an unresolved unit that was deferred still resumes from its open actions and tier;
   - status `incomplete` with no open unit (the Editor-in-Chief gave no verdict, or the global checks failed after integration): `prepare_run.py` prepares a global-only run that repeats the global rounds over the accepted units; if that run also ends without approval and without a unit to reopen, stop and report the remaining issues;
   - a unit unresolved twice at the strongest tier, or failed twice, is **stalled**: stop and ask the user, quoting its open actions; it needs a human decision. `--status` lists stalled units under "NEEDS A HUMAN DECISION", and `prepare_run.py` leaves them out of the plan (and says so) until the user decides; then plan them with `--include-stalled` or by naming them in `--units`.
5. Between runs, read `<stateDir>/guideline_proposals.md` and present the proposals to the user; the committee never edits the guidelines itself.

### 6. Finish

The work is complete when every unit in scope is accepted, the global checks pass and the Editor-in-Chief approved the last run. Report to the user what was accepted, what changed in the roster, the lessons learned, the guideline proposals, the cost in agent calls, and anything that still needs them. Record remaining issues where the project keeps them.

### Running More Agents at Once

A workflow runs only a few agents at a time: the Workflow tool allows min(16, CPUs − 2), which is 2 on a 4-CPU machine, however many units a wave holds. Each workflow has its own allowance, so the way to put more agents to work is to run several workflows side by side on disjoint units. `prepare_run.py --shards K` plans that:

- It divides the units of the plan among K shards. Units that share a file stay in one shard, and a stage that the Scout has yet to divide goes to the first shard. The wave size of a shard is the allowance plus one, so that both of its slots stay busy and its commits come often.
- A shard runs no global round, because the Integration Editor edits shared files and must work alone. A shard keeps its own lessons, lint rules and guideline proposals (`lessons.shard-<i>.md` and so on), which every agent of every shard reads, and its Committer commits only its own units' files, by path.
- When a shard ends, record its result as usual: `--record` also merges the shard's lessons into the committee's files. Verify and commit after each shard; the other shards' uncommitted files are theirs.
- When every shard has been recorded, run `prepare_run.py` again: units still open are planned as before (sharded again if there are many), and when none is open, `--global-only` prepares the run of the global rounds over everything accepted.

Shards of a plan with several stages run those stages side by side. When a later stage builds on an earlier one, plan one stage at a time with `--stages`. Several sharded plans can run at once (one stage while the next is planned, say): give the later plan `--first-shard N` with N above the highest shard number still running, because each shard keeps its lessons in files named by its number, and preparing a plan deletes the argument files of earlier plans, which matters only before they are launched.

How many shards a machine carries depends on the checks, not on the agents: the agents wait on the model, while every build takes a CPU. Unit builds of a few seconds allow two shards per CPU; a check that builds the whole document needs a CPU to itself. Start moderately, watch the load, and raise K for the next set.

A run that is not sharded can leave its global rounds to a later run as well (`--no-global`). That saves a round when several runs follow one another closely and one global review at the end can judge them together; the last of them, or a `--global-only` run, then covers everything accepted.

### Planning Ahead

`prepare_run.py --plan-only` prepares a run of the first reading and the developmental briefs alone. It edits no file of the document, so it can run beside anything, including a run that is still changing shared files the writers will depend on. Record its result: the ledger marks the units as briefed, and the run that revises them starts at the writer with the brief and the readers' first feedback.

### Resume

If a workflow is interrupted, relaunch it with the same `scriptPath` and `args` plus `resumeFromRunId`; finished agents return their cached results. The cache follows the sequence of agent calls: every call up to the first one that differs is replayed, and everything after it runs again. A run with one unit per wave replays exactly; a run whose waves hold several units replays as far as its units' calls come in the same order. If the session itself was lost, `prepare_run.py` rebuilds the plan from the ledger and the committed files, so a new run simply continues.

## How the Committee Improves Itself

- **Lessons.** Every chair records transferable lessons; after each wave the Retrospective Analyst merges them into `lessons.md`, which every writer, reviewer and editor reads before working.
- **Learned lint rules.** Mechanical patterns that keep recurring become entries in `lint_rules.md`, which the Mechanical Checker applies from then on.
- **Escalation.** A writer moves up one tier when the chair asks for it or the same problems repeat for two rounds; a unit left unresolved by a run starts the next run one tier higher, from its open actions.
- **Roster adaptation.** The retrospective may move any role, reader, reviewer, editor or writer tier to a stronger or cheaper model when the evidence is clear. `--record` saves these changes to `roster.json`, and later runs start from them. Disable with `adaptRoster: false`.
- **Guideline proposals.** Gaps and ambiguities in the guidelines are written to `guideline_proposals.md` for the human owner.
- **Focused re-review.** After the first round, only the readers and reviewers whose concerns remain look again, plus the claims and language lenses, because any revision can introduce an overclaim or a slip in the prose. Writers and reviewers always see the latest reader feedback.
- **Whole-document coherence.** Every global round runs the checkers in reading order over the units of the run, the units accepted in earlier runs, and the shared files, which is the whole document once every unit has been revised (repetition across units, citation keys in a shared bibliography) and, for documents with several units, a cross-unit claims review that compares contributions, numbers and terms across the abstract, introduction, unit summaries and conclusion.

## Safety Rules

- Units processed in parallel never share a file; the script places units that share files in different waves. Shared files are changed only by the Integration Editor, who runs alone, and its changes are committed after each global round.
- Units run in waves of `limits.waveSize`: a wave waits for its slowest unit, then for the retrospective and the commit. The barrier is not needed for file safety; it exists so that each wave's lessons reach the next wave and each commit holds finished units. Larger waves trade some of that learning for speed.
- Agents never use git to write, except the Committer, who never amends, rebases or force-pushes.
- Builds go to private output directories under the state directory.
- Content is edited, not rewritten from scratch; removals are recorded with reasons; line endings and encodings are preserved.
- Nobody may invent facts, citations, results or dates; unverifiable material is reported, not written. Editors only reword; any new or changed claim after acceptance is a regression.
- The guidelines are never edited by the committee.

## Cost

A unit costs about 25 to 35 agent calls with the default roster (`prepare_run.py` prints its estimate for the actual roster); a whole-document unit with eight lenses costs more per round but there is only one. A workflow run is capped at about 900 agent calls, so `prepare_run.py` defers what does not fit to the next run. Shards change how fast the calls are made, not how many there are. Token use is dominated by agents reading the rules and the unit, so long units and long guidelines cost more. Reduce cost with fewer readers or lenses, a lower `limits.maxRounds`, cheaper models for lenses that rarely find problems, or smaller stages.
