# Mechanism Render Script

Read the shared render protocol first:

- [../../shared/learning-card-core/references/deterministic-render-protocol.md](../../shared/learning-card-core/references/deterministic-render-protocol.md)

## Script Path

- `scripts/render_mechanism_card.py`

## Local Section Keys

The renderer expects a JSON file passed with `--spec`.

Required top-level fields:

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

Supported `sections` keys:

- `phenomenon`
- `core_variables`
- `causal_chain`
- `key_prerequisites`
- `weakest_step`
- `alternative_explanations`
- `scope`
- `failure_boundaries`
- `supporting_evidence`
- `counter_cases`
- `compressed_explanation`
- `validation_question`
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

Read [../../references/routing-and-dispatch-spec.md](../../references/routing-and-dispatch-spec.md)
for the shared `routing_and_dispatch` structure.

## Usage

Render to stdout:

```powershell
python scripts/render_mechanism_card.py --spec mechanism.json
```

Render directly to a card file:

```powershell
python scripts/render_mechanism_card.py --spec mechanism.json --output "C:\path\to\Card.md"
```
