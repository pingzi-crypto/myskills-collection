# Learning Card Worktree Guide

## Goal

Provide one practical rule set for deciding when the learning-card family
should use a Git worktree.

This guide uses three development routes:

1. Maintenance Route
2. Feature Route
3. Architecture Route

Use the route classification first. Then decide whether worktree is optional,
recommended, or required.

## Core Decision Rule

For the learning-card family, the question is not:

- "Can this be changed in the current working tree?"

The real question is:

- "How large is the regression surface if this change goes wrong?"

If the change touches:

- multiple skills
- router contracts
- shared references
- shared scripts
- progression semantics
- rendering protocol

then treat it as a worktree candidate by default.

## Route 1: Maintenance Route

Use this route for small, local, low-risk work.

Typical changes:

- wording cleanup in one skill
- typo fixes
- one-card-type examples or prompt polishing
- README alignment
- local documentation fixes
- narrow non-behavioral note updates

Worktree rule:

- optional

Recommended branch style:

- `codex/method-doc-cleanup`
- `codex/concept-copy-tune`

Main risk:

- low

Best use case:

- fast cleanup when the change does not alter routing, rendering, or maturity
  behavior

Do not keep the change in Route 1 if it starts to affect:

- duplicate handling
- vault path resolution
- render structure
- shared family semantics

At that point, promote it to Route 2 or Route 3.

## Route 2: Feature Route

Use this route for one bounded capability change that still preserves the
current family architecture.

Typical changes:

- router adds a new capture convenience
- one execution skill gains a new evidence section
- bilingual output behavior changes
- one renderer gains a new local capability
- one card type gets improved promotion review logic
- one skill gets stronger duplicate or anchor handling

Worktree rule:

- recommended

Recommended branch style:

- `codex/router-text-block-upgrade`
- `codex/method-promotion-tuning`
- `codex/misconception-correction-signals`

Main risk:

- medium

Best use case:

- the change is real behavior, but the blast radius is still mostly bounded to
  one skill or one narrow feature area

Validation minimum:

- check the targeted skill directly
- check the router if the feature changes routing assumptions
- verify one representative sample output

If the feature begins to require changes across:

- all four execution skills
- shared references
- router plus renderer contracts

then move it to Route 3.

## Route 3: Architecture Route

Use this route for system-shape changes.

Typical changes:

- extracting or redesigning shared core
- changing router handoff contracts
- changing family-wide progression protocol
- changing family-wide render protocol
- changing family-wide update-flow protocol
- moving repeated logic from local skills into shared infrastructure
- changing how multiple platforms consume the same family rules

Worktree rule:

- required

Recommended branch style:

- `codex/learning-card-core-refactor`
- `codex/router-contract-refactor`
- `codex/progression-protocol-rewrite`

Main risk:

- high

Best use case:

- the change can improve long-term maintainability or expansion potential, but
  failure would create cross-skill regressions

Required validation:

- direct capture still works for all four card types
- router still routes to exactly one execution skill
- update flow still avoids duplicate creation
- stable render stays lean
- expert-ready still requires real dispatch value
- bilingual default still behaves correctly
- vault-root override still works

Architecture work must not be done as an incidental side effect of a small fix.

If the change is Route 3, isolate it deliberately.

## Route Comparison

### Route 1

- scope: one local cleanup
- worktree: optional
- speed: fastest
- safety: high
- long-term value: low to medium

### Route 2

- scope: one bounded capability
- worktree: recommended
- speed: medium
- safety: medium
- long-term value: medium to high

### Route 3

- scope: family-wide structural change
- worktree: required
- speed: slowest
- safety: lowest without isolation
- long-term value: highest if executed well

## Practical Workflow

Use this sequence before starting a learning-card change:

1. classify the change into Route 1, Route 2, or Route 3
2. decide whether worktree is optional, recommended, or required
3. name the branch based on the actual change surface
4. define the validation checklist before editing
5. keep the scope inside the chosen route

If the scope expands during implementation:

- stop
- reclassify the route
- move to a worktree if the new route requires it

## Anti-Patterns

Avoid these behaviors:

- doing Route 3 work directly in the main working tree
- calling a change "small" after it starts touching shared references
- mixing feature work and architecture extraction in one unbounded branch
- changing router, renderer, and progression semantics at the same time without
  a validation plan
- letting one card-type exception silently become a family-wide rule

## Default Recommendation For This Repository

Use this as the default operating policy:

- Route 1 can stay in the main working tree
- Route 2 should usually use a worktree when the change is more than a one-file
  edit
- Route 3 should always use a worktree

For the current learning-card family, most future work will likely fall into
one of these buckets:

- prompt and doc polish -> Route 1
- router or single card-type capability upgrades -> Route 2
- shared-core extraction, protocol changes, or family contract changes ->
  Route 3

## Current Recommendation

Based on the current repository state:

- the shared-reference extraction already moved this family closer to Route 3
  work
- the next step of shared script extraction is also Route 3
- future small content or spec tuning can return to Route 1 or Route 2

This means the repository should not permanently live inside worktrees.

The correct rule is:

- use worktrees for structural evolution
- do not force worktrees for every small edit
