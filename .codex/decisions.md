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

---

### Decision
- Summary: Allow repo-level operator wrappers only as thin delegators into the
  shared learning-card core
- Date: 2026-04-01
- Status: active

### Context
- The shared operator-packet entrypoint is correct but its full script path is
  longer than needed for daily use from the repository root.

### Choice
- Allow repo-level wrapper scripts under `scripts/` when they only forward into
  the shared-core implementation and do not introduce a second protocol or
  duplicate packet-building logic.

### Why
- It shortens the daily command surface without collapsing the current
  architecture.
- It keeps the shared core as the single implementation source of truth.

### Alternatives Rejected
- Option: keep only the long shared-core script path
- Why not: the daily operator flow stays needlessly high-friction.
- Option: move packet logic out of shared core into repo-level wrappers
- Why not: that would create contract drift and duplicate maintenance.

### Impact
- `scripts/` can host thin operator wrappers for daily use.
- Acceptance should verify that repo-level wrappers match shared-core output.

---

### Decision
- Summary: Strengthen bridge-originated live acceptance through read-only
  evidence-chain validation before opening any new live write line
- Date: 2026-04-01
- Status: active

### Context
- The repository already has one live-proven bridge-originated triad for
  update, promotion review, and ambiguous create.
- The remaining gap was not proof that bridge-originated live writes can happen,
  but proof that the full operator session evidence chain still aligns across
  handoff, preflight packet, readiness gate, live report, and target note.

### Choice
- Prefer strengthening the existing live acceptance harness with evidence-chain
  checks for bridge-originated cases.
- Do not open a new real-write validation line unless the contracts materially
  shift beyond what the read-only evidence chain can still prove.

### Why
- It increases confidence in the bridge-originated operator path without
  creating unnecessary vault-write risk.
- It keeps the stronger live acceptance layer reusable, repeatable, and safe to
  rerun on demand.

### Alternatives Rejected
- Option: immediately add another real bridge-originated live write run
- Why not: the existing live triad already proves execution can happen; the
  higher-value gap is contract continuity, not another write.

### Impact
- Bridge-originated live cases should carry structured pointers to handoff,
  preflight packet, and readiness-check artifacts.
- The live acceptance harness should verify that those artifacts still align
  with the final recorded live target.

---

### Decision
- Summary: Keep the current repo-level operator surface as the default and do
  not add a thinner alias yet
- Date: 2026-04-01
- Status: active

### Context
- The repository now has one repo-level daily operator wrapper and one repo-level
  preflight gate wrapper.
- Acceptance, examples, and drift-watch coverage now exist around both.

### Choice
- Treat the current pair of repo-level commands as sufficient:
  - `scripts/use_learning_card_operator_packet.ps1`
  - `scripts/use_learning_card_preflight_gate.ps1`
- Do not add another thinner alias unless new real operator use shows that the
  command path itself is the primary friction point.

### Why
- The remaining operator work is mostly semantic, not syntactic:
  - providing missing inputs
  - choosing the exact existing target card
  - waiting for file-level completion proof
- Another alias would reduce typing slightly but add more surface area to keep
  documented and regression-backed.

### Alternatives Rejected
- Option: add another even thinner alias immediately
- Why not: that would optimize a smaller problem than the current real
  operator bottlenecks.

### Impact
- The current repo-level wrappers become the stable default surface.
- Future operator-surface changes should be justified by new real-use friction,
  not by abstraction preference alone.
