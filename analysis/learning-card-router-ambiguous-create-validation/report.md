# Learning Card Router Ambiguous Create Validation Report

## Scope

Validation target:

- branch `codex/learning-card-spec-validation`
- one ambiguous thread with no explicit target card already in scope
- router-led card-type selection before real create-path execution

Date:

- `2026-03-30`

## Controlled Thread Shape

Source fragment shape:

- user asks whether a skill already loaded in Codex App means compatibility work
  for Claude Code and OpenClaw is no longer needed
- no existing card path is named
- no card type label is supplied up front

Observed ambiguity:

- the thread touches compatibility, platform behavior, and workflow design
- it could superficially look like a concept, a method, or a misconception

## Router Decision

Capture anchor:

- current-session question about whether Codex-visible loading means cross-host
  compatibility work is already complete

Route result:

- `Misconception`

Mode:

- `create`

Downstream skill:

- `$obsidian-misconception-card-capture`

Reason:

- the anchored content mainly required correction of a mistaken inference, not a
  neutral definition or a step-by-step procedure

## Planned Write Target

Expected vault root:

- `C:\Users\pz\Documents\Obsidian Vault`

Expected output path:

- `C:\Users\pz\Documents\Obsidian Vault\学习\Cards\Misconceptions\Skill 已在 Codex 加载不等于 Claude Code 和 OpenClaw 兼容已完成.md`

Duplicate check expectation:

- same-title file should not already exist before creation

## Actual Write Result

Observed outcome:

- pass

Verified:

- the router decision led to a real create-path write under the Misconceptions
  directory
- the created file path was
  `C:\Users\pz\Documents\Obsidian Vault\学习\Cards\Misconceptions\Skill 已在 Codex 加载不等于 Claude Code 和 OpenClaw 兼容已完成.md`
- no existing same-title card was overwritten
- exactly one matching file exists after creation
- the new note frontmatter shows `type: misconception`, `status: seed`, and
  `graph_maturity: none`
- the rendered body preserved bilingual `中文 + English translation` content
- the write confirmed that a thread without an explicit target card can still be
  routed to one dominant execution skill before file creation
- the validation also exposed and then fixed one renderer bug where missing
  optional progression fields could emit an empty placeholder line

## Assessment

This closes the main remaining Route 3 validation gap for the learning-card
family:

- explicit existing-card update path -> already validated
- existing-card promotion-review path -> already validated
- ambiguous no-card-in-scope create path -> now validated with a real write

Current confidence:

- the router can preserve an existing card when one is already in scope
- the router can also classify an ambiguous thread and select one downstream
  skill before first creation
