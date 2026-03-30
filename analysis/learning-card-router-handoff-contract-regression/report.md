# Learning Card Router Handoff Contract Regression Report

## Scope

Validation target:

- branch `codex/router-handoff-contract-regression`
- prompt-level handoff contract for `obsidian-learning-card-router`
- focus: prevent router output from sounding like a card file already exists

Date:

- `2026-03-30`

## Why This Exists

One real usage case showed a prompt-contract failure:

- the router returned a clean classification result
- but the user could still easily infer that card creation had already happened
- the actual downstream execution skill had not run yet, so no card file existed

This regression line turns that boundary into a repeatable contract check.

## Automated Check Shape

Script:

- `analysis/learning-card-router-handoff-contract-regression/scripts/verify_router_handoff_contract.py`

Checks:

- required handoff-boundary phrases exist in the router skill contract
- supporting docs repeat the same execution boundary
- canonical create, update, and promotion-review handoff examples all include:
  - routing-only status
  - explicit next step
  - suggested user reply
- canonical handoff examples do not claim that a file has already been created
  or updated

## Output Artifacts

- `analysis/learning-card-router-handoff-contract-regression/outputs/concept-create-handoff.txt`
- `analysis/learning-card-router-handoff-contract-regression/outputs/method-update-handoff.txt`
- `analysis/learning-card-router-handoff-contract-regression/outputs/misconception-promotion-review-handoff.txt`
- `analysis/learning-card-router-handoff-contract-regression/outputs/manifest.json`

## Status

- pass

## Observed Result

- the router contract files all contain the new execution-boundary wording
- the canonical create, update, and promotion-review handoff samples all
  include:
  - routing-only status
  - explicit next-step execution instruction
  - suggested user reply
- none of the canonical handoff samples falsely claim that a card file already
  exists

## Output Artifact Hashes

- `concept-create-handoff.txt`
  - `41E9E3628E6E559E4CC1FCF193E2DB9AD9F9F807AD5EC0CF71C93BE8F2E3AFAA`
- `method-update-handoff.txt`
  - `D46C90C80D5A53F8BD4EC91ED0E2D49C1CC7559D3B35592D8192603F5824BBC6`
- `misconception-promotion-review-handoff.txt`
  - `75A9C0D10A8E01B20C1BDDDF48A72C6667C384F80DF2A11F8E883D8FC0787A80`
