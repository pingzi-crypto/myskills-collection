# Learning Card Operator Surface Review

## Goal

Decide whether the current repo-level operator surface is already thin enough
for day-to-day use, or whether the repository should add an even thinner alias
or wrapper beyond the current operator-packet entrypoint.

## Current Operator Surface

Primary day-to-day operator entry:

- `pwsh -File scripts/use_learning_card_operator_packet.ps1`

Primary live-run readiness gate:

- `pwsh -File scripts/use_learning_card_preflight_gate.ps1 -CheckFile <...>`

Supporting contract layers already in place:

- operator bridge acceptance
- operator packet acceptance
- preflight gate acceptance
- contract drift watch
- copyable daily docs examples

## Evaluation Criteria

- Does one repo-level command already cover the normal path from router handoff
  to execution prompt?
- Does one repo-level command already cover the live-run readiness gate?
- Would another alias remove meaningful operator work, or only hide an already
  short command string?
- Would another alias increase discovery noise or duplicate the current command
  surface?

## Assessment

- The normal daily path is already one repo-level command plus paste:
  - `scripts/use_learning_card_operator_packet.ps1`
- The live-run readiness path is already one repo-level command plus one
  explicit check file:
  - `scripts/use_learning_card_preflight_gate.ps1`
- The remaining operator effort is not command length. It is:
  - filling missing write inputs
  - choosing the correct existing card when the mode is `update` or
    `promotion review`
  - waiting for file-level completion proof
- A thinner alias would shorten typing slightly, but it would not remove any of
  the real cognitive or workflow steps above.
- Another alias would also create more surface area to document, test, and keep
  aligned with the current repo-level wrappers.

## Conclusion

The current operator surface is thin enough for now.

Recommended policy:

- keep `scripts/use_learning_card_operator_packet.ps1` as the daily operator
  entry
- keep `scripts/use_learning_card_preflight_gate.ps1` as the live-run gate
- do not add another alias or wrapper unless new real operator use shows that
  command invocation itself, rather than missing inputs or execution semantics,
  has become the primary friction point

## Reopen Conditions

Revisit this decision only if one of these becomes true:

- repeated real use shows operators still stop before execution after using the
  repo-level wrapper
- the command path itself is reported as the main friction more than the
  missing-input or completion-proof steps
- a future platform constraint makes `pwsh -File scripts/...` materially harder
  to invoke than it is now
