---
description: Start here. Looks at your project, asks only what it cannot find out, and runs the right mode (write, review, check, or a committee)
argument-hint: "[what you want, in your own words] [file or folder]"
---
Use the academic-writing-committee skill (`${CLAUDE_PLUGIN_ROOT}/skills/academic-writing-committee/SKILL.md`) and follow its section **"Start Here: The Guided Flow"** for: $ARGUMENTS

1. If the request is about a passage, a paragraph or a section, do it now in Write mode; no setup and no questions.
2. Otherwise run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/academic-writing-committee/scripts/project_setup.py detect --json` from the project root (or the folder the user named). Say back what it found in one or two lines.
3. If it found a committee configuration, continue that run: show its status briefly, ask only for what the configuration lacks (size, effort), and resume.
4. Otherwise ask the open questions in one batch with the question tool (at most four questions, four options each, the recommended option first): the task (revise with a committee, revise in this session, review only, check references and language), the publication type if uncertain, the goal, the guidelines if none were found, and for a committee the size and the effort.
5. For a committee: write the configuration with `project_setup.py init` and the answers, run the preflight, state the plan in three lines and launch. For the other tasks: do them now, without a committee.

Never ask what the detection already answered, and never show the configuration file unless the user asks.
