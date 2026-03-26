# Routing And Dispatch Spec

## Goal

Make `Routing and Dispatch` a reusable rule layer rather than a loose list of
related thoughts.

This layer is shared across:

- concept cards
- mechanism cards
- method cards
- misconception cards

## Shared Four-Part Structure

Every card may use the same four routing blocks:

- `Direct Routes`
- `Secondary Routes`
- `Gap Signals`
- `Stop Rules`

Use this structure inside the `Routing and Dispatch` section.

## Section Meanings

### Direct Routes

Use for the strongest one-hop rules.

Write:

- the trigger condition
- the next target card
- the reason this route is preferred

Good pattern:

- "When ..., route to [[...]], because ..."

### Secondary Routes

Use for bounded two-hop or three-hop exploration paths.

Write:

- when the direct route is insufficient
- the next path to try
- the value of that extra hop

Good pattern:

- "If [[A]] clarifies X but not Y, continue to [[B]]."

Do not use this section for unbounded brainstorming.

### Gap Signals

Use when the current graph cannot properly absorb the problem.

Write:

- the signal that the graph is missing something
- what kind of node is missing
- which card type should likely be added

Good pattern:

- "If the graph explains the phenomenon but no card explains the causal
  variable, add a new Mechanism card."

### Stop Rules

Use to define when to stop following the current path.

Write:

- the stop condition
- why the current route is no longer useful
- the next action after stopping

Good pattern:

- "Stop this route after two hops if the problem boundary is still expanding;
  restate the problem or add a missing card."

## Strong Rule Standard

A strong routing rule should include at least:

- a condition
- an action
- a target

Better rules also include:

- a reason

Weak examples:

- "This is related to [[X]]."
- "You can also read [[Y]]."
- "Maybe compare with [[Z]]."

Strong examples:

- "When the definition boundary is unclear, return to [[Concept X]]."
- "If Method A fails and the cause is unclear, inspect [[Mechanism Y]] first."
- "If two nearby explanations compete, compare [[A]] before [[B]] when the
  trigger is external."

## Stage Guidance

### Seed

- routing may stay hidden

### Growing

- `Direct Routes` may contain one early rule

### Stable

- `Direct Routes` should begin to contain strong reusable rules
- the other three sections may remain sparse

### Expert-Ready

Minimum expected evidence:

- two strong `Direct Routes`
- one bounded `Secondary Route`
- one explicit `Gap Signal`
- one explicit `Stop Rule`

## Quantity Guidance

Recommended range per section:

- `Direct Routes`: 2 to 5
- `Secondary Routes`: 1 to 3
- `Gap Signals`: 1 to 3
- `Stop Rules`: 1 to 3

If a section becomes much larger, the card may be carrying too many tasks and
should be split or re-scoped.
