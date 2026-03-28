# Platform Exports

This directory stores non-Codex wrapper entrypoints for the learning-card skill
family.

Purpose:

- keep `skills/` clean for Codex runtime discovery
- keep Claude Code and OpenClaw wrappers in one export-oriented place
- avoid polluting the Codex skill list with wrappers meant for other platforms

Current layout:

- `dist/claude/`
- `dist/openclaw/`

These wrapper files point back to the shared source skills under `skills/`.
