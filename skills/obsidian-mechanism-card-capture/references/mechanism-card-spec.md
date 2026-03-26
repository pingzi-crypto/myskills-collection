# Mechanism Card Spec

## Scope

This skill supports only one output type:

- Mechanism Card

It does not create:

- Concept Card
- Method Card
- Misconception Card
- multiple cards in one run

## Vault Root

All paths in this spec are relative to `VAULT_ROOT`.

Read [vault-path-resolution.md](vault-path-resolution.md) first to resolve that root.

## Source Template

The source mechanism template is stored at:

- `<VAULT_ROOT>/模板/学习卡片模板/card/Mechanism Card.md`

The template's folder constant has already been aligned to:

- `学习/Cards/Mechanisms`

## Target Output Path

Create new cards here:

- `<VAULT_ROOT>/学习/Cards/Mechanisms`

Final file path shape:

- `<VAULT_ROOT>/学习/Cards/Mechanisms/<Mechanism Title>.md`

## Required Fields

Each new card should include these frontmatter fields:

- `id`
- `title`
- `type: mechanism`
- `domain`
- `subdomain`
- `status: seed`
- `created`
- `updated`
- `source`
- `tags`
- `related`
- `confidence`
- `review_cycle`
- `aliases`

## Default Values For New Cards

- `type: mechanism`
- `status: seed`
- `confidence: 1`
- `review_cycle: 30d`
- `tags: [mechanism]`
- `related: []`
- `aliases: []`

## Minimum Input Collection

Before creating a card, collect or infer:

- mechanism title
- capture keywords or thread excerpts
- domain

Optional when useful:

- subdomain
- source

## Duplicate Policy

Before creating a new card, check:

- whether a file with the same title already exists in `<VAULT_ROOT>/学习/Cards/Mechanisms`

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

The body should stay faithful to the Mechanism Card structure and should emphasize:

- the phenomenon being explained
- the core variables
- the causal chain
- key prerequisites
- the weakest step
- alternative explanations
- scope
- failure boundaries
- supporting evidence
- anomalies or counter cases
- compressed explanation
- related cards
- a validation question
- upgrade checkpoints from `seed` onward

## Thread Capture Guidance

Do not try to modify past thread UI state. Instead:

- extract the user-confirmed keywords
- summarize relevant Q&A points
- fold them into the mechanism card sections where they belong

Keep the result concise and mechanism-centered.
