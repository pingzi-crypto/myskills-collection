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

- the source fragment to preserve
- the card type
- the action mode
- the correct downstream skill

The router must explicitly tell the user when routing is finished but no card
file has been created or updated yet.

Read these before routing:

- [../references/learning-card-skill-family.md](../references/learning-card-skill-family.md)
- [references/capture-anchor-rule.md](references/capture-anchor-rule.md)
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

1. Ask which fragment from the current session should be preserved as the card source.
2. Resolve the capture anchor using [references/capture-anchor-rule.md](references/capture-anchor-rule.md).
3. Confirm that the task is still about exactly one learning card boundary.
4. Identify the action mode using [references/routing-modes.md](references/routing-modes.md):
   - `create`
   - `update`
   - `promotion review`
5. If the task clearly targets an existing card, preserve that card's current type unless the user is explicitly correcting a wrong prior classification.
6. Identify what the anchored content is mainly answering.
7. Classify the anchored content into one of the four card types using [references/decision-rubric.md](references/decision-rubric.md).
8. If the anchored content contains multiple possible card types, choose the strongest primary one instead of trying to split immediately.
9. Explain the routing decision in one short sentence.
10. Hand off to the selected card skill with the mode and anchor attached.
11. Explicitly state that routing alone did not create or update any card file.
12. Give one exact next-step instruction so the user knows how to continue into
    real card creation, update, or promotion review.

## Routing Questions

Ask this question first when the user wants to save part of the current session:

> 当前会话哪个片段想要保存成卡片？
> Which fragment from the current session do you want to save as a card?

If the user wants a smaller block inside one assistant reply, allow this follow-up:

> 如果你不是要整条回复，而是其中一段，请给我起始短句和结束短句。
> If you do not want the whole reply and only want one block inside it, give me a short start quote and end quote.

After the fragment is resolved, ask this next:

> 这段内容你最想记录的是？概念，机制，方法还是误解，请用这一组词中的一个回复。
> What do you most want to record from this content: concept, mechanism, method, or misconception? Please reply with exactly one of those labels.

Map those exact replies like this:

- `概念` -> `$obsidian-concept-card-capture`
- `机制` -> `$obsidian-mechanism-card-capture`
- `方法` -> `$obsidian-method-card-capture`
- `误解` -> `$obsidian-misconception-card-capture`

If the user replies with one of those four words, route immediately and do not
re-open the broader English question pattern.

Ask this older question only when the user did not choose one of the four labels
and the dominant type is still unclear:

> What is the thread mainly trying to answer?
> 这段内容主要在回答什么问题？

Route based on the answer:

- "这是什么？ / What is it?" -> `$obsidian-concept-card-capture`
- "为什么会这样？ / Why does it work?" -> `$obsidian-mechanism-card-capture`
- "具体怎么做？ / How do I do it?" -> `$obsidian-method-card-capture`
- "哪里错了？ / Where is the mistake?" -> `$obsidian-misconception-card-capture`

Then ask or infer the second axis:

- 这是新卡吗？ / Is this a new card?
- 这是在更新已有卡吗？ / Is this improving an existing card?
- 这是晋升评审吗？ / Is this specifically a progression or promotion review?

Default mode rule for current-session capture:

- if the user is saving a newly selected fragment and no existing card is already in scope, prefer `create`

## Decision Rules

- Prefer one dominant card type over mixed classification.
- Prefer one action mode over vague blended intent.
- Prefer the anchored assistant reply as the primary recording body instead of the whole thread unless the user clearly asks for a broader span.
- If the task is about strengthening an existing card, route to that card's existing type before inventing a new sibling card.
- If the thread contains several weak signals, choose the one with the clearest usable card shape.
- Do not create or recommend all four card types at once by default.
- If ambiguity remains high, ask one short clarification question before routing.

## Output Expectations

When executing this skill, produce:

1. The selected source fragment.
2. The selected card type.
3. The selected mode:
   - `create`
   - `update`
   - `promotion review`
4. The reason for the choice in one short sentence.
5. The exact downstream skill to use next.
6. An explicit status line saying routing is complete but no card file has been
   created or updated yet.
7. One exact next-step instruction for actual execution by the downstream
   skill.
8. If needed, one clarification question before handoff.

If the user replied with exactly one of `概念 / 机制 / 方法 / 误解`, immediately
route to the corresponding downstream skill and treat the anchored assistant
reply as the primary source body to record.

Do not stop with a handoff that sounds like a card already exists on disk when
the router only classified the thread.

## Handoff Template

After deciding, hand off in this format:

```text
Capture anchor: <selected user message -> first assistant reply after it>
Route result: <Concept | Mechanism | Method | Misconception>
Mode: <create | update | promotion review>
Use $<target-skill> for the next step.
Router status: routing complete only. No card file has been created or updated yet.
Next step: use $<target-skill> now to actually <create | update | review> the card.
Suggested reply: <继续创建 | 继续更新 | 继续评审>
Reason: <one-sentence rationale>
```

## References

- Read [../references/learning-card-skill-family.md](../references/learning-card-skill-family.md) for the system-level boundary between router and execution skills.
- Read [references/capture-anchor-rule.md](references/capture-anchor-rule.md) for how to select the preserved session fragment.
- Read [references/decision-rubric.md](references/decision-rubric.md) for the classification rules and examples.
- Read [references/routing-modes.md](references/routing-modes.md) for how to distinguish new capture, existing-card update, and progression review.
