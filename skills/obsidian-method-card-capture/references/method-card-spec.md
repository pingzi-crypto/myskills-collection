# Method Card Spec

## Scope

This skill supports only one output type:

- Method Card

It does not create:

- Concept Card
- Mechanism Card
- Misconception Card
- multiple cards in one run

## Vault Root

All paths in this spec are relative to `VAULT_ROOT`.

Read [vault-path-resolution.md](vault-path-resolution.md) first to resolve that root.

## Source Template

The source method template is stored at:

- `<VAULT_ROOT>/模板/学习卡片模板/card/Method Card.md`

The template's folder constant has already been aligned to:

- `学习/Cards/Methods`

## Target Output Path

Create new cards here:

- `<VAULT_ROOT>/学习/Cards/Methods`

Final file path shape:

- `<VAULT_ROOT>/学习/Cards/Methods/<Method Title>.md`

## Required Fields

Each new card should include these frontmatter fields:

- `id`
- `title`
- `type: method`
- `domain`
- `subdomain`
- `status: seed`
- `graph_maturity: none`
- `created`
- `updated`
- `source`
- `tags`
- `related`
- `confidence`
- `review_cycle`
- `aliases`

## Default Values For New Cards

- `type: method`
- `status: seed`
- `graph_maturity: none`
- `confidence: 1`
- `review_cycle: 30d`
- `tags: [method]`
- `related: []`
- `aliases: []`

## Minimum Input Collection

Before creating a card, collect or infer:

- method title
- capture keywords or thread excerpts
- domain

Optional when useful:

- subdomain
- source

## Duplicate Policy

Before creating a new card, check:

- whether a file with the same title already exists in `<VAULT_ROOT>/学习/Cards/Methods`

If a same-title card exists:

- do not silently overwrite it
- do not create a duplicate file
- switch to [update-flow.md](update-flow.md)

## Backlink Policy

Search for existing cards only inside:

- `<VAULT_ROOT>/学习/Cards`

Add backlinks only when the match is strong:

- exact title match
- obvious alias match
- explicit user instruction

If uncertain:

- keep `related: []`
- do not invent graph links

## Body Construction Guidance

The body should stay faithful to the Method Card structure and should emphasize:

- the problem the method solves
- the core idea
- method structure
- key design choices
- hidden assumptions
- fit scenarios
- non-fit scenarios
- alternative method comparison
- common misuses
- failure modes
- decision criteria
- representative examples
- a validation question
- knowledge graph relations
- routing and dispatch
- promotion assessment
- upgrade checkpoints from `seed` onward

Default language rule for new cards:

- body content should default to bilingual `中文 + English translation`
- when the renderer spec is structured, prefer section items like:
  - `{ "zh": "中文内容", "en": "English translation" }`
- if only one language is confidently available, keep the content useful first and fill the second language later

For the default visible `stable` render:

- keep the method explanation layer visible
- keep `Local Position`
- keep `Operational Links`
- keep only `Routing and Dispatch > Direct Routes`
- compress progression and promotion notes into one short summary block

Treat these as optional, review-only, or removable from the default `stable` body:

- `validation_question`
- `Growing Checklist`
- `Stable Checklist`
- `Expert-Ready Checklist`
- `Upgrade History`
- expanded multi-block promotion sections

## Knowledge Graph Structure

Each Method Card should reserve these graph sections:

- `Local Position`
- `Operational Links`
- `Routing and Dispatch`

Use the shared relationship grammar from `../references/knowledge-graph-relations.md`.

Progression expectations:

- `seed`: graph sections may stay hidden or minimal
- `growing`: early node-level graph hints may appear
- `stable`: `Local Position` and `Operational Links` should contain real evidence
- `expert-ready`: `Routing and Dispatch` should contain strong rule-level statements

## Promotion Assessment

Method Cards should include a lightweight promotion assessment section with:

- current recommendation
- main reasons
- missing evidence
- next rules worth adding

Use one of these recommendation labels:

- `worth promoting`
- `watchlist`
- `stay stable`

## Thread Capture Guidance

Do not try to modify past thread UI state. Instead:

- if the router already selected a capture anchor, treat the anchored assistant reply as the primary source body
- extract the user-confirmed keywords
- summarize relevant Q&A points
- fold them into the method card sections where they belong

Keep the result concise and method-centered.
