# Direction Todo

## Now

- Keep new learning-card work based on `main` rather than `master`.
- Collect a few more real operator uses to decide whether the new
  operator-packet wrapper is enough, or whether the operator bridge should gain
  an even thinner daily command surface.

## Next

- If confusion still appears in real use, shorten the path from operator packet
  output to actual execution-skill invocation even further.
- Review whether any higher-value aliases, wrapper commands, or docs examples
  should be added beyond the current operator-packet wrapper.
- Decide whether to add a stronger live acceptance layer for a
  bridge-originated operator session after the bridge step.
- If a higher-risk live line is opened, use the new bridge preflight cases as
  the starting packet instead of rebuilding execution prompts manually.
- Use the preflight `*-check.json` outputs as the go/no-go gate before any
  future bridge-originated live operator run.
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
