---
name: obsidian-concept-card-capture
description: Capture, update, or promote one Obsidian Concept Card from the current thread. Use when the user wants to turn Q&A or discussion into one concept-focused learning card, or when an existing Concept Card should gain stronger progression evidence, local graph structure, or concept-routing rules under the resolved vault root at 学习/Cards/Concepts.
---

# Obsidian Concept Card Capture

## Overview

Create, update, or promote exactly one Concept Card from the current thread.
This skill is intentionally narrow: it does not create mechanism, method, or
misconception cards, and it does not create multiple concepts in one pass.

Read these before creating or updating any card:

- [../references/learning-card-skill-family.md](../references/learning-card-skill-family.md)
- [references/concept-card-spec.md](references/concept-card-spec.md)
- [references/progression-rules.md](references/progression-rules.md)
- [../references/progression-protocol.md](../references/progression-protocol.md)
- [../references/knowledge-graph-relations.md](../references/knowledge-graph-relations.md)
- [references/vault-path-resolution.md](references/vault-path-resolution.md)
- [references/render-script.md](references/render-script.md)

## Workflow Decision

Use this skill only when all of the following are true:

- the user wants to record learning from the current thread
- the output should be an Obsidian card
- the scope is one concept, not a bundle of concepts
- the output should stay within one Concept Card boundary

Do not use this skill when:

- the user wants multiple cards in one pass
- the content is better modeled as a mechanism, method, or misconception
- the user wants a large rewrite that really belongs in another card type

## Create Flow

1. Resolve `VAULT_ROOT` using [references/vault-path-resolution.md](references/vault-path-resolution.md).
2. Ask for the single concept title if it is not already explicit.
3. Ask which keywords, Q&A fragments, or thread points should be captured.
4. Ask for `domain` when it is missing. Ask for `subdomain` and `source` only if useful.
5. Check whether a card with the same title already exists under `<VAULT_ROOT>/学习/Cards/Concepts`.
6. If the card already exists, switch to the update flow in [references/update-flow.md](references/update-flow.md).
7. If the card does not exist, create one new Concept Card with `status: seed` and `graph_maturity: none`.
8. Fill the card from the current thread, preferring concise synthesis over long transcript dumps.
9. Add early progression evidence and graph structure only when the thread clearly supports it.
10. When practical, render the final markdown with `scripts/render_concept_card.py` for deterministic structure.
11. Add conservative backlinks only when the match is strong.

## Update Flow

When a same-title card already exists and the user wants to keep working on it:

1. Tell the user that the card already exists and show the existing path.
2. Ask whether they want to update the existing card instead of creating a new one.
3. If the user declines, stop without changing the file.
4. If the user agrees, read the existing card before editing.
5. Merge only the new thread-derived information that materially improves the card.
6. Preserve the original card type, title, id, and overall structure.
7. Update `updated` to the current date.
8. Keep `status` unchanged unless the user explicitly asks to promote it or the task is clearly a progression review.
9. Do not reset `confidence`, `related`, `aliases`, or upgrade history unless the new evidence clearly justifies it.

Use [references/update-flow.md](references/update-flow.md) for the detailed merge rules.

## Promotion Flow

Use the promotion flow when the user wants to:

- mature an existing Concept Card
- decide whether a Concept Card should move beyond `stable`
- add stronger knowledge-graph structure or routing rules

Promotion steps:

1. Read the existing card.
2. Identify the current `status` and `graph_maturity`.
3. Use [references/progression-rules.md](references/progression-rules.md) and [../references/progression-protocol.md](../references/progression-protocol.md) to decide whether the card is a candidate for promotion.
4. Check whether the new thread adds node-level evidence, rule-level evidence, or both.
5. Prefer three outcomes over forced promotion:
   - promote
   - keep current status and mark as watchlist
   - keep current status and recommend staying stable
6. Write the decision into `Promotion Assessment`.
7. Update `graph_maturity` when the graph evidence changes.
8. Append a short note to `upgrade_history` when the status or graph maturity changes.

## Writing Rules

- Create only one concept card per run.
- Keep the title aligned to one concept, not a compound phrase.
- Set `status` to `seed` on first creation.
- Set `graph_maturity` to `none` on first creation unless stronger evidence already exists.
- Default `confidence` to `1` unless the user clearly requests a different value.
- Preserve the structure expected by the Concept Card format.
- Write source-derived content as concise notes, not raw copied conversation logs.
- Use Obsidian wikilinks only for strong, existing matches.
- If graph-link confidence is low, keep the relationship section conservative.
- Do not confuse more links with better progression. `stable` is mainly node-level; `expert-ready` requires rule-level dispatch.

## Card Construction Rules

- Save the card to `<VAULT_ROOT>/学习/Cards/Concepts/<Concept Title>.md`.
- Use the concept title as the note title and file name after sanitizing invalid path characters.
- Include thread-derived material in the body where it improves understanding.
- Keep the card focused on concept definition, boundaries, importance, examples, confusion handling, and upgrade path.
- Use the shared graph structure: `Local Position`, `Operational Links`, and `Routing and Dispatch`.
- Use `Promotion Assessment` to explain promotion choices instead of silently changing maturity.
- Prefer `scripts/render_concept_card.py` to generate the final card layout for new cards.

## Backlink Policy

Only add links when one of these is true:

- the user explicitly names a related existing card
- an existing card title is an exact concept match
- an existing card title is an obvious alias match with high confidence

When unsure:

- leave `related: []`
- keep the related-card area sparse
- avoid inventing dispatch rules

## Output Expectations

When executing this skill, produce:

1. A short note to the user stating the concept being captured.
2. The created or updated file path.
3. A brief summary of what was extracted from the thread.
4. The progression result when promotion was considered:
   - promoted
   - watchlist
   - stay stable
5. Any unresolved ambiguity that should be clarified later.
