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
- The shared bridge now prefers `pwsh` for clipboard-backed operator flows and
  falls back to Windows PowerShell when `pwsh` is unavailable.
- A more product-like operator entrypoint is now being introduced on top of the
  bridge layer:
  - `build_operator_packet_from_handoff.py`
  - `use_operator_packet.ps1`
- A repo-level thin wrapper now exists for the preferred daily operator path:
  - `scripts/use_learning_card_operator_packet.ps1`
- The repo-level thin wrapper now has direct default clipboard-mode acceptance,
  not only `-PrintOnly` equivalence coverage.
- The operator-packet summary now surfaces missing write-critical inputs as a
  separate `Still needed:` line and keeps `Next action:` compact enough to scan
  during real create and update runs.
- The operator-packet summary now also states that only the execution prompt is
  ready and that no card file has been written yet, reducing the chance that
  operators stop after the wrapper step.
- Regression coverage exists for the handoff parser and prompt bridge under
  `analysis/learning-card-handoff-parser/`.
- Operator acceptance coverage exists for the daily wrapper flow under
  `analysis/learning-card-operator-bridge-acceptance/`.
- Operator packet acceptance coverage is being added under
  `analysis/learning-card-operator-packet-acceptance/`.
- Operator packet acceptance now covers the full operator triad under
  `analysis/learning-card-operator-packet-acceptance/`:
  - create
  - update
  - promotion review
- Execution result contract acceptance exists under
  `analysis/learning-card-execution-result-acceptance/`.
- Bridge live preflight coverage now exists under
  `analysis/learning-card-bridge-live-preflight/` to turn canonical handoff
  text plus explicit parameters into execution-ready prompt packets aligned
  with recorded live cases.
- The bridge live preflight layer now also checks that generated packets are
  placeholder-free and emits machine-readable `*-check.json` readiness files.
- A read-only live acceptance harness now exists for the recorded real-write
  validations under `analysis/learning-card-live-acceptance-harness/`.
- The read-only live acceptance harness now covers all three recorded real-write
  shapes:
  - existing-card update
  - existing-card promotion review
  - ambiguous no-card-in-scope create
- One bridge-originated live update run has now been completed from canonical
  handoff -> bridge packet -> preflight gate -> real concept-card update.
- One bridge-originated live promotion-review run has now been completed from
  canonical handoff -> bridge packet -> preflight gate -> real method-card
  review update.
- One bridge-originated live ambiguous create run has now been completed from
  canonical handoff -> bridge packet -> preflight gate -> real misconception
  card creation.
- The shortest daily operator path is now documented more explicitly in the
  existing README and operator manual so users can distinguish bridge output
  from actual card-write proof.
- The docs set now includes copyable daily examples for the operator-packet
  path across create, update, and promotion-review flows.

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
- Users can still stop too early after the bridge step if the downstream
  execution skill is not invoked and no file-level result line is returned.
- The bridge-originated operator stack is now live-proven across all three
  target execution shapes:
  - update
  - promotion review
  - ambiguous create
- The bridge preflight layer is still synthetic; it does not prove that the
  downstream execution skill was actually run in the same session.

## Next Step

- Decide whether the current clarified operator-packet entrypoint is enough, or
  whether the bridge should gain an even thinner daily command surface beyond
  shared scripts after a few more real operator uses.
- The repo-level wrapper now provides that thinner command surface inside the
  repository; the remaining question is whether anything thinner than a single
  repo-local command is still needed.
- If a new higher-risk validation line is opened, prefer targeting the
  bridge-originated operator path rather than re-proving the already-covered
  ambiguous create shape.
- The bridge-originated operator path is now live-proven across update,
  promotion-review, and ambiguous-create shapes and can now be maintained as a
  stable validation line rather than an open gap.

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
- `skills/references/learning-card-standard-operating-manual.md`
- `analysis/learning-card-handoff-parser/report.md`
- `analysis/learning-card-operator-bridge-acceptance/report.md`
- `analysis/learning-card-execution-result-acceptance/report.md`
- `analysis/learning-card-bridge-live-preflight/report.md`
- `analysis/learning-card-bridge-originated-live-validation/report.md`
- `analysis/learning-card-bridge-originated-promotion-review-validation/report.md`
- `analysis/learning-card-bridge-originated-ambiguous-create-validation/report.md`
- `analysis/learning-card-live-acceptance-harness/report.md`
- `analysis/learning-card-operator-packet-acceptance/report.md`
