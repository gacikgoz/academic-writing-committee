---
description: Check a manuscript's language mechanics, claims wording and citations
argument-hint: "[files] [bibliography]"
---
Use the academic-writing-committee skill's checkers on: $ARGUMENTS (single session; never uses the committee)

Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/academic-writing-committee/scripts/check_manuscript.py <manuscript files>` and `python3 ${CLAUDE_PLUGIN_ROOT}/skills/academic-writing-committee/scripts/check_citations.py <manuscript files> --bib <bibliography>` (the bibliography goes after `--bib`, never as a manuscript file; find it from `\bibliography` or `\addbibresource` if the user did not name it). For a document with a free-form reference list instead of a bibliography database, use `--reference-list <file>`. Add `--online --cache .writing-committee/citations-cache.json` when the network allows: it looks every reference up at Crossref, arXiv, doi.org and DataCite and reports NOT_FOUND and a title METADATA_MISMATCH as errors, and a first-author or year METADATA_MISMATCH as a warning. For UNVERIFIED and URL_ONLY entries, and to confirm that a work supports its sentence, open the work by its identifier or the publisher's page. Treat the findings as candidates: confirm each one in context, group them by severity, and propose concrete fixes. Never mark a reference as verified unless you found the work itself.
