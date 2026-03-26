# myskills-collection

Cross-platform skill templates plus a progression-capable Obsidian learning-card
skill family for Codex-style workflows.

## What This Repo Contains

This repository currently has two main parts:

- a starter template for building one skill that can be adapted across three platforms
- a concrete Obsidian learning-card skill family with routing, deterministic rendering, and progression rules

Browse the collection here:

- `skills/README.md`

## Quick Start

The fastest way to start depends on what you want to do.

### Option 1: Start from the template

Use this when you want to create a new reusable skill.

1. Copy `skills/cross-platform-skill-template/` to a new folder with your real skill name.
2. Rewrite `core/guide.md` with the actual workflow.
3. Keep shared logic in `core/`.
4. Keep platform-specific metadata only in the wrapper folders.

### Option 2: Use the Obsidian learning-card family

Use this when you want to turn one thread into one Obsidian learning card.

1. Start with `skills/obsidian-learning-card-router/` if the card type is still unclear.
2. Route to exactly one execution skill:
   - `obsidian-concept-card-capture`
   - `obsidian-mechanism-card-capture`
   - `obsidian-method-card-capture`
   - `obsidian-misconception-card-capture`
3. Let that execution skill create, update, or run promotion review on one card.

### Simplest prompts

```text
Use $obsidian-learning-card-router to choose the right learning card skill and mode for this thread.
```

```text
Use $obsidian-concept-card-capture to work on one concept card from this thread.
Mode: create
Concept title: <single concept>
Keywords or thread points to capture: <keywords>
Domain: <domain>
```

## Main Entries

### Cross-platform template

Use this when you want one shared skill core with thin wrappers for:

- Codex
- Claude Code
- OpenClaw

Path:

- `skills/cross-platform-skill-template/`

Design rule:

> Keep reusable task logic in a shared core, and keep platform-specific behavior in thin wrappers.

### Obsidian learning-card skill family

Use this when you want to capture, update, or promote one Obsidian learning card
from a thread.

The family includes:

- `obsidian-learning-card-router`
- `obsidian-concept-card-capture`
- `obsidian-mechanism-card-capture`
- `obsidian-method-card-capture`
- `obsidian-misconception-card-capture`

Shared references:

- `skills/references/progression-protocol.md`
- `skills/references/knowledge-graph-relations.md`
- `skills/references/learning-card-skill-family.md`

## Obsidian Family Model

The learning-card family uses a two-layer workflow:

1. the router chooses the card type and action mode
2. one execution skill performs the actual create, update, or promotion work

The router decides:

- `concept | mechanism | method | misconception`
- `create | update | promotion review`

The execution skills handle:

- single-card boundaries
- deterministic card rendering
- duplicate detection and safe update flow
- graph structure
- progression evidence
- promotion assessment

## Progression Model

The four execution skills share the same maturity ladder:

- `seed`
- `growing`
- `stable`
- `expert-ready`

They also share a graph-maturity ladder:

- `none`
- `weak`
- `local`
- `dispatchable`

Operational meaning:

- `stable` means the card is a reliable local node
- `expert-ready` means the card has real routing or dispatch value

Not every card should become `expert-ready`.

## Repository Structure

```text
skills/
  cross-platform-skill-template/
    core/
      guide.md
      references/
      scripts/
      assets/
    codex/
      SKILL.md
      agents/openai.yaml
    claude/
      SKILL.md
    openclaw/
      SKILL.md
  obsidian-learning-card-router/
  obsidian-concept-card-capture/
  obsidian-mechanism-card-capture/
  obsidian-method-card-capture/
  obsidian-misconception-card-capture/
  references/
```

## Recommended Use

For new skills:

1. start from `skills/cross-platform-skill-template/`
2. keep shared workflow in `core/`
3. keep platform-specific behavior in wrappers

For Obsidian card capture:

1. use `obsidian-learning-card-router` when the card type is still unclear
2. route to exactly one execution skill
3. let that skill create, update, or run promotion review on one card

## Notes

- This repository now contains both templates and real skills.
- Shared references should stay shared when they express family-wide rules.
- Local references should be added only when a card type genuinely needs specialized logic.
