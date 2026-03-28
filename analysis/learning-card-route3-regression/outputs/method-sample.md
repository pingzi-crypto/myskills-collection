---
id: 20260326200559-method
title: Prompt Narrowing
type: method
domain: AI Collaboration
subdomain: Skill Design
status: stable
graph_maturity: local
created: 2026-03-29
updated: 2026-03-29
source: Sample render test
tags:
  - method
related: []
confidence: 1
review_cycle: 30d
aliases: []
---

# Prompt Narrowing

## 1. 这个方法解决什么问题？
- How can an overly broad request be narrowed into a task that can actually be executed reliably?

## 2. 核心思路
- Constrain the task boundary before deciding the execution path.

## 3. 步骤结构
- Identify the true scope of the request.
- Remove unnecessary targets.
- Lock onto one output target.
- Then execute.

## 4. 关键设计选择
- The method prioritizes scope stability over early coverage.

## 5. 隐含假设
- The operator can judge which goals really belong inside the current task boundary.

## 6. 适用场景
- Useful when the task keeps expanding or mixing multiple objectives.

## 7. 不适用场景
- Less useful when the request is already precise and constrained.

## 8. 与替代方法的比较
- Compared with broad exploratory prompting, this method sacrifices spread to gain execution stability.

## 9. 常见误用
- Over-narrowing too early and discarding constraints that actually matter.

## 10. 失败模式
- If the scope is narrowed too hard, the output can become stable but miss the real goal.

## 11. 决策标准
- If the boundary is still unclear, do not expand implementation yet.

## 12. 代表性例子
- Turning 'optimize my whole knowledge system' into 'first design the progression protocol for one method skill'.

## 13. 验证问题
- Has the current request really been narrowed to one clear output target?

## Knowledge Graph Relations

### Local Position
- 上游概念: [[Problem Framing]] | Prompt narrowing depends on a clear framing of the task boundary.
- 上游机制: [[Scope Drift]] | The method becomes easier to justify once scope drift is understood.
- 相邻或替代方法: [[Prompt Iteration]] | Both improve prompts, but prompt narrowing acts earlier on scope.

### Operational Links
- 前提依赖: [[Single Output Target]] | Without a single output target, narrowing cannot stabilize execution.
- 下游支撑: [[Task Execution]] | Once the scope is narrowed, execution paths become easier to stabilize.
- 关键对比: [[Broad Prompt Exploration]] | One expands possibility space; the other reduces it.
- 纠偏关联: [[More Scope Means Better Results]] | This method corrects the intuition that broader scope always helps.

### Routing and Dispatch

#### Direct Routes
- When the request still mixes multiple goals, route to [[Single Output Target]] before continuing this method.
- If the boundary is unclear because the problem itself is vague, return to [[Problem Framing]].


## Progression Layer

### Upgrade Focus
- 当前阶段：stable
- 图谱成熟度：local
- The card is already a reliable local method node and now has an explicit dispatch skeleton.
- 下一步重点：
  - Add stronger failure fallback rules for when narrowing does not stabilize execution.
- 当前建议：watchlist
- 缺失证据：
  - Fallback behavior after method failure is still too weak.
  - It lacks stronger method-selection arbitration across adjacent strategies.
- 下一步行动规则：
  - When the method fails because the task is misframed, return to [[Problem Framing]].
  - When the method fails because the target is still unstable, return to [[Single Output Target]].
