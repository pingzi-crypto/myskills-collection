---
name: obsidian-misconception-card-capture
description: Capture one misconception from the current thread and create a single Obsidian Misconception Card in seed state. Use when the user wants to turn a mistaken claim, a misleading intuition, or a recurring error pattern into one misconception-focused learning card, save it under the resolved vault root at 学习/Cards/Misconceptions, preserve source cues from the thread, and add conservative backlinks to existing cards.
---

# Obsidian Misconception Card Capture

## Overview

Create exactly one Misconception Card from the current thread. This skill is intentionally narrow: it does not create concept, mechanism, or method cards, and it does not create multiple misconceptions in one pass.

Read [references/misconception-card-spec.md](references/misconception-card-spec.md), [references/vault-path-resolution.md](references/vault-path-resolution.md), and [references/render-script.md](references/render-script.md) before creating or updating any card.

## Workflow Decision

Use this skill only when all of the following are true:

- the user wants to record learning from the current thread
- the output should be an Obsidian card
- the scope is one misconception, not a bundle of misconceptions
- the thread mainly explains a mistaken claim, why it looks plausible, why it is wrong, and how to correct it
- the card should start at `seed`

Do not use this skill when:

- the user wants multiple cards in one pass
- the content is mainly defining a concept
- the content is mainly explaining a causal mechanism
- the content is mainly teaching a method rather than correcting an error

## Capture Workflow

1. Resolve `VAULT_ROOT` using the rules in [references/vault-path-resolution.md](references/vault-path-resolution.md).
2. Ask for the single misconception title if it is not already explicit.
3. Ask which keywords, Q&A fragments, or thread points should be captured.
4. Ask for `domain` when it is missing. Ask for `subdomain` and `source` only if useful.
5. Check whether a card with the same title already exists under `<VAULT_ROOT>/学习/Cards/Misconceptions`.
6. If the card already exists, switch to the update flow in [references/update-flow.md](references/update-flow.md) instead of silently overwriting or creating a duplicate.
7. If the card does not exist, create one new Misconception Card with `status: seed`.
8. Fill the card from the current thread, preferring concise synthesis over long transcript dumps.
9. When practical, render the final markdown with `scripts/render_misconception_card.py` for deterministic structure.
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

- Create only one misconception card per run.
- Keep the title aligned to one misconception, not a mixed error catalog.
- Set `status` to `seed` on first creation.
- Default `confidence` to `1` unless the user clearly requests a different value.
- Preserve the structure expected by the Misconception Card format.
- Write source-derived content as concise notes, not raw copied conversation logs.
- Use Obsidian wikilinks only for strong, existing matches.
- If backlink confidence is low, leave `related: []` and keep the relationship section conservative.

## Card Construction Rules

- Save the card to `<VAULT_ROOT>/学习/Cards/Misconceptions/<Misconception Title>.md`.
- Use the misconception title as the note title and file name after sanitizing invalid path characters.
- Include thread-derived material in the body where it improves understanding.
- Keep the card focused on the mistaken claim, why it seems reasonable, why it is wrong, the correct understanding, what it confuses, representative counterexamples, trigger signals, and corrective action.
- Prefer `scripts/render_misconception_card.py` to generate the final card layout for new cards.

## Backlink Policy

Only add links when one of these is true:

- the user explicitly names a related existing card
- an existing card title is an exact misconception match
- an existing card title is an obvious alias match with high confidence

When unsure:

- leave `related: []`
- keep the "related cards" section sparse

## Output Expectations

When executing this skill, produce:

1. A short note to the user stating the misconception being captured.
2. The created or updated file path.
3. A brief summary of what error pattern or mistaken claim was extracted from the thread.
4. Any unresolved ambiguity that should be clarified later.

## References

- Read [references/misconception-card-spec.md](references/misconception-card-spec.md) for target paths, field defaults, and duplicate-handling rules.
- Read [references/render-script.md](references/render-script.md) for how to use the deterministic misconception card renderer.
- Read [references/update-flow.md](references/update-flow.md) for how to handle same-title cards without creating duplicates.
- Read [references/vault-path-resolution.md](references/vault-path-resolution.md) for how to resolve the vault root before reading templates or writing cards.
