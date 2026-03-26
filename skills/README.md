# Skills Index

This directory stores reusable skills and templates for this collection.

## Available Entries

### `cross-platform-skill-template`

Starter template for building one shared skill core with thin wrappers for:

- Codex
- Claude Code
- OpenClaw

Path:

- `skills/cross-platform-skill-template/`

Use this entry when you want to:

- start a new cross-platform skill from a clean skeleton
- keep shared workflow in `core/`
- isolate platform-specific behavior in wrapper directories

## Suggested Workflow

1. Copy `cross-platform-skill-template/` to a new skill folder.
2. Rename the placeholder skill name in each wrapper.
3. Rewrite `core/guide.md` with the real workflow.
4. Add only the references, scripts, and assets you actually need.
5. Validate each platform wrapper separately.

## Collection Direction

As this repository grows, this index should remain the first place to look for:

- stable skills
- starter templates
- platform-specific variants
