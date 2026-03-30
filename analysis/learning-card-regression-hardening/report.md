# Learning Card Regression Hardening Report

## Scope

Validation target:

- branch `codex/learning-card-regression-hardening`
- shared renderer behavior for missing optional progression fields
- focus: seed-stage cards that still show `Progression Layer`

Date:

- `2026-03-30`

## Why This Exists

This regression line closes a gap revealed by live validation:

- one real seed-card write exposed that missing optional progression fields could
  still leave an empty placeholder block in the rendered markdown
- that issue was fixed in the shared render path
- this report adds an automated boundary check so the same class of bug is less
  likely to reappear silently

## Automated Check Shape

Script:

- `analysis/learning-card-regression-hardening/scripts/verify_optional_progression_rendering.py`

Cases covered:

- Concept seed render with `current_status_notes` present but `next_goal` and
  `current_upgrade_tasks` omitted
- Mechanism seed render with the same omission pattern
- Method seed render with the same omission pattern
- Misconception seed render with the same omission pattern

Assertions:

- `Progression Layer` still renders when there is real progression content
- required status and graph-maturity lines stay visible
- missing optional progression fields do not emit empty placeholder lines

## Output Artifacts

- `analysis/learning-card-regression-hardening/outputs/concept-seed-no-optional-progression.md`
- `analysis/learning-card-regression-hardening/outputs/mechanism-seed-no-optional-progression.md`
- `analysis/learning-card-regression-hardening/outputs/method-seed-no-optional-progression.md`
- `analysis/learning-card-regression-hardening/outputs/misconception-seed-no-optional-progression.md`
- `analysis/learning-card-regression-hardening/outputs/manifest.json`

## Status

- pass

## Observed Result

- all four renderers produced seed-stage outputs with `Progression Layer`
  visible
- required stage lines remained present
- no output contained the old empty optional placeholder lines
- the generated artifacts now preserve this boundary as a repeatable regression
  check instead of a one-off live observation

## Output Artifact Hashes

- `concept-seed-no-optional-progression.md`
  - `54D1EA9FD4C908370BAF1543695D65E35E81728BBC213D5DE19D33DBEF8E440A`
- `mechanism-seed-no-optional-progression.md`
  - `DB0D99CDCA16F6C62FBD181ACD326753E12E178681AA4CEA7547D249A78EA74D`
- `method-seed-no-optional-progression.md`
  - `79BF566808240717B00CCD14C480F557383F6F3942D07C8200E4713048A8A245`
- `misconception-seed-no-optional-progression.md`
  - `B685FBA7ABEBC0CF892DAA8608B378E3A386C90A6B867176F7C83946DF5C2E60`
