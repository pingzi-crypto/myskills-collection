# Capture Anchor Rule

## Goal

Select one concrete fragment from the current session before card-type routing begins.

This avoids treating the whole thread as the source body when the user really
only wants to preserve one local exchange.

## First Router Question

Ask this first when the user wants to save current-session content:

> 当前会话哪个片段想要保存成卡片？
> Which fragment from the current session do you want to save as a card?

The user may answer with:

- a direct quote from one user message
- a short paraphrase of the target user message
- a clear reference to one recent request in the session
- a start quote and end quote for a smaller block inside the anchored assistant reply

## Default Anchor Resolution

Unless the user explicitly asks for a broader span, resolve the capture anchor like this:

1. Use the selected `user message` as the anchor start.
2. Find the first `assistant message` that comes after that user message.
3. Use that first assistant message text as the primary source body for card creation.

This means the default preserved unit is:

- one user message
- the first assistant reply immediately after it

## Text-Block Anchor Override

If the user wants a smaller block inside the anchored assistant reply, allow a
text-block selection with:

- `start quote`
- `end quote`

Resolution order:

1. First resolve the normal anchor:
   - selected user message
   - first assistant reply after it
2. Then search inside that anchored assistant reply for the requested start quote and end quote.
3. Use the text span between those two quotes, inclusive by default, as the primary source body.

Use this override only when:

- the user clearly wants one local block rather than the whole assistant reply
- both quote boundaries can be found with high confidence

If only one boundary is clear, ask one short clarification question instead of
guessing a larger block.

## Example

If the user points to:

- `加一个功能，卡片内容默认 中文+英文翻译的 形式`

then the primary content body should default to the first assistant reply after it:

- the assistant message beginning with `这个功能已经加上了...`

That assistant reply becomes the main recording body for the downstream card
skill unless the user explicitly asks for a larger range.

If the user instead gives a start quote and end quote inside that reply, the
selected text block becomes the main recording body.

## Scope Rule

Prefer the anchored assistant reply over the entire thread when:

- the user wants to save one local exchange
- the thread contains several different topics
- later turns are mostly operational follow-up

Prefer the selected text block over the full anchored assistant reply when:

- the assistant reply contains several separable ideas
- the user explicitly wants only one subsection
- the chosen block already forms a coherent single-card boundary

Use a broader span only when the user clearly asks for:

- the whole thread
- multiple turns
- a merged summary across several exchanges

## Router Handoff Contract

When the anchor is resolved, pass these facts downstream:

- the selected user message
- the first assistant reply after it
- the selected text block when a start quote and end quote were provided
- the rule that the most specific resolved body is the primary source body

## Ambiguity Rule

If two candidate user messages still fit the user's description, ask one short
clarification question and do not guess across distant parts of the thread.
