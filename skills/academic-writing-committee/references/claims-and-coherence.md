# Claims and Coherence

How strong each claim should be, and how the claims of a document hold together: calibration (no overclaiming, no underselling), contribution statements, the chain from research question to evidence to claim, agreement between abstract, introduction, discussion, limitations, and conclusion, and consistency of terms, notation, numbers, and names. This file governs claim strength (`style.md` points here); statistical reporting is in `mathematics-and-notation.md`; sources and verification are in `evidence-and-citations.md`; section-by-section structure is in `structure.md`. This file is the main reference for the **claims** reviewer and is used alongside the **experiments** and **significance** reviewers, the **consistency** editor, and the **examiner**, **pc-reviewer**, and **skimmer** readers where a profile includes them.

All numbers in examples are illustrative. Field and venue conventions differ (for example, on contribution lists, limitation sections, and claims of novelty); check the call, the author instructions, and recent papers from the venue.

## Contents

1. The Calibration Principle
2. Overclaiming
3. Underselling
4. The Calibration Ladder
5. Contribution Statements
6. Aligning Questions, Experiments, and Claims
7. Agreement Across Sections
8. Consistency of Terms, Notation, Numbers, and Names
9. The Claim-Evidence Matrix
10. References Must Be Real and Supportive
11. Final Coherence Checklist

## The Calibration Principle

A claim is calibrated when a skeptical expert who reads the evidence would state it at the same strength. Overclaiming costs credibility with reviewers and readers; underselling hides real contributions and invites the reader to discount them. Both are errors of the same kind: the words and the evidence disagree.

- Decide the strength of a claim from the evidence first, then choose the verb (the ladder below), then the scope.
- Put the qualifier on the uncertain element only, once. "Under assumption A2, the bound is tight" is calibrated; "the bound may possibly be somewhat tight" is not.
- Editing for fluency must not change claim strength. After every language pass, compare the claims before and after.

## Overclaiming

**What to do.** Remove or narrow every claim the evidence does not carry. The most frequent forms:

| Pattern | Before | After |
|---|---|---|
| Unsupported superlative | "the most efficient method" | "the lowest latency among the six methods we evaluated (Table 3)" |
| "First" without a documented search | "the first study of X" | "to our knowledge, the first study of X in Y; Section 2 describes the search" or drop the priority claim and state what is new |
| "Novel" as decoration | "a novel framework" | say what is new: "a framework that, unlike A and B, handles missing modalities at test time" |
| "State of the art" without dated evidence | "achieves state-of-the-art results" | "exceeds the best result we found reported on X as of March 2026 (Ref), 71.2 versus 69.8" |
| "Prove" for empirical results | "our experiments prove that ..." | "our experiments show / indicate that ..." (reserve *prove* for proofs) |
| "Solve" for partial progress | "we solve the cold-start problem" | "we reduce cold-start error by 18% on two datasets" |
| Causal wording for associations | "screen time causes poor sleep" | "screen time was associated with shorter sleep; the design cannot establish direction" |
| Generalizing beyond tested conditions | "the method works for low-resource languages" | "the method improved accuracy on the four low-resource languages tested" |
| Certainty words | "clearly," "undoubtedly," "obviously," "guarantees" | delete, or state the guarantee and its assumptions |
| Universal quantifiers | "always," "never," "in all cases" | the tested cases: "in all 12 configurations" |
| Comparison without uncertainty | "outperforms the baseline" | "outperforms the baseline by 1.4 points (95% CI 0.6 to 2.2, five seeds)" |
| Implications beyond the data | "these results will transform clinical practice" | "if confirmed in a prospective study, these results would support ..." |
| Significance as importance | "a highly significant improvement" | the size, its uncertainty, and why that size matters |

**"State of the art" is a dated, sourced claim.** Results move. Name the benchmark, the comparison set, the date or version, and the source for each competitor's number; say whether numbers are reproduced or copied from papers; and prefer "outperforms the strongest baselines we evaluated" when you cannot vouch for the whole field.

**"First" and "no prior work" are claims about the literature.** They need a documented search (`evidence-and-citations.md`, "Establishing a Gap"). Even with one, "to our knowledge" plus a narrow scope is safer than an unqualified priority claim.

**How to check.** Search for: *first, novel, state of the art, best, superior, prove, solve, guarantee, eliminate, always, never, all, clearly, obviously, cause, lead to, significant, outperform, generalize, robust*. For each hit, find the evidence and apply the ladder. The manuscript checker flags many of these words (see `language-mechanics.md`).

## Underselling

**What to do.** State what you did and found at the strength the evidence supports, early and specifically.

| Pattern | Before | After |
|---|---|---|
| Stacked hedges | "this may possibly suggest a potential improvement" | "this suggests an improvement" |
| Hedging a proved result | "it seems that the algorithm converges" | "the algorithm converges (Theorem 2)" |
| "We try to," "we attempt to" when you succeeded | "we attempt to reduce memory use" | "we reduce memory use by 38%" |
| Buried contribution | the main result appears first on page 6 | state it in the abstract and by the end of the introduction |
| Blurred contribution | "we explore some aspects of X" | "we show that X fails when Y, and give a correction" |
| Apologizing for scope | "this is only a small preliminary study" | "this study of 40 participants estimates the effect size needed to plan a confirmatory trial" |
| Minimizing words | "a simple trick," "merely," "only" | describe what it does; let the reader judge simplicity |
| Missing magnitude | "improves accuracy" | "improves accuracy from 87% to 92%" |
| Limitations that cancel the paper | a limitations section implying no result holds | specific limitations with their likely direction, plus the scope where the claims do hold |
| Vague future work in place of a finding | "more research is needed" | what should be tested next and what result would change the conclusion |

**How to check.** Ask a reader who has seen only the abstract and introduction to write down your contributions. If the list is vague or wrong, the text undersells. Search for *may, might, could, possibly, perhaps, potentially, seems, appears, somewhat, preliminary, try, attempt, simple, merely, only* and keep only the qualifiers that mark real uncertainty.

## The Calibration Ladder

Match the verb and the qualifier to the strongest evidence you actually have. Move down the ladder when the evidence is weaker; never move up for emphasis.

| Rung | Evidence | Verbs | Typical qualifiers |
|---|---|---|---|
| 1 | Proof or derivation, in the document or cited | prove, show, establish, guarantee | "under assumptions A1 to A3," "for all *n* ≥ 2" |
| 2 | Randomized or otherwise identified causal design, replicated or across many settings | cause, increase, reduce, determine | the population, setting, and dose or range tested |
| 3 | Controlled experiment or benchmark comparison with uncertainty | improve, outperform, reduce, exceed, show | "on datasets A to D," "by 2.1 ± 0.4 points (mean ± SD, 5 seeds)" |
| 4 | Observational association, adjusted or not | is associated with, predicts, co-occurs with, is linked to | "after adjusting for X," "in this cohort" |
| 5 | Exploratory, post hoc, small sample, single site | suggest, indicate, are consistent with | "in this sample," "exploratory," "a first estimate" |
| 6 | Qualitative evidence, case studies, argument | illustrate, indicate, we argue | "in these cases," "on this reading" |
| 7 | Reasoning beyond the data | we hypothesize, we speculate, one possible explanation | "if," "would," "a plausible mechanism is" |

- **Scope qualifiers** answer: on which data, population, languages, tasks, hardware, or time period; under which assumptions; at what scale. Put the scope in the same sentence as the claim, not three paragraphs later.
- **Comparative claims** name the comparison set and the metric: "lower error than A, B, and C on D," not "better than existing methods."
- **Mechanism claims** ("because the attention heads specialize") sit on rung 6 or 7 unless an experiment isolates the mechanism; an ablation that removes a component supports "the component contributes," not "the component works by."
- **Negative results** are calibrated too: "we found no difference larger than 1.5 points (95% CI −0.8 to 1.5)" rather than "there is no difference."

Moving a sentence to the right rung:

| Evidence in hand | Overclaimed | Undersold | Calibrated |
|---|---|---|---|
| Theorem 2 with stated assumptions | "always converges" | "seems to converge" | "converges under assumptions A1 to A3 (Theorem 2)" |
| Benchmark gains, five seeds, three datasets | "is superior to existing methods" | "might offer some gains" | "improves F1 by 2.1 to 3.4 points on the three datasets (five seeds)" |
| Cross-sectional survey | "remote work reduces burnout" | "there could perhaps be a link" | "remote work was associated with lower burnout scores" |
| Eight interviews | "practitioners reject automated review" | "a few people said some things" | "six of eight practitioners described automated review as a second opinion, not a replacement" |

## Contribution Statements

A contribution statement is the promise the document makes. Each contribution is:

- **Specific:** what was done or found, not a topic ("we study fairness" is a topic).
- **Verifiable:** a reader can check it against a named result, theorem, artifact, or analysis.
- **Mapped:** it names or implies the section, table, figure, or theorem that delivers it.
- **Scoped:** it carries the qualifiers of the ladder.
- **Distinct:** contributions do not overlap; one result is not listed twice in different words.

Template: *verb + object + distinguishing property + evidence (+ location)*.

| Before | After |
|---|---|
| "We propose a novel approach for efficient inference." | "We introduce block-sparse caching, which cuts decoding memory by 38% at equal accuracy on three benchmarks (Section 4, Table 2)." |
| "We provide extensive experiments." | "We evaluate on 12 datasets in four domains against five tuned baselines, with five seeds each (Section 5)." |
| "We offer insights into model behavior." | "We show that error concentrates on inputs longer than the training maximum (Figure 4), and that length-aware sampling removes most of the gap." |
| "We release code." | "We release the code, trained models, and evaluation scripts at [repository], sufficient to reproduce Tables 2 to 4." |

Contributions by document type:

| Document | What a contribution states |
|---|---|
| Journal article, conference paper | Results, methods, theorems, datasets, artifacts, each with its evidence; often a short list in the introduction (check the venue's custom) |
| Survey, tutorial | The scope and period covered, the taxonomy, the synthesis or comparison it enables, the open problems it identifies; not "we review the literature" |
| Book, textbook | What a reader will be able to do after each part, and what the book does that others do not (coverage, approach, level), stated in the preface |
| Book chapter | The chapter's question and what it adds to the volume; how it connects to adjacent chapters |
| Thesis | Each original contribution, mapped to the chapter and any publication it comes from, with the candidate's own part stated where work was joint |
| Technical report | What was built, measured, or decided, and for whom |
| Grant proposal | Aims and expected outcomes, in the future tense, with preliminary evidence for feasibility; never results not yet obtained presented as achieved |
| Lecture notes | Learning objectives per unit; contribution claims are rarely needed |

**How to check.** Build the contribution map below. Every contribution must have a row with evidence; every row must appear, in the same terms, in the abstract (if space allows), the introduction, and the conclusion.

| # | Contribution (as worded in the introduction) | Evidence | Section | Abstract | Conclusion |
|---|---|---|---|---|---|
| C1 | Block-sparse caching cuts decoding memory by 38% | Table 2 | 4.2 | sentence 3 | paragraph 1 |
| C2 | Error concentrates on long inputs | Figure 4 | 5.3 | sentence 4 | paragraph 1 |

## Aligning Questions, Experiments, and Claims

The document should form one chain: **question → hypothesis or prediction → experiment or analysis → result → interpretation → claim**. Breaks in the chain are a frequent reason reviewers call a paper "not convincing."

**What to do.**

- State the research questions or hypotheses explicitly (numbered, if there are several) and answer each in the results, in the same order and the same terms.
- **Every claim traces to a result.** If a claim in the discussion or conclusion has no table, figure, theorem, or cited source behind it, add the evidence, narrow the claim to what the evidence supports (a hypothesis, if nothing more), or mark it unresolved for the author. Delete it only when the author agrees that nothing can support it.
- **Every result is interpreted.** A table that the text never explains is a result without a claim. Say what to notice and what it means.
- **No orphan experiments.** An experiment that serves no question or contribution distracts and invites doubt. Connect it to a question, move it to an appendix with a sentence of purpose, or cut it.
- **Each component claim needs an ablation or a comparison** that isolates it. "Each of the three modules contributes" requires removing each module.
- **Report negative, null, and mixed results** for the stated questions, and label exploratory analyses as exploratory in methods, results, and discussion.
- **Fair comparison:** baselines tuned with comparable effort and compute; numbers copied from papers marked as such; the same data splits.

| RQ | Experiment | Result | Claim (where) |
|---|---|---|---|
| RQ1: Does caching reduce memory at equal accuracy? | Exp. 1, three benchmarks | Table 2: −38% memory, accuracy within 0.2 points | C1 (abstract, Section 4, conclusion) |
| RQ2: Where do errors concentrate? | Exp. 2, error by input length | Figure 4 | C2 |
| (none) | Exp. 3, speed on CPU | Table 5 | **orphan**: connect to a question or move to appendix |

**Statistical language.** Rules and reasoning are in `mathematics-and-notation.md`. In claims specifically:

- *Significant* means statistically significant, with the test and statistic reported; otherwise use *large*, *substantial*, or a number.
- A nonsignificant result is not "no effect"; "a trend toward significance" is not a finding.
- "Outperforms" needs the margin and its uncertainty; "consistently" means in every reported setting; "robust" names the perturbation that was tested.
- Distinguish percent from percentage points, and relative from absolute change.
- Do not convert an association into an effect size of an intervention.

## Agreement Across Sections

The abstract, introduction, discussion, limitations, and conclusion describe the same work. They differ in depth, not in content.

| Section | Job | Must agree with the rest on |
|---|---|---|
| Abstract | Compress the whole: problem, approach, main results, meaning | contributions, headline numbers, scope, design (for example, "observational") |
| Introduction | Motivate, state the gap, promise the contributions | the contribution list, the questions, the scope |
| Results | Deliver the evidence | the numbers every other section quotes |
| Discussion | Interpret the results, relate them to prior work, give mechanisms and alternatives, state implications | claim strength, scope, how prior work is characterized |
| Limitations | Name the specific threats and their likely direction | what the abstract and conclusion still claim |
| Conclusion | Answer the opening question, restate contributions in light of the evidence, give scope and next step | everything above; it adds nothing new |

**Rules.**

- **Same contributions, same order, same names.** If the introduction lists three contributions, the conclusion revisits three, not two or four.
- **Same numbers.** A value quoted in the abstract is identical, with the same rounding, unit, and denominator, in the results and the conclusion.
- **Same scope.** If the experiments cover four languages, no later section says "languages" without the qualifier.
- **The conclusion adds no new claims,** results, citations, or arguments. It may state implications that the discussion has already argued.
- **Titles, headings, and captions make claims too.** A title such as "X Solves Y" or a caption that says "our method is better" is held to the same ladder as the text. Skimmers and program-committee reviewers read these first.
- **The discussion interprets, it does not repeat** the results section. It relates findings to verified prior work, including work that disagrees, and gives alternative explanations.
- **Limitations are honest and specific:** the source of bias or imprecision, which way it probably pushes the result, and the conditions under which the claims should hold. A limitation stated in the limitations section must not be contradicted by an unqualified claim in the abstract. Some venues require a dedicated limitations section or checklist; check the call.
- **Long documents.** What must agree depends on the type:
  - **Thesis:** the abstract, the introductory chapter, chapter summaries, and the concluding chapter; published papers incorporated as chapters are reconciled with the thesis's framing.
  - **Book:** the preface, chapter openings, and chapter summaries promise and deliver the same things.
  - **Survey:** the stated scope and inclusion criteria match what is actually covered.
  - **Grant proposal:** the aims page, approach, timeline, and budget describe the same aims.

| Before | After |
|---|---|
| Abstract: "across 12 datasets"; Conclusion: "on all standard benchmarks" | both: "on 12 datasets in four domains" |
| Introduction: "we prove convergence"; Section 3: convergence shown empirically | introduction: "we observe convergence in all runs and prove it for the convex case (Theorem 1)" |
| Limitations: "single site"; Abstract: "the intervention improves outcomes in primary care" | abstract: "in one primary-care network, the intervention was associated with ..." |

**How to check.** Put the abstract, the contribution paragraph, the first paragraph of the discussion, the limitations, and the conclusion side by side. Compare them contribution by contribution, number by number, and qualifier by qualifier.

## Consistency of Terms, Notation, Numbers, and Names

**What to do.**

- **Terms.** Keep a term sheet (term, definition, first use, forbidden synonyms). One concept has one name everywhere, including figures, tables, captions, the abstract, and supplementary material. `language-mechanics.md` explains why elegant variation is wrong for technical terms.
- **Notation.** Keep a notation table (`mathematics-and-notation.md`): one symbol per quantity and one quantity per symbol, also in figures and pseudocode.
- **Numbers.** Keep one source of truth. Generate reported numbers from result files where possible (for example, LaTeX macros written by the analysis script), so that a rerun updates every mention. After each revision, search for every headline number.
- **Names.** Spell every name identically throughout, as its owner spells it: methods, models, datasets with their versions, software with its version, people, and institutions. A method renamed during revision must be renamed everywhere, including figure legends.
- **Counts.** The number of contributions, questions, datasets, participants, and experiments is the same wherever it is stated, and denominators reconcile.
- **Cross-references.** Every "Section 4," "Table 2," and "Theorem 1" points to the right element after renumbering.

**How to check.** Search for each defined term's near-synonyms, each headline number, each method and dataset name (including old names), and each count word ("three contributions," "four datasets"). The consistency editor applies the same searches across the whole document and against the glossary.

## The Claim-Evidence Matrix

`evidence-and-citations.md` defines the claim-evidence ledger, which records each claim's sources and verification status. The matrix below adds the cross-section view: where each main claim appears, how strongly it is worded in each place, and whether the evidence carries that strength. Writers update it in their change report for every claim they add or change; the claims reviewer rebuilds it independently and compares, and in a document with several units the cross-unit claims review builds it over the whole document.

**Procedure.**

1. **Extract** every claim from the abstract, the contribution statements, the first paragraph of the discussion, and the conclusion. Add claims elsewhere that a reader would repeat. Give each an ID (C1, C2, ...).
2. **Locate** every place each claim appears, with its exact wording.
3. **Attach evidence:** the table, figure, theorem, analysis, or verified source, with a locator.
4. **Rate the evidence** on the calibration ladder (rung 1 to 7) and note its scope (data, population, conditions).
5. **Rate the wording** in each location on the same ladder.
6. **Compare.** Wording above the evidence rung, or wider than its scope, is overclaimed; wording below it is undersold; wordings that differ between locations are inconsistent.
7. **Find orphans:** results with no claim, claims with no result, experiments with no question.
8. **Act:** narrow, strengthen, unify, add evidence, or mark the claim unresolved for the author. Record the action and recheck after revision.

| ID | Claim | Locations and wording | Evidence (rung, scope) | Verdict | Action |
|---|---|---|---|---|---|
| C1 | Caching cuts memory | Abstract "cuts memory by 38%"; Sec. 4 "38%"; Conclusion "roughly halves memory" | Table 2 (rung 3; three benchmarks, one GPU type) | inconsistent; conclusion overclaims | conclusion: "cuts memory by 38% on three benchmarks" |
| C2 | Errors concentrate on long inputs | Intro "may perhaps relate to length"; Sec. 5 "concentrate on inputs > 2k tokens" | Figure 4 (rung 3) | intro undersells | intro: "concentrate on inputs longer than the training maximum" |
| C3 | Method generalizes across domains | Abstract "generalizes across domains" | four domains, no out-of-domain test (rung 3, narrow) | overclaimed | "improves results in all four domains tested" |

Verdicts: **supported**, **overclaimed**, **undersold**, **inconsistent**, **unsupported**, **orphan**. Any unsupported or overclaimed claim in the abstract or conclusion is a blocker.

## References Must Be Real and Supportive

Every reference must exist, be described correctly, and support the specific sentence that cites it, in direction, population, and strength. A real paper cited for a claim it does not make is as damaging as a fabricated one. Never add a reference that no person has opened, and never let a citation stand in for evidence the document itself should provide. The verification procedure and the source ledger are in `evidence-and-citations.md`; the references reviewer applies them and treats any reference that cannot be found as a blocker. A reference that cannot be verified is removed or replaced with a visible `[[TODO: source for X]]`, and the sentence it supported is narrowed, supported by other verified evidence, or marked unresolved; the claim is not deleted by default.

## Final Coherence Checklist

- [ ] Every claim's wording matches its evidence rung and scope; no unsupported superlatives, priority claims, or "state of the art" without a dated, sourced comparison.
- [ ] *Prove* appears only with proofs; *solve* only for solved problems; causal verbs only with causal designs.
- [ ] No stacked hedges; proved and measured results are stated plainly; no "we try to" for achieved results.
- [ ] Each contribution is specific, verifiable, scoped, distinct, and mapped to its evidence and section.
- [ ] Every research question is answered; every claim traces to a result or verified source; every result is interpreted; no orphan experiments.
- [ ] Negative, null, and exploratory results are reported and labeled.
- [ ] Abstract, introduction, discussion, and conclusion state the same contributions, in the same order and terms, with identical numbers and scope.
- [ ] The conclusion adds no new claims, results, or citations.
- [ ] Limitations are specific, give the likely direction of bias, and are not contradicted elsewhere.
- [ ] Terms, notation, numbers, names, counts, and cross-references are consistent throughout, including figures, tables, and supplements.
- [ ] Every reference is real, correctly described, and supports the sentence that cites it.
- [ ] The claim-evidence matrix has no open overclaimed, unsupported, or inconsistent rows.
