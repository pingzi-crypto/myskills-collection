---
name: obsidian-learning-card-router
description: Route the current thread to the right Obsidian learning card skill and action mode. Use when the user wants to capture, update, or promote one learning card from a thread but it is not yet clear whether the content should become a Concept, Mechanism, Method, or Misconception card, or whether the task is new capture, update, or progression review.
---

# Obsidian Learning Card Router

## Overview

Decide which one of the four Obsidian card skills should handle the current thread:

- `$obsidian-concept-card-capture`
- `$obsidian-mechanism-card-capture`
- `$obsidian-method-card-capture`
- `$obsidian-misconception-card-capture`

This skill is intentionally a router, not a writer. It decides:

- the card type
- the action mode
- the correct downstream skill

Read these before routing:

- [../references/learning-card-skill-family.md](../references/learning-card-skill-family.md)
- [references/decision-rubric.md](references/decision-rubric.md)
- [references/routing-modes.md](references/routing-modes.md)

## Routing Goal

Use this skill when:

- the user wants to turn the current thread into one learning card
- or refine one existing learning card
- the correct card type is not obvious yet
- you need to classify the thread before creating, updating, or promoting anything

Do not use this skill when:

- the correct card type is already clear
- the user explicitly asked for one known card type
- the user wants multiple cards in one pass

## Routing Workflow

1. Confirm that the task is still about exactly one learning card boundary.
2. Identify the action mode using [references/routing-modes.md](references/routing-modes.md):
   - `create`
   - `update`
   - `promotion review`
3. If the task clearly targets an existing card, preserve that card's current type unless the user is explicitly correcting a wrong prior classification.
4. Identify what the thread is mainly answering.
5. Classify the thread into one of the four card types using [references/decision-rubric.md](references/decision-rubric.md).
6. If the thread contains multiple possible card types, choose the strongest primary one instead of trying to split immediately.
7. Explain the routing decision in one short sentence.
8. Hand off to the selected card skill with the mode attached.

## Routing Questions

Ask this question first when the thread center is unclear:

> What is the thread mainly trying to answer?

Route based on the answer:

- "What is it?" -> `$obsidian-concept-card-capture`
- "Why does it work?" -> `$obsidian-mechanism-card-capture`
- "How do I do it?" -> `$obsidian-method-card-capture`
- "Where is the mistake?" -> `$obsidian-misconception-card-capture`

Then ask or infer the second axis:

- Is this a new card?
- Is this improving an existing card?
- Is this specifically a progression or promotion review?

## Decision Rules

- Prefer one dominant card type over mixed classification.
- Prefer one action mode over vague blended intent.
- If the task is about strengthening an existing card, route to that card's existing type before inventing a new sibling card.
- If the thread contains several weak signals, choose the one with the clearest usable card shape.
- Do not create or recommend all four card types at once by default.
- If ambiguity remains high, ask one short clarification question before routing.

## Output Expectations

When executing this skill, produce:

1. The selected card type.
2. The selected mode:
   - `create`
   - `update`
   - `promotion review`
3. The reason for the choice in one short sentence.
4. The exact downstream skill to use next.
5. If needed, one clarification question before handoff.

## Handoff Template

After deciding, hand off in this format:

```text
Route result: <Concept | Mechanism | Method | Misconception>
Mode: <create | update | promotion review>
Use $<target-skill> for the next step.
Reason: <one-sentence rationale>
```

## References

- Read [../references/learning-card-skill-family.md](../references/learning-card-skill-family.md) for the system-level boundary between router and execution skills.
- Read [references/decision-rubric.md](references/decision-rubric.md) for the classification rules and examples.
- Read [references/routing-modes.md](references/routing-modes.md) for how to distinguish new capture, existing-card update, and progression review.
