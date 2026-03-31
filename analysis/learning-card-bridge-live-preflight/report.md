# Learning Card Bridge Live Preflight Report

## Goal

Provide one reusable preflight line for the highest remaining live gap:

- canonical router handoff text
- shared bridge prompt generation
- fully specified downstream execution prompt package
- alignment with a previously recorded real-write target

This line still stops before a new live write. Its job is to prove that an
operator can start from canonical handoff text and assemble an execution-ready
prompt package without manual prompt reconstruction.

## Scope

Current preflight cases cover the three real-write shapes already present in the
repository:

- `concept-update-bridge-packet`
- `method-promotion-review-bridge-packet`
- `misconception-ambiguous-create-bridge-packet`

For each case, the preflight verifies:

- canonical handoff text parses through the shared bridge
- the generated execution prompt contains explicit write-ready parameters
- the generated execution prompt contains no unresolved placeholder markers
- the packet aligns with the linked recorded live case target
- the packet still points to the correct downstream skill and mode

## Rebuild Command

```powershell
python analysis/learning-card-bridge-live-preflight/scripts/verify_bridge_live_preflight.py
```

## Output Artifacts

- `analysis/learning-card-bridge-live-preflight/outputs/concept-update-bridge-packet.txt`
- `analysis/learning-card-bridge-live-preflight/outputs/concept-update-bridge-packet-check.json`
- `analysis/learning-card-bridge-live-preflight/outputs/method-promotion-review-bridge-packet.txt`
- `analysis/learning-card-bridge-live-preflight/outputs/method-promotion-review-bridge-packet-check.json`
- `analysis/learning-card-bridge-live-preflight/outputs/misconception-ambiguous-create-bridge-packet.txt`
- `analysis/learning-card-bridge-live-preflight/outputs/misconception-ambiguous-create-bridge-packet-check.json`
- `analysis/learning-card-bridge-live-preflight/outputs/manifest.json`

## Observed Result

- the repository now has a distinct preflight layer between:
  - router handoff contract
  - bridge generation
  - execution result contract
  - recorded live write evidence
- this layer now emits machine-readable checks so a future live session can
  confirm packet readiness without re-reading the generated prompt manually
- each `*-check.json` now includes the explicit next operator action and the
  file-level completion markers that should appear after a real execution run
- this layer does not prove a new live write happened
- it does prove that the operator can derive a concrete execution packet from
  canonical handoff text for all three live-proven shapes
- the remaining highest-value live gap is now narrower:
  - bridge-originated ambiguous create
