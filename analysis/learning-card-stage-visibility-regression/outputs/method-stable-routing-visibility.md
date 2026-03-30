---
id: 20260330185601429819-method
title: Prompt Scope Reset
type: method
domain: AI协同
subdomain: Stage Visibility Regression
status: stable
graph_maturity: local
created: 2026-03-30
updated: 2026-03-30
source: Automated stage-aware routing visibility check
tags:
  - method
related: []
confidence: 1
review_cycle: 30d
aliases: []
---

# Prompt Scope Reset

## 1. 这个方法解决什么问题？
- 线程已混入多个目标时，如何回到单一输出？
  - EN: How do you return to one output after a thread has mixed multiple goals?

## 2. 核心思路
- 先停，再缩，再重定主目标。
  - EN: Pause, shrink, then re-anchor the primary target.

## 3. 步骤结构
- 

## 4. 关键设计选择
- 

## 5. 隐含假设
- 

## 6. 适用场景
- 

## 7. 不适用场景
- 

## 8. 与替代方法的比较
- 

## 9. 常见误用
- 

## 10. 失败模式
- 

## 11. 决策标准
- 

## 12. 代表性例子
- 

## 13. 验证问题
- 

## Knowledge Graph Relations

### Local Position
- 上游概念: [[Single Card Boundary]] | 重置前先需要边界概念。
- 上游机制: 
- 相邻或替代方法: 

### Operational Links
- 前提依赖: 
- 下游支撑: [[Learning Card Routing]] | 重置后才能重新路由。
- 关键对比: 
- 纠偏关联: 

### Routing and Dispatch

#### Direct Routes
- When scope drift appears mid-execution, route to [[Prompt Scope Reset]] before continuing the current method.


## Progression Layer

### Upgrade Focus
- 当前阶段：stable
- 图谱成熟度：local
- 该稳定态样例用于验证 Method 卡在 stable 时仅显示 Direct Routes。
  - EN: This stable sample verifies that Method cards in stable show only Direct Routes.
- 当前建议：watchlist
