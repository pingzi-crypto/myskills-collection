# Learning Card Route 3 Execution Checklist

## Goal

Provide one concrete execution checklist for Route 3 work on the learning-card
family.

This checklist is for structural changes such as:

- shared-core extraction
- router contract changes
- family-wide render protocol changes
- family-wide update-flow changes
- progression-protocol refactors

Current branch policy:

- use a dedicated Route 3 worktree branch based on `main`
- name it after the actual structural surface, for example
  `codex/router-contract-refactor`

## Before Editing

1. Confirm the change is really Route 3.
2. Define the exact architectural target in one sentence.
3. List which files are expected to change before editing.
4. Decide what must remain type-specific.
5. Define the minimum regression checklist.

## Current Route 3 Target

The current Route 3 target is:

- preserve and extend the current `router + shared core + 4 thin execution
  skills` architecture without collapsing card-type boundaries

The next structural step should be:

- read the active `.codex` continuity files first, then define the next
  structural checkpoint explicitly before editing

## Scope Boundary

Allowed in this Route 3 line:

- shared references
- shared script helpers
- renderer input protocol
- router-to-execution contract clarification
- family documentation needed to support those changes

Not allowed unless explicitly re-scoped:

- redesigning card-type boundaries
- merging the four card types into one monolithic execution skill
- adding unrelated product features
- mixing broad feature work into the same branch without a new checkpoint

## Type-Specific Boundary

These must remain local to each execution skill unless there is a deliberate,
reviewed reason to unify them:

- dominant question
- section-key semantics
- progression thresholds
- routing and dispatch meaning
- evidence standards

## Minimum Validation

Before merging Route 3 work, verify:

1. concept capture still preserves concept semantics
2. mechanism capture still preserves causal semantics
3. method capture still preserves procedural semantics
4. misconception capture still preserves correction semantics
5. router still hands off to exactly one execution skill
6. update flow still prevents duplicate creation
7. stable cards remain lean by default
8. expert-ready still requires real dispatch value
9. bilingual default still behaves as expected
10. vault-root overrides still behave as expected
11. missing optional progression fields do not emit empty placeholder blocks
12. stage-aware routing visibility still hides and reveals the correct sub-blocks
13. router handoff text explicitly marks routing-only status and the next execution step
14. router handoff text explicitly marks the minimum confirmed execution package and any still-missing write inputs

## Checkpoint Rule

Route 3 work should be split into checkpoints.

Recommended checkpoints:

1. shared references extracted
2. shared script helpers introduced
3. execution skills thinned against shared script helpers
4. regression pass completed

Do not let Route 3 remain one long uncheckpointed branch.

## Current Status

Checkpoint status at the moment:

1. shared references extracted
2. shared script helpers introduced -> completed
3. execution skills thinned against shared script helpers -> completed for renderer wrappers
4. regression pass completed -> automated renderer checks completed; manual router/update walkthrough completed; one live real-card update-path write and one live promotion-review write have been completed

Additional note:

- real-card dry-run against existing vault notes has been completed without write-path execution
- controlled handoff-style validation against an explicit existing card has been completed with a real write
- one router-led ambiguous-thread create-path validation has been completed with a real write to cover non-explicit card targeting
- router handoff parsing and operator-facing bridge tooling have been added on
  top of the shared core

Continuity read order before new Route 3 work:

1. `.codex/handoff.md`
2. `.codex/decisions.md`
3. `.codex/todo.md`
4. this checklist
