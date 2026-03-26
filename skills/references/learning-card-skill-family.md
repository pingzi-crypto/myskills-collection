# Learning Card Skill Family

## Goal

Define how the learning-card skill family works as one system instead of five
isolated skills.

The family contains:

- `obsidian-learning-card-router`
- `obsidian-concept-card-capture`
- `obsidian-mechanism-card-capture`
- `obsidian-method-card-capture`
- `obsidian-misconception-card-capture`

## System Shape

The family uses a two-layer design:

1. the router decides intent and card type
2. one execution skill performs the actual create, update, or promotion work

The router should not write cards.

The execution skills should not re-open broad four-way type routing unless the
current classification is clearly wrong.

## Two Routing Axes

Every thread should be classified on two axes.

### Axis 1: action mode

- `create`
- `update`
- `promotion review`

### Axis 2: card type

- `concept`
- `mechanism`
- `method`
- `misconception`

The router should hand off both.

Example:

- `Method + promotion review`

## Responsibilities

### Router

The router is responsible for:

- preserving the one-card boundary
- selecting the dominant card type
- selecting the correct action mode
- avoiding premature multi-card expansion
- handing off to exactly one downstream skill

The router is not responsible for:

- writing card body content
- promotion evidence details
- backlink construction
- graph rendering

### Execution Skills

Each execution skill is responsible for:

- one card type only
- deterministic rendering when practical
- duplicate detection
- safe update flow
- progression evidence in the body
- conservative graph links
- promotion assessment

## Shared Progression Model

All four execution skills share the same progression ladder:

- `seed`
- `growing`
- `stable`
- `expert-ready`

And the same graph-maturity ladder:

- `none`
- `weak`
- `local`
- `dispatchable`

Shared rule:

- `stable` means reliable local-node value
- `expert-ready` means reusable routing or dispatch value

Not every card needs to become `expert-ready`.

## Card-Type Boundaries

### Concept

Use when the thread mainly answers:

- what it is
- what the term means
- what its boundary is

### Mechanism

Use when the thread mainly answers:

- why it happens
- how the causal chain works
- which variables explain the result

### Method

Use when the thread mainly answers:

- how to do it
- what procedure to follow
- how to choose between approaches

### Misconception

Use when the thread mainly answers:

- what the mistaken claim is
- why it looks plausible
- why it is wrong
- how to correct it

## Existing Card Rule

When an existing card is explicitly in scope:

- preserve its current card type by default
- route to `update` or `promotion review`
- do not create a new sibling card unless the user clearly asks for one

## Stable Versus Expert-Ready

The family uses the same structural split across card types.

### Stable

Expected evidence:

- reliable local graph placement
- at least three strong node-level relationships
- enough content depth to act as a dependable local node

### Expert-Ready

Expected evidence:

- reusable routing or dispatch rules
- at least one cross-card-type route
- condition-triggered switching or fallback logic

`expert-ready` should be treated as a candidate review, not as the default
destination.

## Recommended Operating Sequence

For ambiguous threads:

1. route by dominant question
2. decide whether the task is create, update, or promotion review
3. hand off to exactly one execution skill
4. let that skill perform duplicate checks and rendering

For existing cards:

1. preserve the current card type
2. decide whether this is update or promotion review
3. let the execution skill merge or assess maturity

## Anti-Patterns

Avoid these:

- routing to multiple execution skills at once
- creating all four card types by default
- treating `stable` and `expert-ready` as cosmetic status labels
- promoting to `expert-ready` without real dispatch value
- using weak backlinks as fake graph maturity

## Maintenance Rule

When one execution skill changes its progression structure:

- check whether the other three execution skills should match
- check whether the router still routes correctly by mode and type
- update shared references before adding local exceptions
