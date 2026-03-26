---
name: cross-platform-skill-template
description: Template OpenClaw wrapper for a cross-platform skill. Use as a starting point when building a reusable skill that shares core workflow, references, scripts, and assets across Codex, Claude Code, and OpenClaw.
---

# Cross Platform Skill Template

Read the shared workflow in [../core/guide.md](../core/guide.md).

For this OpenClaw wrapper:

- keep platform-neutral logic in `../core/`
- add OpenClaw-specific metadata only in this wrapper
- update the `name` and `description` before actual use
- keep command-dispatch or other OpenClaw-specific rules out of the shared core

## OpenClaw Wrapper Notes

- Add OpenClaw-specific metadata here only when the real skill needs it.
- Keep path rules and OpenClaw-only dispatch behavior local to this wrapper.
- Do not move those fields into the shared core.
