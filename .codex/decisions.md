# Direction Decisions

## Active Decisions

### Decision
- Summary: Treat the learning-card family as the primary long-lived direction in
  this repository
- Date: 2026-03-31
- Status: active

### Context
- The repository contains multiple historical lines and documentation layers,
  but current real work has concentrated on the Obsidian learning-card system.

### Choice
- Treat the learning-card family as the primary project direction and treat
  older or broader lines as secondary unless explicitly revived.

### Why
- It matches the actual implementation activity, analysis coverage, and user
  intent.
- It reduces structural drift and prevents multiple parallel truth sources.

### Alternatives Rejected
- Option: treat all historical lines as equally active
- Why not: that keeps the project structure ambiguous and raises future
  re-entry cost.

### Impact
- Project continuity files should describe the learning-card family first.
- New worktrees should default to learning-card topics on top of `main`.

---

### Decision
- Summary: Keep the system architecture as router plus shared core plus thin
  execution skills
- Date: 2026-03-31
- Status: active

### Context
- The family could have been collapsed into a monolithic all-in-one skill, but
  recent work reinforced the existing split.

### Choice
- Keep routing, shared protocol logic, and card-type execution behavior as
  separate layers.

### Why
- It preserves card-type boundaries.
- It keeps shared behavior centralized without collapsing card semantics.
- It supports bounded regression and cleaner maintenance.

### Alternatives Rejected
- Option: build one 4-in-1 public execution skill
- Why not: that increases ambiguity, weakens boundaries, and makes maintenance
  noisier.

### Impact
- Shared utilities belong in `skills/shared/learning-card-core/`.
- Card-type semantics stay inside the four execution skills.

---

### Decision
- Summary: Treat canonical router handoff text as the stable boundary between
  routing and execution
- Date: 2026-03-31
- Status: active

### Context
- Users needed a clear transition from router output to actual execution, and
  recent work added parser and bridge tooling for that boundary.

### Choice
- Keep the router handoff text explicit, machine-parseable, and stable enough
  for shared bridge tooling.

### Why
- It prevents router output from sounding like a completed write.
- It enables reusable prompt generation and operator tooling.
- It gives regression tests a canonical contract surface.

### Alternatives Rejected
- Option: rely on informal free-form router output
- Why not: it makes downstream automation and operator reuse brittle.

### Impact
- Router contract changes should be checked against bridge tooling and
  handoff-parser regressions.
- The shared bridge script is now part of the expected operator workflow.
