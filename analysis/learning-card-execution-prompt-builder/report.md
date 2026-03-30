# Learning Card Execution Prompt Builder Report

## Goal

Provide one small shared utility that turns router results into a ready-to-fill
execution-skill prompt skeleton.

This is a product-facing bridge between:

- router classification
- downstream execution prompt construction

## Added Utility

Script:

- `skills/shared/learning-card-core/scripts/build_execution_prompt.py`

Use it when:

- the router has already chosen card type and mode
- you want a faster next-step execution prompt
- you do not want to manually rewrite the downstream skill template every time

## Covered Shapes

- `create`
- `update`
- `promotion review`

Supported card types:

- `concept`
- `mechanism`
- `method`
- `misconception`

## Example Commands

Concept create:

```powershell
python skills/shared/learning-card-core/scripts/build_execution_prompt.py `
  --card-type concept `
  --mode create `
  --capture-anchor "windows系统有自带的截图功能吗？如果有快捷键是什么 -> first assistant reply after it" `
  --title "Windows 自带截图方式" `
  --point "Windows 自带多种截图方式" `
  --point "Print Screen" `
  --point "Win + Shift + S" `
  --domain "Windows Workflow" `
  --vault-root "C:\Users\pz\Documents\Obsidian Vault"
```

Method update:

```powershell
python skills/shared/learning-card-core/scripts/build_execution_prompt.py `
  --card-type method `
  --mode update `
  --existing-card "Learning Card Routing" `
  --point "把 router 的问题改成中英双语" `
  --vault-root "C:\Users\pz\Documents\Obsidian Vault"
```

Misconception promotion review:

```powershell
python skills/shared/learning-card-core/scripts/build_execution_prompt.py `
  --card-type misconception `
  --mode "promotion review" `
  --existing-card "More Cards Means Better Learning" `
  --point "当前线程在评估 expert-ready 条件" `
  --vault-root "C:\Users\pz\Documents\Obsidian Vault"
```

## Output Artifacts

- `analysis/learning-card-execution-prompt-builder/outputs/concept-create.txt`
- `analysis/learning-card-execution-prompt-builder/outputs/method-update.txt`
- `analysis/learning-card-execution-prompt-builder/outputs/misconception-review.txt`
- `analysis/learning-card-execution-prompt-builder/outputs/manifest.json`

## Observed Result

- the shared builder can produce a ready-to-fill execution prompt for all three
  common mode shapes
- create output includes title, keywords, domain, subdomain, source, and vault
  root slots
- update output includes existing card, merge points, source, and vault root
- promotion-review output includes existing card, promotion evidence, source,
  and vault root
- the builder is useful when the router has already classified the thread but
  the operator still needs a fast next-step execution prompt

## Output Artifact Hashes

- `concept-create.txt`
  - `FADF48481D8DE87C022FC17518D15874AF9F1782EB3663BE1BDC0E6D698AB044`
- `method-update.txt`
  - `468456DBC27A09CD524BBCE248A1B358E1C278989F14B12878B855CE716EE319`
- `misconception-review.txt`
  - `20B45551C2142B17D0150A3E3375FB726EC91589C83F08A889E488CE7451BDBB`
