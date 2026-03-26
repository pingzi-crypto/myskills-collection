# Misconception Progression Rules

## Goal

Define what changes in a Misconception Card when it moves upward in maturity.

## Stage Expectations

### Seed

The card should already explain:

- the mistaken claim
- why it looks plausible
- why it is wrong
- the corrected understanding

Graph expectation:

- no reliable graph structure required yet

### Growing

The card should add:

- what the error confuses
- trigger signals
- representative counterexamples
- early node-level graph hints

Graph expectation:

- `graph_maturity: weak`

### Stable

The card should add:

- clearer corrective action
- stronger local graph placement
- reliable links to the correct replacement nodes
- clearer distinction from nearby misconceptions

Graph expectation:

- `Local Position` and `Operational Links` carry real content
- at least three strong node-level relationships
- `graph_maturity: local`

### Expert-Ready

The card should add:

- rule-level correction and return-path statements
- priority rules for stacked misconceptions
- reusable debugging or teaching routes
- strong re-entry rules into the correct knowledge path

Graph expectation:

- `Routing and Dispatch` contains strong rules, not weak suggestions
- at least one cross-card-type route
- `graph_maturity: dispatchable`

## Misconception-Specific Strong Rule Patterns

Strong examples:

- "When this mistaken claim appears, correct it before returning to [[...]]."
- "If the confusion is actually definitional, switch to [[...]] instead of staying in misconception mode."
- "When multiple misconceptions are present, fix [[A]] before [[B]] because it is more upstream."
- "After correction, route to [[...]] to rebuild the right model."

Weak examples:

- "You can also read [[...]]."
- "This probably relates to [[...]]."

## Promotion Assessment Targets

Use one of these outcomes:

- `worth promoting`
- `watchlist`
- `stay stable`

When in doubt, prefer `watchlist` or `stay stable` over optimistic promotion.
