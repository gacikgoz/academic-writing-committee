# Evidence and Citations

How to find sources, keep track of what supports each claim, verify it, and cite it. The governing rule: a fluent sentence is not evidence, and a citation you have not opened is not a citation.

## Contents

1. What Needs a Citation
2. Finding the Literature
3. Establishing a Gap
4. The Source Ledger
5. The Claim-Evidence Ledger
6. Verification Workflow
7. Citing Well
8. Fabricated and Secondhand Citations
9. Citation Styles and Reference Management
10. Final Citation Audit

## What Needs a Citation

| Cite | Do not cite |
|---|---|
| Direct quotations, always with a page or other locator | Common knowledge in the field |
| Specific data, statistics, and results from others | Your own new findings in this document |
| Others' ideas, theories, arguments, and methods | Generic tools that need no attribution |
| Datasets, software, protocols, standards, reused figures | Statements so basic that a citation would look like padding |
| Any claim a skeptical reader could reasonably doubt | |

Match the kind of evidence to the kind of claim: empirical claims need data, formal claims need a proof or derivation, claims about the state of a field need the literature. Every nonobvious claim rests on one of these or is marked as the author's own argument or speculation.

## Finding the Literature

### Building the Search

1. List the core concepts of the question (usually two to four), a few secondary concepts, and the method terms.
2. For each concept, list synonyms: the terms other disciplines use, older terminology, broader and narrower terms. Missing synonyms are the main cause of both thin searches and false gaps.
3. Join synonyms with OR within a concept and join concepts with AND: `(feedback OR "knowledge of results") AND (timing OR delay*) AND (retention OR "long-term learning")`.
4. Choose databases by field: multidisciplinary indexes for breadth, plus the field's own (for example, biomedical, education, social science, computing, or mathematics indexes and the relevant preprint server).
5. Fix inclusion and exclusion criteria before screening: dates, languages, publication types, populations, methods.

### Three Rounds

- **Direct.** Run the queries over a recent window, read abstracts, and keep what bears on the question.
- **Adjacent.** Harvest new terms and frameworks from the first round and search neighboring fields for other approaches to the same problem.
- **Foundational.** Follow citations backward and forward to the works most of your sources rely on, and confirm that they are still in use.

Keep a search log: database, exact query, date, number of results, number kept at each screening stage. A systematic review requires it; any other project benefits from it when a reviewer asks how sources were found.

### Search Problems

| Symptom | Remedy |
|---|---|
| Too few results | Add synonyms, widen dates, search adjacent fields |
| Too many to screen | Tighten concepts, restrict to the question's population or method |
| Nothing older than a decade | Trace the most-cited works and textbook references |
| One research group or school dominates | Search for rival frameworks and critics |
| Nothing found on the topic | Assume different terminology before assuming a gap |

## Establishing a Gap

"No one has studied X" is a claim, and an empty search is weak evidence for it.

- State the gap in a bounded sentence or two: what is missing, for which population, setting, or method.
- Collect independent evidence for it, ideally three or more items: authors who name the limitation, a question raised and left open, two literatures that do not cite each other, a topic treated only as a boundary case. Record the citation, the passage, and why it shows the gap.
- Classify it: nothing exists, only preliminary or unsatisfactory work exists, or competing accounts exist without resolution.
- Look for it three ways and trust a gap that appears in at least two: a concept-by-method grid with empty cells; a list of problems posed against solutions offered; a timeline showing topics abandoned or just emerging.
- Run the false-gap check: search again with synonyms and in neighboring fields.
- Reject gaps that are merely terminological, trivial, or not addressable by the planned work.

## The Source Ledger

One row per source, kept in a spreadsheet, a reference manager's notes, or a CSV file.

| Field | Content |
|---|---|
| Key | The citation key or ID used in the manuscript |
| Reference | Authors, year, title, venue |
| Identifier | DOI, ISBN, PMID, arXiv ID, or stable URL |
| Version and status | Published, preprint, or accepted manuscript; any correction, retraction, or expression of concern |
| What it supports | The claim or claims it is cited for |
| Locator | Page, section, table, figure, or equation where the support is |
| Verification | Status (unverified or verified), who opened it, and when |
| Access notes | License, permission needed for reuse, confidentiality |

The ledger holds metadata and short notes. Do not paste restricted or copyrighted full text into it.

To check the ledger mechanically, save it as a CSV file with at least the columns `key` (or `citekey`, `source_id`, `id`) and `status` (or `verification_status`), where `status` starts with `verified` once someone has opened the source, and pass it with `scripts/check_citations.py <files> --ledger sources.csv`. An optional `locator` column enables the locator check; other columns (who verified the source and when, for example) are kept for people and ignored by the script. It reports cited keys missing from the ledger, cited keys whose status is not verified, and verified rows without a locator.

## The Claim-Evidence Ledger

For high-stakes documents (clinical, policy, regulatory, a thesis's central claims) or when several people or AI tools draft, track claims as well as sources. The ledger records the sources behind each claim; the claim-evidence matrix in `claims-and-coherence.md` compares how each claim is worded across sections. Use both for research documents.

| Field | Content |
|---|---|
| Claim ID | For example C014 |
| Location | Section and paragraph where it appears, and everywhere it repeats |
| Claim | One sentence |
| Kind | Factual, numeric, method, result, interpretive, or declaration |
| Evidence | Source keys with locators, or the dataset, analysis, table, or figure |
| Status | Confirmatory, exploratory, or descriptive, for results |
| Fit | Supported, partly supported, or unsupported, with the mismatch (direction, size, population, outcome, time point, causal wording, scope, uncertainty) |
| Action | Narrow the wording, add uncertainty, add evidence, or mark unresolved for the author |

- While drafting, you can tag sentences with the claim ID in a comment or a marker such as `[claim:C014]` and remove the markers when references are rendered.
- A composite sentence is supported only if every part is.
- Build the ledger at least for every claim in the abstract and the conclusions: those are the ones readers repeat.
- Unsupported and conflicting claims stay in an open-issues list, out of submission-ready prose.

A ledger entry for every factual sentence is right for high-assurance work and disproportionate for a textbook chapter of settled material. Scale the ledger to the stakes, but never skip the verification below.

## Verification Workflow

**For each source:**

1. Open the authoritative record (publisher page, repository record, the book itself).
2. Confirm title, authors, year, venue, and identifier against it.
3. Find the passage, table, or figure that supports your claim and record the locator.
4. Check that it supports the claim as you state it: same direction, population, intervention or exposure, outcome, time point, and degree of certainty.
5. Check the version and status: preprint or published, corrected, retracted.
6. Mark it verified, with your name and the date.

**For each claim:** classify it, map it to verified sources or to your own data, record its uncertainty, and reword it if the evidence supports less than the sentence says.

Search-engine snippets, abstracts alone, AI-generated summaries, your memory, and another paper's reference list are ways to discover sources. None of them verifies anything.

## Citing Well

- **Choose the form by emphasis.** Author-prominent ("Lee (2021) showed ...") when who said it matters; information-prominent ("... improves retention (Lee, 2021)") when the fact matters.
- **Synthesize.** Group sources that make the same point and distinguish those that differ: "While A argues X, B and C find Y." A string of citations after a vague sentence is not synthesis.
- **Prefer the original.** Cite the primary source for a method, dataset, result, or policy. Cite a review for an overview, and say that it is a review.
- **Secondary citation is a last resort.** If you cannot obtain the original, say so: "(Original, 1950, as cited in Review, 2020)." Never cite the original as if you had read it.
- **Quotations.** Check them character by character, give the locator, keep the context and any negation, and mark omissions and changes. Translate with a note on who translated.
- **Paraphrase from understanding,** not by substituting words in the source's sentence, and still cite.
- **Label unreviewed work.** Mark preprints and working papers as such, and check whether a published or corrected version has replaced them.
- **Balance.** Recent work for the state of the art, older work for foundations, more than one group or school, and the work that disagrees with you. Keep self-citation to what the argument needs.
- **Fit over prestige.** Do not choose sources by citation count, venue rank, or recency quotas, and do not pad. Reference counts and "citations per page" targets vary by field; the test is whether each doubtful claim is supported.
- **Attribute reused material.** Figures, tables, data, code, and long quotations need attribution and, where the license requires, permission.

## Fabricated and Secondhand Citations

Language models produce references that look right and do not exist, or that exist and do not say what is claimed: wrong authors on a real title, a real DOI for a different paper, invented page numbers, invented quotations.

- Never add a reference that no person has opened. If a source cannot be located, remove the reference or replace it with a visible `[[TODO: source for X]]`, and make the sentence it supported narrower, supported by other verified evidence, or marked unresolved for the author. Do not delete the claim by default: the author's own data may support it.
- Never complete missing fields by guessing. Leave the field empty and visible until the record is checked.
- Do not write an example reference that looks real. Use obvious placeholders such as `[[TODO: source for X]]`.
- When an assistant proposes a source, treat it as a search lead. Verification is the six steps above, done on the source itself.
- Check the direction of support: a paper cited for a claim sometimes reports the opposite, or reports it only for a subgroup.
- Check for retractions and corrections, which reference managers and old bibliographies do not show reliably.

## Citation Styles and Reference Management

Use a reference manager or a structured bibliography file (BibTeX, CSL JSON), keep citation keys stable, and let the tool render the list. Free typing of references is where errors enter. Inspect the rendered list by hand anyway.

| Family | In text | Reference list | Typical fields |
|---|---|---|---|
| Author-date (APA, Chicago author-date, Harvard) | (Lee & Osei, 2021); three or more authors as (Lee et al., 2021) in APA 7 at the time of writing (check the current edition) | Alphabetical by author | Social sciences, education, some sciences |
| Numeric (IEEE, Vancouver, many journals) | [3] or a superscript; ranges as [1]–[4] (check the style file: some superscript styles use a hyphen) | Order of first citation | Engineering, computing, medicine |
| Notes and bibliography (Chicago notes) | Footnote or endnote | Alphabetical bibliography | History, humanities |

- The venue's current style file or author instructions decide details such as title capitalization, journal abbreviations, the number of authors listed before "et al.," and DOI format. Style manuals are revised; do not rely on memory of an edition.
- Include a DOI or other persistent identifier wherever one exists.
- Cite software, datasets, and standards with version and identifier, as you would cite papers.
- In author-date styles, give page numbers for quotations and for specific claims in long works.

## Final Citation Audit

- [ ] Every in-text citation has a reference-list entry, and every entry is cited (unless the venue allows a wider bibliography).
- [ ] Every source in the list has been opened by an author and is marked verified in the ledger.
- [ ] Every doubtful or quantitative claim has a source or is the document's own result.
- [ ] Quotations carry locators; reused figures, tables, and data carry attribution and permission.
- [ ] No duplicate entries; identifiers are well formed; names and years match the sources.
- [ ] Retractions, corrections, and superseded preprints have been checked.
- [ ] No long stretch of unsupported assertions, and no section that only strings citations together.
- [ ] Format matches the venue's style, checked on the rendered output.

`scripts/check_citations.py <files> --bib <bibliography>` automates the mechanical parts (keys, duplicates, required fields, identifier syntax, ledger status); `--reference-list <file>` does the same for a free-form list. With `--online` it looks each reference up at Crossref, arXiv, doi.org, and DataCite: NOT_FOUND and a title mismatch are errors, and UNVERIFIED and URL_ONLY entries need a search by hand. It cannot tell whether a work supports its claim, so open each reference through its identifier or the publisher's page.
