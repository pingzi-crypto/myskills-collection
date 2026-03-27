---
id: 20260327000003-method-audit
title: Section Priority Compression
type: method
domain: Learning Card Design
subdomain: Template Slimming Audit
status: stable
graph_maturity: local
created: 2026-03-27
updated: 2026-03-27
source: Structured slimming audit sample
tags:
  - method
related: []
confidence: 1
review_cycle: 30d
aliases: []
---

# Section Priority Compression

## 1. 这个方法解决什么问题？
- How can a learning card be trimmed without losing the information needed for retrieval, routing, and upgrade?

## 2. 核心思路
- Rank sections by answer-criticality, routing value, and uniqueness, then cut the lowest-yield material first.

## 3. 步骤结构
- State the dominant question of the card.
- Keep the sections that answer or bound that question.
- Keep graph sections only when they carry real local value.
- Gate progression scaffolding by maturity or review mode.
- Render the shortest version that still supports reuse.

## 4. 关键设计选择
- The method prefers signal density over template completeness.

## 5. 隐含假设
- The reviewer can tell the difference between useful nuance and habitual filler.

## 6. 适用场景
- Use it when cards feel complete but still hard to scan or retrieve from.

## 7. 不适用场景
- Do not use it when the card is weak because the topic itself is still unclear.

## 8. 与替代方法的比较
- Unlike a purely aesthetic rewrite, this method cuts by information yield rather than by sentence style alone.

## 9. 常见误用
- Removing graph sections too early and leaving the card isolated.
- Keeping every checklist because it feels productive.

## 10. 失败模式
- The method fails when the reviewer trims high-value boundary sections together with low-value scaffolding.

## 11. 决策标准
- If a section neither changes retrieval, graph placement, nor next action, it is a compression candidate.

## 12. 代表性例子
- Merging status notes, next goal, and upgrade tasks into one short maintenance block while preserving the concept core and local graph placement.

## 13. 验证问题
- After trimming, can a future self still answer what this card is for, where it fits, and what to do next?

## Knowledge Graph Relations

### Local Position
- 上游概念: [[Single-Card Boundary]] | Clear boundaries make section ranking easier.
- 上游机制: [[Section Bloat Drift]] | The method is a response to that drift.
- 相邻或替代方法: [[Template Rewrite]] | Both reduce verbosity, but this method uses information yield as the ranking rule.

### Operational Links
- 前提依赖: [[Card Type Routing]] | Section compression assumes the right card type is already chosen.
- 下游支撑: [[Default Stable Render]] | It produces a thinner default card shape.
- 关键对比: [[Complete Template Filling]] | One rewards completeness; the other rewards signal density.
- 纠偏关联: [[More Sections Make a Better Learning Card]] | The method corrects that impulse operationally.

### Routing and Dispatch

#### Direct Routes
- When the problem is conceptual rather than operational, return to [[Single-Card Boundary]].
- When the problem is repeated re-expansion after trimming, route to [[More Sections Make a Better Learning Card]].


## Progression Layer

### Upgrade Focus
- 当前阶段：stable
- 图谱成熟度：local
- The method already works as a reliable local procedure for slimming stable cards.
- 下一步重点：
  - Add a lightweight scoring shortcut for faster review passes.
- 当前建议：watchlist
- 缺失证据：
  - It still needs stronger arbitration between trimming a card and splitting it into two cards.
- 下一步行动规则：
  - If compression removes a whole second question, split the card instead of trimming harder.
