# Mechanism Progression Rules

## Goal

Define what changes in a Mechanism Card when it moves upward in maturity.

## Stage Expectations

### Seed

The card should already explain:

- what phenomenon is being explained
- the core variables
- the minimum causal chain
- a compact explanation of why the outcome happens

Graph expectation:

- no reliable graph structure required yet

### Growing

The card should add:

- clearer preconditions
- scope and failure boundaries
- at least one alternative mechanism or counter case
- early node-level graph hints

Graph expectation:

- `graph_maturity: weak`

### Stable

The card should add:

- a stronger causal chain with identifiable weak links
- evidence or repeated observational support
- reliable local graph placement
- confidence about when this mechanism does and does not explain the outcome

Graph expectation:

- `Local Position` and `Operational Links` carry real content
- at least three strong node-level relationships
- `graph_maturity: local`

### Expert-Ready

The card should add:

- mechanism switching rules
- competing-mechanism arbitration rules
- diagnosis routes when the current explanation fails
- cross-type routes to concept or method cards when clarification or action is needed

Graph expectation:

- `Routing and Dispatch` contains strong rules, not weak suggestions
- at least one cross-card-type route
- `graph_maturity: dispatchable`

## Mechanism-Specific Strong Rule Patterns

Strong examples:

- "When the key variable is still undefined, return to [[...]] first."
- "If this mechanism cannot explain the anomaly, compare it against [[...]]."
- "When the mechanism is already clear and the question becomes actionable, route to [[...]]."
- "If both [[A]] and [[B]] can explain the outcome, prefer [[A]] when the trigger is external."

Weak examples:

- "This may relate to [[...]]."
- "Another mechanism is [[...]]."

## Stable Versus Expert-Ready Split

`stable` means the mechanism is a reliable local explanatory node.

`expert-ready` means the mechanism can actively dispatch:

- to a better explanation
- to a prerequisite concept
- to a method once action is clearer
- to a competing mechanism when diagnosis requires discrimination

## Promotion Assessment Targets

Use one of these outcomes:

- `worth promoting`
- `watchlist`
- `stay stable`

When in doubt, prefer `watchlist` or `stay stable` over optimistic promotion.
