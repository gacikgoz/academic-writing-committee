# Review and Revision

Revising your own draft, reviewing someone else's manuscript, and responding to reviewers.

## Contents

1. Revision Passes
2. Diagnostics
3. Self-Review Rubrics
4. Author's Final Audit
5. Coherence Pass for Long Documents
6. Reviewing a Manuscript
7. Writing Review Comments
8. The Review Report
9. Responding to Reviewers
10. Response Letter Template

## Revision Passes

Revise from large to small. Polishing sentences in a section that will be moved or cut wastes the effort. Take a break between passes, and get a reader who has not seen the draft.

| Pass | Question | Typical actions |
|---|---|---|
| 1. Structure | Does each section do its job, in the right order and proportion? | Reorder, cut, split, merge; fix the outline |
| 2. Argument | Is the thesis clear, and does every claim follow? | Add missing steps and mechanisms; answer objections; align question, method, result, conclusion |
| 3. Evidence | Is each claim supported and each number right? | Verify sources; reconcile numbers; label exploratory work; narrow overclaims |
| 4. Clarity | Can the intended reader follow every paragraph? | Fix topic sentences; define terms; add transitions that carry logic |
| 5. Style | Is the prose direct and consistent? | Cut clutter; fix voice, tense, parallelism, terminology |
| 6. Format and polish | Does it meet the venue's rules? | Citation style, numbering, cross-references, captions, typos |

When time is short, sort the work: what the document cannot go out without (core contribution, correct results, sound structure), what it should have (complete related work, polished prose), and what would be nice. Get a complete draft before perfecting any part.

Record each problem with its severity (threatens acceptance, lowers quality, or polish), a concrete fix, and where. Fix the severe ones first. If a unit is just below standard, repair its weakest dimension and reassess; do not rewrite everything.

## Diagnostics

Quick, mechanical tests that expose problems reading alone misses.

- **Topic-sentence ladder.** List the first sentence of every paragraph. The list should tell the story. Gaps and repetitions show where the structure fails.
- **Reverse outline.** Write one line per paragraph saying what it actually does. Look for paragraphs that could be moved without loss, do two jobs, or do none.
- **Label audit.** Search for each key term and its near-synonyms. One concept should have one label in text, tables, figures, and captions.
- **Contribution check.** The contribution is stated in one sentence in both the abstract and the introduction, and the conclusion answers it.
- **Because check.** Every reported effect or design choice has its mechanism or reason.
- **Scope sentence.** The discussion ends with the claim and its boundaries.
- **Promise check.** List what the introduction promises; mark where each is delivered.
- **Skeptical referee.** Reread as a critical but fair referee, and write down every question, objection, missing definition, and unsupported step. Answer each in the text, or move it to the limitations.
- **Read aloud,** or use text-to-speech. Running out of breath means the sentence is too long; stumbling means awkward construction; boredom means repetition.
- **Venue comparison.** Reread two or three recent papers from the target venue and compare structure, tone, and density.

### Common Argument Failures

| Symptom | Test | Fix |
|---|---|---|
| Unclear thesis | Can you state it in one sentence? | Write that sentence, put it in the introduction and the conclusion, and cut or rework parts that do not serve it |
| Unsupported claims | Mark every claim; which have no argument, citation, or result? | Attach support to each, narrow it, or delete it |
| Unclear structure | Reverse outline: does each paragraph build on the one before? | Reorder, add the missing step, or merge paragraphs that do one job |
| Jargon overload | Could an adjacent-field reader follow it? | Define each term at first use; replace terms used only once |
| Weak objections | Would a real critic recognize the objection as theirs? | State the strongest version, grant what is valid, and concede what you cannot answer |

### Fast Presubmission Sweep

When time is short, run four quick, mechanical passes in this order. They are checks, not targets: no voice percentages or sentence-length quotas.

- **A. Structure.** Topic-sentence ladder and label audit.
- **B. Argument.** Contribution sentence, *because* check, scope sentence.
- **C. Evidence.** The main figure and results table stand alone; robustness checks are summarized in one place; every effect has a magnitude and an interval.
- **D. Style.** Clutter pass: search for hedges that do no work, nominalizations, "it is" and "there is" openers, "significant" without a statistic, "very," and empty passives (see `style.md`).

`scripts/check_manuscript.py` and `scripts/check_citations.py` find the mechanical problems (placeholders, clutter, unreferenced floats, missing or uncited references). They do not judge argument or evidence.

## Self-Review Rubrics

Use a rubric to force a judgment on each dimension and a list of concrete defects. Do not treat the total as a measurement: the same person or model that wrote the text is grading it, so scores drift upward. The value is in the written defects and in an independent reader. Pass marks (such as 80 percent) are arbitrary; the usable rule is that no dimension may be left at "needs revision."

### Chapter or Section

Rate each dimension as excellent, good, acceptable, or needs revision, and write the evidence for the rating.

| Dimension | Good means |
|---|---|
| Argument | Clear claim; each step supported; premises justified; strongest objection addressed |
| Evidence and citation | Every doubtful claim supported; sources accurate, relevant, and verified; key literature used |
| Clarity | Terms defined; sentences direct; an adjacent-field reader can follow |
| Structure and flow | Logical order; each paragraph has a job; matches the outline and its target length |
| Fit | Voice, terminology, notation, and format match the venue or the project's guidelines |

### Whole Manuscript

| Dimension | Questions |
|---|---|
| Thesis and argument | Is the thesis stated early and held throughout? Do the parts add up? |
| Literature | Is the work positioned fairly against the right sources? |
| Method | Is the approach explicit, justified, consistently applied, and are its limits stated? |
| Originality | Is the contribution specific and distinguished from named prior work? |
| Clarity | Could a nonspecialist in the field summarize it after one reading? |
| Structure | Do proportions fit the importance of each part? |
| Venue fit and completeness | Are scope, length, format, and required statements all met? |

### Review of the Outline

Review the outline as a referee would, on the same dimensions, and require at least three specific problems with fixes. Finding weak method description or an unclear contribution at this stage costs minutes; after drafting it costs days.

## Author's Final Audit

The checks a careful reviewer will run, done first by the author.

- [ ] **Claims.** For every claim in the abstract and conclusions: where is the supporting result, and do direction, size, population, outcome, time point, and certainty match? Narrow any that do not.
- [ ] **Chain.** Objective, outcome, method, result, and conclusion line up for each research question.
- [ ] **Numbers.** Each quantity has the same value, unit, and denominator in the abstract, text, tables, figures, and supplement. Sample sizes reconcile through every stage.
- [ ] **Methods and results.** Every result uses a method described in the methods; every described method has a result or an explanation.
- [ ] **Labels.** Exploratory and post hoc analyses are marked; "no difference" claims have estimates and intervals.
- [ ] **Limitations** are specific and bounded.
- [ ] **Citations** audited (see `evidence-and-citations.md`).
- [ ] **Displays** complete, referenced, and consistent with the text (see `figures-and-tables.md`).
- [ ] **Declarations and reporting checklist** complete (see `integrity-and-ai.md`).
- [ ] **Registration and protocol** agree with what the manuscript reports, or deviations are explained.
- [ ] **No placeholders,** tracked changes, or comments remain. Venue limits and format are met.
- [ ] A full read-through by every author after the last substantive change.

## Coherence Pass for Long Documents

After all chapters of a thesis, book, or long report exist:

- **Terminology and notation.** Extract the key terms and symbols per chapter; confirm one meaning each and agreeing definitions.
- **Dependencies.** Each chapter uses only what earlier chapters introduced; forward references are promises, not prerequisites.
- **Roadmap and promises.** The introduction's outline matches what the chapters do; the conclusion answers each promise and adds no new argument.
- **Bridges.** Each chapter opens by connecting to the previous one and closes by handing over.
- **Evenness.** No chapter is without citations where claims need them; depth and length are in proportion to importance.
- **Repetition.** Remove background repeated across chapters, especially in a thesis assembled from papers.

Keep a per-chapter log of terms introduced, results established, and open issues. It makes this pass fast.

## Reviewing a Manuscript

### Before Accepting

- Accept only if the work is within your competence and you have the time. State the limits of your expertise and name the specialist review that is needed (for example, statistics).
- Disclose conflicts of interest: financial, personal, institutional, recent collaboration or competition, strong intellectual commitment. The editor decides.
- Treat the manuscript as confidential. Do not share it, involve a junior colleague without the editor's permission, use its ideas, or keep copies beyond the venue's rules.
- **AI tools.** Many journals and funders prohibit or restrict giving a manuscript or grant application under review to an AI tool, because doing so discloses confidential material. Do not, unless the venue's current policy explicitly allows it and confidentiality is assured; disclose any permitted use. The assessment must be your own in every case.

### Order of Work

1. **Orient.** Write a neutral summary: the question, the design and unit of analysis, the comparison, the outcomes, the main claims. No judgment yet.
2. **Claims against evidence.** For the central claims, check that the results support them in direction, size, population, and certainty. This check is the heart of the review. A private table keeps it honest:

   | Claim | Where stated | Evidence offered | Fit and gap |
   |---|---|---|---|
   | The intervention raised retention | Abstract; Discussion, para. 1 | Table 2, one site, 8 weeks | Supported for 8 weeks at one site; abstract implies long-term and general |

3. **Methods and statistics,** in this order: question and target quantity; design and unit; sampling, allocation, controls; sample size or precision; exclusions and missing data; whether the analysis matches the design; multiplicity and prespecification; estimates and uncertainty; interpretation and generalization. (Details and a checklist: `mathematics-and-notation.md`.)
4. **Reproducibility and transparency.** Protocol and registration and whether the report matches them; whether the data and code statement describes something that exists and is accessible; software versions.
5. **Ethics and integrity.** Approvals, consent, conflicts, signs of overlap or image problems.
6. **Reporting completeness** against the applicable guideline, **displays,** and **writing.** For **citations,** check three things:
   - Do the cited works support the claims as stated? Spot-check the ones central claims rest on.
   - Is foundational or rival work missing, especially work that would change the interpretation?
   - Is there self-citation or padding the argument does not need, or a retracted source?
7. **Draft the comments,** most important first. Where a "no difference" claim rests on a nonsignificant test, ask for the estimate, its interval, and the effect sizes it rules out, or an equivalence analysis with a justified margin.

### Classify Each Criticism

| Class | Meaning | How to write it |
|---|---|---|
| Not reported | Information needed to assess the work is missing | Ask for it; do not infer a flaw from silence |
| Potential problem | The method as reported may not answer the question | Explain the concern and what would resolve it |
| Demonstrated inconsistency | Two parts of the submission conflict | Give both locations; do not guess the cause |
| Integrity concern | Evidence of a serious problem | Describe neutrally, to the editor only |

A reporting-guideline checklist measures completeness, not quality: do not turn it into a score. A well-reported study can be badly designed, and a badly reported one may simply be unassessable.

### Suspected Integrity Problem

1. Record the exact location (figure panel, table row, passage) and describe what you see neutrally: "Panels 3B and 4D appear to show the same image at different scales."
2. Put it in the confidential comments to the editor only. Do not accuse, speculate about intent, or mention it in the author report.
3. Do not contact the authors or investigate further yourself. The editor follows the venue's procedure.

## Writing Review Comments

Give every substantive comment five parts:

1. **Location:** section, paragraph, line, figure, or table.
2. **Observation:** what is stated, missing, inconsistent, or unsupported.
3. **Criterion:** the evidence, methodological principle, or policy it is measured against.
4. **Why it matters:** the consequence for validity, interpretation, or reproducibility.
5. **Request:** a specific, bounded action.

> *Methods, paragraph 3.* The unit of analysis is unclear: three measurements appear to come from each participant, but the test treats all measurements as independent. If they are repeated measures, the standard errors are too small and the main comparison may not hold. Please state the unit and use an analysis that accounts for within-participant dependence, or explain why independence is justified.

Compare "The statistics are weak," which gives the authors nothing to act on.

- **Be proportionate.** Request new experiments or analyses only when a central claim depends on them, and say which claim. Often a narrower claim, a sensitivity analysis, or a stated limitation is the right remedy. Mark optional suggestions as optional.
- **Do not impose preferences.** A method is not wrong because another is more familiar to you. Avoid rules of thumb ("n is too small," "apply Bonferroni") in place of reasoning.
- **Do not ask for citations to your own work** unless they are essential, and say so if you do.
- **Tone.** Criticize the work, not the authors. No sarcasm, no speculation about competence or motive, no comments on the authors' English beyond what affects understanding. Where the evidence supports only a question, ask a question.
- **Acknowledge strengths** specifically, with locations.
- A reviewer's misreading is information for the authors too; say what in the text led you there.

## The Review Report

```text
COMMENTS TO THE AUTHORS

Summary
[The question, approach, and main claims, in your own words. No judgment.]

Strengths
[Specific, with locations.]

Major comments (validity, support for central claims, reproducibility, ethics)
M1. Location: [section, paragraph, line, figure, or table]
    Observation: [what is stated, missing, inconsistent, or unsupported]
    Criterion: [the evidence, principle, or policy it is measured against]
    Why it matters: [consequence for validity, interpretation, or reproducibility]
    Request: [a specific, bounded action; say if it is optional]
M2. [...]

Minor comments (clarity, consistency, displays, citations, reporting details)
m1. [Location: request]

Limits of this review
[What you could not assess, and what specialist review is needed.]

CONFIDENTIAL COMMENTS TO THE EDITOR
[Conflicts and limits of competence; any permitted assistance used; integrity,
ethics, or overlap concerns with exact locations; requests for specialist
review; a recommendation only if the form asks for one.]
```

Keep the two channels consistent: the author-facing report contains the whole scientific assessment, and the confidential part does not contradict it. Reviewers advise and editors decide.

### Final Check Before Sending a Review

- [ ] Authorization and your role (invited reviewer, coreviewer approved by the editor) are documented.
- [ ] Conflicts are resolved or disclosed to the editor.
- [ ] Limits of your competence and any need for specialist review are stated.
- [ ] You know the venue's review model and policies, including its rules on AI tools.
- [ ] No unauthorized person, tool, or service received the manuscript; any permitted assistance is disclosed.
- [ ] The two channels are separate and consistent.
- [ ] Every criticism is specific, located, supported, proportionate, and professional in tone.
- [ ] Nothing is invented: no citation, analysis, experiment, result, or editorial outcome you did not check or were not told.
- [ ] You have planned to delete the manuscript and notes, or to retain them only as the venue allows.

## Responding to Reviewers

The same triage and principles apply to a thesis committee's or examiner's report and to a grant panel's summary statement; for grant resubmissions see also `publishing-and-grants.md`.

### Triage

| Kind of comment | Usual response |
|---|---|
| Methodological concerns, errors, missing literature, unclear writing, gaps in logic | Fix it |
| Requests for more analyses or restructuring; disputes over interpretation | Do what strengthens the paper; where you do less, explain and offer a partial step (a sensitivity analysis, a limitation, a narrower claim) |
| Requests outside the paper's scope; misreadings; reviewers who contradict each other | Explain respectfully; for contradictions, state which course you took and why, and let the editor judge |

### Principles

- Answer every comment, including those you disagree with. Number them (R1.1, R1.2, R2.1).
- Change the manuscript, not only the letter. If a reviewer misunderstood, the text was probably unclear; revise it even when the reviewer was wrong.
- Be specific about what changed and where: quote the new text with section, page, and line.
- When facts change (a number, an analysis), update the analysis and every place the number appears before writing the response, then recheck consistency.
- Disagree with evidence and reasons, courteously, and never by fabricating, hiding, or overstating.
- Do not promise what the manuscript does not deliver.
- Keep reviewer reports confidential; do not paste them into unauthorized tools.
- Submit a marked-up version if the venue asks, and have all authors approve the response.

### Three Stances

- **Agree:** "We agree. We have [action]. The revised text reads: '...' (Section 3.2, lines 210 to 218)."
- **Partly agree:** "The reviewer is right that [valid point]. A full [requested analysis] is not possible because [reason]; we have instead [partial step] and now state this limitation (Section 5, lines 402 to 409)."
- **Disagree:** "We considered this carefully. We have kept [choice] because [reason and evidence]. To prevent the reading the reviewer describes, we clarified [passage] (lines 120 to 126)."

## Response Letter Template

```text
Manuscript [ID]: [Title]
Response to Reviewers

Dear Dr. [Editor],

Thank you for the opportunity to revise our manuscript. We have addressed every
comment. Reviewer comments appear in italics, our responses in plain text, and
quotations from the revised manuscript are indented. Line numbers refer to the
[clean / marked-up] revised version.

Summary of main changes
1. [Change, and the comments it addresses]
2. [...]

Reviewer 1

Comment 1.1. [Reviewer's comment, quoted or closely paraphrased]

Response. [What you did and why, in two to five sentences.]

Change. [Section, page, lines]: "[revised text]"

Comment 1.2. [...]

Reviewer 2

Comment 2.1. [...]

We hope the revised manuscript is now suitable for publication, and we are glad
to make further changes.

Sincerely,
[Corresponding author, for all authors]
```

Replace every bracket before sending. The summary of main changes lets the editor verify the revision in a minute.
