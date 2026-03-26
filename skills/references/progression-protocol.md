# Progression Protocol

## Goal

Define how learning cards progress from `seed` to `expert-ready` by adding
real content and graph capability, not by only changing `status`.

## Shared Principles

- Progression must show up in the card body.
- `stable` means the card is a reliable node in the local knowledge graph.
- `expert-ready` means the card can participate in graph dispatch.
- `expert-ready` is not the default end state for every card.
- `expert-ready` is about reliable dispatch, not just richer content.

## Two Growth Axes

### Content maturity

- `seed`: the card answers its primary question at a minimal useful level
- `growing`: the card adds boundaries, comparisons, and non-fit awareness
- `stable`: the card supports reliable use in varied local situations
- `expert-ready`: the card supports transfer, teaching, and difficult edge cases

### Graph maturity

- `none`: no reliable graph structure yet
- `weak`: early relationship hints exist
- `local`: the card can be placed reliably in a local graph
- `dispatchable`: the card includes reusable routing rules

Recommended mapping:

- `seed` -> `none`
- `growing` -> `weak`
- `stable` -> `local`
- `expert-ready` -> `dispatchable`

## Relationship Granularity

### Node-level relationships

Node-level relationships answer:

- which nodes connect to this card
- what type of connection exists
- why the connection is strong enough to keep

These relationships support `stable`.

### Rule-level relationships

Rule-level relationships answer:

- when to switch to another node
- what order to use multiple nodes in
- what to do when two nodes compete
- where to fall back when the current path fails
- when the graph is missing a needed node
- when to stop searching the current path

These relationships support `expert-ready`.

## Stable Gate

Use `stable` only when the card already behaves like a reliable local node.

Hard gates:

- the card boundary is stable
- the local graph position is stable

Minimum expectations:

- at least three strong node-level relationships
- at least two different relationship types
- at least one structural relationship
- at least one functional relationship
- a clear explanation of the card's local graph position
- enough boundary clarity that the card would not easily change type

## Stable Standard

A card is ready for `stable` only when it can function as a reliable local node.

Minimum expectations:

- at least three strong node-level relationships
- at least two different relationship types
- at least one structural relationship
- at least one functional relationship
- a clear explanation of the card's local graph position

## Expert-Ready Candidate Screen

Before promotion review, first ask whether the card is worth promoting.

Hard gates:

- the card is already a high-quality `stable`
- the local graph position is no longer drifting
- real usage has shown a need for routing or dispatch
- the card is not too narrow, too fragile, or too one-off

Dispatch value signals:

- high-frequency entry point
- strong branching or routing value
- conflict or choice arbitration value
- transferable dispatch logic across similar topics
- learning, teaching, or debugging route value

Use `expert-ready` review only when at least three of those signals are present.

## Stable To Expert-Ready Promotion Gate

Required:

- at least two strong rule-level statements
- at least one cross-card-type dispatch rule
- at least one explicit condition-triggered route
- stable local graph positioning already exists
- at least one explicit gap-detection rule
- at least one explicit stop rule

Choose at least two:

- ordered multi-node sequence
- conflict arbitration rule
- failure fallback rule
- route-planning rule
- teaching or transfer rule

## Routing And Dispatch Structure

Use the shared four-part routing layer from
`routing-and-dispatch-spec.md`:

- `Direct Routes`
- `Secondary Routes`
- `Gap Signals`
- `Stop Rules`

Guidance by stage:

- `seed`: this layer may stay hidden
- `growing`: `Direct Routes` may begin to appear
- `stable`: `Direct Routes` should start carrying real value; the other
  sections may stay early or sparse
- `expert-ready`: all four sections should contain substantive rules or expose
  explicit gaps

## Expert-Ready Review Standard

Before promotion, first confirm that the card is already a high-quality
`stable`.

Core review targets:

- `Direct Routes`: at least two strong direct rules
- `Secondary Routes`: at least one bounded multi-hop path
- `Gap Signals`: at least one explicit missing-node trigger
- `Stop Rules`: at least one explicit termination rule

These are stronger than simple "related cards" lists. The card should show
that it can route, not just connect.

## Promotion Outcomes

### Worth promoting

Use when the card is worth promoting and has enough rule-level evidence.

### Watchlist

Use when the card shows dispatch potential but still lacks enough rule-level evidence.

### Stay stable

Use when the card is a strong local node but should not become a dispatch hub.
