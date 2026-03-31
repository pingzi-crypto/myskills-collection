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
- `skills/shared/learning-card-core/scripts/use_handoff_bridge.ps1`

Regression script:

- `analysis/learning-card-handoff-parser/scripts/verify_handoff_parser.py`

It reuses:

- `skills/shared/learning-card-core/scripts/build_execution_prompt.py`

## Covered Behavior

- reads `Capture anchor`, `Route result`, `Mode`, and `Still needed before write`
- infers card type and action mode
- preserves the capture anchor when present
- emits a downstream execution prompt skeleton with placeholders for any still-
  missing write inputs
- accepts router handoff text from file, inline text, stdin, or clipboard
- can copy the generated execution prompt back to the clipboard for operator use
- includes a thin PowerShell wrapper for the default clipboard-to-clipboard
  operator path

## Output Artifacts

- `analysis/learning-card-handoff-parser/inputs/concept-create-handoff.txt`
- `analysis/learning-card-handoff-parser/inputs/method-update-handoff.txt`
- `analysis/learning-card-handoff-parser/inputs/misconception-review-handoff.txt`
- `analysis/learning-card-handoff-parser/outputs/concept-create-prompt.txt`
- `analysis/learning-card-handoff-parser/outputs/method-update-prompt.txt`
- `analysis/learning-card-handoff-parser/outputs/misconception-review-prompt.txt`
- `analysis/learning-card-handoff-parser/outputs/manifest.json`

Rebuild command:

```powershell
python analysis/learning-card-handoff-parser/scripts/verify_handoff_parser.py
```

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
- the parser line is now regression-backed, so future router handoff changes can
  be checked against stable execution-prompt outputs
- file input and stdin input now produce identical prompt output for the same
  canonical handoff text

## Output Artifact Hashes

- `concept-create-prompt.txt`
  - `8791CAE5C5D1ADC57349F72E5CEDE070FFDE5DDBBFEE688B96B9D6724CBFFE69`
- `method-update-prompt.txt`
  - `B7D6B14BF75C0DF2840207B148E602947C924895355ADBB9BC31040639A52D25`
- `misconception-review-prompt.txt`
  - `FA9B01F01031FB16D862324BD9B5523705F1FF7087545CBAF3D14BE6AC07DECC`
