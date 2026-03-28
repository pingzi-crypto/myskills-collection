# Obsidian Learning Card Family

This document gives one place to understand the learning-card skill family in this repository.

## Family Structure

### Router

- `obsidian-learning-card-router`

Use this first when the card type is still unclear.

Its only job is to classify a thread into one of these four execution skills:

- `obsidian-concept-card-capture`
- `obsidian-mechanism-card-capture`
- `obsidian-method-card-capture`
- `obsidian-misconception-card-capture`

### Execution Skills

- `obsidian-concept-card-capture`
  Creates one Concept Card
- `obsidian-mechanism-card-capture`
  Creates one Mechanism Card
- `obsidian-method-card-capture`
  Creates one Method Card
- `obsidian-misconception-card-capture`
  Creates one Misconception Card

### Shared Core

- `skills/shared/learning-card-core/`

This layer stores family-wide procedural rules such as:

- vault-path protocol
- same-title update flow
- deterministic render protocol

This shared layer does not replace the four execution skills.

## Decision Model

Route based on the dominant question in the thread:

- "What is it?" -> Concept
- "Why does it work?" -> Mechanism
- "How do I do it?" -> Method
- "What is the mistake?" -> Misconception

The default rule is:

> create one best-fit card, not all four card types at once

## Shared Design Principles

All four execution skills share the same design constraints:

- create exactly one card per run
- start new cards at `seed`
- resolve `VAULT_ROOT` before reading or writing
- use duplicate detection before creating a new file
- use an update flow instead of silent overwrite
- prefer deterministic render scripts for new cards
- add backlinks conservatively

## Vault Paths

Once `VAULT_ROOT` is resolved, the four default destinations are:

- Concept -> `学习/Cards/Concepts`
- Mechanism -> `学习/Cards/Mechanisms`
- Method -> `学习/Cards/Methods`
- Misconception -> `学习/Cards/Misconceptions`

## Suggested Usage Order

### When the type is unclear

1. Use `obsidian-learning-card-router`
2. Let it choose the dominant card type
3. Hand off to the selected execution skill

### When the type is already clear

Call the matching execution skill directly.

## Recommended Prompt Pattern

### Router

```text
Use $obsidian-learning-card-router to choose the right learning card skill for this thread.
Goal: create exactly one card from the current discussion.
If the type is ambiguous, ask one short clarification question.
```

### Direct execution

```text
Use $obsidian-concept-card-capture to capture one concept from this thread.
Concept title: <single concept>
Keywords or thread points to capture: <keywords or short excerpts>
Domain: <domain>
Subdomain: <optional subdomain>
Source: <optional source>
Vault root: <optional vault path>
```

Swap the skill name and title field for mechanism, method, or misconception.

## Why This Family Exists

This family is designed to avoid two common failures:

- using one overly broad skill for all card types
- creating all four card types by default for every topic

The system stays cleaner when routing and writing are separated.
