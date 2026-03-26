---
name: cross-platform-skill-template
description: Template Claude Code wrapper for a cross-platform skill. Use as a starting point when building a reusable skill that shares core workflow, references, scripts, and assets across Codex, Claude Code, and OpenClaw.
---

# Cross Platform Skill Template

Read the shared workflow in [../core/guide.md](../core/guide.md).

For this Claude Code wrapper:

- keep platform-neutral logic in `../core/`
- add Claude-specific fields only in this wrapper
- update the `name` and `description` before actual use
- keep advanced Claude features out of the shared core

## Claude Wrapper Notes

- Add Claude-specific frontmatter here only when the real skill needs it.
- Examples: tool restrictions, forked context, or other Claude-only behavior.
- Do not move those fields into the shared core.
