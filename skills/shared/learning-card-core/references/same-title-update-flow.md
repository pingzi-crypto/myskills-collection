# Same-Title Update Flow

## Goal

Handle same-title learning cards safely.

This flow exists to prevent:

- duplicate cards for the same topic
- silent overwrites
- unnecessary resets of card maturity

## Trigger

Use this flow when a same-title card already exists in the resolved card-type
directory.

The exact path shape is defined by the local card-type spec.

## User Confirmation

Before editing the existing card:

- tell the user the card already exists
- show the existing path
- ask whether they want to update the existing card

If the user does not confirm:

- stop
- do not create a duplicate file
- do not modify the existing file

## Read Before Edit

Before updating:

- read the entire existing card
- identify which sections already have content
- identify what the current thread adds that is genuinely new

## Merge Rules

When updating an existing card:

- preserve `id`
- preserve `title`
- preserve `type`
- preserve `created`
- update `updated`
- keep `status` unchanged unless the user explicitly wants a promotion
- review `graph_maturity` separately from `status`
- keep `confidence` unchanged unless the user explicitly wants a revision
- keep existing `aliases` unless there is a clear new alias
- keep existing `related` links unless there is a strong new relationship

## Content Rules

Add or refine only what the new thread materially improves.

The exact section priorities are type-specific, but the family-wide rule is:

- merge targeted improvements
- do not rewrite the whole card if only one or two sections need improvement

## Status Handling

Default rule:

- existing `status` wins

Only change status when:

- the user explicitly asks for a promotion or downgrade
- the update is specifically about advancing the card maturity

Do not auto-promote from `seed` to `growing` just because more content was
added.

When the update is explicitly about maturity:

- use `Promotion Assessment` to record whether the card is worth promoting
- prefer `watchlist` or `stay stable` over optimistic promotion when evidence is
  incomplete
- do not claim `expert-ready` unless strong rule-level dispatch statements were
  added

## Related Links Handling

When updating related links:

- prefer preserving existing links
- add only strong new links
- do not replace stable links with speculative ones

## Output Expectations

After an update, report:

1. that an existing card was updated
2. the file path
3. which sections changed
4. whether the card was promoted, watchlisted, or kept stable
5. any ambiguity that still remains
