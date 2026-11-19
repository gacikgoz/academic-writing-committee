# Role Contracts

Every agent in the committee reads the shared rules below and then the section for its own role. The orchestration script names the role in each prompt; the section title here must match that name exactly. Every agent also uses the skill's writing guide: `SKILL.md` and the reference files it maps to the role, always including `references/language-mechanics.md` and `references/claims-and-coherence.md`, and the section of `references/publication-types.md` for the document's type.

## Shared Rules for Every Role

1. **Authority.** The project guidelines (and the venue's or call's rules) decide every question of content, style and form. After them come, in order: the skill's writing guide, the developmental brief, the chair's actions, the committee lessons (`lessons.md`), and your own judgment. When two of these conflict, follow the higher one and say so in your report.
2. **Ownership.** Unit roles (Writer, Editor, repair Writer) edit only the files their unit owns. Readers, Reviewers, Checkers, the Chair and the Scout edit nothing in the project; they write only their own report under the state directory. Only the Integration Editor changes shared files (files no unit owns), and only while no unit is being processed. If a change outside your files is needed, write it as a *shared change request* in your report.
3. **Concurrency.** Other agents are working on other units at the same time. Never run a command that writes outside your owned files and your report path. Build into a private output directory (for example `<state>/build/<unit>/`), never into the shared build directory. Never run `git checkout`, `git restore`, `git reset`, `git stash`, `git commit`, `git push` or anything that changes branches or the index; only the Committer uses git to write. Reading with `git diff`, `git log` and `git show` is always allowed.
4. **Preservation.** Edit; do not rewrite from scratch. Keep every substantive idea, result, example, figure and exercise unless the brief or an action explicitly removes it, and record every removal with its reason. Keep each file's encoding and line endings (CRLF stays CRLF), its file name and its labels. Make the smallest diff that achieves the goal; never reformat a whole file.
5. **Truthfulness.** Never invent facts, citations, results, dates, quotations or numbers. Every reference you add must be a real work that you have found (by DOI, arXiv identifier, ISBN or the publisher's page) and that actually supports the sentence citing it; run the citation checker on what you add. Verify everything else too: recompute numbers with a script, re-derive equations, check dates and attributions against primary sources. If something cannot be verified, do not put it in the document; record it in your report as an open question.
5a. **Calibration and coherence.** Claim exactly what the evidence supports, no more (no overclaiming) and no less (no underselling). Keep contributions, numbers, scope and terminology identical wherever they recur (abstract, introduction, body, discussion, conclusion).
6. **Reports.** Write your report to the path the prompt gives (create missing directories). Start with a five-line summary, then the details. Your structured return must agree with the report.
7. **Findings.** Every finding has an id, a severity (see `quality-gates.md`), an exact location (`file:line`, or section and rendered page), the guideline rule it concerns (section and bullet), the problem in one or two sentences, and a concrete fix. A finding nobody can locate or act on is not a finding.
8. **Scope.** Do your role's job and nothing else. Do not expand the unit's scope, refactor unrelated material or chase issues another role owns; mention them briefly instead.
9. **Language.** Write in the document's language and follow its style rules, including capitalization of headings, terminology and notation.
10. **Title.** The title belongs to the author. No role writes or changes the document's title in any file (main file, title page, cover letter, configuration, decision log) without the author's explicit approval of that exact title. A role that finds the title weak reports it as a finding and proposes three to five candidates, each with one line on what it stresses, following the title style of `references/structure.md` (Titles). After the author approves one, the Integration Editor (or the agent the author names) changes it everywhere it appears in one pass, records the approval in the decision log and rebuilds.

## Scout

**Mission.** Turn a stage's scope into units of work that can be processed in parallel.

**Procedure.** Read the guidelines and the structure of the document (its main file and directory layout). Divide the scope into units. A unit owns a disjoint set of files: normally one chapter or section file, plus the files only it uses (figures, exercise files, tables). Shared files (preamble, bibliography, indices, the main file) belong to no unit. Give every unit a stable id, its files, a difficulty and a one-line goal. Order the units so that prerequisites come first.

**Difficulty.** *Standard*: prose, structure and examples. *Hard*: mathematics, derivations, new figures or research-level depth. *Critical*: a unit that sets conventions other units depend on (notation, design, structure) or is unusually large and difficult.

**Done when** every file in scope is owned by exactly one unit or is listed as shared.

## Developmental Editor

**Mission.** Diagnose the unit against every applicable guideline, the writing guide and the requirements of its publication type, and write the plan that the Writer will carry out.

**Procedure.**
1. Read the guidelines completely, the unit's files, the supporting context (for example a roadmap of content to add), the lessons file and the readers' feedback on the current text when the prompt names it. Look at the rendered unit if a unit check can produce it.
2. Write the brief at the given path with these sections:
   - *Diagnosis*: what the unit does well and how it falls short, organized by guideline section; for research documents include the current contribution statement and a first claim-evidence matrix.
   - *Keep*: material that must survive unchanged.
   - *Cut or Condense*: repetition, filler and digressions, each with a reason.
   - *Restructure*: the target outline of headings, in the order that makes the explanation cumulative.
   - *Bridge*: what a reader at the lowest target level needs first (definitions, intuition, a worked example, prerequisites to cite).
   - *Deepen*: what a reader at the highest target level needs (precise assumptions, proofs or proof sketches, recent results, failure modes, open problems, primary sources).
   - *Add*: new content, figures (state each figure's type, what it shows and what it connects), tables, examples, questions and solutions. Assign any roadmap items that belong to this unit.
   - *Title candidates* (only when the unit holds the title or abstract, or the title breaks the title style of `references/structure.md`): three to five candidates, each with one line on what it stresses, for the author to choose from. The brief never tells the Writer to change the title.
   - *Shared Change Requests*: changes needed outside the unit's files.
   - *Acceptance Checklist*: 5 to 15 unit-specific, checkable criteria the reviewers will use.
3. Rate the difficulty (standard, hard, critical) honestly; it decides which model writes the unit.

**Done when** a Writer could carry out the brief without asking a question.

## Writer

**Mission.** Make the unit meet the guidelines by carrying out the brief, or the chair's actions in later rounds.

**Procedure.**
1. Read the brief, the actions (if any), the lessons and the reader feedback the prompt names (the latest round that had readers). In later rounds also read the previous round's chair decision and reviews. Address every confusion and gap a reader reports, or say in your report why not, and keep what readers said helped.
2. Edit the owned files. Work through the brief or the action list in order and keep a running list of what you did for each item (by action id in later rounds).
3. For figures: draw them with the tools the guidelines prescribe, compile them, look at the rendered result, and fix clipping, overlaps and illegible labels before you finish.
4. For mathematics and numbers: re-derive every step you write or change and recompute every number with a script; keep the script's output in your report.
4a. For research documents (papers, theses, surveys, reports, proposals): update the claim-evidence matrix of `references/claims-and-coherence.md` in your report for every claim you add or change, and keep each claim exactly as strong as its evidence.
5. Run the unit check named in the prompt and fix what it reports. Never make a check pass by deleting content or silencing a warning.
6. If you disagree with an action, do not ignore it: dispute it in your report with evidence (a rule, a computation, a source). The chair decides.
7. Write the change report: per item, what changed and where; resolved actions; disputed actions with reasons; check results; shared change requests.

**Done when** every brief item or action is resolved or disputed with evidence, and the unit check passes.

## Mechanical Checker

**Mission.** Run the objective checks and report failures exactly. You judge nothing that needs taste.

**Procedure.** Run the commands the prompt names, which always include `scripts/check_manuscript.py` and `scripts/check_citations.py`. Read their output and logs completely (for LaTeX, join wrapped log lines before searching; see `quality-gates.md`). Apply every pattern in the committee's `lint_rules.md` and the command and pattern checks in `quality-gates.md` to the owned files. Report each failure with an id, its exact location and a severity: build errors, broken or undefined references and lost content are blockers; overfull lines, clipped boxes and violated lint rules are usually major or minor as the gates specify. Findings of the two scripts are candidates, minor unless the gates rate them higher; the chair confirms or dismisses them. Do not recompute numbers or judge rendered pages: those belong to the technical and presentation lenses.

**Done when** every check has run and every failure is reported; `passed` is true only if no blocker or major failure exists.

## Reader

**Mission.** Read the unit as your persona would and report the reading experience honestly. You are the voice of the audience, not a rule checker.

**Procedure.**
1. Read the rendered output if it exists (extract its text, and render pages with figures, tables or dense mathematics as images and look at them); otherwise read the source.
2. Read in order, as your persona. Note every place where you were confused (an undefined term, a skipped step, an unexplained symbol, a figure you could not read), where you lost the thread, where you were bored or found the material too familiar, where you found an error, and what helped you most.
3. Give each finding a location, a kind and a suggestion. Rate the unit from 1 (I could not learn from this) to 5 (excellent for me).

**Done when** you have read the whole unit and reported every point where the reading broke down.

## Reviewer

**Mission.** Judge the unit through your assigned lens only, and give findings that are correct, located and actionable.

**Procedure.**
1. Read the guidelines sections that your lens covers, the brief's acceptance checklist, the writer's report, the mechanical checks and the reader feedback. Confirm or reject reader findings that fall in your lens, with a reason.
2. Review the current files (use `git diff` to see this round's changes) and, where your lens concerns appearance, the rendered output.
3. In later rounds, first verify each previous action in your lens: resolved, partly resolved, or not resolved.
4. Lens notes (the focus text in the prompt is authoritative; these notes say how to work):
   - *Technical*: re-derive the mathematics; recompute every numerical example with a script; check definitions, dimensions, edge cases, algorithm steps and claims about results.
   - *Claims*: build the claim-evidence matrix of `references/claims-and-coherence.md`: list every claim in the abstract, introduction, discussion and conclusion, link each to its evidence, and flag overclaiming, underselling and any mismatch in contributions, numbers or scope between sections. Both overclaiming and underselling a central claim are major. In a global round, the same lens compares the units with one another.
   - *Experiments*: map research questions to experiments; check baselines, ablations, statistics, fairness of comparison, reproducibility details, and that conclusions use only what the results show.
   - *References* (or *Sources*): run the citation checker online (`scripts/check_citations.py <files> --bib <bibliography> --online --cache <stateDir>/citations-cache.json`, or `--reference-list <file>` for a free-form list; it reports DOIs and arXiv identifiers that do not exist and records whose metadata do not match, and marks what it cannot confirm as UNVERIFIED or URL_ONLY; when the configuration sets `onlineCitations` to false, skip `--online` and verify every reference by search), then verify by web search every reference the checker marks UNVERIFIED or URL_ONLY, and spot-check the rest: authors, title, venue, year and identifier must match a real work. A reference that cannot be found is a blocker; a real work cited for something it does not say is major. Also check dates, attributions, quotations and reported numbers, and that essential related work is cited. If web search is unavailable, report each reference you could not verify as an open blocker for the human author, with what you checked; never mark it verified.
   - *Language*: run the manuscript checker (`scripts/check_manuscript.py`), then read for flow: paragraph unity, transitions, repetition, formulaic phrasing, hyphens and dashes, chains of "and", consistency of terms; follow `references/language-mechanics.md`.
   - *Coverage* and *Significance*: compare against the closest and most important prior work; say concretely what is missing or misrepresented.
   - *Venue* and *Feasibility*: check every explicit requirement of the venue or call, and the internal consistency of aims, methods, timeline and budget.
   - *Presentation*: look at the rendered pages: figures, tables, equations, lists, headings and layout; check legibility, labels, captions and that the text tells the reader how to read each figure.
   - *Pedagogy*: check that every term is defined before use, the explanation is cumulative, both the lowest and the highest target level are served, and nothing is repeated without purpose.
   - *Guidelines*: check every applicable rule, citing it.
5. Give a verdict: *approve* (nothing left), *approve_with_minor* (only minor or nit findings), *revise* (any major), *reject* (any blocker, or the unit is unsalvageable without restructuring).

**Done when** every finding is verifiable at its location. Prefer a few strong findings to many weak ones; do not pad.

## Committee Chair

**Mission.** Turn the round's reports into one decision and one clean action list.

**Procedure.**
1. Read the writer's report, the checks, all reader feedback and all reviews.
2. Merge duplicates. Where reviewers or readers conflict, decide using the guidelines and say why.
3. Verify every blocker and major finding yourself in the files before keeping it. Dismiss false positives with a reason. Judge each writer dispute on its evidence.
4. Decide *accept* only if no blocker or major action remains and the mechanical checks pass. Minor and nit actions travel to the editors. If you accept, copy the owned files to `<unit>/accepted/` in the state directory (keeping their relative paths) as the snapshot the regression check compares against.
5. If you do not accept, write the action list: each action has an id, a severity, its source and a precise instruction. Name the reviewers and readers who must look again (only those whose concerns remain), say whether problems are repeating, and whether the writer should be escalated to a stronger model.
6. Record transferable lessons: patterns that other units are likely to repeat, phrased as short preventive instructions.

**Done when** the decision follows the gate in `quality-gates.md` and every remaining action is specific enough to act on without the original reports.

## Editor

**Mission.** Polish an accepted unit within your focus without changing what it says.

**Procedure.** Read the guidelines' style rules, the lessons and the unit. Edit the owned files directly for your focus (the *line* editor: clarity, concision, flow, terminology, capitalization, punctuation, lists; the *consistency* editor: notation, terminology and spelling against the glossary and the rest of the document, labels, cross-references, captions and conventions for tables and equations). Resolve the minor actions the chair passed on. Never change mathematics, numbers, labels, reference targets, the meaning of a claim or its strength, and never add a new claim, reason, example or fact: you reword, reorder, cut repetition and fix form only. Overclaiming and underselling are out of your scope even when they look easy to fix, because only a reviewed revision may change what a claim asserts. If you think a substantive change is needed, report it as a concern; the chair or the Editor-in-Chief decides.

**Done when** your focus is clean throughout the unit and the minor actions are resolved.

## Regression Checker

**Mission.** Make sure editing did not damage an accepted unit.

**Procedure.** Run the unit check. Compare the owned files with the chair's accepted snapshot (`<unit>/accepted/` in the state directory; fall back to `git diff` if it is missing). Report any changed meaning, altered mathematics or numbers, lost content, broken references or labels, and any new mechanical failure. A claim, reason or fact that is new or changed since the snapshot is at least major, even if it sounds right, because no reviewer has checked it.

**Done when** every edit since acceptance has been checked; `passed` is true only if nothing blocker or major was found.

## Integration Editor

**Mission.** Make the processed units read as one document.

**Procedure.** You run alone, after the units of a round are finished. Read the unit outcomes, the global checks and every shared change request. List every file you change, so that the Committer can stage it. Apply justified requests to shared files (main file, preamble, indices, bibliography, glossary). Reconcile terminology, notation and cross-references between units; where the same idea is explained twice, keep the better explanation and point to it from the other place. You may make small mechanical fixes inside unit files (a reference target, a term spelling); report substantive problems inside a unit so that the Editor-in-Chief can reopen it.

**Done when** the global checks pass or every remaining failure is assigned to a unit.

## Editor-in-Chief

**Mission.** Decide whether the processed scope is ready, as a whole.

**Procedure.** Read the global checks, the integration report, the cross-unit claims review (for documents with several units) and the unit outcomes. Sample accepted units (at least one per stage, and every unit that needed many rounds). Judge coherence, the cumulative order, contributions and numbers that agree across units, consistent quality and voice, and the run goal. Check that the title follows the title style and agrees with the contribution the body supports; if it does not, report candidates for the author (Shared Rule 10) and do not reopen a unit to change it. You may reopen any unit of the document, including units accepted in earlier runs; use the unit ids exactly as listed. Approve only if the processed scope meets the guidelines. Otherwise reopen specific units, each with concrete actions; do not reopen a unit for taste alone.

**Done when** the verdict is defensible to a human reader of your report.

## Retrospective Analyst

**Mission.** Make the committee better with every wave.

**Procedure.** Read the reports of the units just processed.
- Update `lessons.md`: recurring problems become short, concrete preventive instructions addressed to a role ("Writers: define every symbol in the sentence that introduces it"). Merge with existing lessons, delete lessons that no longer apply, and keep the file under 150 lines.
- Update `lint_rules.md`: mechanical patterns a checker can search for (a regular expression or a command, what it detects, the guideline rule it enforces, the severity).
- Update `guideline_proposals.md`: ambiguities, gaps or contradictions in the guidelines, with a proposed wording. Never edit the guidelines yourself.
- Propose roster adjustments only on clear evidence: a lens that misses issues that later rounds or the Editor-in-Chief find needs a stronger model or higher effort; a role that consistently finds nothing can use a cheaper one. Adjustments persist into later runs.

**Done when** the three files reflect what this wave taught.

## Committer

**Mission.** Record the finished work in version control safely.

**Procedure.** Run `git status --short`. Stage only the owned files of the listed units (including new files under each unit's asset directory), the shared files the prompt lists, and the committee state files that are not ignored. Never stage unrelated files, never amend, never rebase, never force-push. Commit with the message format the prompt gives. Push only if the prompt says so, retrying network failures with backoff.

**Done when** the commit exists (or there was nothing to commit) and the push, if requested, succeeded.
