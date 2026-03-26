---
name: cross-platform-skill-template
description: Template Codex wrapper for a cross-platform skill. Use as a starting point when building a reusable skill that shares core workflow, references, scripts, and assets across Codex, Claude Code, and OpenClaw.
---

# Cross Platform Skill Template

Read the shared workflow in [../core/guide.md](../core/guide.md).

For this Codex wrapper:

- keep platform-neutral logic in `../core/`
- keep Codex-specific behavior in this file
- update the `name` and `description` before actual use
- add deeper references only when the real skill needs them

## Codex Wrapper Notes

- Add Codex-specific routing or invocation guidance here.
- Keep `SKILL.md` lean and move details into `../core/references/`.
- If you need UI metadata, keep `agents/openai.yaml` in sync with this file.
