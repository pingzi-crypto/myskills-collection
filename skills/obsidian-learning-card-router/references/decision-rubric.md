# Decision Rubric

## Goal

Classify one thread into one dominant learning card type.

When a capture anchor has already been selected, classify the anchored content
instead of the entire thread by default.

The available targets are:

- `$obsidian-concept-card-capture`
- `$obsidian-mechanism-card-capture`
- `$obsidian-method-card-capture`
- `$obsidian-misconception-card-capture`

## Primary Decision Question

Ask:

> 这段内容主要在回答什么问题？
> What is this thread mainly trying to answer?

If the user already answered with one of these exact labels:

- `概念`
- `机制`
- `方法`
- `误解`

route directly without reopening the broader question.

## Routing Table

### Concept

Use when the thread mainly answers:

- What is it?
- What does this term mean?
- What is its essence?
- How is it different from related concepts?

Route to:

- `$obsidian-concept-card-capture`

### Mechanism

Use when the thread mainly answers:

- Why does it happen?
- How does it work?
- What variables or causal chain explain the result?

Route to:

- `$obsidian-mechanism-card-capture`

### Method

Use when the thread mainly answers:

- How do I do it?
- What procedure should I follow?
- When should I use this method instead of another one?

Route to:

- `$obsidian-method-card-capture`

### Misconception

Use when the thread mainly answers:

- What is the mistaken claim?
- Why does it look plausible?
- Why is it wrong?
- How should it be corrected?

Route to:

- `$obsidian-misconception-card-capture`

## Existing Card Override

If the task clearly targets an existing card:

- preserve that card's current type by default
- route to the same downstream skill
- do not reclassify unless the user is explicitly fixing a wrong card type

Examples:

- updating an existing `Mechanism` card stays `Mechanism`
- promoting an existing `Method` card stays `Method`

## Tie-Breaking Rules

When a thread contains signals from more than one card type:

1. Prefer the type that dominates the thread's center of gravity.
2. Prefer the type that has the clearest single-card boundary.
3. Prefer one card now and let sibling cards emerge later if needed.
4. If an existing card is already in scope, prefer preserving its type over speculative rerouting.

Do not default to:

- creating all four card types
- routing to multiple skills at once

## Examples

### Example 1

Thread focus:

- defining what a term means
- clarifying boundaries

Route to:

- `$obsidian-concept-card-capture`

### Example 2

Thread focus:

- explaining a feedback loop
- identifying core variables
- describing a causal chain

Route to:

- `$obsidian-mechanism-card-capture`

### Example 3

Thread focus:

- describing a reusable procedure
- comparing it against alternatives

Route to:

- `$obsidian-method-card-capture`

### Example 4

Thread focus:

- correcting a recurring mistaken belief
- explaining why that belief is attractive but false

Route to:

- `$obsidian-misconception-card-capture`

### Example 5

Thread focus:

- deciding whether an existing stable card deserves stronger graph structure
- reviewing routing rules or promotion evidence

Route to:

- the existing card's current type

## Clarification Rule

If the dominant type is still unclear, ask one short question that forces a choice between:

- definition
- mechanism
- method
- misconception

For Chinese-first routing, prefer:

> 这段内容你最想记录的是？概念，机制，方法还是误解，请用这一组词中的一个回复。
> What do you most want to record from this content: concept, mechanism, method, or misconception? Please reply with exactly one of those labels.

Example:

> 这段内容你主要想记录：这是什么、为什么会这样、具体怎么做，还是哪里错了？
> Do you mainly want to capture what it is, why it works, how to do it, or what the mistake is?
