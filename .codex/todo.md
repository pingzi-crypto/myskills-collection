# Direction Todo

## Now

- Keep new learning-card work based on `main` rather than `master`.
- Collect a few more real operator uses to decide whether the new repo-level
  operator-packet wrapper is enough, or whether any thinner command surface is
  still needed.

## Next

- If confusion still appears in real use, shorten the path from operator packet
  output to actual execution-skill invocation even further.
- Review whether any higher-value aliases, wrapper commands, or docs examples
  should be added beyond the current operator-packet wrapper.
- If a higher-risk live line is opened, use the new bridge preflight cases as
  the starting packet instead of rebuilding execution prompts manually.
- Maintain the now-live-proven bridge-originated stack as contracts evolve, and
  rerun the triad when router, bridge, or execution contracts materially shift.

## Later

- Revisit project-level branch policy if `master` ever needs to be retired or
  explicitly archived.
- Extend regression coverage when router or shared-core contracts expand.

## Blocked

- None.

## Done Recently

- Added the router handoff prompt parser.
- Added bridge regression coverage for router handoff parsing.
- Added operator-facing stdin and clipboard modes to the handoff bridge.
- Added a thin PowerShell wrapper for the default clipboard-to-clipboard
  operator path.
- Added operator acceptance coverage for the wrapper-driven bridge flow.
- Added execution result contract acceptance after the bridge step.
- Added a read-only live acceptance harness for the existing real-write
  validation line.
- Wrote the initial project-level `.codex` continuity files.
- Hardened the bridge to prefer `pwsh` and documented the shortest daily
  operator flow more explicitly.
- Extended the read-only live acceptance harness to cover the recorded
  ambiguous create real-write case as well.
- Added bridge live preflight acceptance for update, promotion review, and
  ambiguous create packets aligned to recorded live cases.
- Completed one bridge-originated live update run from canonical handoff to a
  real concept-card update on disk.
- Completed one bridge-originated live promotion-review run from canonical
  handoff to a real method-card review update on disk.
- Completed one bridge-originated live ambiguous create run from canonical
  handoff to a real misconception-card create on disk.
- Compressed the operator-packet summary so `Still needed:` carries missing
  fields and `Next action:` stays action-focused in real use.
- Added an explicit operator-packet status line so wrapper output states that
  no card file has been written yet.
- Added a repo-level thin wrapper for the operator-packet flow and validated
  that it matches the shared-core wrapper output.
- Added direct clipboard-mode acceptance for the repo-level operator-packet
  wrapper so the daily default path is regression-covered.
- Expanded operator-packet acceptance from create-only coverage to the full
  create/update/promotion-review triad.
- Added copyable docs examples for the repo-level operator-packet path across
  create, update, and promotion-review flows.
- Strengthened bridge-originated live acceptance with read-only evidence-chain
  checks across handoff, preflight packet, readiness gate, live report, and
  target note.
- Added a repo-level preflight gate wrapper and acceptance line so future
  bridge-originated live runs can consume `*-check.json` outputs as an actual
  go/no-go gate.
- Added a cross-layer contract drift watch so router, operator-packet,
  preflight, execution-result, and live-harness expectations can be checked
  together after contract changes.
