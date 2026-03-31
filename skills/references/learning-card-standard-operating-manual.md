# Learning Card Standard Operating Manual

## Goal

Provide one short operator-facing manual for the three most common learning-card
flows:

- create
- update
- promotion review

Use this as the quickest practical guide when you do not want to re-read the
full skill family docs.

## Core Rule

Always distinguish these two layers:

1. router output proves classification only
2. execution skill output proves that a card file was actually created, updated,
   or reviewed

If you still see `Router status: routing complete only`, no card file exists
yet.

## Flow 1: Create

Use when:

- the content should become a new card
- no existing card is already in scope

Step 1: Router

Ask the router to classify the thread if the type is still ambiguous.

Expected router result shape:

```text
Route result: <Concept | Mechanism | Method | Misconception>
Mode: create
Router status: routing complete only. No card file has been created or updated yet.
Execution package confirmed:
- Capture anchor: ...
- Card type: ...
- Mode: create
- Downstream skill: ...
Still needed before write:
- title
- keywords or thread points
- domain
- vault root
Suggested reply: 继续创建
```

Step 2: Execution skill

Call the routed execution skill and fill the missing write inputs:

- title
- keywords or thread points
- domain
- vault root

Expected execution result shape:

```text
<Card type> captured: <title>
Created file: <path>
Summary: <what was extracted>
```

Trust `Created file:` as the proof that the note was actually written.

## Flow 2: Update

Use when:

- an existing card should absorb new material
- the task is not mainly about maturity review

Step 1: Router

Expected router result shape:

```text
Mode: update
Router status: routing complete only. No card file has been created or updated yet.
Execution package confirmed:
- Capture anchor: ...
- Card type: ...
- Mode: update
- Downstream skill: ...
Still needed before write:
- existing card title or path confirmation
- vault root
Suggested reply: 继续更新
```

Step 2: Execution skill

Call the routed execution skill with:

- existing card title or path
- new thread points to merge
- vault root

Expected execution result shape:

```text
<Card type> updated: <title>
Updated file: <path>
Summary: <what changed>
```

Trust `Updated file:` as the proof that the note was actually modified.

## Flow 3: Promotion Review

Use when:

- the task is about `seed / growing / stable / expert-ready`
- the thread is mainly deciding whether a card should stay stable, move to
  watchlist, or be promoted

Step 1: Router

Expected router result shape:

```text
Mode: promotion review
Router status: routing complete only. No card file has been created or updated yet.
Execution package confirmed:
- Capture anchor: ...
- Card type: ...
- Mode: promotion review
- Downstream skill: ...
Still needed before write:
- existing card title or path confirmation
- vault root
Suggested reply: 继续评审
```

Step 2: Execution skill

Call the routed execution skill with:

- existing card title or path
- promotion evidence from the thread
- vault root

Expected execution result shape:

```text
Reviewed file: <path>
Promotion result: <promoted | watchlist | stay stable>
Summary: <why>
```

Trust `Reviewed file:` plus `Promotion result:` as the proof that the review was
actually performed.

## Fast Decision Table

- If type is unclear: use `obsidian-learning-card-router` first.
- If router output still says `routing complete only`: the card does not exist
  yet.
- If you see `Created file:`: new card write completed.
- If you see `Updated file:`: existing card update completed.
- If you see `Reviewed file:`: promotion review completed.

## Minimal Operator Checklist

Before you stop, verify:

- the router has identified exactly one card type
- the mode is one of `create / update / promotion review`
- the execution skill has actually run
- the output contains a file-level result line

If the file-level result line is missing, treat the task as not finished yet.

## Optional Helpers

If you already know card type and mode explicitly, use:

- `skills/shared/learning-card-core/scripts/build_execution_prompt.py`

If you want to reuse the router handoff text directly, use:

- `skills/shared/learning-card-core/scripts/build_execution_prompt_from_handoff.py`

Example:

```powershell
python skills/shared/learning-card-core/scripts/build_execution_prompt_from_handoff.py `
  --handoff-file analysis/learning-card-handoff-parser/inputs/concept-create-handoff.txt
```

Fastest operator path on Windows:

```powershell
pwsh -File skills/shared/learning-card-core/scripts/use_handoff_bridge.ps1
```

That flow lets you copy the router handoff block, run one command, and paste the
generated execution prompt directly into the next turn.

If you want stdout only and do not want to overwrite the clipboard:

```powershell
pwsh -File skills/shared/learning-card-core/scripts/use_handoff_bridge.ps1 `
  -PrintOnly
```

This reduces manual prompt rewriting between router output and execution skill.

Acceptance reference:

- `analysis/learning-card-operator-bridge-acceptance/report.md`
- `analysis/learning-card-execution-result-acceptance/report.md`
