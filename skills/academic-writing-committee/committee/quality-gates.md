# Quality Gates

This file defines how severe a problem is, when a unit or a run counts as finished, and which objective checks every project should run. The project's guidelines add their own rules; where they are stricter, they win.

## Severity Scale

| Severity | Meaning | Examples |
|---|---|---|
| **Blocker** | The document is wrong, broken, dishonest or loses content. Never shipped. | A false claim, a wrong equation or number, a failed build, an undefined reference, text cut off the page, content deleted without record, a reference that cannot be found or does not exist, a fabricated quotation, result or date, an unsupported or overclaimed claim in the abstract or conclusion. |
| **Major** | A substantive violation of the guidelines, or a problem that stops the target reader from learning or misleads them. Must be fixed before acceptance. | Overclaiming (a claim stronger than its evidence); underselling a central claim or contribution (a supported result hedged, buried or called "merely" a small step); contributions, numbers or scope that differ between abstract, introduction, body and conclusion; a conclusion that adds new claims; a cited work that does not support the sentence; a missing baseline, ablation or uncertainty estimate that a claim depends on; a required element missing (for example a figure, worked example or required venue section); a term used before it is defined; an explanation that is not cumulative; an unreadable or misleading figure; a level gap; a section that repeats another without purpose; pervasive repetitive or formulaic wording; a title that breaks the title style of `references/structure.md` (an abbreviation, a claim the evidence does not carry, the contribution shrunk to one component or stage); a title written or changed without the author's explicit approval. |
| **Minor** | A local defect in clarity, style or form. Fixed by the editors. | A cosmetic extra hedge on a peripheral statement, a clumsy sentence, a repeated word or sentence opening, a chain of "and", an en or em dash in prose, a caption or a table (house rule; where a project allows dashes, a hyphen where an en dash belongs or an em dash used as a habitual connector), a comma right after a conjunction or sentence-initial connective, a paragraph that opens with "To", an abbreviation used before it is written out, an internal identifier of the studied software (a function or operation name, a code identifier, a file name, a version or a hash) in prose, a caption, a table or a figure, an inconsistent term, a caption that does not say what to notice, a list that is not parallel, a heading not in the required case. |
| **Nit** | A matter of taste. Fixed only if cheap. | Word choice between two correct options. |

Severity follows the effect on the reader, not the effort of the fix. Anything that changes what a claim says or how strongly it says it is at least major and goes to the writer, because editors may not change claim strength; an editor who finds such a problem reports it as a concern for the chair or the Editor-in-Chief.

## Unit Acceptance Gate

A unit is accepted only when all of the following hold:

1. The chair has decided *accept*, and no blocker or major action is open.
2. The unit check passes: no errors, no undefined references, no content cut off, and no failure the lint rules mark as major. The chair may dismiss a checker finding as a false positive only with a written reason; a confirmed build error, undefined reference or loss of content is never dismissed.
3. Every action from every round is resolved, or dismissed by the chair with a written reason.
4. No reader has an open major finding. In particular the newcomer persona is never left asking "what is this?" and the expert persona finds something worth reading.
5. The editors have finished, and the regression check passed against the accepted snapshot.

## Run Completion Gate

A run is complete only when every unit in scope is accepted, the global checks pass (after the Integration Editor's fixes), nothing is deferred to a later run, and the Editor-in-Chief approves without reopening a unit. Anything less is reported as *continue* (units deferred to the next run) or *incomplete* (units unresolved), together with every open action. A run never reports success it has not reached.

## Disputes and Waivers

A writer who disagrees with an action disputes it in the change report with evidence: a guideline rule, a computation, a source. The chair rules on the evidence and records the reason. A chair may waive a finding only with a written reason that cites the guidelines; a waiver is visible in the chair report and in the run summary. Taste never overrides an explicit guideline.

## Evidence Standard

A finding must be checkable by someone who has not read your report: give `file:line` (or section and rendered page), quote the problematic text when it is short, and say what the correct state is. Numerical and mathematical findings include the computation that shows the error.

## Mechanical Check Catalog

Use the checks that apply to the project's format. Projects add their own commands in their configuration (`checks.unit`, `checks.global`), and the retrospective adds learned patterns to `lint_rules.md`. The Mechanical Checker runs the commands and searchable patterns below; the items marked *(lens)* need judgment and belong to the reviewer named, not to the checker.

### LaTeX Builds

- **Build:** compile into a private output directory with the engine the project requires; any error (`!` lines in the log) is a blocker.
- **Read the whole log.** TeX wraps log lines at 79 characters, so join continuation lines before searching; a word such as "undefined" can be split across two lines.
- **References:** `Reference ... undefined`, `Citation ... undefined` and `There were undefined references` are blockers; `multiply defined` labels are major.
- **Overfull boxes:** an overfull `\hbox` wider than 1pt is major (text runs into the margin); report the input line.
- **Boxes and floats:** tcolorbox messages such as "upper box part has become overfull" mean text may be cut off: blocker until the rendered page shows that no text is lost. `Float too large` is major.
- **Fonts and characters:** `Missing character` and font substitution warnings are major.
- **Rendered check** *(lens: presentation)*: for units with figures, tables or heavy mathematics, render the affected pages to images and look at them; clipping, overlapping labels and illegible text are major.

### Structure and Cross-References

- Every `\ref`, `\eqref`, `\cite` and hyperlink target exists and points to the intended content.
- Headings follow the hierarchy and the capitalization the guidelines require.
- Every figure and table is referred to in the text before or near where it appears, and has a caption that says what to notice.

### Mathematics and Numbers

- Every displayed equation is punctuated as part of its sentence and every symbol is defined before or right after use.
- Every numerical example is recomputed by a script; a mismatch is a blocker *(lens: technical)*.
- Dimensions and shapes agree across the equations, the text and the figures.

### Prose

- Run `scripts/check_manuscript.py` on the unit's files: it reports dash and hyphen misuse, internal identifiers (house rule R6), chains of "and", repetition (of words, phrases, and sentence openings), formulaic transitions, overclaiming, stacked hedges, long sentences, and placeholder text. Its findings are candidates: a reviewer confirms each in context.
- Terms follow the glossary; one concept, one name.
- Lists are parallel in grammar and no deeper than the guidelines allow.
- No placeholder text (`TODO`, `XXX`, `??`, or dummy Latin filler) remains. This includes a `[[TODO: source for ...]]` left where an unverifiable reference was removed: before acceptance the writer narrows the sentence or supports it with verified evidence, and if neither is possible the chair leaves the unit unresolved so that a person decides (`references/evidence-and-citations.md`).

### Claims and Coherence *(lens: claims)*

- The claim-evidence matrix of `references/claims-and-coherence.md` has no unsupported claim.
- Contributions, key numbers and scope are identical in the abstract, introduction, body, discussion and conclusion; the conclusion adds nothing new.

### References

- Run `scripts/check_citations.py <files> --bib <bibliography>` (or `--reference-list <file>`), with `--online` in global rounds and for the references lens: no missing or duplicate keys, no malformed identifier, no entry the source ledger marks as unverified, no NOT_FOUND reference and no title METADATA_MISMATCH. UNVERIFIED and URL_ONLY references are verified by search before acceptance. A clean report does not show that a work supports the sentence citing it.
- Every reference is confirmed to exist by opening it through its identifier or the publisher's page, and it supports the sentence that cites it *(lens: references)*.

### Markdown and Other Formats

- Links and anchors resolve; headings are unique within a page; code blocks name their language.
- For word-processor formats, check styles rather than direct formatting, and check that cross-references are fields rather than typed numbers.

## Reader Satisfaction

Reader ratings guide the chair but do not override the guidelines. A persona's rating of 1 or 2 always needs an explanation in the chair report and usually a major action. A rising trend in ratings across rounds is the best single signal that the revision is working.
