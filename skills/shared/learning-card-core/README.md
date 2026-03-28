# Learning Card Core

This directory stores shared implementation references for the Obsidian
learning-card family.

Current shared references:

- `references/vault-path-protocol.md`
- `references/same-title-update-flow.md`
- `references/deterministic-render-protocol.md`

Current shared scripts:

- `scripts/render_common.py`

Boundary rule:

- shared core owns procedural and rendering protocol
- execution skills still own card-type semantics
- router still owns broad thread classification

Use this directory to centralize family-wide behavior without collapsing the
four card types into one monolithic execution skill.
