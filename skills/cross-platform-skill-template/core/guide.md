# Cross-Platform Skill Core Guide

## Purpose

Replace this file with the platform-neutral workflow for your skill.

Keep this file focused on:

- what the skill does
- when it should be used
- the top-level workflow
- expected outputs
- which references, scripts, or assets to read next

## Recommended Shape

1. State the task boundary in 1-2 sentences.
2. List the input signals that should trigger the skill.
3. Describe the main workflow in 3-7 steps.
4. Point to deeper references only when needed.
5. Keep platform-specific behavior out of this file.

## Example Workflow

1. Read the user request and confirm it matches the skill boundary.
2. Read [references/checklist.md](references/checklist.md).
3. Load any domain-specific references needed for this task.
4. Run scripts from [scripts/](scripts/) only when deterministic execution is useful.
5. Produce the requested output in the required format.

## Output Contract

Replace this section with the stable output shape for the skill.

Example:

- Summary
- Findings
- Risks
- Recommended next steps
