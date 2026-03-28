# myskills-collection

Progression-capable Obsidian learning-card skills with a Codex runtime layout
and exportable wrappers for Claude Code and OpenClaw.

## What This Repo Contains

This repository contains one main skill family:

- a concrete Obsidian learning-card skill family with routing, deterministic rendering, and progression rules

Browse the collection here:

- `skills/README.md`

## Quick Start

The fastest way to start is to use the Obsidian learning-card family.
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

## Main Entry

### Obsidian learning-card skill family

Use this when you want to capture, update, or promote one Obsidian learning card
from a thread.

The family includes:

- `obsidian-learning-card-router`
- `obsidian-concept-card-capture`
- `obsidian-mechanism-card-capture`
- `obsidian-method-card-capture`
- `obsidian-misconception-card-capture`

Each skill includes:

- a root `SKILL.md` under `skills/` used by Codex
- exportable wrappers for Claude Code under `dist/claude/`
- exportable wrappers for OpenClaw under `dist/openclaw/`

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
  obsidian-learning-card-router/
    SKILL.md
  obsidian-concept-card-capture/
    SKILL.md
  obsidian-mechanism-card-capture/
    SKILL.md
  obsidian-method-card-capture/
    SKILL.md
  obsidian-misconception-card-capture/
    SKILL.md
  references/
dist/
  claude/
    obsidian-learning-card-router/SKILL.md
    obsidian-concept-card-capture/SKILL.md
    ...
  openclaw/
    obsidian-learning-card-router/SKILL.md
    obsidian-concept-card-capture/SKILL.md
    ...
```

## Recommended Use

For Obsidian card capture:

1. use `obsidian-learning-card-router` when the card type is still unclear
2. route to exactly one execution skill
3. let that skill create, update, or run promotion review on one card

## Notes

- This repository now contains only the real learning-card skills, not a starter template.
- `skills/` is the Codex runtime directory and should stay free of extra platform wrappers.
- `dist/claude/` and `dist/openclaw/` are export surfaces, not Codex runtime entrypoints.
- Shared references should stay shared when they express family-wide rules.
- Local references should be added only when a card type genuinely needs specialized logic.
