# Skills Index

This directory stores reusable skills and templates for this collection.

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

### `obsidian-concept-card-capture`

Skill for turning the current thread into exactly one Obsidian Concept Card.

Path:

- `skills/obsidian-concept-card-capture/`

Use this entry when you want to:

- capture one concept from Q&A or discussion
- create a new `seed` concept card
- save it under the resolved vault root at `学习/Cards/Concepts`
- add conservative backlinks to existing cards

Prompt template:

```text
Use $obsidian-concept-card-capture to capture one concept from this thread.
Concept title: <single concept>
Keywords or thread points to capture: <keywords or short excerpts>
Domain: <domain>
Subdomain: <optional subdomain>
Source: <optional source>
Vault root: <optional vault path>
```

### `obsidian-mechanism-card-capture`

Skill for turning the current thread into exactly one Obsidian Mechanism Card.

Path:

- `skills/obsidian-mechanism-card-capture/`

Use this entry when you want to:

- capture one causal explanation from Q&A or discussion
- create a new `seed` mechanism card
- save it under the resolved vault root at `学习/Cards/Mechanisms`
- add conservative backlinks to existing cards

Prompt template:

```text
Use $obsidian-mechanism-card-capture to capture one mechanism from this thread.
Mechanism title: <single mechanism>
Keywords or thread points to capture: <keywords or short excerpts>
Domain: <domain>
Subdomain: <optional subdomain>
Source: <optional source>
Vault root: <optional vault path>
```

### `obsidian-method-card-capture`

Skill for turning the current thread into exactly one Obsidian Method Card.

Path:

- `skills/obsidian-method-card-capture/`

Use this entry when you want to:

- capture one practical procedure or strategy from Q&A or discussion
- create a new `seed` method card
- save it under the resolved vault root at `学习/Cards/Methods`
- add conservative backlinks to existing cards

Prompt template:

```text
Use $obsidian-method-card-capture to capture one method from this thread.
Method title: <single method>
Keywords or thread points to capture: <keywords or short excerpts>
Domain: <domain>
Subdomain: <optional subdomain>
Source: <optional source>
Vault root: <optional vault path>
```

### `obsidian-misconception-card-capture`

Skill for turning the current thread into exactly one Obsidian Misconception Card.

Path:

- `skills/obsidian-misconception-card-capture/`

Use this entry when you want to:

- capture one mistaken claim or recurring error pattern from Q&A or discussion
- create a new `seed` misconception card
- save it under the resolved vault root at `学习/Cards/Misconceptions`
- add conservative backlinks to existing cards

Prompt template:

```text
Use $obsidian-misconception-card-capture to capture one misconception from this thread.
Misconception title: <single misconception>
Keywords or thread points to capture: <keywords or short excerpts>
Domain: <domain>
Subdomain: <optional subdomain>
Source: <optional source>
Vault root: <optional vault path>
```

## Suggested Workflow

1. Copy `cross-platform-skill-template/` to a new skill folder.
2. Rename the placeholder skill name in each wrapper.
3. Rewrite `core/guide.md` with the real workflow.
4. Add only the references, scripts, and assets you actually need.
5. Validate each platform wrapper separately.

## Collection Direction

As this repository grows, this index should remain the first place to look for:

- stable skills
- starter templates
- platform-specific variants
