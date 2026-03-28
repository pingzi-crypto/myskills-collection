# Learning Card Shared Core Blueprint

## Goal

Define a safe refactor path for evolving the learning-card family from:

- `router + 4 execution skills`

into:

- `router + shared core + 4 thin execution skills`

This blueprint is intentionally not a plan for collapsing the family into one
single execution skill.

## Recommendation

Do not replace the current family with a true `4-in-1` monolithic skill.

Use this target shape instead:

1. keep the router as the only broad classification entry
2. keep four card-type-specific execution skills as explicit boundaries
3. extract repeated infrastructure into one shared core

The design goal is:

- one system at the user level
- four semantic card types at the knowledge level
- one reusable implementation core at the maintenance level

## Why Not A Single 4-in-1 Skill

The current family has three different kinds of complexity:

- routing complexity
- rendering complexity
- progression and graph-evidence complexity

If all three are merged into one public skill, the likely failure mode is not
functional breakage. The likely failure mode is semantic drift:

- card-type boundaries become less explicit
- progression standards get flattened
- debugging gets slower because classification and rendering failures mix
- local exceptions accumulate inside one oversized prompt and one oversized flow

For this family, fewer entrypoints are less important than preserving:

- stable type judgment
- credible progression standards
- clear graph and dispatch meaning

## Target Architecture

### Layer 1: Router

Keep:

- `obsidian-learning-card-router`

Responsibilities:

- choose the source fragment
- preserve the one-card boundary
- classify the dominant card type
- classify the action mode
- hand off to exactly one execution skill

The router should still not write cards.

### Layer 2: Shared Core

Create a shared core used by all four execution skills.

Suggested directory:

```text
skills/shared/learning-card-core/
  references/
  scripts/
  templates/
```

The shared core should own infrastructure, not semantic type decisions.

### Layer 3: Thin Execution Skills

Keep these public execution entries:

- `obsidian-concept-card-capture`
- `obsidian-mechanism-card-capture`
- `obsidian-method-card-capture`
- `obsidian-misconception-card-capture`

Each skill should become thinner over time and mostly define:

- what this card type means
- what minimum evidence this type requires
- what type-specific routing and dispatch structure looks like
- how this type maps into the shared renderer and update flow

## What To Extract Into Shared Core

The following parts are good shared-core candidates because they are procedural
or infrastructural rather than semantic:

- vault path resolution
- duplicate detection workflow
- safe update flow
- anchored source-fragment resolution
- text-block selection logic
- bilingual rendering protocol
- common frontmatter normalization
- status and graph-maturity enums
- deterministic render helpers
- shared validation for renderer input
- promotion review skeleton
- common sample-spec schema

Good end state:

- one shared script entry for shared validation and rendering primitives
- one shared reference for common progression protocol
- one shared reference for graph-maturity semantics

## What Must Stay Type-Specific

Do not over-unify these parts.

They are the main reason the family should not become a single monolith:

- dominant-question rubric for each card type
- minimum meaningful evidence per type
- section priorities per type
- relation semantics per type
- routing and dispatch rules per type
- stable threshold per type
- expert-ready threshold per type
- examples of good and bad captures per type

Example:

- a Method card and a Mechanism card can both mention decision rules
- but a Method card uses them as operational procedure
- while a Mechanism card uses them as explanatory structure

If these differences are flattened into one schema, card quality drops even
when rendering still "works".

## Public Interface Rule

The public interface should continue to look like a family, not like one giant
tool.

That means:

- ambiguous thread -> use router
- known type -> call the matching execution skill directly

Do not force every direct capture through a single generic card-creation skill.

The user-level simplification should come from:

- better docs
- better prompt patterns
- more reusable internals

not from removing type boundaries.

## Migration Sequence

Use this order to keep the family stable while refactoring.

### Phase 1: Freeze Semantics

Before extracting shared pieces:

- document the current type boundaries
- document current stable and expert-ready standards
- document current routing and dispatch expectations

This prevents accidental semantic flattening during refactor.

### Phase 2: Extract Shared References

Move repeated family-wide rules into shared references first:

- bilingual rule
- update rule
- vault path rule
- render input shape
- graph-maturity ladder

At this phase, behavior should not change.

### Phase 3: Extract Shared Scripts

After the references are stable:

- introduce shared helper scripts
- keep per-type scripts as thin wrappers if needed
- verify rendered output parity on sample specs

This is the highest-value technical extraction step.

### Phase 4: Thin The Execution Skills

Once shared scripts exist:

- reduce repeated instruction blocks inside each execution skill
- keep only type-specific semantics and type-specific examples
- point repeated workflow steps back to the shared core

### Phase 5: Reassess Router Surface

Only after the family is stable again should you consider:

- whether the router prompt should become more concise
- whether a higher-level "learning-card system" wrapper is useful

This wrapper, if added, should still dispatch internally to the router or one
execution skill. It should not replace the family architecture.

## Validation Checklist

Before merging any shared-core refactor, verify all of the following:

- direct concept capture still works without opening the other three type specs
- direct mechanism capture still preserves causal wording
- direct method capture still preserves procedural wording
- direct misconception capture still preserves error-correction structure
- router still selects exactly one downstream skill
- stable cards still render lean by default
- expert-ready review still requires real dispatch value
- bilingual rendering still defaults to `zh + en`
- vault-root overrides still work
- existing cards still route to update or promotion review instead of silent recreate

## Worktree Guidance

Shared-core refactors should use a worktree.

Reason:

- they touch multiple skills
- they affect both shared references and execution behavior
- they have a meaningful regression surface

Suggested naming:

- `codex/learning-card-core-refactor`
- `codex/router-anchor-refactor`
- `codex/method-progression-tuning`

Rule of thumb:

- single-skill wording cleanup -> worktree optional
- one card-type renderer change -> worktree recommended
- shared-core extraction or router contract change -> worktree required

## Expected Benefits

If done with the boundary above, the likely upside is:

- lower maintenance cost
- easier multi-platform consistency
- clearer room for future card types
- easier testing with shared sample specs
- better ability to add scoring, review, and promotion heuristics later

## Worst Failure Mode

The worst outcome is not a runtime error.

The worst outcome is a false simplification:

- one big shared flow
- many hidden exceptions
- weaker type judgment
- flatter progression standards
- cards that look consistent but encode less useful knowledge

That failure mode should be treated as architectural regression even if the
skill still produces output.

## Practical Decision

Use this blueprint as the default decision rule:

- do not build a true public `4-in-1` execution skill now
- do extract a shared core
- do preserve the router and four type-specific execution surfaces

This gives the family the best balance between:

- usability
- maintainability
- semantic precision
- long-term extension potential
