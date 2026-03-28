---
id: 20260326201012-concept
title: Deterministic Card Rendering
type: concept
domain: AI Collaboration
subdomain: Skill Design
status: stable
graph_maturity: local
created: 2026-03-29
updated: 2026-03-29
source: Current Codex thread on skill execution stability
tags:
  - concept
related: []
confidence: 1
review_cycle: 30d
aliases: []
---

# Deterministic Card Rendering

## 1. 这个概念在回答什么问题？
- How can a learning card keep a stable final structure instead of relying on ad hoc manual formatting every time?

## 2. 一句话定义
- Deterministic Card Rendering means deciding the content first and then using a fixed renderer to produce the final card structure.

## 3. 核心本质
- It separates semantic judgment from structural output so each layer can become stable in its own way.

## 4. 为什么重要
- It reduces formatting drift across runs.
- It makes skill outputs easier to compare, validate, and maintain.

## 5. 核心逻辑
- Extract the concept-level content from the thread.
- Map that content into fixed sections.
- Let a renderer generate the final Markdown shape.

## 6. 成立前提
- The target card structure is already stable enough to render deterministically.
- The input has already been narrowed to one clear concept.

## 7. 失效边界
- If the input still mixes multiple concepts, deterministic rendering will only produce consistently mixed output.
- If the schema keeps changing, renderer stability will also drift.

## 8. 易混概念与区别
- It is easy to confuse this with simply having a template file; the key difference is a fixed rendering flow.

## 9. 正例
- First build a JSON spec, then run the renderer to produce the final card.

## 10. 反例或误用
- Manually copying an old card and editing it freehand until field order and section style slowly diverge.

## 11. 常见误解
- A stable structure does not automatically mean high-quality content.

## 12. 我的表达
- Let me think about the content, and let the renderer own the shape.

## 13. 待验证问题
- When updating an existing card, should the same rendering skeleton still be reused whenever possible?

## Knowledge Graph Relations

### Local Position
- 上位概念: [[Skill Output Stability]] | Deterministic rendering is a lower-level implementation of output stability.
- 下位概念: [[Deterministic Method Rendering]] | Method-card rendering is one concrete branch of this idea.
- 相邻概念: [[Template-Driven Writing]] | Both pursue consistency, but one relies on a renderer and the other leans on a static template.

### Operational Links
- 前提依赖: [[Single Concept Capture]] | Deterministic rendering only helps after the card boundary is already compressed to one concept.
- 下游支撑: [[Prompt Narrowing]] | Stable rendering makes it easier to compare outputs from narrowed prompts.
- 关键对比: [[Template-Driven Writing]] | One emphasizes a fixed generation flow, the other emphasizes a reusable template.
- 纠偏关联: [[Templates Alone Guarantee Stability]] | This concept corrects the mistaken idea that templates alone are sufficient.

### Routing and Dispatch

#### Direct Routes
- When the thread is still defining what deterministic rendering is, stay in this concept card before switching to implementation details.
- If the idea is clear but the next question becomes how to apply it in a workflow, route to [[Prompt Narrowing]].


## Progression Layer

### Upgrade Focus
- 当前阶段：stable
- 图谱成熟度：local
- This concept already has reliable local graph placement and early routing value.
- 下一步重点：
  - Add a stronger arbitration rule for when to move from definition work to method or mechanism work.
- 当前建议：watchlist
- 缺失证据：
  - It still lacks stronger cross-card arbitration rules.
  - Its gap-detection behavior is still narrow.
- 下一步行动规则：
  - When definition work turns into workflow design, route to a method card.
  - When definition work turns into causal explanation, route to a mechanism card.
