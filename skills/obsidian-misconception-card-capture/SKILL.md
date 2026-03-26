---
name: obsidian-misconception-card-capture
description: Capture, update, or promote one Obsidian Misconception Card from the current thread. Use when the user wants to turn a mistaken claim, a misleading intuition, or a recurring error pattern into one misconception-focused learning card, or when an existing Misconception Card should gain stronger progression evidence, local graph structure, or correction-routing rules under the resolved vault root at 学习/Cards/Misconceptions.
---

# Obsidian Misconception Card Capture

## Overview

Create, update, or promote exactly one Misconception Card from the current thread.
This skill is intentionally narrow: it does not create concept, mechanism, or
method cards, and it does not create multiple misconceptions in one pass.

Read these before creating or updating any card:

- [../references/learning-card-skill-family.md](../references/learning-card-skill-family.md)
- [references/misconception-card-spec.md](references/misconception-card-spec.md)
- [references/progression-rules.md](references/progression-rules.md)
- [../references/progression-protocol.md](../references/progression-protocol.md)
- [../references/knowledge-graph-relations.md](../references/knowledge-graph-relations.md)
- [references/vault-path-resolution.md](references/vault-path-resolution.md)
- [references/render-script.md](references/render-script.md)

## Workflow Decision

Use this skill only when all of the following are true:

- the user wants to record learning from the current thread
- the output should be an Obsidian card
- the scope is one misconception, not a bundle of misconceptions
- the thread mainly explains a mistaken claim, why it looks plausible, why it is wrong, and how to correct it
- the output should stay within one Misconception Card boundary

Do not use this skill when:

- the user wants multiple cards in one pass
- the content is mainly defining a concept
- the content is mainly explaining a causal mechanism
- the content is mainly teaching a method rather than correcting an error

## Create Flow

1. Resolve `VAULT_ROOT` using [references/vault-path-resolution.md](references/vault-path-resolution.md).
2. Ask for the single misconception title if it is not already explicit.
3. Ask which keywords, Q&A fragments, or thread points should be captured.
4. Ask for `domain` when it is missing. Ask for `subdomain` and `source` only if useful.
5. Check whether a card with the same title already exists under `<VAULT_ROOT>/学习/Cards/Misconceptions`.
6. If the card already exists, switch to the update flow in [references/update-flow.md](references/update-flow.md).
7. If the card does not exist, create one new Misconception Card with `status: seed` and `graph_maturity: none`.
8. Fill the card from the current thread, preferring concise synthesis over long transcript dumps.
9. Add early progression evidence and graph structure only when the thread clearly supports it.
10. When practical, render the final markdown with `scripts/render_misconception_card.py` for deterministic structure.
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

- mature an existing Misconception Card
- decide whether a Misconception Card should move beyond `stable`
- add stronger knowledge-graph structure or correction-routing rules

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

- Create only one misconception card per run.
- Keep the title aligned to one misconception, not a mixed error catalog.
- Set `status` to `seed` on first creation.
- Set `graph_maturity` to `none` on first creation unless stronger evidence already exists.
- Default `confidence` to `1` unless the user clearly requests a different value.
- Preserve the structure expected by the Misconception Card format.
- Write source-derived content as concise notes, not raw copied conversation logs.
- Use Obsidian wikilinks only for strong, existing matches.
- If graph-link confidence is low, keep the relationship section conservative.
- Do not confuse more links with better progression. `stable` is mainly node-level; `expert-ready` requires rule-level correction and return-path rules.

## Card Construction Rules

- Save the card to `<VAULT_ROOT>/学习/Cards/Misconceptions/<Misconception Title>.md`.
- Use the misconception title as the note title and file name after sanitizing invalid path characters.
- Include thread-derived material in the body where it improves understanding.
- Keep the card focused on the mistaken claim, why it seems reasonable, why it is wrong, the correct understanding, trigger signals, counterexamples, and corrective action.
- Use the shared graph structure: `Local Position`, `Operational Links`, and `Routing and Dispatch`.
- Use `Promotion Assessment` to explain promotion choices instead of silently changing maturity.
- Prefer `scripts/render_misconception_card.py` to generate the final card layout for new cards.

## Backlink Policy

Only add links when one of these is true:

- the user explicitly names a related existing card
- an existing card title is an exact misconception match
- an existing card title is an obvious alias match with high confidence

When unsure:

- leave `related: []`
- keep the related-card area sparse
- avoid inventing dispatch rules

## Output Expectations

When executing this skill, produce:

1. A short note to the user stating the misconception being captured.
2. The created or updated file path.
3. A brief summary of what error pattern or mistaken claim was extracted from the thread.
4. The progression result when promotion was considered:
   - promoted
   - watchlist
   - stay stable
5. Any unresolved ambiguity that should be clarified later.
