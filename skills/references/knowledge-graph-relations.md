# Knowledge Graph Relations

## Goal

Keep graph links precise enough for promotion review and deterministic rendering.

## Shared Structure

Every card may use the same three graph layers:

- `Local Position`
- `Operational Links`
- `Routing and Dispatch`

`Local Position` and `Operational Links` are mostly node-level.
`Routing and Dispatch` is rule-level.

Within `Routing and Dispatch`, use the shared sub-structure from
`routing-and-dispatch-spec.md`:

- `Direct Routes`
- `Secondary Routes`
- `Gap Signals`
- `Stop Rules`

## Core Relationship Types

- `parent`: the target is a higher-level abstraction or category
- `child`: the target is a lower-level specialization or branch
- `adjacent`: the target is a nearby peer, not a parent, child, or dependency
- `depends_on`: this card needs the target as a prerequisite or stabilizing base
- `enables`: this card makes the target easier, clearer, or more achievable
- `contrasts_with`: comparing the target improves judgment or choice quality
- `corrects`: this card fixes the target's error, misuse, or mistaken claim
- `routes_to`: under a stated condition, the next step should move to the target

## Relationship Selection Order

Choose the most specific strong relationship that fits:

1. `corrects`
2. `routes_to`
3. `depends_on`
4. `enables`
5. `parent` or `child`
6. `contrasts_with`
7. `adjacent`

If no strong relationship fits, do not add the link.

## Decision Hints

Use `depends_on` when the current card becomes unstable without the target.

Use `enables` when the target is not a strict prerequisite but becomes easier or
stronger because of this card.

Use `contrasts_with` when comparison itself improves judgment.

Use `adjacent` only when the cards are near peers and no stronger relationship applies.

Use `routes_to` only when a real condition, switch, or next-step rule exists.

## Rule-Level Statement Standard

Weak statements do not qualify for promotion:

- "You can also look at [[X]]."
- "This may relate to [[Y]]."

Strong rule-level statements include condition plus action, for example:

- "When the concept boundary is unclear, switch to [[X]]."
- "If both [[A]] and [[B]] seem relevant, choose [[A]] first."
- "If execution fails and the cause is unclear, fall back to [[Y]]."

For stronger dispatch maturity, also include:

- bounded secondary paths
- explicit missing-node triggers
- explicit stop rules

## Rendering Guidance

Low stages may hide empty graph sections.

`stable` should expose empty `Local Position` or `Operational Links` as missing structure.

`expert-ready` should expose empty `Routing and Dispatch` as a real gap.
