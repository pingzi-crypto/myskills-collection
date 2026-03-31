# Direction Handoff

## Goal

- Keep the learning-card family usable as a long-lived, low-pollution workflow:
  router classification, shared-core bridge utilities, thin execution skills,
  deterministic rendering, and regression-backed evolution.

## Current State

- `main` is the active branch and current source of truth for this project.
- The active system shape is:
  - router
  - shared learning-card core
  - four execution skills
- Router handoff is explicitly classification-only and does not imply that a
  card file already exists.
- The shared parser can turn canonical router handoff text into a downstream
  execution prompt skeleton.
- The operator-facing bridge now supports:
  - `--handoff-file`
  - `--handoff-text`
  - `--stdin`
  - `--from-clipboard`
  - `--copy`
  - `use_handoff_bridge.ps1` as the thinnest Windows wrapper
- Regression coverage exists for the handoff parser and prompt bridge under
  `analysis/learning-card-handoff-parser/`.
- Operator acceptance coverage exists for the daily wrapper flow under
  `analysis/learning-card-operator-bridge-acceptance/`.

## Locked Decisions

- Treat the learning-card family as the primary long-lived direction in this
  repository.
- Keep the architecture as router plus shared core plus thin execution skills.
- Use canonical router handoff text as a stable machine-readable boundary
  between routing and execution.

## Open Risks

- Some future sessions may accidentally start from `master` or other stale local
  lines instead of `main`.
- Some older repository descriptions may still imply broader or older structure
  assumptions and need periodic cleanup.
- The current operator bridge is usable but still script-first; future users may
  still want a more product-like wrapper beyond the current thin PowerShell
  helper.

## Next Step

- Decide whether the current thin PowerShell wrapper plus operator acceptance is
  enough, or whether the bridge should gain a more product-like wrapper beyond
  shared scripts.

## Acceptance

- The project has a stable `.codex` continuity layer.
- The learning-card direction can be re-entered without relying on chat memory.
- Future work starts from `main` and uses the current learning-card-first
  architecture by default.

## Key Files

- `README.md`
- `skills/README.md`
- `skills/references/learning-card-skill-family.md`
- `skills/references/learning-card-standard-operating-manual.md`
- `skills/shared/learning-card-core/scripts/build_execution_prompt_from_handoff.py`
- `skills/shared/learning-card-core/scripts/use_handoff_bridge.ps1`
- `analysis/learning-card-handoff-parser/report.md`
- `analysis/learning-card-operator-bridge-acceptance/report.md`
