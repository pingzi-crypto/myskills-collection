# Concept Progression Rules

## Goal

Define what changes in a Concept Card when it moves upward in maturity.

## Stage Expectations

### Seed

The card should already explain:

- what question the concept answers
- a working one-sentence definition
- the concept's core essence
- a small validation question

Graph expectation:

- no reliable graph structure required yet

### Growing

The card should add:

- boundary awareness
- nearby concept comparison
- examples and counter-examples
- early node-level graph hints

Graph expectation:

- `graph_maturity: weak`

### Stable

The card should add:

- clearer failure boundaries
- stronger confusion handling
- reliable local graph placement
- concept-level support for adjacent methods or mechanisms

Graph expectation:

- `Local Position` and `Operational Links` carry real content
- at least three strong node-level relationships
- `graph_maturity: local`

### Expert-Ready

The card should add:

- rule-level concept routing statements
- concept-to-mechanism or concept-to-method dispatch rules
- boundary-conflict arbitration
- reusable concept-first learning routes

Graph expectation:

- `Routing and Dispatch` contains strong rules, not weak suggestions
- at least one cross-card-type route
- `graph_maturity: dispatchable`

## Concept-Specific Strong Rule Patterns

Strong examples:

- "When the question shifts from definition to causality, switch to [[...]]."
- "If the concept boundary is still unclear, compare [[A]] before proceeding."
- "Once the definition is clear and execution is needed, route to [[...]]."
- "For beginners, use [[...]] -> [[...]] -> [[...]] in that order."

Weak examples:

- "You can also read [[...]]."
- "This is related to [[...]]."

## Promotion Assessment Targets

Use one of these outcomes:

- `worth promoting`
- `watchlist`
- `stay stable`

When in doubt, prefer `watchlist` or `stay stable` over optimistic promotion.
