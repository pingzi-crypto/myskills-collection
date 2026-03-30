# Learning Card Live Card Dry-Run Report

## Scope

Validation target:

- branch `codex/learning-card-spec-validation`
- real existing Obsidian learning cards
- dry-run only

Date:

- `2026-03-30`

Method:

- read real cards from the Obsidian vault
- do not modify vault files
- evaluate expected router result, expected mode, and expected target path

## Cards Reviewed

- `C:\Users\pz\Documents\Obsidian Vault\学习\Cards\Methods\Prompt Narrowing.md`
- `C:\Users\pz\Documents\Obsidian Vault\学习\Cards\Concepts\Deterministic Card Rendering.md`
- `C:\Users\pz\Documents\Obsidian Vault\学习\Cards\Methods\Learning Card Routing.md`

## Dry-Run Cases

### Case 1

Card:

- `Prompt Narrowing`

Observed current state:

- `type: method`
- `status: stable`
- `graph_maturity: local`

Expected live trigger:

- user wants to refine fallback behavior or strengthen dispatch rules

Expected route:

- `$obsidian-method-card-capture`

Expected mode:

- `update` when adding method detail
- `promotion review` when explicitly reassessing `stable` vs `expert-ready`

Expected same-title target path:

- `C:\Users\pz\Documents\Obsidian Vault\学习\Cards\Methods\Prompt Narrowing.md`

Dry-run assessment:

- pass

Reason:

- existing card is explicit and correctly typed
- same-title path is stable
- local update notes and shared same-title flow both support preserving this path

### Case 2

Card:

- `Deterministic Card Rendering`

Observed current state:

- `type: concept`
- `status: stable`
- `graph_maturity: local`

Expected live trigger:

- user wants to add stronger arbitration rules between definition work and downstream method or mechanism work

Expected route:

- `$obsidian-concept-card-capture`

Expected mode:

- `update` for concept refinement
- `promotion review` if the explicit question is whether the card deserves `expert-ready`

Expected same-title target path:

- `C:\Users\pz\Documents\Obsidian Vault\学习\Cards\Concepts\Deterministic Card Rendering.md`

Dry-run assessment:

- pass

Reason:

- router should preserve the existing card type because the card is already in scope
- current card body still matches concept semantics rather than method semantics

### Case 3

Card:

- `Learning Card Routing`

Observed current state:

- `type: method`
- `status: expert-ready`
- `graph_maturity: dispatchable`

Expected live trigger:

- user wants to test or extend routing rules against more complex mixed-thread cases

Expected route:

- `$obsidian-method-card-capture`

Expected mode:

- `promotion review` if the focus is maturity and dispatch sufficiency
- `update` if the focus is adding more representative routing examples

Expected same-title target path:

- `C:\Users\pz\Documents\Obsidian Vault\学习\Cards\Methods\Learning Card Routing.md`

Dry-run assessment:

- pass

Reason:

- the note is already a strongly typed Method card
- it has explicit dispatch structure, so the existing-card override should dominate over speculative rerouting

## Outcome

Dry-run result:

- existing-card targeting looks stable on real vault notes
- same-title update routing points at the expected on-disk file paths
- current router and update-flow rules remain coherent when applied to real cards

## Remaining Gap

This report still does not replace one true live write-path validation.

Still recommended:

- run one real Codex session that explicitly targets an existing card
- let the system choose `update` or `promotion review`
- confirm the final write stays on the same note path without duplicate creation
