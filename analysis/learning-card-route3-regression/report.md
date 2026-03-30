# Learning Card Route 3 Regression Report

## Scope

Regression target:

- commit `ae35c1b`
- branch `codex/learning-card-core-refactor`
- focus: shared-core protocol extraction and shared renderer helper extraction

Date:

- `2026-03-29`

## Automated Checks

### Renderer Sample Execution

Status:

- pass

Executed wrappers:

- `skills/obsidian-concept-card-capture/scripts/render_concept_card.py`
- `skills/obsidian-mechanism-card-capture/scripts/render_mechanism_card.py`
- `skills/obsidian-method-card-capture/scripts/render_method_card.py`
- `skills/obsidian-misconception-card-capture/scripts/render_misconception_card.py`

Output artifacts:

- `analysis/learning-card-route3-regression/outputs/concept-sample.md`
- `analysis/learning-card-route3-regression/outputs/mechanism-sample.md`
- `analysis/learning-card-route3-regression/outputs/method-sample.md`
- `analysis/learning-card-route3-regression/outputs/misconception-sample.md`

Observed result:

- all four wrappers resolved the shared helper at `skills/shared/learning-card-core/scripts/render_common.py`
- all four sample specs rendered successfully
- no runtime import failures occurred after the shared-core extraction

### Python Syntax Validation

Status:

- pass

Command class:

- `python -m py_compile` over the shared helper and the four renderer wrappers

Observed result:

- no syntax errors

### Shared Spec Validation Failure Path

Status:

- pass

Check shape:

- run one renderer with an intentionally invalid spec
- verify the shared-core validator rejects the input before rendering
- verify the CLI returns a concise validation error instead of a Python traceback

Observed result:

- invalid `status` values are rejected by the shared validator
- wrapper scripts now exit with a stable `Spec validation failed: ...` message
- the invalid spec does not fall through into partial rendering

## Output Artifact Hashes

- `concept-sample.md`
  - `7BF0D03EAF51CA2D342CA1232D623FF60A4EEA50F58C2D761926E96D442F252A`
- `mechanism-sample.md`
  - `A0642436F6F160AC6497B46D2A6BEFAD1DE106ED8419211A2AB092B27DA4202A`
- `method-sample.md`
  - `BF3566D60B0A5EF2BD70837011BCC071D20BC16E3F844322977948857A30B5D5`
- `misconception-sample.md`
  - `5526B680FA20E2EFAA6F65FAC20C4A2BEF200532234CE94FA8442133EA0220A6`

## Structural Assessment

### Verified

- shared procedural references are in place under `skills/shared/learning-card-core/references/`
- shared script helper is in place under `skills/shared/learning-card-core/scripts/render_common.py`
- shared spec validation now runs before deterministic rendering
- renderer wrappers are thinner and keep card-type-specific section schemas
- deterministic rendering still works after moving common logic into the shared core

### Not Fully Automated Yet

- router handoff behavior in a live conversation
- update-flow behavior against real existing Obsidian cards
- vault-root override behavior against multiple vault paths in one manual session

Those checks were not broken by this commit surface, but they still require
session-level manual verification rather than script-only verification.

## Checkpoint Decision

Route 3 checkpoint status:

- shared references extracted -> complete
- shared script helpers introduced -> complete
- execution skills thinned against shared script helpers -> complete for renderer wrappers
- automated regression pass -> complete
- live session router/update validation -> still recommended before merge to `main`

## Recommendation

This Route 3 line is now stable enough for either of these next steps:

1. push the branch and preserve it as the architecture refactor baseline
2. run one live end-to-end manual capture through the router before merging
