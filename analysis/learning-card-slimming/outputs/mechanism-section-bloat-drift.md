---
id: 20260327000002-mechanism-audit
title: Section Bloat Drift
type: mechanism
domain: Learning Card Design
subdomain: Template Slimming Audit
status: stable
graph_maturity: local
created: 2026-03-27
updated: 2026-03-27
source: Structured slimming audit sample
tags:
  - mechanism
related: []
confidence: 1
review_cycle: 30d
aliases: []
---

# Section Bloat Drift

## 1. Phenomenon Explained
- Why learning cards become longer and lower-signal when every possible section stays permanently visible.

## 2. Core Variables
- Template width
- Deletion friction
- Boundary confidence
- Progression pressure

## 3. Causal Chain
- A wide template invites filler, filler normalizes section completion, section completion hides weak signal, and the card gradually optimizes for fullness instead of retrieval value.

## 4. Key Preconditions
- The template must make it easy to keep optional sections visible even when their content is weak.

## 5. Weakest Link
- The weakest step is review discipline; without active pruning, optional sections become permanent ballast.

## 6. Alternative Mechanisms
- Some bloat comes from unclear source threads rather than from template width alone.

## 7. Scope
- This mechanism mainly explains mature card families with many reusable sections, not tiny scratch notes.

## 8. Failure Boundaries
- If the card is too new to have real optional sections yet, bloat drift is not the main cause of verbosity.

## 9. Supporting Evidence
- Across filled samples, progression and review scaffolding consume a large share of rendered words even when the card's real learning payload is already complete.

## 10. Counter Cases
- A short template can still produce bloated cards when the thread itself is badly scoped.

## 11. Compressed Explanation
- Section bloat drift happens when template completion becomes more important than signal density.

## 12. Validation Question
- Is the extra section carrying new retrieval value, or only proving that the template was filled?

## Knowledge Graph Relations

### Local Position
- Upstream Concepts: [[Single-Card Boundary]] | Weak boundaries make it easier for extra sections to sneak in.
- Trigger Conditions: [[Always-On Review Scaffolding]] | Permanent checklists and status blocks trigger the drift.
- Downstream Results: [[Low-Signal Cards]] | The mechanism lowers retrieval density and raises maintenance burden.
- Adjacent Mechanisms: [[Scope Drift]] | Scope drift widens the topic, while section bloat drift widens the template.

### Operational Links
- Prerequisites: [[Stable Card Family]] | The mechanism appears only after the template gains enough reusable structure.
- Enables: [[Section Priority Compression]] | Understanding the mechanism justifies trimming action.
- Contrasts: [[Rich Evidence Density]] | High detail is not the same as low-signal bloat.
- Corrections: [[More Sections Make a Better Learning Card]] | Correcting the misconception removes one cause of this drift.

### Routing and Dispatch

#### Direct Routes
- When the problem is deciding what to cut first, route to [[Section Priority Compression]].
- If the problem is not template width but topic width, return to [[Single-Card Boundary]].


## Progression Layer

### Upgrade Focus
- Current status: stable
- Graph maturity: local
- The mechanism already explains why mature card templates tend to overproduce low-value sections.
- Next goal:
  - Add a stronger distinction between topic drift and template drift.
- Current recommendation: watchlist
- Missing evidence:
  - It still needs a stronger switch rule for distinguishing section drift from topic drift.
- Next rules worth adding:
  - If trimming section count does not improve retrieval, inspect topic routing before pruning further.
