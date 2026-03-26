# Render Script

## Purpose

Use `scripts/render_misconception_card.py` to make misconception card structure deterministic.

The agent should still synthesize the content, but the final markdown layout
should be rendered by the script whenever practical.

## Script Path

- `scripts/render_misconception_card.py`

## Input Model

The script expects a JSON file passed with `--spec`.

Minimum required fields:

- `title`
- `domain`

Useful optional top-level fields:

- `subdomain`
- `source`
- `status`
- `confidence`
- `created`
- `updated`
- `id`
- `tags`
- `related`
- `aliases`

Optional `sections` object keys:

- `mistaken_claim`
- `why_it_seems_plausible`
- `why_it_is_wrong`
- `correct_understanding`
- `what_it_confuses`
- `representative_counterexamples`
- `trigger_signals`
- `corrective_action`
- `related_cards_section`
- `current_status_notes`
- `next_goal`
- `growing_checklist`
- `stable_checklist`
- `expert_ready_checklist`
- `current_upgrade_tasks`
- `upgrade_history`

Each section value may be:

- a string
- a list of strings

## Usage

Render to stdout:

```powershell
python scripts/render_misconception_card.py --spec misconception.json
```

Render directly to a card file:

```powershell
python scripts/render_misconception_card.py --spec misconception.json --output "C:\path\to\Card.md"
```

## Rules

- Prefer the script for new card creation when the content has already been synthesized.
- For updates, use the script only if it helps preserve deterministic layout without clobbering existing content.
- Do not treat the script as the source of truth for semantic decisions. The agent still decides what content belongs in each section.
