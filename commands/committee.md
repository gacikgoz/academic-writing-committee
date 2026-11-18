---
description: Run the self-improving writing committee until every part of the document is approved (--no-committee for a single-session revision)
argument-hint: "[--no-committee | --size low|medium|high|full] [configuration file] [stages or units]"
---
Use the academic-writing-committee skill (`${CLAUDE_PLUGIN_ROOT}/skills/academic-writing-committee/SKILL.md`) in **committee mode** for: $ARGUMENTS

If the arguments contain `--no-committee` (or "no committee"), follow the skill's "No-Committee Option" instead: revise the document yourself in this session, one unit at a time in reading order, against its guidelines, running both checkers and the project's build on each unit; launch no workflow and no subagents.

If the arguments contain `--size low|medium|high|full` (or a size in words, such as "a medium committee"), pass that size to `prepare_run.py` with `--size`; without one, the configuration's `committeeSize` applies (default `full`). Tell the user the size, the committee it gives and the estimated agent calls before launching.

Otherwise follow `${CLAUDE_PLUGIN_ROOT}/skills/academic-writing-committee/committee/procedure.md` from start to finish: find or write the project configuration, run the preflight checks, prepare the run, launch the committee workflow, record and verify each run, and continue automatically until every unit and the whole document are approved or a unit needs a human decision.
