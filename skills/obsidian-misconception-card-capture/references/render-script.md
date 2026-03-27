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
- `graph_maturity`
- `confidence`
- `created`
- `updated`
- `id`
- `tags`
- `related`
- `aliases`
- `review_cycle`

Optional `sections` object keys:

- `mistaken_claim`
- `why_it_seems_plausible`
- `why_it_is_wrong`
- `correct_understanding`
- `what_it_confuses`
- `representative_counterexamples`
- `trigger_signals`
- `corrective_action`
- `local_position`
- `operational_links`
- `routing_and_dispatch`
- `current_status_notes`
- `next_goal`
- `growing_checklist`
- `stable_checklist`
- `expert_ready_checklist`
- `promotion_assessment`
- `current_upgrade_tasks`
- `upgrade_history`

Each section value may be:

- a string
- a list of strings
- a dictionary for structured graph or promotion sections

For `routing_and_dispatch`, prefer a dictionary with:

- `direct_routes`
- `secondary_routes`
- `gap_signals`
- `stop_rules`

Read `../../references/routing-and-dispatch-spec.md` for the shared structure.

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
- Use stage-aware rendering:
  - `seed` may hide empty high-stage sections
  - `stable` should expose graph structure and a lean progression summary
  - `stable` should default to `Routing and Dispatch > Direct Routes` only
  - `expert-ready` should expose the full `Routing and Dispatch` layer and promotion assessment gaps
  - `expert-ready` should expose missing sub-blocks inside `Routing and Dispatch`

## Lean Stable Render

For default `stable` cards, prefer a slimmer render:

- keep the misconception correction layer
- keep `Knowledge Graph Relations > Local Position`
- keep `Knowledge Graph Relations > Operational Links`
- keep only `Routing and Dispatch > Direct Routes`
- collapse progression notes into one compact `Upgrade Focus` block

Do not keep these as always-on default sections for `stable` renders:

- `Growing Checklist`
- `Stable Checklist`
- `Expert-Ready Checklist`
- `Upgrade History`
- expanded multi-block promotion scaffolding
