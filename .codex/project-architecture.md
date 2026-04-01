# Project Architecture

## Purpose

This file is the project-level source of truth for long-lived structure inside
this repository.

It should stay smaller and more stable than chat history, session concludes, or
analysis reports.

## Project Goal

- Maintain one progression-capable Obsidian learning-card skill family with a
  low-pollution Codex runtime layout, shared core utilities, and exportable
  wrappers for Claude Code and OpenClaw.

## Organization Model

- One primary project direction: the learning-card skill family.
- Shared references and shared core scripts live under `skills/references/` and
  `skills/shared/learning-card-core/`.
- Repo-level daily operator wrappers may live under `scripts/` when they only
  delegate into shared core and do not create a parallel protocol layer.
- Concrete runtime skills live under `skills/obsidian-*`.
- Export wrappers live under `dist/claude/` and `dist/openclaw/`.
- Regression and validation artifacts live under `analysis/`.
- Project continuity files live under `.codex/`.

## Direction Map

### Direction
- Name: learning-card-family
- Goal: evolve the router, shared core, execution skills, and operator workflow
  as one coherent system
- What belongs here:
  - `skills/obsidian-learning-card-router/`
  - `skills/obsidian-concept-card-capture/`
  - `skills/obsidian-mechanism-card-capture/`
  - `skills/obsidian-method-card-capture/`
  - `skills/obsidian-misconception-card-capture/`
  - `skills/references/`
  - `skills/shared/learning-card-core/`
  - `scripts/` for thin repo-level operator wrappers
  - `dist/claude/` and `dist/openclaw/` for this family
  - `analysis/learning-card-*`
- What does not belong here:
  - unrelated generic skill templates
  - a second parallel skill-family architecture for the same learning-card flow
  - session-only notes that should stay in `.codex/sessions/`
- Preferred worktree name:
  - `codex/<learning-card-topic>`
- Primary state files:
  - `.codex/handoff.md`
  - `.codex/decisions.md`
  - `.codex/todo.md`
- Notes:
  - `main` is the active delivery branch
  - `master` should be treated as a legacy line unless explicitly revived

## Worktree Policy

- Reuse the current project when work stays inside the learning-card family.
- Create a new worktree for a bounded implementation line, regression line, or
  documentation line that may overlap with other ongoing work.
- Base new worktrees on `main`, not `master`, unless the user explicitly asks
  to work on the legacy line.
- Keep temporary branches short-lived and delete them after merge.
- Do not create a separate Codex project unless the work stops being primarily
  about the learning-card family in this repository.

## Decision Boundaries

- Direction-local implementation and regression decisions can be made inside the
  learning-card direction.
- Changes that alter the project shape, active branch policy, or direction map
  should be recorded here and in `.codex/decisions.md`.
- User confirmation is still required for destructive repo operations,
  large-scope restructuring, or reviving a retired parallel architecture line.

## Change Rules

- A project architecture change has happened when:
  - the active long-lived direction changes
  - the branch or worktree policy changes
  - the repo starts or retires a major parallel skill-family line
- After a real structure change:
  1. update `.codex/project-architecture.md`
  2. record the locked decision in `.codex/decisions.md`
  3. update `.codex/todo.md` if follow-up work is needed
  4. refresh `.codex/handoff.md` for the active direction
  5. capture the session conclude when the work session ends

## Current Open Questions

- Whether the current operator-facing bridge should stop at the shared script
  layer or gain a more product-like wrapper for day-to-day card capture.
- Whether any remaining repository docs still imply an older template-first
  project shape and should be normalized to the current learning-card-first
  structure.

## Review Trigger

Revisit this file when:

- a second long-lived direction becomes real
- `master` is intentionally revived as an active delivery line
- the learning-card family splits into multiple semi-independent systems
- worktree usage repeatedly conflicts with the current single-direction model
