# Publication Types

What each kind of academic document is for, how it is built, how it is judged, how it usually fails, and how the committee is configured for it. Section-level craft (titles, abstracts, introductions, methods, results, discussion) is in `structure.md`; prose in `style.md`; citations in `evidence-and-citations.md`; displays in `figures-and-tables.md`; reporting guidelines and disclosure in `integrity-and-ai.md`; responding to reviews in `review-and-revision.md`; claim strength in `claims-and-coherence.md`; submission and funder rules in `publishing-and-grants.md`. This file carries what differs by type: the judge and the decision, the parts each type must have, typical failures, and the committee configuration; the craft of each part lives in the files above.

Length and format figures below are typical ranges, not rules. The call for papers, the journal's author guide, the publisher's contract, the funder's solicitation, or the institution's regulations always decide. Read them first, and look at three to five recent accepted examples from the same venue.

## Contents

1. Using This File
2. Journal Article
3. Conference Paper, Short Paper, Workshop Paper, and Extended Abstract
4. Survey, Systematic Review, and Tutorial
5. Thesis and Dissertation
6. Book (Textbook or Monograph)
7. Book Chapter
8. Lecture Notes
9. Technical Report and White Paper
10. Grant Proposal
11. Documents That Mix Types
12. Comparison Table

## Using This File

**What to do.** Before planning or revising, name the type, the primary judge (who decides the document's fate), and the decision that judge makes: accept, fund, pass, adopt, or assign. Then read that type's section and set `publicationType` in the committee configuration to the matching profile in `profiles/`.

**How to check it.** You can complete this sentence from the draft alone: "This is a [type] for [readers]; [judge] will decide whether to [decision], mainly on [criteria]." If you cannot, the type or the audience is unsettled, and structure decisions will drift.

Every section below covers the same six elements: purpose and readers, structure, length and format, what the judges look for (the label names the type's judges: reviewers, examiners, editors or readers), failure modes, and committee configuration. Reader personas and reviewer lenses are defined in `committee/catalog.json`.

### Committee Mechanics Common to All Types

- **Unitization.** Profiles with `"unitization": "whole-document"` judge the document as one unit: list the main file under `documents` in the configuration, and the run makes one unit per file at the profile's `defaultDifficulty`. Profiles with `"unitization": "chapters"` expect stages whose units are chapters or lectures (see `committee/config.md`).
- **Adding and dropping.** To add one lens or reader, name its catalog key in `addReviewers` or `addReaders`; to remove one, use `dropReviewers` or `dropReaders`. A full `readers`, `reviewers`, or `editors` list in the configuration replaces the profile's list.
- **Whole-document coherence.** For documents with several units, every global round adds a cross-unit claims review: it compares contributions, key numbers, terms, and scope across the abstract, introduction, unit summaries, and conclusion, and the editor-in-chief reopens the units that disagree.
- **Editors.** Every profile runs the `line` editor, then the `consistency` editor.
- **Limits.** Whole-document profiles use more rounds on one unit (`maxRounds` 6, `waveSize` 4); chapter profiles use fewer rounds over more units (`maxRounds` 5, `waveSize` 6). Raise `maxRounds` only for a unit that keeps failing on substance, not on style.

## Journal Article

**Purpose and readers.** A complete, citable record of a study, argument, or result, read by specialists who may build on it and by researchers in adjacent fields who want the idea. It is judged by a handling editor and two or more peer reviewers with time to read closely.

**Structure.** Default to the paper skeleton below; the field's conventions (IMRaD in empirical sciences, theorem-proof in mathematics, argument sections in humanities) can reshape it. Section-level detail is in `structure.md`.

| Part | Must achieve |
|---|---|
| Title | Name the subject and the finding or contribution; claim no more than the body shows |
| Abstract | Problem, gap, approach, main result with numbers, scope; every number matches the body |
| Introduction | Stakes, the precise gap, this work, an explicit contribution statement, roadmap |
| Related work | Position the contribution against the closest prior work, grouped by approach, fairly |
| Method | Enough detail for a competent reader to evaluate and, where feasible, repeat the work |
| Experiments or results | Answer each research question in order, with uncertainty, baselines, and ablations |
| Discussion | Interpret against prior work, give mechanisms and alternative explanations |
| Limitations | Specific threats, their likely direction, and the boundaries of the claims |
| Conclusion | Answer the opening question in its own terms; no new results or citations |

**The contribution statement** is the spine. Each item names what is new and points to where it is supported.

- Before: "We study the problem of X and present some interesting findings."
- After: "We contribute (1) an estimator for X that remains unbiased under missing labels (Section 3); (2) a benchmark of 12 datasets on which it reduces error relative to the strongest baseline (Section 5); and (3) an analysis of when it fails (Section 6)." (Illustrative; use only numbers the paper reports.)

**Length and format.** Highly field-dependent. Many journals set a main-text word limit, a reference limit, or a figure limit; some (common in mathematics and theoretical fields) set none. Letters and brief communications are far shorter than full articles. Abstracts usually run 150 to 300 words and may need to be structured. Check the author guide for article types, limits, required statements, and supplementary material rules.

**What reviewers look for.** Is the question important and the gap real? Is the method sound and fully described? Do the results support the stated contributions, with appropriate uncertainty and comparisons? Is related work fair and current? Is the article clear enough to follow without the authors present? Are data, code, and materials available as the journal requires?

**Failure modes.**
- Contributions in the abstract and introduction that differ in number, wording, or strength from those in the discussion and conclusion.
- Overclaiming ("first," "state of the art," "proves") without dated evidence, or underselling the real contribution under stacked hedges (see `claims-and-coherence.md`).
- A limitations paragraph written for form ("future work should consider other datasets").
- Related work listed paper by paper with no positioning sentence.
- Methods reconstructed from results, or analyses in the results that the methods never declared.

**Committee configuration** (`journal-article.json`). Whole document, difficulty `hard`. Readers: `expert` (depth and missing work) and `adjacent` (jargon and motivation for neighboring fields). Reviewers: `technical`, `claims`, `experiments`, `significance`, `references`, `presentation`, `language`, `venue`. For a theoretical or argumentative article with no experiments, drop `experiments`; `technical` then carries the proofs and `claims` the argument. For a broad-readership journal, add `generalist` or `skimmer`.

## Conference Paper, Short Paper, Workshop Paper, and Extended Abstract

**Purpose and readers.** A conference paper reports a contribution quickly to a community that triages hundreds of submissions. Its first judge is a program committee member reading under time pressure; its later readers skim the first page to decide whether to read on. In computing and some engineering fields, peer-reviewed conference papers are primary archival publications; in many other fields a conference contribution is an abstract or a talk and the archival version goes to a journal. Find out which applies before deciding how complete the paper must be.

**Structure.** Same parts as the journal article, compressed, with two differences.

- **The first page carries the paper.** Problem, why it is hard, key insight, contribution list, and the headline result must all be visible by the end of the introduction, often with a figure that shows the idea or the main result.
- **Related work may move** after the experiments, when the approach is easier to compare once seen. The rough page allocation for an eight-page computing paper is in `structure.md`, Conference Papers in Computing.

| Variant | Typical scope | What it must still do |
|---|---|---|
| Full paper | Complete method and evaluation | Everything in the journal table, within the page limit |
| Short paper | One focused idea or result | State problem, gap, and contribution in half a page; one convincing piece of evidence |
| Workshop paper | Early or exploratory work | Make the idea and its promise clear; label preliminary results as preliminary |
| Extended abstract | A talk or poster proposal | Problem, approach, main finding, why the audience should care; often few or no references |

**Length and format.** Typical in computing: about 6 to 10 pages for a full paper, 2 to 4 for a short or workshop paper, 1 to 2 for an extended abstract. Venues differ on whether references, appendices, and required checklists count toward the limit, whether supplementary material is reviewed, and whether submissions must be anonymized for double-anonymous (also called double-blind) review. The template is usually mandatory and is often checked mechanically. Check the call.

**What reviewers look for.** Clear novelty against the closest prior work; soundness; an evaluation with strong, tuned, current baselines, ablations, and reported variance; reproducibility details; and whether the claims are believable from the abstract, introduction, and main results table alone. Reviewers also check fit to the venue's scope.

**Failure modes.**
- The contribution is first stated on page 3.
- Experiments that do not map to the stated contributions, or baselines that are weak, untuned, or outdated.
- Results reported as single runs with no variance where the field expects several seeds.
- Cutting to the page limit by shrinking figures below legibility, deleting limitations, or removing method details needed to reproduce (see `structure.md`, Position Papers and Short Papers, for what to cut instead).
- Broken anonymization: self-citation in the first person, acknowledgments, repository links that reveal identity.
- A workshop or short paper that claims full-paper conclusions from preliminary evidence.

**Committee configuration** (`conference-paper.json`). Whole document, difficulty `hard`. Readers: `pc-reviewer` (the twenty-minute accept-or-reject read), `expert`, and `skimmer` (can the contribution be recovered from title, abstract, figures, and conclusion). Reviewers: the journal set (`technical`, `claims`, `experiments`, `significance`, `references`, `presentation`, `language`) plus `venue`, which checks the page limit, template, anonymization, and required statements. For an extended abstract, drop `experiments` and `presentation` and keep `claims` so preliminary results stay labeled as preliminary.

## Survey, Systematic Review, and Tutorial

**Purpose and readers.** A survey organizes a literature so that newcomers can enter the field and experts can see its shape, gaps, and trends. A systematic review answers a focused question reproducibly from all eligible studies. A tutorial teaches a method well enough that a reader can apply it. Readers are newcomers, experts checking coverage, and practitioners choosing a method.

**Structure.**

| Part | Must achieve |
|---|---|
| Introduction | Motivation, scope (topics, period, exclusions), review questions, contributions relative to earlier surveys |
| Scope and selection method | How works were found and chosen: sources, queries, dates, inclusion and exclusion criteria; for systematic reviews, the registered protocol, screening, extraction, and risk-of-bias procedure |
| Background | The minimum shared vocabulary and notation, fixed once and reused |
| Taxonomy | A classification with stated dimensions, defensible boundaries, and every surveyed work placed in it |
| Thematic sections | Per category: the idea, representative works, strengths, limits, and how they compare |
| Comparison tables | Consistent columns (assumptions, data, guarantees, cost, evaluation setting) across all rows |
| Synthesis | Trends, trade-offs, contradictions and their likely causes, what no single paper shows |
| Open problems | Per problem: current progress, what is missing, what solving it would enable |
| Conclusion | What the field knows, what it does not, and where the review's own coverage stops |

A survey synthesizes; it does not list (section design is in `structure.md`, Review Articles).

- Before: "Smith et al. proposed A. Jones et al. proposed B. Lee et al. proposed C."
- After: "Methods in this family trade label efficiency for robustness: A and B need no labels but degrade under shift, whereas C recovers robustness at the cost of a labeled calibration set (Table 3)."

A tutorial replaces the taxonomy with a teaching sequence: motivation, a running example, the method built up step by step, a complete worked case, pitfalls, and pointers to further reading. Apply the cumulative-explanation rules for textbooks (see `structure.md`, Textbooks and Lecture Notes).

**Length and format.** Surveys are commonly longer than research articles and carry long reference lists; some survey venues set their own limits. Systematic reviews in many fields are expected to follow a reporting guideline (PRISMA 2020 in health and many other fields; software engineering often follows Kitchenham's guidelines) and may need registration (PROSPERO for many health reviews). Details are in `integrity-and-ai.md`. Check the venue and the field's guideline.

**What reviewers look for.** Coverage that is complete and balanced for the stated scope and period; a taxonomy that clarifies rather than relabels; accurate description of every cited work; synthesis and comparison; a reproducible selection method where one is claimed; useful open problems; and a clear difference from existing surveys.

**Failure modes.**
- References that do not exist or do not say what the survey attributes to them. In a survey this is fatal; verify every entry (see `evidence-and-citations.md`).
- No stated scope, so any omission looks like a gap in coverage.
- A taxonomy whose categories overlap or whose dimensions change from section to section.
- Comparison tables with inconsistent columns or blank cells left unexplained.
- Open problems that are generic ("more data," "better efficiency") rather than specific.
- A "systematic" label on a review with no documented search.

**Committee configuration** (`survey.json`). Whole document, difficulty `hard`. Readers: `newcomer`, `expert`, `practitioner`. Reviewers: `coverage` (scope, balance, taxonomy, synthesis), `claims`, `references` (every cited work must exist and be described accurately), `technical`, `presentation`, `language`, `venue` (the venue's limits and, for a systematic review, the reporting guideline). For a survey too long to judge as one unit, define stages with one unit per major section and let the integration editor keep the taxonomy, notation, and comparison tables consistent across units. For a tutorial, add `pedagogy`.

## Thesis and Dissertation

**Purpose and readers.** A thesis demonstrates that the candidate has made an original, substantiated contribution and commands the field. Its judges are examiners (internal and external) and a committee; its later readers are researchers who want the full account behind the papers. Terms differ by country: in some systems "thesis" is the doctoral document and "dissertation" the master's, in others the reverse; follow the institution's usage.

**Structure.** One argument across chapters.

| Part | Must achieve |
|---|---|
| Abstract | The research questions, the contributions, and the main findings, in the same words as the introduction and conclusion |
| Introduction chapter | Problem, research questions, contribution list with the chapter that delivers each and any publication it draws on, scope, outline |
| Background or literature chapter | A critical synthesis by theme that ends in the gaps the thesis fills |
| Core chapters | Each answers one research question: opening that links to earlier chapters, content, discussion, summary that hands over to the next |
| Contribution or general discussion chapter | Answer the research questions across chapters, show how the parts form one contribution, state limits |
| Conclusion | Summary of contributions, limitations, future work, all consistent with the introduction |

**How chapters, published papers, and the contribution chapter relate.**
- In a monograph thesis, chapters are written for the thesis and may later yield papers. In a thesis by publication (also called an article-based or compilation thesis), the core chapters are the papers, framed by an introduction and a synthesis chapter. Many institutions allow a hybrid. Check the regulations for which form is permitted and how published work must be included.
- Map contributions to chapters and chapters to papers in one table in the introduction, and keep it true.
- Unifying reused papers, declaring coauthors' roles, and the cross-chapter consistency pass are in `structure.md` (Theses and Dissertations) and `review-and-revision.md` (Coherence Pass for Long Documents).
- The contribution chapter is not a summary of each chapter in turn. It argues what the chapters establish together that none establishes alone.

Before: "Chapter 4 presented a method. Chapter 5 presented experiments."
After: "Chapter 4's estimator and Chapter 5's benchmark together answer RQ2: the estimator is unbiased in theory and remains within the reported error bound on the five benchmark datasets that meet its assumptions."

**Length and format.** Varies widely by country, institution, degree, and field; doctoral theses are much longer than master's theses, and some institutions set a maximum word count or require a specific template, front matter, and declarations. Check the regulations and the graduate school's formatting guide.

**What examiners look for.** Originality; whether each claimed contribution is substantiated; consistency of the contributions across abstract, introduction, chapters, and conclusion; command of the literature; sound methods; honest limitations; and the candidate's own contribution in joint work. Examiners prepare questions about the weakest points, so find them first.

**Failure modes.**
- A stapled collection of papers with no argument connecting them.
- Contributions that change in number or wording between the introduction and the conclusion.
- A literature chapter that is an annotated bibliography.
- Inconsistent notation and terminology across chapters that began as separate papers.
- Overclaiming originality where a published paper by others overlaps.

**Committee configuration** (`thesis.json`). Units are chapters, difficulty `hard`. Readers: `examiner`, `expert`, `generalist` (committee members outside the specialty). Reviewers: `guidelines` (put the institution's rules in the guidelines file), `technical`, `claims`, `experiments`, `references`, `presentation`, `language`. Each chapter's `claims` lens checks that chapter; the cross-unit claims review in every global round and the editor-in-chief check that the contributions are stated identically in the abstract, introduction, chapters, and conclusion. Put the introduction, the contribution chapter, and the conclusion in a final stage, so that they are revised after the core chapters, or reopen them after the core chapters change. For a nonempirical thesis, drop `experiments`.

## Book (Textbook or Monograph)

**Purpose and readers.** A textbook teaches a subject cumulatively to students and self-learners; a monograph presents an extended argument or body of research to specialists. Both are read over weeks, out of order by some readers, and are judged by a publisher's editor and external reviewers at the proposal stage, then by adopters and readers.

**Structure.** The book is designed before the chapters.

| Part | Must achieve |
|---|---|
| Preface | Audience, prerequisites, what the book covers and omits, paths through the chapters |
| Chapter sequence | Dependency order: nothing used before it is introduced; forward references only as promises |
| Each chapter | Motivating question, objectives as abilities, exposition, worked examples, summary, exercises (textbook) or argument and conclusion (monograph) |
| Cross-chapter apparatus | Notation table, glossary, index, consistent numbering of definitions, figures, and examples |
| End matter | Solutions or hints where promised, references, appendices for prerequisites |

Chapter design, cumulative explanation, worked examples, and exercises are in `structure.md`, Textbooks and Lecture Notes. At book level, also keep a dependency map (what each chapter assumes and provides) and check it after every reorganization.

**Length and format.** The publisher's contract sets the extent (words or pages), figure count, and manuscript format. Agree on these before drafting; for the proposal itself, follow the publisher's proposal guidelines.

**What reviewers look for.** A clear audience and a reason this book is needed beside competing titles; correct, current content; a sensible order; for textbooks, examples and exercises that teach; for monographs, a sustained argument that adds to the field.

**Failure modes.**
- Chapters written as independent essays with drifting notation, repeated introductions, and missing cross-references.
- Coverage pursued over understanding: definitions without motivation, results without worked examples.
- Exercises that do not match the objectives, or that were never solved by the author.
- Level drift: an entry-level chapter followed by one that assumes graduate background without saying so.

**Committee configuration** (`book.json`). Units are chapters, difficulty `standard` (raise individual chapters with `difficultyOverrides`). Readers: `newcomer`, `expert`, `chapter-skimmer` (can a student reviewing for an exam find the essentials from the headings, figures, boxes, and summary). Reviewers: `guidelines`, `technical`, `claims`, `pedagogy`, `presentation`, `references`, `language`. The integration editor, the cross-unit claims review, and the editor-in-chief keep terminology, notation, numbers, and cumulative order consistent across chapters. Run a first stage that settles notation and the preamble before chapters are revised, and a final stage for the preface and introduction. For a research monograph, raise `claims` to `opus`/`high`, keep `pedagogy` only if the book teaches, and replace the `newcomer` reader with `adjacent`.

## Book Chapter

**Purpose and readers.** A chapter in an edited volume or handbook gives an authoritative, self-contained account of one topic for the volume's readers, who may read only this chapter. Its judges are the volume editors and sometimes external reviewers.

**Structure.**
- **Opening** that states the topic, why it matters, the chapter's scope, and what the reader needs to know beforehand.
- **Body** organized by the topic's logic: a mini-survey, a tutorial, or a research synthesis, depending on what the editors commissioned.
- **Closing** with the state of knowledge, open questions, and pointers into the literature.
- **Fit to the volume:** use the volume's style sheet, cross-reference sibling chapters where the editors ask, and avoid re-deriving what a sibling chapter covers.

Before: "As discussed in the previous chapter, the model is trained as usual."
After: "We train the model by stochastic gradient descent on the loss in Equation (2) (Chapter 3 of this volume treats optimization in depth)."

**Length and format.** The editors set the word or page limit, the reference style, and the template in the invitation or contract. Check it, and ask early about reuse of your own published material and about figure permissions.

**What editors look for.** Self-containment, authority (accurate, current, balanced), fit with the volume's scope and level, and compliance with the style sheet and deadline.

**Failure modes.**
- A recycled research paper with a new title: too narrow, too dense, and dependent on the original's context.
- Silent dependence on the reader having read other chapters.
- A one-sided account of a contested topic in a volume meant to be a reference.

**Committee configuration** (`book-chapter.json`). Whole document, difficulty `hard`. Readers: `newcomer` (self-containment) and `expert` (authority). Reviewers: `guidelines` (put the volume's style sheet in the guidelines file), `technical`, `claims`, `references`, `presentation`, `language`. For a tutorial-style chapter, add `pedagogy`; for a survey-style chapter, add `coverage`.

## Lecture Notes

**Purpose and readers.** Notes teach one course, usually to students who attend lectures but read the notes alone. They are judged by whether students can learn from them, not by coverage.

**Structure.**
- **Course level:** a syllabus page with prerequisites, objectives, and the lecture sequence; stable numbering across versions; a dated version line.
- **Each lecture:** where the course stands, the one main result of the lecture, exposition with full sentences for reasoning that would be spoken, worked examples, a summary of what to remember, exercises, and the link to the next lecture.
- **Marking:** distinguish essential material from enrichment so students know what is examinable.

Before: "Thm 3.2. Proof: trivial by 3.1."
After: "Theorem 3.2 says that the estimator is consistent. The proof applies Lemma 3.1 to each term; the only step that needs care is the interchange of limit and sum, which holds because the terms are bounded."

**Length and format.** No external norm; set by the course. Keep lectures roughly parallel in length and construction so that students know where to look.

**What readers look for.** Can a student who missed the lecture follow the notes? Are the examples and exercises enough to practice? Are the notation and numbering stable?

**Failure modes.**
- Slide fragments presented as notes: no connective reasoning.
- Results used before they are covered, because the lecture order changed and the notes did not.
- Exercises without any answers or hints, or with solutions in a different notation.

**Committee configuration** (`lecture-notes.json`). Units are lectures or chapters, difficulty `standard`. Readers: `newcomer` and `chapter-skimmer`. Reviewers: `technical`, `pedagogy`, `presentation`, `language`, `references`. Prefer worked examples and exercises over completeness. For graduate courses, add the `expert` reader; if the notes cite research results in detail, add `claims`.

## Technical Report and White Paper

**Purpose and readers.** A technical report records work fully for practitioners and specialists: a system, a study, a benchmark, or an evaluation, often including what papers omit (full parameters, negative results, dead ends). A white paper argues for an approach or decision to informed nonspecialists. Both may be published without peer review, so the authors carry the whole burden of accuracy.

**Structure.** Front matter, a one-page executive summary that stands alone, purpose and scope, background and requirements, a body organized by the thing reported, results, recommendations, and appendices (details in `structure.md`, Technical Reports). Every recommendation must follow from evidence in the report.

Before: "We recommend adopting framework B."
After: "We recommend framework B for workloads under the latency budget in Section 2, because it met the budget in all six configurations tested (Table 4); for batch workloads the evidence favors neither framework."

**Length and format.** Set by the issuing institution or report series, which may assign a report number and require a template. White papers are usually short; check the commissioning organization's expectations.

**What readers look for.** Accuracy, reproducibility, clear scope, actionable and justified recommendations, and an honest account of what was not tested.

**Failure modes.**
- An executive summary that promises more than the body shows.
- Recommendations without evidence, or evidence without a recommendation.
- Marketing language in a white paper ("revolutionary," "seamless") that a technical reader discounts.
- No version or date, so readers cannot tell which report is current.

**Committee configuration** (`technical-report.json`). Whole document, difficulty `standard`. Readers: `practitioner` and `expert`. Reviewers: `technical`, `claims`, `references`, `presentation`, `language`. If the report contains experiments or benchmarks, add `experiments`. For a white paper addressed to decision makers, add the `generalist` reader.

## Grant Proposal

**Purpose and readers.** A proposal persuades a funder that a specific project is important, new, feasible for this team, and worth its cost. Its judges are a panel of specialist reviewers and generalists who score against published criteria, often under time pressure and in competition with many other proposals.

**Structure.** Funders name and order the sections differently; map these functions onto the funder's template rather than imposing them.

| Function | Must achieve |
|---|---|
| Summary or abstract | The problem, the aims, the approach, and the expected outcome, readable by a generalist |
| Aims or objectives | Two to four specific, testable aims; each states what will be done and what will be known afterwards |
| Significance | Why the problem matters, what is known, the gap, and who benefits when it is closed |
| Innovation | What is new in concept, method, or application, relative to the closest existing work |
| Approach | For each aim: rationale, methods, expected results, how success is measured, risks and alternatives |
| Feasibility | Preliminary results, team expertise, access to data, equipment, and partners |
| Timeline | Milestones and deliverables per aim, consistent with the approach and the team's effort |
| Budget justification | Every cost tied to an activity in the approach; nothing unexplained, nothing missing |
| Required statements | Data management, ethics, broader impact, and other items the call lists |

Before: "Aim 1: To explore the role of X in Y."
After: "Aim 1: Determine whether X causes Y in setting Z. We will test this with design W (Section C.1). Expected outcome: an estimate of the effect of X with enough precision to rule in or out an effect of the size reported in pilot data."

**Length and format.** Funders set strict limits per section (pages or characters), fonts, margins, and attachments, and many reject noncompliant proposals without review. Review criteria are published in the call; some are named explicitly, such as the U.S. National Science Foundation's Intellectual Merit and Broader Impacts. Copy the call's criteria and requirements into the guidelines file. Funder-specific advice is in `publishing-and-grants.md`.

**What reviewers look for.** Significance, innovation, a rigorous and feasible approach, preliminary evidence, a capable team, a realistic timeline and budget, and alternatives for risky steps. Generalists on the panel need the significance and main idea without specialist knowledge.

**Failure modes.**
- Aims that are activities ("explore," "investigate") rather than questions with outcomes.
- Aims that depend on each other so that failure of the first sinks the rest, with no alternative.
- Aims, timeline, and budget that disagree (an aim with no milestones, a cost with no activity).
- A problem asserted but not shown to be important, or methods without an analysis plan.
- No preliminary evidence of feasibility, or no discussion of what could go wrong.
- Overpromising beyond the duration and team; or burying the innovation under background.
- Ignoring the call's priorities; noncompliance with the template, page limit, or required statements; small type and dense pages.

**Committee configuration** (`grant-proposal.json`). Whole document, difficulty `hard`. Readers: `generalist` and `specialist`. Reviewers: `venue` (compliance with the call), `significance`, `feasibility`, `claims`, `references`, `language`. If the approach contains derivations, statistical power calculations, or preliminary results, add `technical`.

## Documents That Mix Types

Many documents combine types. Choose the primary type by the decision the document must win and who makes it; then borrow lenses and readers from the secondary type.

**What to do.**
1. Name the primary judge and decision. That sets the profile.
2. List what the secondary type adds (a taxonomy, experiments, exercises, a funding request).
3. Add the corresponding lens or reader with `addReviewers` or `addReaders`, and drop what does not apply with `dropReviewers` or `dropReaders`.
4. Write to the primary type's structure and length rules; fit the secondary material inside it.

| Document | Primary profile | Borrow from |
|---|---|---|
| Thesis by publication | `thesis` | `journal-article` lenses (`significance`, `venue` if chapters must match published versions) |
| Survey with new experiments or a new benchmark | `survey` | `experiments` lens; state the new contribution separately from the review |
| Journal extension of a conference paper | `journal-article` | Check the journal's policy on prior publication and how much new material it expects |
| Tutorial chapter in a textbook | `book` | `coverage` for the further-reading section |
| Survey chapter in an edited volume | `book-chapter` | `coverage` lens |
| Lecture notes becoming a textbook | `book` | Keep the `chapter-skimmer` reader; add `expert` |
| Technical report later submitted as a paper | `journal-article` or `conference-paper` | Cut to the venue's limit; move details to supplements |
| Proposal with substantial preliminary results | `grant-proposal` | `technical` and, if results are experimental, `experiments` |
| Position or perspective paper | `journal-article` or `conference-paper` | Drop `experiments`; keep `claims` and `significance` |

**How to check it.** The profile's `goal` matches what success means for this document; every distinctive part (taxonomy, experiments, exercises, aims) has a lens that will read it; nothing in the configuration judges the document by a type it is not (for example, `experiments` on a pure survey).

## Comparison Table

Lengths are typical ranges only; the venue, publisher, funder, or institution decides.

| Type | Primary judge | Central question | Unit | Readers | Distinctive lenses | Typical length |
|---|---|---|---|---|---|---|
| Journal article | Editor and peer reviewers | Is it sound, new, and complete? | Whole | expert, adjacent | experiments, significance, venue | Set by journal; varies widely by field |
| Conference paper | Program committee | Is the contribution clear and convincing within the limit? | Whole | pc-reviewer, expert, skimmer | experiments, significance, venue | About 6 to 10 pages (full), 2 to 4 (short) in computing |
| Survey or review | Editor and reviewers | Is coverage complete, organized, and accurate? | Whole or sections | newcomer, expert, practitioner | coverage, references, venue | Often longer than an article |
| Thesis | Examiners | Is it original, substantiated, and coherent? | Chapters | examiner, expert, generalist | guidelines, claims, experiments | Set by institution |
| Book | Publisher, reviewers, adopters | Does it teach or argue cumulatively? | Chapters | newcomer, expert, chapter-skimmer | pedagogy, guidelines | Set by contract |
| Book chapter | Volume editors | Is it self-contained and authoritative? | Whole | newcomer, expert | guidelines, claims | Set by editors |
| Lecture notes | Students and instructor | Can a student learn from them alone? | Lectures | newcomer, chapter-skimmer | pedagogy | Set by the course |
| Technical report | Practitioners | Is it accurate and actionable? | Whole | practitioner, expert | claims, technical | Set by the series |
| Grant proposal | Review panel | Is it significant, new, and feasible? | Whole | generalist, specialist | venue, significance, feasibility | Strict per-section limits in the call |
