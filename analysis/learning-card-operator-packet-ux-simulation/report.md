# Learning Card Operator Packet UX Simulation Report

## Goal

Simulate the current operator-packet output across the three common learning-card
flows and tighten the summary layer before more real-world usage accumulates.

This line focuses on operator comprehension, not on live writing.

## Simulated Flows

- `create`
- `update`
- `promotion review`

## Evaluation Questions

- Can the operator identify the downstream skill in one glance?
- Can the operator see what is still missing before execution?
- Can the operator see what result markers prove completion?
- Does the wrapper avoid pretending that the card is already written?

## Observed Improvements

- the packet now states that only the execution prompt is ready and that no
  card file has been created, updated, or reviewed yet
- the packet now surfaces `Still needed:` explicitly instead of forcing the
  operator to infer missing inputs from placeholders inside the prompt
- the `Next action:` line no longer repeats the full missing-field list, so the
  summary remains scannable in longer create and update cases
- the wrapper now distinguishes `Execution prompt preview:` from
  `Execution prompt copied to clipboard:` so `-PrintOnly` no longer sounds like
  a clipboard write happened
- the summary remains short enough to scan before the execution prompt block

## Simulation Assessment

- `create`
  - clarity score: 5/5
  - strongest signal: missing fields and completion proof are both visible
- `update`
  - clarity score: 5/5
  - strongest signal: existing-card confirmation remains explicit
- `promotion review`
  - clarity score: 5/5
  - strongest signal: completion proof includes `Promotion result:` so the
    operator can distinguish review from update

## Remaining UX Risk

- the operator packet is still a wrapper around a multi-line execution prompt,
  so the next compression opportunity is a thinner alias or command surface
  rather than further shrinking the summary block itself
