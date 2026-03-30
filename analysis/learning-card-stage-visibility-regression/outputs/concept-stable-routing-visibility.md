---
id: 20260330185601429819-concept
title: Single Card Boundary
type: concept
domain: AI协同
subdomain: Stage Visibility Regression
status: stable
graph_maturity: local
created: 2026-03-30
updated: 2026-03-30
source: Automated stage-aware routing visibility check
tags:
  - concept
related: []
confidence: 1
review_cycle: 30d
aliases: []
---

# Single Card Boundary

## 1. 这个概念在回答什么问题？
- 什么情况下应该只保留一张卡？
  - EN: When should only one card be kept?

## 2. 一句话定义
- 单卡边界是防止线程失焦的第一道约束。
  - EN: A single-card boundary is the first constraint against thread drift.

## 3. 核心本质
- 

## 4. 为什么重要
- 

## 5. 核心逻辑
- 

## 6. 成立前提
- 

## 7. 失效边界
- 

## 8. 易混概念与区别
- 

## 9. 正例
- 

## 10. 反例或误用
- 

## 11. 常见误解
- 

## 12. 我的表达
- 

## 13. 待验证问题
- 

## Knowledge Graph Relations

### Local Position
- 上位概念: [[Task Scope]] | 单卡边界依赖任务边界先被说明。
- 下位概念: 
- 相邻概念: 

### Operational Links
- 前提依赖: 
- 下游支撑: [[Learning Card Routing]] | 稳定单卡边界后，路由才更可靠。
- 关键对比: 
- 纠偏关联: 

### Routing and Dispatch

#### Direct Routes
- When the term boundary drifts, route back to [[Single Card Boundary]].


## Progression Layer

### Upgrade Focus
- 当前阶段：stable
- 图谱成熟度：local
- 该稳定态样例用于验证 stable 只显示 Direct Routes。
  - EN: This stable sample verifies that stable only exposes Direct Routes.
- 当前建议：watchlist
- 缺失证据：
  - Still lacks stronger dispatch rules.
