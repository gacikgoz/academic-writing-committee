---
description: Independent committee review of an academic document, with a prioritized report and no edits (--no-committee for a single-session review)
argument-hint: "[--no-committee | --size low|medium|high|full] [--effort low|medium|high|xhigh|max|default] [main file] [publication type] [venue or call]"
---
Use the academic-writing-committee skill (`${CLAUDE_PLUGIN_ROOT}/skills/academic-writing-committee/SKILL.md`) in **review mode** for: $ARGUMENTS

If the arguments contain `--no-committee` (or "no committee"), or the Workflow tool is not available, follow the skill's "No-Committee Option": review the document yourself in this session with `references/review-and-revision.md`, report the findings by severity, and change nothing.

If the arguments contain `--size low|medium|high|full` (or a size in words, such as "a medium committee"), pass that size to `prepare_run.py` with `--size`; without one, the configuration's `committeeSize` applies (default `full`). If the arguments contain `--effort <level>`, pass it to `prepare_run.py` with `--effort`. If neither the arguments nor the configuration's `effort` give an effort level, **ask the user** which to use before preparing the run (`low`, `medium`, `high` recommended, `xhigh`, `max`, or `default` for each role's own), in one question together with the size if that is open too; never choose it for them. Tell the user the size, the effort, the committee and writer ladder they give, and the estimated agent calls before launching.

Otherwise follow the skill's review-mode steps: find the document, its type and its venue with `scripts/project_setup.py detect` and ask only what it leaves open ("Start Here" in `SKILL.md`), write a minimal configuration with `project_setup.py init`, prepare the run with `--review-only`, and launch the committee workflow. The readers and reviewer lenses of the type's profile assess the current text in parallel and the committee chair verifies and consolidates their findings into a prioritized report; nothing in the document is changed. Summarize the report for the user when it finishes.
