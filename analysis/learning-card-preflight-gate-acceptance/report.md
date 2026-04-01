# Learning Card Preflight Gate Acceptance Report

## Goal

Provide one acceptance line for the repo-level go/no-go gate that sits in front
of any future bridge-originated live operator run.

This line validates that machine-readable preflight `*-check.json` outputs can
be consumed through one short operator command instead of being read manually.

## Acceptance Target

Primary wrapper:

- `scripts/use_learning_card_preflight_gate.ps1`

Covered gate shapes:

- existing `go` checks emitted by bridge live preflight
- one synthetic `no-go` check with unresolved placeholders

## Rebuild Command

```powershell
python analysis/learning-card-preflight-gate-acceptance/scripts/verify_preflight_gate_acceptance.py
```

## Output Artifacts

- `analysis/learning-card-preflight-gate-acceptance/outputs/concept-update-gate.txt`
- `analysis/learning-card-preflight-gate-acceptance/outputs/method-promotion-review-gate.txt`
- `analysis/learning-card-preflight-gate-acceptance/outputs/misconception-ambiguous-create-gate.txt`
- `analysis/learning-card-preflight-gate-acceptance/outputs/misconception-bridge-create-gate.txt`
- `analysis/learning-card-preflight-gate-acceptance/outputs/synthetic-no-go-gate.txt`
- `analysis/learning-card-preflight-gate-acceptance/outputs/manifest.json`

## Observed Result

- the repository now has one repo-level command for consuming preflight checks
  as a real go/no-go gate
- current bridge-preflight `go` packets can be reviewed through a short summary
  showing skill, mode, target, completion proof, and next action
- `no-go` packets now fail with a non-zero exit code and surface their blocking
  placeholders explicitly
- future bridge-originated live runs can use the check JSON as an actual gate,
  not only as an analysis artifact
