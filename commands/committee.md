---
description: Run the self-improving writing committee until every part of the document is approved (--no-committee for a single-session revision)
argument-hint: "[--no-committee | --size low|medium|high|full] [--effort low|medium|high|xhigh|max|default] [configuration file] [stages or units]"
---
Use the academic-writing-committee skill (`${CLAUDE_PLUGIN_ROOT}/skills/academic-writing-committee/SKILL.md`) in **committee mode** for: $ARGUMENTS

If the arguments contain `--no-committee` (or "no committee"), follow the skill's "No-Committee Option" instead: revise the document yourself in this session, one unit at a time in reading order, against its guidelines, running both checkers and the project's build on each unit; launch no workflow and no subagents.

If the arguments contain `--size low|medium|high|full` (or a size in words, such as "a medium committee"), pass that size to `prepare_run.py` with `--size`; without one, the configuration's `committeeSize` applies (default `full`). If the arguments contain `--effort <level>`, pass it to `prepare_run.py` with `--effort`. If neither the arguments nor the configuration's `effort` give an effort level, **ask the user** which to use before preparing the run (`low`, `medium`, `high` recommended, `xhigh`, `max`, or `default` for each role's own), in one question together with the size if that is open too; never choose it for them. Tell the user the size, the effort, the committee and writer ladder they give, and the estimated agent calls before launching.

Otherwise follow `${CLAUDE_PLUGIN_ROOT}/skills/academic-writing-committee/committee/procedure.md` from start to finish: begin with the skill's guided flow ("Start Here" in `SKILL.md`: `scripts/project_setup.py detect`, the open questions in one batch, `project_setup.py init`), or continue the configuration it finds; then run the preflight checks, prepare the run, launch the committee workflow, record and verify each run, and continue automatically until every unit and the whole document are approved or a unit needs a human decision.
