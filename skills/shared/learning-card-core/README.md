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

Boundary rule:

- shared core owns procedural and rendering protocol
- shared core owns common spec validation before deterministic rendering
- execution skills still own card-type semantics
- router still owns broad thread classification

Use this directory to centralize family-wide behavior without collapsing the
four card types into one monolithic execution skill.
