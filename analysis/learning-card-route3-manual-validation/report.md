# Learning Card Route 3 Manual Validation Report

## Scope

Validation target:

- branch `codex/learning-card-core-refactor`
- router classification rules
- routing mode selection rules
- same-title update protection rules

Date:

- `2026-03-29`

Method:

- manual rule walkthrough
- no real Obsidian vault files were modified
- no real user card was updated during this validation

## Sources Reviewed

- `skills/obsidian-learning-card-router/SKILL.md`
- `skills/obsidian-learning-card-router/references/decision-rubric.md`
- `skills/obsidian-learning-card-router/references/routing-modes.md`
- `skills/shared/learning-card-core/references/same-title-update-flow.md`
- local card-type update notes for concept and method cards

## Manual Scenario Results

### Scenario 1

Input shape:

- user selects one current-session fragment
- user answers the type question with exact label `方法`
- no existing card is in scope

Expected:

- route directly to `$obsidian-method-card-capture`
- mode should default to `create`

Observed:

- pass

Reason:

- router explicitly maps exact label replies and skips reopening the broader
  classification question
- default mode for current-session capture without an existing card is `create`

### Scenario 2

Input shape:

- anchored content mainly explains why something works
- content emphasizes variables and causal chain
- no existing card is in scope

Expected:

- route to `$obsidian-mechanism-card-capture`
- mode should be `create`

Observed:

- pass

Reason:

- decision rubric maps "why it happens / how it works / causal chain" to
  `Mechanism`

### Scenario 3

Input shape:

- existing Method card is explicitly in scope
- user wants to add more detail rather than review maturity

Expected:

- preserve `Method` type
- route to `update`
- do not create a sibling card

Observed:

- pass

Reason:

- existing-card override says preserve current type by default
- routing-modes says existing named card plus refinement intent should use
  `update`

### Scenario 4

Input shape:

- existing stable card is explicitly in scope
- user asks whether it should become `expert-ready`

Expected:

- preserve current card type
- route to `promotion review`

Observed:

- pass

Reason:

- routing-modes explicitly maps maturity-stage and dispatch-review questions to
  `promotion review`

### Scenario 5

Input shape:

- anchored content is about a mistaken claim
- content explains why it looks plausible, why it is wrong, and how to correct it

Expected:

- route to `$obsidian-misconception-card-capture`

Observed:

- pass

Reason:

- decision rubric maps that pattern directly to `Misconception`

### Scenario 6

Input shape:

- same-title card already exists in the target card directory
- user has not yet confirmed an update

Expected:

- system must not silently create a duplicate
- system must ask whether to update the existing card
- if the user declines, stop without modifying files

Observed:

- pass

Reason:

- shared same-title update flow makes user confirmation mandatory before editing
- duplicate creation is explicitly disallowed in that state

## Manual Validation Outcome

Validated at rule level:

- exact-label routing path
- dominant-question routing path
- existing-card type preservation
- update vs promotion-review separation
- same-title duplicate protection

Not validated in this report:

- live conversation behavior inside the Codex UI
- real Obsidian vault update against an existing note on disk
- multi-vault override handling through one live thread

## Assessment

The Route 3 refactor did not weaken the declared router or update-flow contract
at the instruction level.

Current state:

- automated renderer regression -> complete
- manual router/update rule walkthrough -> complete
- live end-to-end session against a real card -> still recommended before merge
