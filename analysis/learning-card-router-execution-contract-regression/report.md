# Learning Card Router Execution Contract Regression Report

## Scope

Validation target:

- branch `codex/router-execution-contract-regression`
- router-to-execution minimum handoff package
- focus: make missing write-critical inputs explicit instead of implied

Date:

- `2026-03-30`

## Why This Exists

Clarifying "routing only" solves only half of the handoff problem.

The second half is whether the router makes it clear which inputs are already
known and which still need to be collected before the execution skill can
actually write or review a card.

This regression line turns that minimum handoff package into a static contract.

## Automated Check Shape

Script:

- `analysis/learning-card-router-execution-contract-regression/scripts/verify_router_execution_contract.py`

Checks:

- the router skill defines the minimum execution package
- the routing-modes reference defines mode-specific missing-input behavior
- the family doc states that missing write inputs must be marked explicitly
- the README tells users that router output should include both confirmed and
  still-missing inputs
- canonical create, update, and promotion-review handoffs all include:
  - routing-only status
  - confirmed execution package
  - still-needed write inputs
  - next-step execution instruction

## Output Artifacts

- `analysis/learning-card-router-execution-contract-regression/outputs/concept-create-minimum-package.txt`
- `analysis/learning-card-router-execution-contract-regression/outputs/method-update-minimum-package.txt`
- `analysis/learning-card-router-execution-contract-regression/outputs/misconception-review-minimum-package.txt`
- `analysis/learning-card-router-execution-contract-regression/outputs/manifest.json`

## Status

- pass

## Observed Result

- the router skill now defines the minimum execution package explicitly
- the routing-modes reference now states which missing inputs should be called
  out for `create`, `update`, and `promotion review`
- the family doc now treats missing write inputs as part of the handoff
  contract rather than an implicit downstream detail
- all canonical handoff samples include:
  - routing-only status
  - confirmed execution package
  - still-needed write inputs
  - next-step instruction

## Output Artifact Hashes

- `concept-create-minimum-package.txt`
  - `1C44053FC191EEEA330F18BD106D679FB601DAC540F5E84CCBB9E4269D046B11`
- `method-update-minimum-package.txt`
  - `F28FF94216D7BF7FC48C40BAC04143292CEF139E09377CBAD7EE18F756F226B1`
- `misconception-review-minimum-package.txt`
  - `63D7A7BA1E1687CED7B27ADCE5D725DD4C80154CAAC9BC6C06F3F642400EEC06`
