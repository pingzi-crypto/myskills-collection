# Learning Card Operator Bridge Acceptance Report

## Goal

Provide one operator-facing acceptance line for the shortest daily bridge path:

- canonical router handoff text
- thin PowerShell wrapper
- downstream execution prompt skeleton

This line is narrower than full live card writing. It validates the bridge that
an operator actually uses before invoking the execution skill.

## Acceptance Target

Primary wrapper:

- `skills/shared/learning-card-core/scripts/use_handoff_bridge.ps1`

Underlying bridge:

- `skills/shared/learning-card-core/scripts/build_execution_prompt_from_handoff.py`

## Acceptance Checks

- wrapper `-HandoffFile -PrintOnly` output matches the parser output for:
  - `create`
  - `update`
  - `promotion review`
- default clipboard-in and clipboard-out wrapper flow reproduces the canonical
  concept-create execution prompt

## Rebuild Command

```powershell
python analysis/learning-card-operator-bridge-acceptance/scripts/verify_operator_bridge_acceptance.py
```

## Output Artifacts

- `analysis/learning-card-operator-bridge-acceptance/outputs/concept-create-wrapper-printonly.txt`
- `analysis/learning-card-operator-bridge-acceptance/outputs/method-update-wrapper-printonly.txt`
- `analysis/learning-card-operator-bridge-acceptance/outputs/misconception-review-wrapper-printonly.txt`
- `analysis/learning-card-operator-bridge-acceptance/outputs/concept-create-wrapper-clipboard.txt`
- `analysis/learning-card-operator-bridge-acceptance/outputs/manifest.json`

## Observed Result

- the thin PowerShell wrapper reproduces the same execution prompt skeleton as
  the canonical parser for all three common mode shapes
- the default clipboard-to-clipboard operator path is now acceptance-backed
- this gives the repository a stable daily-use bridge between router output and
  execution-skill invocation without requiring operators to hand-build prompt
  parameters
