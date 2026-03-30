# Skills Index

This directory stores the concrete learning-card skill family for this collection.

## Family Overview

Shared learning-card references:

- `skills/references/learning-card-skill-family.md`
- `skills/references/learning-card-standard-operating-manual.md`
- `skills/references/learning-card-shared-core-blueprint.md`
- `skills/references/learning-card-worktree-guide.md`
- `skills/references/learning-card-route-3-execution-checklist.md`
- `skills/references/progression-protocol.md`
- `skills/references/knowledge-graph-relations.md`

Shared implementation core:

- `skills/shared/learning-card-core/references/vault-path-protocol.md`
- `skills/shared/learning-card-core/references/same-title-update-flow.md`
- `skills/shared/learning-card-core/references/deterministic-render-protocol.md`
- `skills/shared/learning-card-core/scripts/render_common.py`

## Available Entries

### `obsidian-learning-card-router`

Router for deciding which one of the four Obsidian learning-card execution
skills should handle the current thread, and whether the task is:

- `create`
- `update`
- `promotion review`

Path:

- `skills/obsidian-learning-card-router/`
- export wrappers:
  - `dist/claude/obsidian-learning-card-router/`
  - `dist/openclaw/obsidian-learning-card-router/`

Use this entry when you want to:

- classify a thread before writing a card
- choose between concept, mechanism, method, and misconception
- preserve one-card boundaries
- avoid defaulting to all four card types at once

Prompt template:

```text
Use $obsidian-learning-card-router to choose the right learning card skill and mode for this thread.
Goal: work on exactly one learning card.
If the type is ambiguous, ask one short clarification question.
After routing, explicitly show:
- routing-only status
- minimum execution package already confirmed
- still-missing write inputs the downstream skill must collect
```

### `obsidian-concept-card-capture`

Execution skill for turning one thread into one Obsidian Concept Card, or for
updating or promoting an existing Concept Card.

Path:

- `skills/obsidian-concept-card-capture/`
- export wrappers:
  - `dist/claude/obsidian-concept-card-capture/`
  - `dist/openclaw/obsidian-concept-card-capture/`

Use this entry when you want to:

- capture one concept from Q&A or discussion
- update one existing concept card
- review whether a concept card should stay stable, move to watchlist, or be promoted
- save it under the resolved vault root at `学习/Cards/Concepts`

Prompt template:

```text
Use $obsidian-concept-card-capture to work on one concept card from this thread.
Mode: <create | update | promotion review>
Concept title: <single concept>
Keywords or thread points to capture: <keywords or short excerpts>
Domain: <domain>
Subdomain: <optional subdomain>
Source: <optional source>
Vault root: <optional vault path>
```

### `obsidian-mechanism-card-capture`

Execution skill for turning one thread into one Obsidian Mechanism Card, or for
updating or promoting an existing Mechanism Card.

Path:

- `skills/obsidian-mechanism-card-capture/`
- export wrappers:
  - `dist/claude/obsidian-mechanism-card-capture/`
  - `dist/openclaw/obsidian-mechanism-card-capture/`

Use this entry when you want to:

- capture one causal explanation from Q&A or discussion
- update one existing mechanism card
- review whether a mechanism card should stay stable, move to watchlist, or be promoted
- save it under the resolved vault root at `学习/Cards/Mechanisms`

Prompt template:

```text
Use $obsidian-mechanism-card-capture to work on one mechanism card from this thread.
Mode: <create | update | promotion review>
Mechanism title: <single mechanism>
Keywords or thread points to capture: <keywords or short excerpts>
Domain: <domain>
Subdomain: <optional subdomain>
Source: <optional source>
Vault root: <optional vault path>
```

### `obsidian-method-card-capture`

Execution skill for turning one thread into one Obsidian Method Card, or for
updating or promoting an existing Method Card.

Path:

- `skills/obsidian-method-card-capture/`
- export wrappers:
  - `dist/claude/obsidian-method-card-capture/`
  - `dist/openclaw/obsidian-method-card-capture/`

Use this entry when you want to:

- capture one practical procedure or strategy from Q&A or discussion
- update one existing method card
- review whether a method card should stay stable, move to watchlist, or be promoted
- save it under the resolved vault root at `学习/Cards/Methods`

Prompt template:

```text
Use $obsidian-method-card-capture to work on one method card from this thread.
Mode: <create | update | promotion review>
Method title: <single method>
Keywords or thread points to capture: <keywords or short excerpts>
Domain: <domain>
Subdomain: <optional subdomain>
Source: <optional source>
Vault root: <optional vault path>
```

### `obsidian-misconception-card-capture`

Execution skill for turning one thread into one Obsidian Misconception Card, or
for updating or promoting an existing Misconception Card.

Path:

- `skills/obsidian-misconception-card-capture/`
- export wrappers:
  - `dist/claude/obsidian-misconception-card-capture/`
  - `dist/openclaw/obsidian-misconception-card-capture/`

Use this entry when you want to:

- capture one mistaken claim or recurring error pattern from Q&A or discussion
- update one existing misconception card
- review whether a misconception card should stay stable, move to watchlist, or be promoted
- save it under the resolved vault root at `学习/Cards/Misconceptions`

Prompt template:

```text
Use $obsidian-misconception-card-capture to work on one misconception card from this thread.
Mode: <create | update | promotion review>
Misconception title: <single misconception>
Keywords or thread points to capture: <keywords or short excerpts>
Domain: <domain>
Subdomain: <optional subdomain>
Source: <optional source>
Vault root: <optional vault path>
```

## Suggested Obsidian Workflow

1. Use `obsidian-learning-card-router` if the type is still ambiguous.
2. Let the router explicitly say whether it only classified the thread or an execution skill has actually written a card.
3. Route to exactly one execution skill.
4. Let that skill handle duplicate checks, rendering, and progression assessment.
5. Promote only when the card has real node-level or rule-level evidence.

## End-to-End Example

This is the safest mental model:

1. `obsidian-learning-card-router` only classifies the thread.
2. The router does not create or update any card file.
3. The downstream execution skill does the real write.

Example:

User asks to save a thread fragment about Windows screenshot capabilities.

Router output should look like:

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
Reason: 这段内容主要在解释截图方式的类型和边界，属于概念卡。
```

At this point, no card file exists yet.

The user or agent must continue into the execution skill, for example:

```text
Use $obsidian-concept-card-capture to work on one concept card from this thread.
Mode: create
Concept title: Windows 自带截图方式
Keywords or thread points to capture:
- Windows 自带多种截图方式
- Print Screen
- Win + Shift + S
- Snipping Tool
Domain: Windows Workflow
Vault root: C:\Users\pz\Documents\Obsidian Vault
```

Only after that execution step should the user expect a result shaped like:

```text
Concept captured: Windows 自带截图方式
Created file: <VAULT_ROOT>/学习/Cards/Concepts/Windows 自带截图方式.md
Summary: extracted the built-in screenshot methods, their shortcuts, and their boundary differences.
```

Longer user-view examples live at:

- `analysis/learning-card-end-to-end-examples/report.md`

Short operator manual:

- `skills/references/learning-card-standard-operating-manual.md`
 
## Collection Direction

As this repository grows, this index should remain the first place to look for:

- stable skill families
- routing entry points
- execution skills with real workflows

Codex runtime rule:

- keep `skills/` limited to the entries Codex should actually discover
- keep non-Codex wrappers under `dist/` so they do not pollute Codex runtime discovery
