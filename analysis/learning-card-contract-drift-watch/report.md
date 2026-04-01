# Learning Card Contract Drift Watch Report

## Goal

Provide one cross-layer watch line for the current learning-card contracts so
future changes can detect incompatible drift earlier.

This line does not replace the existing layer-specific regressions. Its job is
to connect them and confirm that the same mode, downstream skill, and completion
proof still line up across the stack.

## Watch Lines

Daily operator triad:

- router minimum package
- operator packet
- execution result

Bridge-originated live triad:

- preflight check
- live acceptance harness

Covered mode shapes:

- `create`
- `update`
- `promotion review`

## Rebuild Command

```powershell
python analysis/learning-card-contract-drift-watch/scripts/verify_contract_drift_watch.py
```

## Output Artifacts

- `analysis/learning-card-contract-drift-watch/outputs/daily-operator-create-watch.json`
- `analysis/learning-card-contract-drift-watch/outputs/daily-operator-update-watch.json`
- `analysis/learning-card-contract-drift-watch/outputs/daily-operator-review-watch.json`
- `analysis/learning-card-contract-drift-watch/outputs/bridge-live-update-watch.json`
- `analysis/learning-card-contract-drift-watch/outputs/bridge-live-review-watch.json`
- `analysis/learning-card-contract-drift-watch/outputs/bridge-live-create-watch.json`
- `analysis/learning-card-contract-drift-watch/outputs/manifest.json`

## Observed Result

- the repository now has one watch layer that detects whether:
  - router and operator packet still agree on mode and downstream skill
  - operator packet completion markers still match execution-result proof lines
  - bridge preflight checks still agree with bridge-originated live evidence
    chains
- this gives the project one smaller place to rerun when router, bridge, or
  execution contracts materially shift
