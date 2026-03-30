# Deterministic Render Protocol

## Purpose

Provide the shared rendering rules used across the learning-card family.

Execution skills may still use different renderer scripts and different
section-key sets, but they should follow the same structural protocol.

## Core Rule

The agent still decides the semantic content.

The renderer is responsible for deterministic markdown layout when practical.

Do not treat the renderer as the source of truth for card-type semantics or
promotion decisions.

## Shared Input Expectations

All renderer inputs should support these family-wide ideas:

- required identity fields such as `title`
- basic classification fields such as `domain`
- optional metadata such as `status`, `graph_maturity`, `confidence`,
  `created`, `updated`, `id`, `tags`, `related`, `aliases`, and `review_cycle`
- a `sections` object carrying card-type-specific body content

Section names remain card-type-specific.

Before rendering, shared-core validators should verify:

- required top-level identity fields are present
- family-wide enums such as `status` and `graph_maturity` are valid
- list-like metadata fields keep stable shapes
- structured sections such as graph links, routing, and promotion blocks keep
  object form where required
- unknown section keys are rejected at the wrapper level instead of being
  silently ignored

## Bilingual Content Rule

When content is synthesized from the thread, default to bilingual items shaped
like:

```json
{ "zh": "...", "en": "..." }
```

When bilingual content is available, prefer:

- Chinese as the main bullet text
- an indented `EN:` translation line immediately below it

## Routing And Dispatch Rule

When a renderer supports `routing_and_dispatch`, prefer a structured object
containing:

- `direct_routes`
- `secondary_routes`
- `gap_signals`
- `stop_rules`

Read `../../../references/routing-and-dispatch-spec.md` for the shared
sub-structure.

## Stage-Aware Rendering

Use stage-aware rendering:

- `seed` and `growing` should render only populated core sections
- `seed` and `growing` should hide empty graph or progression scaffolding
- `stable` should expose graph structure and a lean progression summary
- `stable` should default to `Routing and Dispatch > Direct Routes` only
- `expert-ready` should expose the full `Routing and Dispatch` layer and
  promotion assessment gaps
- `expert-ready` should expose missing sub-blocks inside `Routing and Dispatch`

For early-stage renders, do not keep empty placeholder headings in the body.

If a `seed` or `growing` card has no meaningful progression content yet, omit
the progression layer entirely.

## Lean Stable Render

For default `stable` cards, prefer a slimmer render:

- keep the card-type explanation layer
- keep `Knowledge Graph Relations > Local Position`
- keep `Knowledge Graph Relations > Operational Links`
- keep only `Routing and Dispatch > Direct Routes`
- collapse progression notes into one compact `Upgrade Focus` block

Do not keep these as always-on default sections for `stable` renders:

- `Growing Checklist`
- `Stable Checklist`
- `Expert-Ready Checklist`
- `Upgrade History`
- expanded multi-block promotion scaffolding

## Update Safety

For updates, use the renderer only when it helps preserve deterministic layout
without clobbering existing content.

Do not use deterministic rendering as an excuse to rewrite stable human-edited
content that the current thread did not materially improve.
