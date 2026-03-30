# Routing Modes

## Goal

Distinguish whether the downstream card skill should create a new card,
update an existing card, or run a progression review.

## Available Modes

- `create`
- `update`
- `promotion review`

## Create

Use `create` when:

- the user wants to capture a new learning card
- the user selects one fragment from the current session to preserve
- no same-title card is already in scope
- the main question is first-time capture rather than maturity review

Signals:

- "turn this into a card"
- "create a card for this"
- "record this thread"
- "保存成卡片"
- "记录这段内容"

## Update

Use `update` when:

- an existing card is already named, linked, or opened
- the user wants to add or refine content
- the focus is not mainly on progression status

Signals:

- "update this card"
- "merge this thread into the existing card"
- "补充这张卡"

## Promotion Review

Use `promotion review` when:

- the task is explicitly about `seed`, `growing`, `stable`, or `expert-ready`
- the user wants stronger graph structure, routing rules, or maturity assessment
- the thread is mainly deciding whether an existing card should stay stable, be watchlisted, or be promoted

Signals:

- "should this be stable or expert-ready"
- "promote this card"
- "add routing and dispatch"
- "review the progression"

## Existing Card Priority

If an existing card is explicitly in scope:

- prefer `update` or `promotion review`
- do not route to `create` unless the user explicitly wants a separate sibling card

## Output Rule

Always hand off with both:

- capture anchor
- card type
- action mode

And always make the execution boundary explicit:

- routing alone did not write any card file yet
- the user still needs the downstream execution skill to actually create,
  update, or review the card

And always include the minimum execution package:

- resolved capture anchor
- selected card type
- selected action mode
- downstream execution skill
- any still-missing write inputs that must be collected before execution

Mode-specific minimum follow-up:

- `create`: if title, keywords, domain, or vault root are still missing, say so
- `update`: if the target existing card is not explicit yet, say that the
  downstream skill still needs the existing card path or title confirmation
- `promotion review`: if the target existing card is not explicit yet, say that
  the downstream skill still needs the existing card path or title confirmation

Examples:

- `Concept + create`
- `Mechanism + update`
- `Method + promotion review`
