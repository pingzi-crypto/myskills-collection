# Direction Todo

## Now

- Check the remaining project docs for stale structure language or old branch
  assumptions.
- Keep new learning-card work based on `main` rather than `master`.
- Decide whether the current thin PowerShell wrapper is enough, or whether the
  operator bridge should gain a more product-like wrapper.

## Next

- Tighten the shortest end-to-end operator flow from router handoff to actual
  execution-skill invocation.
- Review whether any higher-value aliases, wrapper commands, or docs examples
  should be added beyond the current PowerShell wrapper.
- Decide whether to add a stronger acceptance layer for actual execution-skill
  invocation after the bridge step.

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
