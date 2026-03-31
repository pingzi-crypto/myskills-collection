# Learning Card Core

This directory stores shared implementation references for the Obsidian
learning-card family.

Current shared references:

- `references/vault-path-protocol.md`
- `references/same-title-update-flow.md`
- `references/deterministic-render-protocol.md`

Current shared scripts:

- `scripts/render_common.py`
- `scripts/build_execution_prompt.py`
- `scripts/build_execution_prompt_from_handoff.py`
- `scripts/use_handoff_bridge.ps1`

Shared script intent:

- `scripts/render_common.py`: deterministic shared rendering helpers
- `scripts/build_execution_prompt.py`: build an execution prompt when card type
  and mode are already explicit
- `scripts/build_execution_prompt_from_handoff.py`: parse canonical router
  handoff text and emit the matching execution prompt skeleton, including
  operator-friendly stdin and clipboard entry modes; prefers `pwsh` on Windows
  and falls back to Windows PowerShell when needed
- `scripts/use_handoff_bridge.ps1`: thin PowerShell wrapper for the handoff
  bridge; defaults to clipboard in and clipboard out for day-to-day operator use

Boundary rule:

- shared core owns procedural and rendering protocol
- shared core owns common spec validation before deterministic rendering
- execution skills still own card-type semantics
- router still owns broad thread classification

Use this directory to centralize family-wide behavior without collapsing the
four card types into one monolithic execution skill.
