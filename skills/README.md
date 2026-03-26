# Skills Index

This directory stores reusable skills, concrete skill families, and starter
templates for this collection.

## Family Overview

Shared learning-card references:

- `skills/references/learning-card-skill-family.md`
- `skills/references/progression-protocol.md`
- `skills/references/knowledge-graph-relations.md`

## Available Entries

### `cross-platform-skill-template`

Starter template for building one shared skill core with thin wrappers for:

- Codex
- Claude Code
- OpenClaw

Path:

- `skills/cross-platform-skill-template/`

Use this entry when you want to:

- start a new cross-platform skill from a clean skeleton
- keep shared workflow in `core/`
- isolate platform-specific behavior in wrapper directories

### `obsidian-learning-card-router`

Router for deciding which one of the four Obsidian learning-card execution
skills should handle the current thread, and whether the task is:

- `create`
- `update`
- `promotion review`

Path:

- `skills/obsidian-learning-card-router/`

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
```

### `obsidian-concept-card-capture`

Execution skill for turning one thread into one Obsidian Concept Card, or for
updating or promoting an existing Concept Card.

Path:

- `skills/obsidian-concept-card-capture/`

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
2. Route to exactly one execution skill.
3. Let that skill handle duplicate checks, rendering, and progression assessment.
4. Promote only when the card has real node-level or rule-level evidence.

## Collection Direction

As this repository grows, this index should remain the first place to look for:

- stable skill families
- starter templates
- routing entry points
- execution skills with real workflows
