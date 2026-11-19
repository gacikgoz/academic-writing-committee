# Sources

The writing guide of this skill (`SKILL.md` and the eight references named in the table below) is a synthesis written in new words. It selects, reorganizes, and restates guidance from the five MIT-licensed skills listed below, resolves the points where they disagree, and adds original material where they were silent. No long passage is copied from any source.

The two scripts in `scripts/` are adapted works, not unchanged copies. Each names its source files and the changes in its header, and each remains under the MIT license of the scripts it derives from. The license texts are reproduced verbatim in `LICENSES/`, one file per copyright holder.

Nothing in this skill comes from `wentorai/research-claw`, which is under the Business Source License.

The rest of the skill is original work written for this plugin and draws on none of the five sources: `references/publication-types.md`, `references/language-mechanics.md`, `references/claims-and-coherence.md`, the modes, publication types and "Five Standards" sections of `SKILL.md`, everything under `committee/`, `profiles/`, `templates/` and `workflow/`, and `scripts/prepare_run.py`. The language-mechanics, repetition and calibration rules of the two checkers are also original additions.

**License of this skill.** The synthesis text and the scripts are released under the MIT License. Any copy or adaptation must keep the source notices in `LICENSES/` and this file.

## Source Skills

| # | Repository and path | License and copyright | Commit read |
|---|---|---|---|
| 1 | https://github.com/jamditis/claude-skills-journalism, `research-toolkit/skills/academic-writing/` | MIT, Copyright (c) 2025 Joe Amditis (`LICENSES/Joe-Amditis-MIT.txt`) | `e1f38cb` |
| 2 | https://github.com/vishalsachdev/claude-code-skills, `skills/paper-writing/` | MIT. Skill license: Copyright (c) 2026 Claude Code Community (`LICENSES/Claude-Code-Community-MIT.txt`). Repository license: Copyright (c) 2026 Vishal Sachdev (`LICENSES/Vishal-Sachdev-MIT.txt`) | `542096a` |
| 3 | https://github.com/K-Dense-AI/claude-scientific-skills, `skills/scientific-writing/` | MIT, Copyright (c) 2025 K-Dense Inc. (`LICENSES/K-Dense-Inc-MIT.md`) | `2d2065f` |
| 4 | https://github.com/K-Dense-AI/claude-scientific-skills, `skills/peer-review/` | MIT, Copyright (c) 2025 K-Dense Inc. (same file) | `2d2065f` |
| 5 | https://github.com/lishix520/academic-paper-skills, `strategist/` and `composer/` | MIT, Copyright (c) 2025 Li Shixiong (`LICENSES/Li-Shixiong-MIT.txt`) | `c325557` |

Source 2 restates, with attribution, ideas from Jason Bennett Thatcher's "Rules for Writing Elite Information Systems Papers" (SSRN). The ideas taken up here (lead with the claim, one label per construct, parallel logic from theory to discussion, mechanisms, boundary conditions in place of vague future work, time-boxed diagnostic passes) are expressed in new words and generalized beyond information systems. The source's bibliographic details for that paper could not be verified and are not repeated; consult SSRN before citing it.

## Surveyed and Not Used

| Candidate | License | Why it is not used |
|---|---|---|
| https://github.com/wentorai/research-claw | Business Source License 1.1 (personal, non-commercial, and academic use only until 2030-03-12) | Its license does not allow reuse in an MIT-licensed plugin. |
| Other skills in the repositories of sources 1 to 5, including K-Dense's `literature-review`, `citation-management`, `research-grants`, `scientific-critical-thinking`, and `latex-posters` | MIT (same files in `LICENSES/`) | Present in the copies examined but not drawn on. No reason was recorded for each, so treat them as candidates for a later revision rather than as rejected. |

The search that found these repositories was not logged beyond this table, so the survey cannot be audited in full; a later revision should record each candidate it examines, with its license and the reason for using or leaving it.

## What Draws on What

| File | Main sources | Notes |
|---|---|---|
| `SKILL.md` | 2 (workflow, working with an author), 3 (accuracy before fluency, no fabrication, evidence-first drafting, placeholders), 5 (outline as specification, dependency order), 1 (compliance steps) | Principles and checklists are consolidated from all five |
| `references/style.md` | 2 (concision tables, active and passive, tense, paragraphs, hedging zones), 1 (transitions, wordiness fixes, tense by section), 3 (meaning-preserving edits, inclusive language, no numeric targets), 5 (transition scaffolds, clarity tests) | All before-and-after examples are new |
| `references/structure.md` | 2 (abstract and introduction formulas, conference, survey, position, report, thesis, and short-paper skeletons), 3 (title, methods, results, discussion checklists; declarations as records), 5 (argument, critical, conceptual, and case sections; six-part introduction; outline as specification), 1 (funnel and reverse funnel) | The section on textbooks and lecture notes and the thesis guidance on paper-based theses and the defense are original |
| `references/evidence-and-citations.md` | 3 (source and claim registries, verification procedure, quotation and source-choice rules, citation audit), 5 (three-round search, synonym generation, gap as an evidenced claim, false-gap check), 1 (Boolean search, search log, citation phrasing), 2 (when to cite, integration forms), 4 (claim-evidence matrix fields, citation review) | |
| `references/figures-and-tables.md` | 3 (choice of display, table and figure checklists, alt text, flow diagrams, provenance), 4 (figure and image review), 2 (exhibit planning, caption conventions) | The section on teaching figures and a few design rules (bars from zero, direct labels) are original |
| `references/mathematics-and-notation.md` | 2 (notation table, macros, problem statements, algorithm levels, proof sketches), 3 (number descriptors, precision, binary-outcome effects), 4 (p-values, equivalence, unit of analysis, multiplicity, missing data, causal and prediction checks, statistics audit condensed to a checklist, heuristics to avoid) | The guidance on equations as prose, definitions, and proofs is original and follows standard mathematical-writing conventions |
| `references/integrity-and-ai.md` | 1 (prohibited and permitted AI uses, disclosure template, presubmission verification, detector limits, misconduct and questionable practices), 3 (no-fabrication list, AI-use record, confidentiality, CRediT, integrity practices and the ALLEA code, open science, reporting-guideline workflow), 4 (confidentiality in review, guideline map, guidelines are not scores), 2 (authorship basics) | Policy statements are reduced to durable principles with instructions to check current texts |
| `references/review-and-revision.md` | 4 (review workflow, four-way classification, five-part comments, proportionate requests, tone, two channels, report scaffold, final check before sending, claim-evidence table, handling suspected integrity problems), 2 (revision passes, diagnostics, reverse outline, read-aloud, response principles), 5 (rubric dimensions, coherence pass, skeptical referee, prioritizing fixes, common argument failures), 1 (triage of reviewer comments, response stances, letter structure), 3 (response workflow, cross-section audit) | The letter template is rewritten; the presubmission sweep restates source 2's time-boxed passes without time or score targets |
| `references/publishing-and-grants.md` | 1 (journal selection, predatory-venue screening, open-access routes, funder mandates, preprint servers, identifiers, cover letter, aims page, grant sections, budget), 3 (venue policy record, submission review, archival handoff), 2 (venue modeling and cultures), 5 (preprint server fit) | Grant principles, common failings, and resubmission guidance are expanded with original material; reviewer simulation follows source 5's outline review |
| `references/publication-types.md`, `references/language-mechanics.md`, `references/claims-and-coherence.md` | none | Original |
| `committee/`, `profiles/`, `templates/`, `workflow/committee.js`, `scripts/prepare_run.py` | none | Original |
| `scripts/check_manuscript.py` | Adapted from 3 (`scripts/lint_manuscript.py`, `scripts/_common.py`) and 2 (`scripts/check_paper.py`) | See the header of the file |
| `scripts/check_citations.py` | Adapted from 4 (`scripts/audit_citations.py`) and 3 (`scripts/check_references.py`, `scripts/_common.py`) | See the header of the file |

## Editorial Decisions

- **Hedging.** Source 2 contains both "remove hedges such as *suggests*" and "use them to calibrate." This skill keeps calibrated hedging (one hedge, on the uncertain element), because removing hedges where uncertainty is real produces overclaims.
- **Abstract opening.** Context first (sources 1, 2) and contribution first (the Thatcher rules in source 2) are both offered, with the venue's recent papers as the tiebreaker.
- **Verb "strengthening."** Source 2's advice to replace *show* and *use* with *demonstrate* and *utilize* is dropped; it conflicts with concision.
- **"This paper argues."** Source 2 calls it an error; major style guides accept it, so it is allowed.
- **Caption placement.** Stated as a venue matter, not as a universal rule.
- **Numeric gates.** Citation counts, pass marks, similarity percentages, sentence-length and passive-voice targets (sources 2 and 5) are kept only as rough priors or dropped. Rubrics are kept as prompts for written defects, with a warning against trusting self-assigned scores.
- **Claim ledger.** Source 3 requires a ledger entry for every factual sentence in every document. Here the ledger scales with the stakes, while verification of every cited source stays mandatory.
- **Field-specific thresholds.** Measurement cut-offs from one survey-research tradition (source 2) and fixed statistical rules of thumb are not presented as general rules.
- **Dated policy claims.** Counts of journals, deadlines, dollar thresholds, named model versions, vendor comparisons, and descriptions of individual journals' AI rules (sources 1, 3, 4) are replaced by principles and "check the current policy."
- **Omitted.** The instruction in sources 3 and 4 to add a citation to their own paper to users' manuscripts; agent-control and tool-specific instructions; the interactive score calculators of source 5; the score-producing linter of source 2 in its original form; the manifest- and marker-dependent validators of sources 3 and 4 in their original form.

## Scripts: Why Adapted and Not Copied

The source scripts that qualified on safety grounds (standard library, no network, read-only; the online verification of `check_citations.py` is an original, opt-in addition) either accept only Markdown and depend on a custom marker and manifest scheme with no tool to produce its hashes (sources 3 and 4), or use heuristics that misfire on decimals, abbreviations, and LaTeX and print an invented overall score (source 2). The two scripts here keep their useful rules, work on Markdown, LaTeX, and plain text, stand alone, and report line-numbered findings without scores.
