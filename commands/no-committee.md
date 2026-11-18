---
description: Plain academic writing without the committee (one session, no subagents)
argument-hint: "[write | review | check | revise] [file, section or topic] [publication type] [instructions]"
---
Use the academic-writing-committee skill (`${CLAUDE_PLUGIN_ROOT}/skills/academic-writing-committee/SKILL.md`) with the **no-committee option** for: $ARGUMENTS

Follow the section "No-Committee Option" of the skill: work in this session only, with no subagents and no Workflow tool. Choose the mode from the request (write, review, check, or a revision of a whole document unit by unit; write when it is unclear). Identify the publication type (ask only if it cannot be inferred), read the guide and the references it maps to the task, and do the work directly. Before you finish, run the manuscript checker and, when the text cites sources, the citation checker on what you changed, and fix what they report. A review changes nothing in the document.
