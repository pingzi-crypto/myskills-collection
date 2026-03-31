# Learning Card Live Acceptance Harness Report

## Goal

Provide one reusable harness for the current real-write validation line without
performing a new write.

This harness reads structured case files and verifies:

- the real target note still exists
- the target note still sits in the expected card-type directory
- duplicate safety still holds for the recorded same-title glob
- the original source report still contains the expected write-validation facts

## Scope

Current cases:

- `concept-update-live-write`
- `concept-update-bridge-originated-live-write`
- `method-promotion-review-live-write`
- `method-promotion-review-bridge-originated-live-write`
- `misconception-ambiguous-create-live-write`

These are based on the already-recorded live validations under:

- `analysis/learning-card-live-write-validation/report.md`
- `analysis/learning-card-live-promotion-review-validation/report.md`

## Rebuild Command

```powershell
python analysis/learning-card-live-acceptance-harness/scripts/verify_live_acceptance_harness.py
```

## Output Artifacts

- `analysis/learning-card-live-acceptance-harness/outputs/concept-update-check.json`
- `analysis/learning-card-live-acceptance-harness/outputs/method-promotion-review-check.json`
- `analysis/learning-card-live-acceptance-harness/outputs/manifest.json`

## Observed Result

- the current repository now has a reusable read-only harness around the
  previously recorded live validations for:
  - existing-card update
  - bridge-originated existing-card update
  - existing-card promotion review
  - bridge-originated existing-card promotion review
  - ambiguous no-card-in-scope create
- this harness does not replace a future new live write, but it keeps the
  already-earned live validation line from decaying into one-off narrative
  reports
- the remaining higher-value bridge-originated gap is now:
  - ambiguous create
