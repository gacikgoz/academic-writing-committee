# Document Structure

How to organize papers, theses, textbooks and lecture notes, review articles, and reports. Grant proposals are in `publishing-and-grants.md`. Page and word counts here are starting proportions; the venue's instructions and three to five recent examples from the venue decide.

## Contents

1. Choosing a Structure
2. Narrative Order and Saying It Once
3. Titles
4. Abstracts
5. Introductions
6. Related Work
7. Methods
8. Results
9. Discussion, Limitations, and Conclusions
10. Conference Papers in Computing
11. Argumentative Papers
12. Position Papers and Short Papers
13. Review Articles
14. Technical Reports
15. Theses and Dissertations
16. Textbooks and Lecture Notes
17. End Matter

## Choosing a Structure

| Document | Default skeleton |
|---|---|
| Empirical paper | Introduction, Methods, Results, Discussion (IMRaD), with abstract and end matter |
| Computing conference paper | Introduction, Background and Problem, Approach, Experiments, Related Work, Conclusion |
| Argumentative or theoretical paper | Introduction, positions and their limits, argument chapters, objections, conclusion |
| Review article | Introduction, review method, thematic sections, cross-cutting synthesis, open problems |
| Technical report | Summary, purpose and scope, body organized by the system or study, recommendations, appendices |
| Thesis | Introduction, background or literature, core chapters, general discussion, conclusion |
| Textbook chapter | Motivation, objectives, cumulative exposition with worked examples, summary, exercises |

IMRaD is a default, not a law: study design, the reporting guideline, the article type, and the venue can each change it. Whatever the skeleton, three properties hold:

- **Skim test.** A reader of the title, abstract, headings, first sentences of paragraphs, and displays knows what was done, why it matters, and what is new.
- **Hourglass.** Open broad (why this matters), narrow to the precise question and evidence, and widen again to what it means.
- **Parallel thread.** Each claim appears in the same words wherever it recurs: question, hypothesis, method, result, discussion. Number research questions or hypotheses and answer each by number.

## Narrative Order and Saying It Once

A finished paper reads as a research paper, not as a lab ledger or an evidence audit. Its reader wants to know the problem, the idea, how the idea works, and what was found. How the evidence was kept is the business of the record behind the paper, and it reaches the text only where a reader needs it.

- **Narrative order.** Problem, idea, method, implementation, case study or evaluation, results, discussion. A research paper in another field keeps the same arc in its own skeleton (IMRaD above).
- **Section openings.** Each section opens with one or two sentences that say what it does and how it follows from the previous one: "With the queue model defined, this section shows how the scheduler uses it to reserve slots." Nothing longer; a roadmap of every subsection is not needed.
- **One idea per paragraph, connected.** Each paragraph states its point first and hands over to the next (`language-mechanics.md`, Fluency and Coherence). Terms, numbers, and claims are identical wherever they recur (`claims-and-coherence.md`).
- **Say each thing once.** Each fact, caveat, limitation, definition, and claim has one best place: the definition where the term is first needed, the result in the results, the limitation in the Limitations subsection. Elsewhere use a short pointer ("the reserve size of Section 3.2") or nothing. The abstract, introduction, and conclusion summarize the same work at different depths (`claims-and-coherence.md`, Agreement Across Sections); they do not copy sentences from one another or from the body, and no paragraph repeats another.
- **One Limitations subsection.** Collect the limitations in one compact subsection, usually at the end of the discussion. Each names the threat, its likely direction, and the boundary it sets (Discussion, Limitations, and Conclusions, below). At the claim itself, keep only the qualifier the claim needs, in a few words ("on the four clusters tested"), with a pointer if the reader needs more. The same caveat is not restated in the introduction, the results, the discussion, and the conclusion.
- **Where provenance goes.** Versions, run identifiers, which script computed which number, counts of files, and archive locations belong in the data or code availability statement, a supplement, or the evidence record (house rule R6 in `language-mechanics.md`). The evaluation may carry one plain sentence on where its numbers come from: "All results come from one set of runs on the public traces listed under Data availability." The rest of the text says what was done and found, not how it was recorded.
- **Plain words for the work, not the bookkeeping.** "Committed," "archived," "recorded run," "run family," "static reading at one revision," a repeated label such as "secondary analysis," "ledger," "the provenance of each number," and an evidence-level tag after every claim make a paper read like an audit. Say what happened instead: "we measured," "a second analysis of the same runs," "reading the source code."
- **Readable in one pass.** Short, clear sentences; each term of art explained once, at first use, so that an engineer from a neighboring field can follow; a concrete example where an abstract description would make the reader work.

| Ledger | Paper |
|---|---|
| "The recorded run family, committed and archived at one revision, yields a median latency of 41 ms (evidence level: measured)." | "On the four test clusters, the median latency was 41 ms (Table 2)." |
| The single-workload caveat in the introduction, the results, the discussion, and the conclusion | the caveat once, in Limitations; "on one workload" at the headline claim |
| "Section 5 reports a secondary analysis of the archived outputs, computed by the analysis script over 212 files." | "Section 5 analyzes the same runs a second way, by error type." |

All values in the table are illustrative.

**How to check.** Read only the first sentence of each section: together they should tell the story in order. Build a repetition map: list each fact, caveat, limitation, definition, and headline claim with every place it appears, and choose the one place it stays. `scripts/check_manuscript.py` reports sentences repeated across paragraphs, sections, or files (`CROSS_SECTION_REPEAT`) and paragraphs dense with audit vocabulary (`LEDGER_LANGUAGE`); a reader still has to find the paraphrased repeats.

## Titles

- Name the subject and the contribution or finding in the fewest words that stay specific. Put the key terms a searcher would type near the front.
- Claim no more than the paper supports: no causal verb for an association, no population wider than the sample, no "novel" or "first" without evidence (`claims-and-coherence.md`).
- Name the design when the field expects it ("a randomized trial," "a systematic review").
- Avoid questions the paper does not answer and puns that hide the topic. A title-and-subtitle form works when the first part states the topic and the second the approach or result.

### Title Style (House Rules)

These rules are the skill's defaults for the title of an article, report or thesis; a venue's instructions or the project's guidelines may override them.

- **T1. Short and striking.** A title is a name, not a descriptive homework sentence. When the work has a system name, prefer the form *Name: what it does for whom*.
- **T2. Lead with the method and the contribution, and name the domain.** In applied artificial intelligence, the method and the artificial intelligence contribution come first and the application domain is named. Do not shrink the contribution to one component ("tool use" when the system orchestrates several integrated systems), and do not name only one stage ("Deriving ...," "Training ...") when the contribution is a whole pipeline.
- **T3. No abbreviations or acronyms.** Write "Graph Neural Network," not "GNN." A system name is allowed when the subtitle makes clear what it is.
- **T4. No claim the evidence does not carry.** An aim may be named as the target setting ("for integrated operations"), never as a result. Avoid words whose connotations the guidelines exclude, for example military "joint operations," or "swarm" and "fleet" when the work is about neither.
- **T5. No vague scope prefix.** Do not open with a phrase that hides the contribution ("Towards integrated X operations: ..."); the words before the colon carry the most weight.

| Before | Why it fails | After (shape) |
|---|---|---|
| An Approach for Using Language Models to Train Retrieval for Clinical Notes | a homework sentence (T1); one stage, "Train," for a whole pipeline (T2) | *Name*: Retrieval-Augmented Language Models for Searching Clinical Notes |
| Towards Integrated Grid Operations: An LLM Tool-Use Approach | a scope prefix (T5); an acronym (T3); one component, "tool use," for an orchestrating system (T2) | *Name*: Language Model Orchestration of Power Grid Control Systems |
| Autonomous Swarm Coordination for Joint Operations (a study of one inspection robot) | connotations and claims the work does not carry (T4) | a title that names what was built and for whom |

### Choosing and Changing the Title

The title belongs to the author. The procedure is the same for every role and every run:

1. Propose three to five candidate titles, each with one line on what it stresses (method, contribution, domain, audience) and which rule it trades off, if any. The candidates go to the author, in the reply or in an agent's report, marked as candidates.
2. Never write a title into any file of the project (main file, title page, cover letter, configuration, decision log) until the author has explicitly approved one. A committee agent that finds a weak title reports it and proposes candidates; it does not change it.
3. Once the author approves a title, change it in one pass everywhere it appears (the main file, the title page, the cover letter, the project configuration, the decision log and any metadata), record the approval and its date in the decision log, and rebuild the document.

`scripts/check_manuscript.py` reports an abbreviation in the title (TITLE_ABBREVIATION) and a long title (TITLE_TOO_LONG); the other rules are checked by reading.

## Abstracts

Write the abstract last and make it mirror the finished text: every number must match the same quantity, population, and analysis in the body.

| Slot | Content | Typical length |
|---|---|---|
| Context | The problem and why it matters | 1 to 2 sentences |
| Gap or question | What is unknown; the objective | 1 sentence |
| Approach | Design, data or material, key method | 1 to 3 sentences |
| Findings | Main results with numbers and uncertainty | 2 to 3 sentences |
| Meaning | Conclusion limited to what was shown; scope | 1 to 2 sentences |

- Usual length is 150 to 300 words; check the limit and whether headed (structured) sections are required. Short papers use 100 to 150 words.
- Self-contained: no citations unless required, no undefined acronyms, no reference to figures.
- **Two openings.** Context first suits broad-audience and biomedical venues; contribution first ("We show that ...") suits venues where readers triage many papers. Follow the venue's recent papers, and in either case have the contribution stated by the second sentence or the third.
- Name the proposal; do not describe the paper. "We propose a compression model of memory consolidation" tells more than "This paper explores issues of memory."
- For an argumentative paper the slots become: puzzle, what existing accounts miss, what this paper does, the thesis as a claim, significance.

## Introductions

The introduction is a funnel that ends in a promise the rest of the paper keeps.

1. **Context and stakes.** Open with a concrete claim, puzzle, or tension, not with "X has attracted much attention." A good hook makes the reader ask *why*.
2. **What is known and the specific problem.** Only the background needed to see the gap, drawn from sources you have read.
3. **The gap.** What is missing, wrong, or unresolved, stated precisely ("Despite extensive work on X and Y, Z remains unmeasured in ..."). A gap is a claim about the literature and needs evidence (see `evidence-and-citations.md`).
4. **This work.** The question or hypothesis, the approach, and why the approach fits.
5. **Contributions.** What is new, in a sentence or a short parallel list. Make each item specific and checkable: the technique and what it achieves, the result with its benchmark and baseline, the artifact and where to find it.
6. **Roadmap** (optional in short papers). One clause per section, saying what each does.

- Length is about 10 to 20 percent of the paper, commonly one to two pages.
- Define the key concept early and keep its label fixed from here on.
- Do not preview results the paper does not deliver, and make no priority claim ("first," "no prior work") that `claims-and-coherence.md` would reject.
- The introduction and conclusion should rhyme: the conclusion answers the opening question in the opening's terms.
- For longer argumentative papers a six-part version works: hook, background, positions in the literature (grouped by approach, each with its limit), this paper's approach and thesis, contributions, roadmap. As a rough prior only, the hook takes about a tenth of the introduction, background a sixth, and the positions about a third; the rest goes to the thesis, contributions, and roadmap.
- In theory-driven papers, state the claim before surveying the literature, and define each construct in its own paragraph: the definition, how it differs from its nearest neighbor, and how it is measured. Use that label unchanged in the hypotheses, measures, results, and discussion.

## Related Work

- Organize by theme, approach, or position, never by date and never one paper per sentence.
- For each group: who holds it, the core idea stated fairly, and the limitation that matters for your question. Then say how your work differs.
- End with a positioning paragraph: what the groups jointly leave open and where this paper sits.
- Be fair. Present competing work in a form its authors would accept, and include work that challenges your approach.
- Placement varies: after the introduction when the reader needs it to follow the approach, near the end when the approach is easier to compare once seen.

## Methods

Test: could a competent researcher evaluate the work and, where feasible, repeat it from this section and its supplements? Describe what was done, not what would have been ideal, and never reconstruct methods from results. Cover what applies:

- Design, setting, dates; protocol or registration; deviations from the plan, with timing.
- Participants, specimens, datasets, or sources: eligibility, selection, exclusions, sample size and its rationale.
- Interventions, exposures, comparators; materials, instruments, software, and versions.
- Outcomes and variables: definitions, timing, how measured, thresholds.
- Controls against bias: randomization, masking, baselines, held-out data.
- Analysis: models, assumptions, handling of missing data, multiplicity, sensitivity analyses; which analyses were prespecified (confirmatory) and which were exploratory.
- Ethics approval and consent, stated only as verified; access to data, code, and materials.

## Results

- Report in the order of the stated questions or hypotheses, and answer each.
- Report first, interpret later, unless the venue merges Results and Discussion.
- Give the flow of participants, samples, or records, with exclusions and missing data, before the outcomes.
- For each finding: direction, size, uncertainty, the denominator or sample size, and the unit. A compact pattern is mechanism or relation, estimate with interval, boundary condition, robustness: "Overload raised conflict (b = 0.31, 95% CI 0.12 to 0.50); the effect was weaker under high control and held across specifications" (illustrative).
- Include negative, null, unexpected, and adverse findings, and label exploratory and post hoc analyses as such.
- Use only methods the Methods section declares. Do not equate crossing a threshold with importance.
- Where questions are numbered, open each answer with a short block (illustrative values):

  > **RQ2.** Does feedback timing affect retention? **Answer:** Delayed feedback raised retention by 6 points (95% CI 2 to 10; Table 3). **Robustness:** the estimate held without the two smallest classes. **Boundary:** the effect was absent for recall items.

## Discussion, Limitations, and Conclusions

A reverse funnel:

1. The main findings, in one short paragraph, as answers to the stated questions.
2. Interpretation against prior work that you have verified, including work that disagrees.
3. Mechanisms and alternative explanations: for each effect, the *because*, and what else could produce it.
4. Implications, theoretical and practical, without prescribing action beyond the evidence.
5. Limitations, then boundaries.
6. What should be tested next.

- **One paragraph per main finding** usually works: state the finding, interpret it, compare it with related work, and draw the implication.
- **Limitations are specific, and stated once.** Name the source of bias, imprecision, missing data, or measurement error, and say which way it probably pushes the result. Collect them in one compact Limitations subsection; elsewhere a brief qualifier at the claim is enough (Narrative Order and Saying It Once, above). A generic paragraph added for form is worth nothing.
- **Turn limitations into boundary conditions.** Instead of "future research should examine other factors," write where the claim is expected to hold and where it should weaken, and why. End the discussion with a scope sentence: the claim plus its boundaries.
- **Conclusions synthesize.** Restate the thesis in light of the evidence, show how the parts add up, and return to the opening puzzle. No new arguments, results, or citations. Do not end on an apology or on "more research is needed" alone.

## Conference Papers in Computing

- **Introduction** (about a page): problem, why it is hard, key insight, contribution list, one-paragraph summary of results.
- **Background and problem formulation:** notation table; the problem as *Given*, *Goal*, *Constraints*.
- **Approach:** intuition in plain language, an overview figure, then components, then the formal statement. Present an algorithm at three levels: idea in a sentence, diagram or example, pseudocode with inputs and outputs. State complexity, correctness, or convergence with a proof sketch; full proofs go in an appendix.
- **Experiments:** datasets, baselines with a one-line description each, metrics and why each is used, implementation details (hardware, hyperparameters, seeds), main results with mean and spread over several runs, ablations that remove components singly and jointly, sensitivity analysis, error or qualitative analysis.
- **Related work,** **conclusion,** and **appendices** for proofs, extra experiments, and implementation details.
- Rough allocation for eight pages: introduction 1, related work 1, approach 2, experiments and results 2.5, discussion and conclusion 1, abstract and slack 0.5. References are usually outside the limit.

## Argumentative Papers

For philosophy, theory, and other papers whose evidence is reasoning.

- **Argument section.** State the claim the section defends and why the thesis needs it. Number the premises; justify each separately (citation, argument, or an earlier result of the paper) and answer the most likely worry about it. Show the inference step by step. Then take the strongest objection to the conclusion and reply.
- **Critical section.** Reconstruct the opposing view in its strongest form, with quotations from the original, so that its holders would accept your summary. Then criticize: state the problem, why it undermines the view, the evidence, and the likely reply. Prefer internal criticism (the view fails by its own standards) or name the assumption you reject.
- **Conceptual section.** Why the concept matters, a precise definition, how it differs from neighbors, examples, its role in your account, likely confusions.
- **Case section.** Why this case, a sourced description, the framework applied element by element, and what rival accounts would predict. The analysis should reveal something not obvious beforehand.
- **Objections.** State each as a real critic would, grant what is valid, answer the strongest form, and concede as a limitation what you cannot answer.

## Position Papers and Short Papers

- **Position paper.** State the claim bluntly in the introduction; describe the current state and why it is a problem; give each argument as claim, evidence, reasoning, link to the thesis; devote a section to objections; end with implications for each audience.
- **Short paper or extended abstract** (two to four pages). Problem, gap, and contribution in half a page; the key idea; one compelling result; brief related work; 10 to 15 references.
- **Cutting to a page limit.** Move detail to an appendix or supplement, merge related work into the introduction, drop secondary experiments, then tighten prose. Do not shrink figures below legibility or delete limitations.

## Review Articles

Decide the type first, because it sets the obligations.

| Type | Purpose | Method section must give |
|---|---|---|
| Narrative review | Expert synthesis and argument | Scope and how sources were chosen, at least briefly |
| Scoping review | Map the extent and kinds of evidence | Protocol, search, eligibility, charting method |
| Systematic review, with or without meta-analysis | Answer a focused question reproducibly | Registered protocol, full search strategies and dates, eligibility criteria, screening and extraction procedure, risk-of-bias assessment, synthesis method |

- **Introduction:** motivation, scope, review questions, contributions, organization.
- **Thematic sections:** define the category, describe the approaches in it with their strengths and limits, compare them (a table with consistent columns helps), and list open problems.
- **Cross-cutting synthesis:** common themes, trade-offs, contradictions and their likely causes, trends, gaps.
- **Future directions:** for each, current progress, what is missing, and what closing the gap would enable.
- A review synthesizes; it does not list (example in `publication-types.md`, Survey). Each section should say something that no single source says. Reporting guidelines for reviews are in `integrity-and-ai.md`.

## Technical Reports

- Front matter: title, authors, date, version, summary, contents.
- **Executive summary** on one page: purpose, background, approach in two or three sentences, key findings, recommendations, and a one-sentence bottom line. It must stand alone.
- Introduction: purpose and scope, intended readers, related documents. Background: context, requirements, constraints, assumptions.
- Organize the body by the thing reported (system: overview, architecture, components, interfaces; study: method, setup, results, analysis), not by forced IMRaD.
- Reports can and should carry what papers omit: full parameters, complete data tables, negative results, and dead ends. Put them in appendices with a glossary.

## Theses and Dissertations

- **The thesis has one argument.** State it in the introduction as a small set of research questions or claims, and make every chapter earn its place by answering one of them. Say which chapter answers which.
- **Introduction chapter:** problem and stakes, questions, contributions (with pointers to chapters and to any published papers they draw on), scope and limits, outline.
- **Background or literature chapter:** a critical synthesis organized by theme that ends in the gaps the thesis fills. It shows command of the field; it is not an annotated bibliography.
- **Core chapters,** each with: an opening that states the chapter's question, how it builds on earlier chapters, its contributions, and its organization; the content; a discussion of what the results mean and their limits; and a summary that lists the contributions and hands over ("Having established X, Chapter 5 asks Y").
- **General discussion and conclusion:** answer the research questions across chapters, state the overall contribution, limits, and future work.
- **Consistency across chapters:** one notation, one terminology, one citation style. If chapters began as papers, remove repeated background, unify symbols, and add bridges.
- **Paper-based (compilation) thesis.** Check the institution's rules first. Write one integrated introduction and one general discussion that make the papers a single argument, add linking text between them, and state for each paper its publication status and your own contribution to it, with the coauthors' roles.
- **Abstract and lay summary** are written for the committee and external examiners, who may not be specialists: the questions, what was done, the answers, and the overall contribution, with no undefined terms.
- **Preparing for the defense or viva.** List the questions a skeptical examiner would ask (the skeptical-referee pass in `review-and-revision.md` produces them), prepare short answers with pointers to chapters, and know the weakest point of each chapter and what you would do about it. Committee feedback is handled like reviewer comments.
- Write to a specification: an outline to the third heading level with a target length, the content, and the key sources for each part.

## Textbooks and Lecture Notes

A teaching text is judged by what the reader can do afterwards, not by coverage.

### Chapter Design

- **Open with the question.** Start from a problem the reader cannot yet solve, or a concrete case, so the need for the new idea is felt before the idea arrives.
- **State objectives as abilities.** "After this chapter you can derive ..., compute ..., decide when ..." Each objective should be testable by an exercise.
- **State prerequisites** with pointers to where they were covered.
- **Close the loop.** End with a summary of results (definitions, formulas, procedures) the reader can use for review, a note on what the chapter did not cover, and the link to the next chapter.
- Keep chapters parallel in construction so that readers learn where to look.

### Cumulative Explanation

- **Nothing is used before it is introduced.** Order the material by dependency and keep a list of what each chapter assumes and provides. A forward reference is acceptable only as a promise ("we return to this in Chapter 7"), never as a dependency.
- **One new idea at a time.** Introduce it, show it at work, and only then generalize or combine it with another.
- **Concrete before abstract.** Give a specific example, picture, or small computation, then the general statement, then a second example that tests the boundary.
- **Motivate every definition and theorem.** Say what problem it solves and what would go wrong without it. After a formal statement, restate it in plain words.
- **Show the reasoning, not only the result.** Give each step of a derivation with its justification; name the step where students usually go wrong and say why.
- **Reuse earlier material deliberately.** Bring back earlier examples and notation so that knowledge accumulates, and say so when you do.
- Address the reader's likely misconception directly instead of hoping the correct account displaces it.

### Worked Examples

- Place a worked example immediately after the idea it uses. Start with the simplest case that is not trivial, then add one complication at a time.
- Show the full solution: state the problem, name the method and why it applies, carry out each step with its reason, check the answer (units, limiting case, order of magnitude), and say what the example teaches.
- Follow an example with a near-identical problem for the reader to try, then with one that needs a small extension.
- Include at least one example where the method fails or does not apply, so that readers learn its conditions.
- Use real or realistic numbers and state where they come from. Never present invented data as real.

### Exercises

- Tie each exercise to an objective, and cover every objective.
- Grade the set: recall and direct application first, then problems combining ideas, then open-ended or proof problems. Mark the difficulty.
- Mix in problems from earlier chapters; spaced, mixed practice helps material stay.
- Write problems that cannot be solved by matching a template from the chapter, and include some that ask for explanation, estimation, or criticism of a flawed solution.
- Solve every exercise before publishing it. Provide answers or hints for a subset and keep full solutions consistent with the chapter's notation.

### Lecture Notes

- Notes are read without the lecturer: write full sentences for the reasoning that would be spoken, not only what would be on the board.
- One lecture, one main result. Begin with where the course stands and what today adds; end with what to remember and what comes next.
- Mark what is essential and what is enrichment. Keep numbering stable across versions so that references made in class stay valid, and date each version.

## End Matter

Typical order, where the venue does not fix one: acknowledgments; author contributions; funding and the funder's role; competing interests; ethics, consent, and registration; data, code, and materials availability; AI-use disclosure; references; appendices and supplements. Treat every declaration as a record to verify, not as boilerplate (see `integrity-and-ai.md`). The availability statement is the one place for provenance: what was archived, where, in which version, and how to rerun it. The body then need not say it again.
