---
name: obsidian-learning-card-router
description: Route the current thread to the right Obsidian learning card skill. Use when the user wants to capture one learning card from a thread but it is not yet clear whether the content should become a Concept, Mechanism, Method, or Misconception card.
---

# Obsidian Learning Card Router

## Overview

Decide which one of the four Obsidian card skills should handle the current thread:

- `$obsidian-concept-card-capture`
- `$obsidian-mechanism-card-capture`
- `$obsidian-method-card-capture`
- `$obsidian-misconception-card-capture`

This skill is intentionally a router, not a writer. It decides the card type and hands off to the correct card skill.

Read [references/decision-rubric.md](references/decision-rubric.md) before routing.

## Routing Goal

Use this skill when:

- the user wants to turn the current thread into one learning card
- the correct card type is not obvious yet
- you need to classify the thread before creating anything

Do not use this skill when:

- the correct card type is already clear
- the user explicitly asked for one known card type
- the user wants multiple cards in one pass

## Routing Workflow

1. Confirm that the task is to create exactly one learning card.
2. Identify what the thread is mainly answering.
3. Classify the thread into one of the four card types using [references/decision-rubric.md](references/decision-rubric.md).
4. If the thread contains multiple possible card types, choose the strongest primary one instead of trying to split immediately.
5. Explain the routing decision in one short sentence.
6. Hand off to the selected card skill.

## Routing Questions

Ask this question first:

> What is the thread mainly trying to answer?

Route based on the answer:

- "What is it?" -> `$obsidian-concept-card-capture`
- "Why does it work?" -> `$obsidian-mechanism-card-capture`
- "How do I do it?" -> `$obsidian-method-card-capture`
- "Where is the mistake?" -> `$obsidian-misconception-card-capture`

## Decision Rules

- Prefer one dominant card type over mixed classification.
- If the thread contains several weak signals, choose the one with the clearest usable card shape.
- Do not create or recommend all four card types at once by default.
- If ambiguity remains high, ask one short clarification question before routing.

## Output Expectations

When executing this skill, produce:

1. The selected card type.
2. The reason for the choice in one short sentence.
3. The exact downstream skill to use next.
4. If needed, one clarification question before handoff.

## Handoff Template

After deciding, hand off in this format:

```text
Route result: <Concept | Mechanism | Method | Misconception>
Use $<target-skill> for the next step.
Reason: <one-sentence rationale>
```

## References

- Read [references/decision-rubric.md](references/decision-rubric.md) for the classification rules and examples.
