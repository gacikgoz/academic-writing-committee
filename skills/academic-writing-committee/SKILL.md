---
name: academic-writing-committee
description: Writes, revises, reviews, and checks academic documents of every type (books, book chapters, journal articles, conference papers, surveys, theses, technical reports, grant proposals, and lecture notes), and runs a self-improving multi-agent committee of writers, readers, reviewers, and editors over a whole manuscript; with --no-committee (or "no committee") it works as a plain single-session academic-writing skill. Use when drafting or revising academic prose; fixing dashes, repetition, or flow; calibrating claims; checking that references are real; peer review or responding to reviewers; a committee review; choosing a venue or preprint server; open-access and funder mandates (Plan S, Nelson Memo); reporting guidelines (CONSORT, PRISMA); authorship (CRediT, ORCID); preregistration; AI-use disclosure; or grant proposals.
---

# Academic Writing Committee

This skill produces academic text that is accurate, clear, fluent, and honest about its evidence, for any publication type. It has four modes, and a no-committee option that keeps it to plain single-session academic writing. This file gives the principles, the process, and quick checklists; `references/` holds the detail, `profiles/` the committee defaults per publication type, `committee/` the multi-agent committee, and `scripts/` the checkers. Paths below are relative to this skill's directory, `${CLAUDE_SKILL_DIR}`.

**Order of authority.** The venue's current instructions and the project's own guidelines come first, then the field's conventions, then this skill. Numbers given here (lengths, counts, proportions) are starting points, not rules.

## Start Here: The Guided Flow

The user should never need to know the modes, the flags or the configuration format. Drive the work with what the project already says and a few questions; never ask what the repository answers.

1. **Small, local requests need no setup.** A sentence, a paragraph, a section the user points to, a question about style: do it in Write mode at once, with the checkers on what changed. Ask nothing unless the request is ambiguous.
2. **For anything about a whole document** (revise, review, check, "help me with my paper"), first run, silently:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/project_setup.py detect --json
   ```
   It reads the project without changing it. It reports the main document, its class and venue, a publication-type guess with its confidence, chapters, the bibliography, guideline and context files, a build command, an existing committee configuration and its ledger, git state and installed tools. It also lists the questions that remain open. Take every detected value as known and say it back in one or two lines ("A NeurIPS paper, main.tex, 42 references in refs.bib, no guidelines file").
3. **An existing configuration means a run is under way.** Continue it: print `prepare_run.py <config> --status` in two or three lines, ask only what the configuration lacks (size, effort), and resume. Do not set up again.
4. **Ask the open questions with the question tool, in one batch.** That is at most four questions with at most four options each, the recommended option first and marked "(Recommended)". Order them by how much the answer changes:
   - **The task**, if the request does not make it clear: revise with a committee, revise in this session without one, review only (a report, no edits), or check references and language.
   - **The publication type**, only when the confidence is not high: offer the guess first.
   - **The goal**: submission to the detected venue, meeting the detected guidelines, or clearer prose without changing the content.
   - **The guidelines**, only when none were found.
   - **For a committee: the size and the effort** (sizes `low`, `medium`, `high`, `full`; effort `high`, `medium`, `xhigh`, `low`, with `max` and `default` accepted as Other). If they do not fit in the first batch, ask them in a second, never in a third.
5. **Write the configuration from the answers** without showing JSON, unless the user asks:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/project_setup.py init --type T --size S --effort E --goal "..." [--guidelines f.md]
   ```
6. **Go.** Run the preflight of `committee/procedure.md`, prepare the run, state the plan in three lines (units, committee, estimated agent calls), and launch. Answers given in this flow count as the user's request for a multi-agent run; do not ask for a separate confirmation. Without the Workflow tool, say so in one line and continue without a committee.

Problems the detection reports (no git repository, uncommitted changes, a missing build tool) are raised once, with the fix, at the point they matter: before the first committee run, not before a single-session task.

## Modes

| Mode | When | What to do |
|---|---|---|
| **Write** | Draft, revise, or polish text | Identify the publication type and stage, read the references the task needs (routing below), and edit the actual text. Then run `check_manuscript.py` on what changed, and `check_citations.py` when the text cites a bibliography, and fix what they find. |
| **Review** | Judge a manuscript without changing it | For a quick review, follow `references/review-and-revision.md` and report findings by severity. For an independent committee review, prepare a run with `scripts/prepare_run.py <config> --review-only` and launch the committee workflow (below); the type's readers and reviewer lenses work in parallel, and the chair consolidates a prioritized report. Nothing in the document changes. |
| **Committee** | Bring a whole document up to its guidelines | Start with the guided flow above, then follow `committee/procedure.md`: preflight, prepare, launch, record, verify, and continue until every unit and the whole document are approved. |
| **Check** | Mechanical audit | Run `scripts/check_manuscript.py` and `scripts/check_citations.py` (below); confirm each finding in context before changing anything. |

Responding to reviewers runs in Write mode, and writing a review report as a reviewer runs in Review mode; both use `references/review-and-revision.md`.

## No-Committee Option

The skill can always run as plain academic writing, with no committee: one session, no subagents, and no Workflow tool. Use this option when the request contains `--no-committee` or "no committee" (or "without a committee", "single session"), when the user invokes `/academic-writing-committee:no-committee`, or when the Workflow tool is not available. With the option on:

- **Write** and **Check** run exactly as in the table above; they never use the committee.
- **Review** is the quick review of `references/review-and-revision.md`: read the manuscript yourself, report findings by severity, and change nothing. Do not run `prepare_run.py` or launch a workflow.
- **Committee** becomes a single-session revision. Work through the document one unit at a time (a chapter or section, in reading order) as in Write mode, against the project's guidelines when it has them. For each unit, read it as a newcomer and as a referee would, revise it, run both checkers and the project's build, and fix what they find before moving on. Keep the author's text where no rule requires a change. Nothing is written to the committee's ledger.
- The principles, the four standards, the process, the checklists and the checkers below apply unchanged.

Say once, at the start, that the run is without a committee.

## Committee Runs

Review and committee runs use the Workflow tool, so they need the user's explicit request for a multi-agent run. A request to use this skill's committee or review mode counts as that request, unless it asks for no committee. State the plan and the expected number of agents before launching.

**Committee size.** A committee run has four sizes: `low` (one reader, two lenses, the line editor, at most 2 rounds per unit, a two-tier writer ladder Sonnet → Sonnet, every role on Sonnet or below), `medium` (one reader, three lenses, the line editor, at most 3 rounds, writers Sonnet → Opus → Opus, every role on Opus or below, the Editor-in-Chief included), `high` (two readers, five lenses, both editors, at most 4 rounds, writers Sonnet → Opus → Fable → Fable) and `full` (the whole profile of the publication type, the default). Each unit has one writer per round, starting on the tier its difficulty sets. The user chooses the size in words ("a medium committee"), with `--size` on the commands, or with `committeeSize` in the configuration; `prepare_run.py --size` applies it, and `committee/sizes.json` defines it.

**Effort: always ask.** Before preparing a committee run or a committee review, ask the user which effort level the committee should work at, unless they already named one (in the request, with `--effort` on the commands, or as `effort` in the configuration). Ask once, as one question in the guided flow's batch, with these options: `high` (recommended for most work), `medium`, `xhigh`, `low`, and accept `max` or `default` (each role keeps its own effort) as Other. Say briefly what changes: more effort means more careful work, more tokens and slower runs. If the size is not settled either, ask for both in the same message. Pass the answer with `prepare_run.py --effort`. Every role then runs at that effort except the mechanical checker and the committer; the last writer tier runs one level higher. Never choose an effort for the user, and do not ask again for later runs of the same task.

## Publication Types

Name the type, its primary judge, and the judge's decision before planning or revising. `references/publication-types.md` gives, for each type, its purpose and readers, structure, length, what judges look for, typical failures, and the committee configuration; `profiles/<type>.json` holds the committee defaults.

| Type | Judged by | Central question | Profile |
|---|---|---|---|
| Journal article | Editor and reviewers | Is it sound, new, and complete? | `journal-article` |
| Conference paper (full, short, workshop) | Program committee | Is the contribution clear and convincing within the page limit? | `conference-paper` |
| Survey, systematic review, tutorial | Editor and reviewers | Is the coverage complete, organized, and accurate? | `survey` |
| Thesis or dissertation | Examiners | Is it original, substantiated, and coherent? | `thesis` |
| Book (textbook or monograph) | Publisher, reviewers, adopters | Does it teach or argue cumulatively? | `book` |
| Book chapter | Volume editors | Is it self-contained and authoritative? | `book-chapter` |
| Lecture notes | Students and instructor | Can a student learn from them alone? | `lecture-notes` |
| Technical report or white paper | Practitioners | Is it accurate and actionable? | `technical-report` |
| Grant proposal | Review panel | Is it significant, new, and feasible? | `grant-proposal` |

## How to Work with an Author

- Before giving advice, establish what is missing from this intake. Ask one question at a time, starting with the one that changes the answer most:
  - [ ] Document type (paper, thesis chapter, textbook chapter, grant, review report, response letter).
  - [ ] Venue, call, or institution, and its rules.
  - [ ] Intended readers.
  - [ ] Stage: planning, drafting, revising, responding, or final checks.
  - [ ] Evidence and sources available, and the reporting guideline if one applies.
  - [ ] Confidentiality: whose material this is and what may be shared with tools.
- Work on the actual draft. Generic section advice is a fallback for when there is no text yet.
- Edit to improve, not to replace. Keep the author's voice, terminology, and claims unless they are the problem, and say why each substantive change helps.
- Never change what a sentence claims while polishing it. If a claim looks wrong or unsupported, flag it; do not quietly strengthen, weaken, or "fix" it.
- Put missing facts in visible placeholders such as `[[TODO: sample size]]`. Never fill a gap with plausible text.
- The human authors decide and are accountable. Present analysis and options; mark what you verified and what you did not.

## Core Principles

1. **Accuracy before fluency.** A fluent sentence is not evidence. Keep observation, estimate, interpretation, and speculation distinct.
2. **Nothing invented.** No fabricated or guessed citations, identifiers, quotations, data, methods, approvals, author roles, or declarations. Missing information stays visibly missing.
3. **Claim strength matches the evidence.** Choose verbs by what the design supports: association is not cause, a nonsignificant result is not "no effect," and "the first" needs a documented search. Hedge once, where the uncertainty is, and not at all where the evidence is firm. Underselling a supported result is as wrong as overclaiming an unsupported one.
4. **Lead with the point.** The document, each section, and each paragraph open with their most important statement. A reader of the title, abstract, headings, first sentences, and displays should get the whole argument.
5. **One term, one meaning.** Each concept and each symbol keeps one name everywhere: text, equations, tables, figures, and captions.
6. **Explain, do not only report.** Give the mechanism or reason (the *because*) for each effect and each choice, and the boundary within which the claim holds.
7. **Report the whole record.** Include negative, null, and unexpected results, missing data, and deviations from the plan. Label analyses as confirmatory, exploratory, or descriptive.
8. **Every number is fully described.** Give its unit, denominator, sample, time point, and uncertainty, identical wherever the number appears.
9. **Limitations are specific.** Name the source of bias or imprecision and its likely direction; turn "more research is needed" into a stated boundary and the next test.
10. **Write for the adjacent-field reader.** Define terms at first use, prefer plain words, and use nothing before it has been introduced.
11. **Sources are real, opened, and supportive.** Every cited work exists, has been read, and supports the sentence that cites it.
12. **Confidential material stays where it is authorized.** Unpublished manuscripts, reviews, grant applications, and sensitive data do not go to outside services, AI tools included, without authorization.

## Four Standards Every Text Meets

Reviewers often raise these points. Each standard has a reference with the full rules, and a checker finds candidates.

**1. Language mechanics** (`references/language-mechanics.md`)
- Hyphen for compound modifiers before a noun ("a two-layer network"; "the network has two layers"), never after an *-ly* adverb ("a widely used method").
- En dash for ranges (pages 12–15, 2019–2023) and for pairs of equals (Kullback–Leibler, encoder–decoder); "from 5 to 10," never "from 5–10."
- Em dash rarely, at most about one pair per paragraph, closed up in American style, and only where a comma, a colon, or parentheses would not do. Never a hyphen, a spaced hyphen, or a double hyphen in its place. A true minus sign for negative numbers.
- No chains of *and*: at most two coordinated clauses; no "and also" or "and/or"; one serial-comma convention.
- No repetition: no content word three or more times in a short span, no runs of the same sentence opening, no stacked additive transitions ("Moreover ... Furthermore ... Additionally"). Technical terms stay fixed; vary only ordinary words.

**2. Fluency and coherence** (`references/language-mechanics.md`, `references/style.md`)
- Each paragraph has one point, stated first; each sentence follows from the one before; each transition names a real relation (cause, contrast, consequence, example).
- Read in sequence, the first sentences of the paragraphs give the argument of the section.
- No generic or formulaic phrasing ("plays a crucial role," "in today's rapidly evolving landscape"): say the specific thing.

**3. Calibrated claims and a coherent whole** (`references/claims-and-coherence.md`)
- No overclaiming: no unsupported superlatives, "proves" for empirical results, "state of the art" without dated evidence, or generalization beyond the conditions tested.
- No underselling: no stacked hedges, no contribution buried or left vague, no "merely" for a supported result.
- Questions, contributions, experiments, results, discussion, and conclusion line up one to one. Every contribution in the abstract and introduction has specific evidence in the body. The discussion and conclusion restate it without inflating it, and every claim in the conclusion traces to a result.
- Numbers, names, terms, and notation are identical wherever they recur.

**4. Real references** (`references/evidence-and-citations.md`)
- Cite only works you have found and opened. Check authors, title, venue, year, and identifier (DOI, arXiv identifier, ISBN, or publisher page) against the work itself.
- A reference that cannot be verified is removed or replaced with a visible `[[TODO: source for X]]`; the sentence it supported is narrowed, supported by other verified evidence, or marked unresolved for the author. A real work cited for something it does not say is as serious as a fake one.
- `scripts/check_citations.py --online` looks every reference up at Crossref, arXiv, doi.org, and DataCite. It reports DOIs and arXiv identifiers that do not exist (NOT_FOUND) and records whose metadata do not match; references it cannot confirm are UNVERIFIED or URL_ONLY and must be checked by search. It cannot tell whether a work supports its sentence, so open each reference you cite.

## Process

### 1. Plan

- Fix the venue or audience and record its rules: length, structure, citation style, required statements, and policies on preprints, data, and AI use (`references/publishing-and-grants.md`).
- State the question, the gap, and the contribution in one sentence each. If you cannot, the project is not ready to draft.
- Read three to five recent examples from the venue and note their structure, proportions, and voice.
- Search the literature and start the source ledger; support the gap with evidence (`references/evidence-and-citations.md`).
- Choose the reporting guideline for the study design, and settle authorship and contribution roles early (`references/integrity-and-ai.md`).
- Plan the figures and tables; they are the frame of the document (`references/figures-and-tables.md`).

### 2. Outline

- Write the outline as a specification: headings to the third level, a target length for each part, the point each part makes, and the evidence and sources it will use (`references/structure.md`).
- Outline only from evidence you have. Park unsupported ideas in an open-issues list.
- For a long document, order the material by dependency and record what each chapter assumes and provides. Start a term and notation sheet.
- Review the outline as a referee would and fix the weak points before drafting.

### 3. Draft

- Draft the concrete parts first: methods, then results and displays, then the introduction, discussion, and conclusion. Write the abstract and title last. For argumentative work, draft the introduction first to fix the thesis, and expect to rewrite it.
- Before each section, reread its outline entry and the end of the previous section.
- Separate drafting from editing. A complete rough draft is worth more than a polished fragment.
- Keep placeholders for missing facts and citations, and add sources to the ledger as you use them.
- Describe methods as they were performed, and present results in the order of the questions.

### 4. Revise

- Revise in passes from large to small: structure, argument, evidence, clarity, style, format (`references/review-and-revision.md`).
- Run the diagnostics: the topic-sentence ladder, a reverse outline, a label audit, the *because* check, the claim-evidence matrix (`references/claims-and-coherence.md`), and a reread as a skeptical referee.
- Fix prose with `references/language-mechanics.md` and `references/style.md`; fix mathematics, numbers, and statistics with `references/mathematics-and-notation.md`.
- For a long document, run the coherence pass across chapters: terminology, notation, dependencies, and promises kept.
- Get a reader who has not seen the draft; self-assessment misses what the writer already knows. The committee's reader personas serve this purpose.

### 5. Verify

- Open and check every source, and audit the citations against the reference list.
- Reconcile every number across abstract, text, tables, figures, and supplement; trace denominators through each stage.
- Check each claim in the abstract and conclusion against the result that supports it.
- Complete the reporting-guideline checklist and every declaration from records.
- Confirm that code and data reproduce the reported results, especially where an assistant helped write code.
- Run the checkers in `scripts/`.

### 6. Finalize

- Resolve every placeholder, comment, and tracked change.
- Convert to the venue's template, then recheck citations, cross-references, symbols, tables, and figures in the rendered output.
- Write the AI-use disclosure and other statements in the venue's wording and place.
- Prepare the cover letter and any checklist, and have every author approve the final files.
- After a decision, answer reviewers point by point, changing the manuscript and not only the letter.
- After publication, deposit the permitted version, archive data and code, and correct errors openly.

## Quick Checklists

### Paragraph

- [ ] The first sentence states the point; the rest support it; the last hands over.
- [ ] One idea, one term per concept, no term used before it is defined.
- [ ] Every doubtful claim has a source or is the document's own result.
- [ ] Verbs match the evidence; at most one hedge per claim.
- [ ] No filler openers, no chains of *and*, no repeated opening words, no "significant" without a statistic.

### Section

- [ ] The section does the job its place in the structure requires, and nothing else.
- [ ] The first sentences of its paragraphs, read alone, give its argument.
- [ ] Results are separate from interpretation, unless the venue merges them.
- [ ] Each effect has a mechanism; each limitation is specific.
- [ ] Each figure and table is introduced before it appears and has a caption that stands alone.

For the whole document, use the Final Coherence Checklist in `references/claims-and-coherence.md` and the Checklist in `references/language-mechanics.md`. Before submission, use the Author's Final Audit in `references/review-and-revision.md`; for a response letter or a review report, use the checklists in the same file.

## Routing by Task

Every task also reads `language-mechanics.md` (which governs punctuation and repetition) and `claims-and-coherence.md` (which governs claim strength). All files are in `references/`.

| Task | Read |
|---|---|
| Any document, at the start | `publication-types.md` (its type: readers, judges, structure, length, failure modes, committee setup), then the rows below |
| Journal or conference paper | `structure.md`, `style.md`, `figures-and-tables.md`, `mathematics-and-notation.md` as needed, `review-and-revision.md`; `evidence-and-citations.md`, `integrity-and-ai.md`, and `publishing-and-grants.md` before submission |
| Survey or systematic review | `structure.md` (Review Articles), `evidence-and-citations.md`, `style.md`, `integrity-and-ai.md` (reporting guidelines such as PRISMA) |
| Thesis or dissertation chapter | `structure.md` (Theses and Dissertations), `style.md`, `review-and-revision.md` (Coherence Pass for Long Documents), `mathematics-and-notation.md` as needed |
| Book, book chapter, or lecture notes | `structure.md` (Textbooks and Lecture Notes), `style.md`, `figures-and-tables.md` (Figures in Teaching Texts), `mathematics-and-notation.md` |
| Technical report | `structure.md` (Technical Reports), `style.md`, `figures-and-tables.md` |
| Grant proposal or resubmission | `publishing-and-grants.md` (Grant Proposals, Budget Justification), `style.md` |
| Prose: sentences, word choice, paragraphs, voice, and tense | `style.md` |
| Overclaiming, underselling, contributions that do not match the results | `claims-and-coherence.md` (Calibration Ladder, Claim-Evidence Matrix) |
| Citations: searching, establishing a gap, verifying, citing | `evidence-and-citations.md` (the source ledger and the claim-evidence ledger record the sources behind each claim; the matrix in `claims-and-coherence.md` compares its wording across sections) |
| Figures, tables, image integrity, alt text | `figures-and-tables.md` |
| Notation, equations, proofs, algorithms, statistics | `mathematics-and-notation.md` |
| Reviewing a manuscript | `review-and-revision.md` (Reviewing a Manuscript), `mathematics-and-notation.md` (Statistical Review Checklist) |
| Responding to reviewers, a committee, or a panel | `review-and-revision.md` (Responding to Reviewers) |
| AI use and disclosure, authorship (CRediT, ORCID), confidentiality, reporting guidelines (CONSORT, PRISMA), preregistration | `integrity-and-ai.md` |
| Venue choice, predatory venues, preprints, identifiers, open access and funder mandates (Plan S, Nelson Memo), cover letters | `publishing-and-grants.md` |

## Checkers

Both scripts use only the Python standard library and never modify their input. Their findings are candidates for review, and a clean report proves nothing about correctness: the language reviewer and the line editor still read the text.

```bash
# Prose mechanics and claim wording in Markdown, LaTeX, or plain text
python3 ${CLAUDE_SKILL_DIR}/scripts/check_manuscript.py paper.tex
python3 ${CLAUDE_SKILL_DIR}/scripts/check_manuscript.py chapters/*.tex --min-severity warning

# Citation keys and bibliography entries (BibTeX or CSL JSON), with online verification
python3 ${CLAUDE_SKILL_DIR}/scripts/check_citations.py paper.tex --bib refs.bib --online --cache refs-cache.json

# A free-form reference list (LaTeX \item or \bibitem, Markdown or text) without a database
python3 ${CLAUDE_SKILL_DIR}/scripts/check_citations.py --reference-list references.tex --online

# Cited keys against the source ledger: a CSV with the columns key and status (status starts
# with "verified" once the source was opened) and an optional locator column
python3 ${CLAUDE_SKILL_DIR}/scripts/check_citations.py paper.tex --bib refs.bib --ledger sources.csv
```

Run either with `--help` for its options. Both accept `--json`, and both exit with status 1 when they report an error-level finding.

## The Writing Committee

For a long document, or whenever the user asks for writers, readers, reviewers, and editors, run the committee. It divides the document into units with disjoint files. Reader personas read each unit first, and a developmental editor writes its brief. A tiered writer (Sonnet, then Opus, then Fable as problems persist) revises the unit. Each revision then passes a mechanical checker on Haiku (the project's build plus `check_manuscript.py` and `check_citations.py`), the reader personas and reviewer lenses of the publication type, and a committee chair who verifies the findings and decides. Accepted units go to the line and consistency editors and a regression check. In each global round the checkers run over the whole document, an integration editor reconciles the units, a cross-unit claims review compares contributions and numbers, and an editor-in-chief approves or reopens units. Lessons, learned lint rules, and roster changes from each wave feed every later agent and every later run.

| File | Contents |
|---|---|
| `committee/procedure.md` | The procedure to follow, step by step, including resuming and cost |
| `committee/roles.md` | Every role's contract and the shared rules (authority, truthfulness, calibration) |
| `committee/quality-gates.md` | Severity levels and the gates a unit must pass |
| `committee/models.md` | Models, effort levels, and committee size by publication type |
| `committee/config.md` | The project configuration file, `writing-committee.json` |
| `committee/catalog.json` | Every reader persona, reviewer lens, and editor |
| `profiles/*.json`, `templates/*.json` | Committee defaults per publication type, and example configurations |
| `scripts/project_setup.py` | `detect` reads what the project already says (document, type, venue, chapters, bibliography, guidelines, build, an existing run) and lists the open questions; `init` writes the configuration from the answers |
| `scripts/prepare_run.py` | Expands units, applies the profile, writes the workflow arguments, records results (`--review-only` for a review, `--shards K` for several workflows at once, `--plan-only` for briefs ahead of the revision) |
| `workflow/committee.js` | The committee workflow, launched with the Workflow tool |

## Sources and Licenses

This skill is a synthesis, in new wording, of several MIT-licensed academic-writing skills, with original additions where they were silent. `SOURCES.md` lists them and what was drawn from each; `LICENSES/` holds their license texts.
