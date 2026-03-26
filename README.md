# myskills-collection

Cross-platform skill templates for Codex, Claude Code, and OpenClaw.

## What This Repo Contains

This repository currently includes a starter template for building one skill that can be adapted across three platforms:

- Codex
- Claude Code
- OpenClaw

The template lives here:

- `cross-platform-skill-template/`

## Design Goal

The template follows a simple rule:

> Keep reusable task logic in a shared core, and keep platform-specific behavior in thin wrappers.

That means:

- `core/` stores shared workflow, references, scripts, and assets
- `codex/` stores the Codex wrapper
- `claude/` stores the Claude Code wrapper
- `openclaw/` stores the OpenClaw wrapper

## Directory Structure

```text
cross-platform-skill-template/
├─ core/
│  ├─ guide.md
│  ├─ references/
│  ├─ scripts/
│  └─ assets/
├─ codex/
│  ├─ SKILL.md
│  └─ agents/openai.yaml
├─ claude/
│  └─ SKILL.md
└─ openclaw/
   └─ SKILL.md
```

## How To Use This Template

1. Copy `cross-platform-skill-template/` to a new folder with your real skill name.
2. Replace the placeholder skill name `cross-platform-skill-template` in each wrapper.
3. Rewrite `core/guide.md` with the real workflow.
4. Add only the references, scripts, and assets your skill actually needs.
5. Keep platform-specific fields only in the matching wrapper.

## Compatibility Strategy

Use this template when you want:

- one shared task definition
- one shared set of references and scripts
- separate wrappers for each platform

Do not force all platform-specific features into a single shared `SKILL.md`.

## Notes

- The repository intentionally keeps the template minimal.
- Platform-specific metadata should stay local to each wrapper.
- Shared files should remain platform-neutral whenever possible.
