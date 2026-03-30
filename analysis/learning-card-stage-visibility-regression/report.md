# Learning Card Stage Visibility Regression Report

## Scope

Validation target:

- branch `codex/study-card-family`
- shared stage-aware visibility rules for `Routing and Dispatch`
- focus: `stable` vs `expert-ready` rendering boundaries

Date:

- `2026-03-30`

## Why This Exists

The shared render protocol now depends on stage-aware visibility rules:

- `stable` should remain lean and expose only `Direct Routes`
- `expert-ready` should expose the full routing frame, including placeholder
  sub-blocks when some routing evidence is still missing

This regression line turns that contract into a repeatable automated check
instead of leaving it as a documentation-only promise.

## Automated Check Shape

Script:

- `analysis/learning-card-stage-visibility-regression/scripts/verify_stage_aware_routing_rendering.py`

Cases covered:

- Concept `stable`
- Concept `expert-ready`
- Mechanism `stable`
- Mechanism `expert-ready`
- Method `stable`
- Method `expert-ready`
- Misconception `stable`
- Misconception `expert-ready`

Assertions:

- `stable` outputs expose `Routing and Dispatch > Direct Routes`
- `stable` outputs suppress `Secondary Routes`, `Gap Signals`, and `Stop Rules`
  even when those blocks exist in the input spec
- `expert-ready` outputs expose all four routing sub-block headings
- `expert-ready` outputs render placeholder gap lines when optional routing
  sub-blocks are omitted

## Output Artifacts

- `analysis/learning-card-stage-visibility-regression/outputs/manifest.json`
- `analysis/learning-card-stage-visibility-regression/outputs/*.md`

## Status

- pass

## Observed Result

- all eight cases rendered successfully
- `stable` outputs exposed only `Direct Routes` inside `Routing and Dispatch`
  even when the input spec contained all four routing blocks
- `expert-ready` outputs exposed all four routing sub-block headings
- `expert-ready` outputs rendered placeholder gap lines when `secondary_routes`,
  `gap_signals`, or `stop_rules` were omitted from the input spec
- the current shared renderer behavior matches the declared stage-aware protocol

## Output Artifact Hashes

- `concept-stable-routing-visibility.md`
  - `C4E42E75C5F44B359B73D9F8A33494B9E7DB06142245119F9489A95FF301D099`
- `concept-expert-routing-visibility.md`
  - `7E1D62B5C66F75B9AADF34D47D5F2C3A57DF01C3A7EFC70483EC5A75B353579B`
- `mechanism-stable-routing-visibility.md`
  - `1FE2B2B838D5E67F1CF80BB8646C5AFE20E2D8EA42088E2EE3D2E1107C51128D`
- `mechanism-expert-routing-visibility.md`
  - `4E20BB0963C7606E310163A4F525D5880B76875445C28C4133C81B639D3DBF57`
- `method-stable-routing-visibility.md`
  - `97DA433427938EB31685683C3188F3EB4EBC8E3BD80A41FDF82430F3A2A6A042`
- `method-expert-routing-visibility.md`
  - `CF4904DB1460BD124A760A2323FB2744CA011284948E993556127C3589A2D7BF`
- `misconception-stable-routing-visibility.md`
  - `B1FEEE0F9FEB7A8927A7F8FD3410BA34035DD633AAE8A36F542B782F40EF48CA`
- `misconception-expert-routing-visibility.md`
  - `BBEA2DCA869341DCDEBF2E002F7FBA3FDA10747429DC0ABE37C0221CC2EB2315`
