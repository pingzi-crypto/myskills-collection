# Learning Card Handoff Parser Report

## Goal

Provide one small shared bridge utility that reads router handoff text and
directly produces a downstream execution prompt skeleton.

This removes one more manual step between:

- router classification output
- execution-skill prompt construction

## Added Utility

Script:

- `skills/shared/learning-card-core/scripts/build_execution_prompt_from_handoff.py`

It reuses:

- `skills/shared/learning-card-core/scripts/build_execution_prompt.py`

## Covered Behavior

- reads `Capture anchor`, `Route result`, `Mode`, and `Still needed before write`
- infers card type and action mode
- preserves the capture anchor when present
- emits a downstream execution prompt skeleton with placeholders for any still-
  missing write inputs

## Output Artifacts

- `analysis/learning-card-handoff-parser/inputs/concept-create-handoff.txt`
- `analysis/learning-card-handoff-parser/inputs/method-update-handoff.txt`
- `analysis/learning-card-handoff-parser/inputs/misconception-review-handoff.txt`
- `analysis/learning-card-handoff-parser/outputs/concept-create-prompt.txt`
- `analysis/learning-card-handoff-parser/outputs/method-update-prompt.txt`
- `analysis/learning-card-handoff-parser/outputs/misconception-review-prompt.txt`
- `analysis/learning-card-handoff-parser/outputs/manifest.json`

## Observed Result

- the new parser can read canonical router handoff text and recover:
  - card type
  - action mode
  - capture anchor
  - still-missing write inputs
- the generated execution prompt skeleton matches the correct downstream prompt
  shape for `create`, `update`, and `promotion review`
- this reduces one more manual step between router output and execution-skill
  invocation

## Output Artifact Hashes

- `concept-create-prompt.txt`
  - `77C1ED52941B27214DDF543ECEC91B011BDC47B33C88EC54DBE89300B2C1EA68`
- `method-update-prompt.txt`
  - `3E7B5B8B5B5254640A0D1731E896692DBFCA5A92C683C2B030B0B876E7E9F673`
- `misconception-review-prompt.txt`
  - `B71A8CE9265A7FA2605D4F19D8FD5496452D24F9E583A3371661CC8E23C3CC6C`
