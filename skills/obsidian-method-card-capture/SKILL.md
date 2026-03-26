---
name: obsidian-method-card-capture
description: Capture one method from the current thread and create a single Obsidian Method Card in seed state. Use when the user wants to turn a practical way of doing something, a procedure, or an actionable strategy into one method-focused learning card, save it under the resolved vault root at 学习/Cards/Methods, preserve source cues from the thread, and add conservative backlinks to existing cards.
---

# Obsidian Method Card Capture

## Overview

Create exactly one Method Card from the current thread. This skill is intentionally narrow: it does not create concept, mechanism, or misconception cards, and it does not create multiple methods in one pass.

Read [references/method-card-spec.md](references/method-card-spec.md), [references/vault-path-resolution.md](references/vault-path-resolution.md), and [references/render-script.md](references/render-script.md) before creating or updating any card.

## Workflow Decision

Use this skill only when all of the following are true:

- the user wants to record learning from the current thread
- the output should be an Obsidian card
- the scope is one method, not a bundle of methods
- the thread mainly explains how to do something, when to apply it, or how it compares with alternatives
- the card should start at `seed`

Do not use this skill when:

- the user wants multiple cards in one pass
- the content is mainly defining a concept
- the content is mainly explaining a causal mechanism
- the content is mainly a misconception or correction pattern

## Capture Workflow

1. Resolve `VAULT_ROOT` using the rules in [references/vault-path-resolution.md](references/vault-path-resolution.md).
2. Ask for the single method title if it is not already explicit.
3. Ask which keywords, Q&A fragments, or thread points should be captured.
4. Ask for `domain` when it is missing. Ask for `subdomain` and `source` only if useful.
5. Check whether a card with the same title already exists under `<VAULT_ROOT>/学习/Cards/Methods`.
6. If the card already exists, switch to the update flow in [references/update-flow.md](references/update-flow.md) instead of silently overwriting or creating a duplicate.
7. If the card does not exist, create one new Method Card with `status: seed`.
8. Fill the card from the current thread, preferring concise synthesis over long transcript dumps.
9. When practical, render the final markdown with `scripts/render_method_card.py` for deterministic structure.
10. Add conservative backlinks only when the match is strong.

## Update Flow

When a same-title card already exists:

1. Tell the user that the card already exists and show the existing path.
2. Ask whether they want to update the existing card instead of creating a new one.
3. If the user declines, stop without changing the file.
4. If the user agrees, read the existing card before editing.
5. Merge only the new thread-derived information that improves the card.
6. Preserve the original card type, title, id, and existing structure.
7. Update `updated` to the current date.
8. Keep `status` unchanged unless the user explicitly asks to promote it.
9. Do not reset `confidence`, `related`, `aliases`, or upgrade history unless the new evidence clearly justifies it.

Use [references/update-flow.md](references/update-flow.md) for the detailed merge rules.

## Writing Rules

- Create only one method card per run.
- Keep the title aligned to one method, not a mixed toolkit.
- Set `status` to `seed` on first creation.
- Default `confidence` to `1` unless the user clearly requests a different value.
- Preserve the structure expected by the Method Card format.
- Write source-derived content as concise notes, not raw copied conversation logs.
- Use Obsidian wikilinks only for strong, existing matches.
- If backlink confidence is low, leave `related: []` and keep the relationship section conservative.

## Card Construction Rules

- Save the card to `<VAULT_ROOT>/学习/Cards/Methods/<Method Title>.md`.
- Use the method title as the note title and file name after sanitizing invalid path characters.
- Include thread-derived material in the body where it improves understanding.
- Keep the card focused on the problem the method solves, the core idea, structure, design choices, hidden assumptions, fit and non-fit scenarios, comparisons, misuses, failure modes, examples, and decision criteria.
- Prefer `scripts/render_method_card.py` to generate the final card layout for new cards.

## Backlink Policy

Only add links when one of these is true:

- the user explicitly names a related existing card
- an existing card title is an exact method match
- an existing card title is an obvious alias match with high confidence

When unsure:

- leave `related: []`
- keep the "related cards" section sparse

## Output Expectations

When executing this skill, produce:

1. A short note to the user stating the method being captured.
2. The created or updated file path.
3. A brief summary of what practical procedure or strategy was extracted from the thread.
4. Any unresolved ambiguity that should be clarified later.

## References

- Read [references/method-card-spec.md](references/method-card-spec.md) for target paths, field defaults, and duplicate-handling rules.
- Read [references/render-script.md](references/render-script.md) for how to use the deterministic method card renderer.
- Read [references/update-flow.md](references/update-flow.md) for how to handle same-title cards without creating duplicates.
- Read [references/vault-path-resolution.md](references/vault-path-resolution.md) for how to resolve the vault root before reading templates or writing cards.
