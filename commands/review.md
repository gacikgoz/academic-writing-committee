---
description: Independent committee review of an academic document, with a prioritized report and no edits (--no-committee for a single-session review)
argument-hint: "[--no-committee | --size low|medium|high|full] [main file] [publication type] [venue or call]"
---
Use the academic-writing-committee skill (`${CLAUDE_PLUGIN_ROOT}/skills/academic-writing-committee/SKILL.md`) in **review mode** for: $ARGUMENTS

If the arguments contain `--no-committee` (or "no committee"), or the Workflow tool is not available, follow the skill's "No-Committee Option": review the document yourself in this session with `references/review-and-revision.md`, report the findings by severity, and change nothing.

If the arguments contain `--size low|medium|high|full` (or a size in words, such as "a medium committee"), pass that size to `prepare_run.py` with `--size`; without one, the configuration's `committeeSize` applies (default `full`). Tell the user the size, the committee it gives and the estimated agent calls before launching.

Otherwise follow the skill's review-mode steps: set up a minimal committee configuration for the document and its publication type, prepare the run with `--review-only`, and launch the committee workflow. The readers and reviewer lenses of the type's profile assess the current text in parallel and the committee chair verifies and consolidates their findings into a prioritized report; nothing in the document is changed. Summarize the report for the user when it finishes.
