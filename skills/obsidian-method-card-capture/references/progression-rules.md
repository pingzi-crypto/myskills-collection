# Method Progression Rules

## Goal

Define what changes in a Method Card when it moves upward in maturity.

## Stage Expectations

### Seed

The card should already explain:

- what problem the method solves
- the core idea
- the minimum usable structure
- a small validation question

Graph expectation:

- no reliable graph structure required yet

### Growing

The card should add:

- fit and non-fit scenarios
- method boundary awareness
- comparison with nearby alternatives
- at least early node-level graph hints

Graph expectation:

- `graph_maturity: weak`

### Stable

The card should add:

- hidden assumptions
- failure modes
- decision criteria
- reliable local graph placement

Graph expectation:

- `Local Position` and `Operational Links` carry real content
- at least three strong node-level relationships
- `graph_maturity: local`

### Expert-Ready

The card should add:

- rule-level dispatch statements
- method selection or arbitration rules
- fallbacks when execution fails
- reusable route-planning value

Graph expectation:

- `Routing and Dispatch` contains strong rules, not weak suggestions
- at least one cross-card-type route
- `graph_maturity: dispatchable`

## Method-Specific Strong Rule Patterns

Strong examples:

- "When the prerequisite concept is still unclear, return to [[...]] first."
- "If execution fails and the cause is unclear, fall back to [[...]]."
- "If both [[A]] and [[B]] seem valid, choose [[A]] when time is constrained."
- "For beginners, use [[...]] -> [[...]] -> [[...]] in that order."

Weak examples:

- "You can also read [[...]]."
- "This is somewhat related to [[...]]."

## Promotion Assessment Targets

Use one of these outcomes:

- `worth promoting`
- `watchlist`
- `stay stable`

When in doubt, prefer `watchlist` or `stay stable` over optimistic promotion.
