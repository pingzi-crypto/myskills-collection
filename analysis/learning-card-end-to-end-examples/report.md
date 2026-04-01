# Learning Card End-to-End Examples

## Goal

Show one user-visible chain from:

- router classification
- explicit handoff boundary
- downstream execution input
- actual execution result shape

This document is for operator understanding, not renderer regression.

## Example 1: Concept Create

### User Intent

The user wants to save this thread fragment:

- `windows系统有自带的截图功能吗？如果有快捷键是什么`

### Router Step

Expected router output:

```text
Capture anchor: `windows系统有自带的截图功能吗？如果有快捷键是什么` -> first assistant reply after it
Route result: `Concept`
Mode: `create`
Use `$obsidian-concept-card-capture` for the next step.
Router status: routing complete only. No card file has been created or updated yet.
Execution package confirmed:
- Capture anchor: selected user message -> first assistant reply after it
- Card type: Concept
- Mode: create
- Downstream skill: $obsidian-concept-card-capture
Still needed before write:
- title
- keywords or thread points
- domain
- vault root
Next step: use `$obsidian-concept-card-capture` now to actually create the card.
Suggested reply: `继续创建`
Reason: 这段内容主要在回答“Windows 自带截图方式都是什么、各自代表什么”，核心是功能与边界说明。
```

Important interpretation:

- routing is complete
- card creation is not complete
- no Obsidian file should be expected yet

### Execution Step

The next user or agent turn should call the execution skill with the missing
write inputs filled in:

```text
Use $obsidian-concept-card-capture to work on one concept card from this thread.
Mode: create
Concept title: Windows 自带截图方式
Keywords or thread points to capture:
- Windows 自带多种截图方式
- `Print Screen`
- `Win + Shift + S`
- Snipping Tool
- 全屏截图与区域截图的差异
Domain: Windows Workflow
Subdomain: Screenshot Tools
Source: current Codex thread on built-in Windows screenshots
Vault root: C:\Users\pz\Documents\Obsidian Vault
```

### Execution Result

Only after the execution skill runs should the result look like:

```text
Concept captured: Windows 自带截图方式
Created file: C:\Users\pz\Documents\Obsidian Vault\学习\Cards\Concepts\Windows 自带截图方式.md
Summary: extracted the built-in screenshot options, their shortcuts, and their boundary differences.
Progression result: stay seed
```

### User-Level Rule

Practical shortcut:

- if the router output still says `Router status: routing complete only`, the
  card does not exist yet
- only trust `Created file:` or `Updated file:` lines from the execution skill
  as proof that a note was actually written

## Example 2: Method Update

### User Intent

The user wants to merge new bilingual-routing guidance into an existing method
card.

### Router Step

Router output can already know:

- card type: `Method`
- mode: `update`

But if the existing target card is not explicit yet, the handoff still needs to
say so:

```text
Still needed before write:
- existing card title or path confirmation
- vault root
```

That means the downstream skill still has to identify the exact existing note
before any update can happen.

### Operator Packet Step

The repo-level daily shortcut can now turn that handoff into the next execution
prompt:

```powershell
pwsh -File scripts/use_learning_card_operator_packet.ps1
```

Expected operator summary shape:

```text
Operator packet ready.
Status: Execution prompt ready only. No card file has been created, updated, or reviewed yet.
Downstream skill: $obsidian-method-card-capture
Mode: update
Completion proof: Updated file:, Summary:
Still needed: existing card title or path confirmation, vault root
```

### Execution Result

Only after the execution skill runs should the result look like:

```text
Method updated: Router bilingual clarification flow
Updated file: C:\Users\pz\Documents\Obsidian Vault\学习\Cards\Methods\Router bilingual clarification flow.md
Summary: merged the bilingual question pattern and clarified when the router should ask for card type confirmation.
```

## Example 3: Promotion Review

### User Intent

The user wants to review whether one misconception card has enough graph and
routing evidence to move upward.

### Router Step

For `promotion review`, the same rule applies:

- routing can classify the task as a review
- but if the exact existing card is not explicit, no review write should happen
  yet

### Operator Packet Step

The same repo-level daily shortcut applies:

```powershell
pwsh -File scripts/use_learning_card_operator_packet.ps1
```

Expected operator summary shape:

```text
Operator packet ready.
Status: Execution prompt ready only. No card file has been created, updated, or reviewed yet.
Downstream skill: $obsidian-misconception-card-capture
Mode: promotion review
Completion proof: Reviewed file:, Promotion result:, Summary:
Still needed: existing card title or path confirmation, vault root
```

### Execution Result

Only after the target note is explicit should the execution skill return a
result such as:

```text
Reviewed file: C:\Users\pz\Documents\Obsidian Vault\学习\Cards\Misconceptions\误把路由完成当作写卡完成.md
Promotion result: watchlist
Summary: review found that the card has a clear correction rule but still lacks enough graph-routing evidence for promotion.
```

## Core Rule

Use this distinction everywhere:

- router output proves classification
- execution output proves file-level change
