# Learning Card Slimming Audit

This audit judges the four-card family under one assumption:

- target state: a default `stable` card render
- goal: keep high-retrieval, high-boundary, high-graph value content visible
- score rule: `8-10 = Must keep`, `5-7 = Optimize / stage-gate`, `0-4 = Redundant in default render`
- test method: fill one realistic sample for each card type, render it, then score each body section

## Summary

| Card Type | Sections | Must | Optimize | Redundant | Avg Score | Core Words | Graph Words | Progression Words | Reduction Opportunity |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Concept Card | 30 | 7 | 15 | 8 | 5.67 | 231 | 205 | 118 | 38.9% |
| Mechanism Card | 29 | 9 | 13 | 7 | 6.0 | 196 | 191 | 107 | 35.8% |
| Method Card | 30 | 9 | 14 | 7 | 6.0 | 230 | 171 | 99 | 35.9% |
| Misconception Card | 25 | 9 | 10 | 6 | 6.08 | 154 | 178 | 115 | 31.1% |

## Frontmatter Baseline

- Must keep: id, title, type, domain, status, graph_maturity, created, updated
- Keep but compress when possible: subdomain, source, tags, confidence, review_cycle
- Redundant by default: related, aliases

## Concept Card

Sample spec: `analysis\learning-card-slimming\samples\concept-single-card-boundary.json`
Rendered output: `analysis\learning-card-slimming\outputs\concept-single-card-boundary.md`

| Section | Layer | Score | Classification | Words | Items | Highest Overlap |
| --- | --- | ---: | --- | ---: | ---: | --- |
| `one_sentence_definition` | core | 10 | Must keep | 21 | 1 | examples (0.19) |
| `essence` | core | 9 | Must keep | 16 | 1 | promotion_assessment.missing_evidence (0.15) |
| `question_answered` | core | 9 | Must keep | 13 | 1 | examples (0.15) |
| `core_logic` | core | 8 | Must keep | 27 | 3 | one_sentence_definition (0.17) |
| `failure_boundaries` | core | 8 | Must keep | 25 | 2 | one_sentence_definition (0.18) |
| `examples` | core | 7 | Optimize / stage-gate | 22 | 1 | one_sentence_definition (0.19) |
| `why_it_matters` | core | 7 | Optimize / stage-gate | 18 | 2 | common_misunderstandings (0.12) |
| `confusions` | core | 6 | Optimize / stage-gate | 18 | 1 | growing_checklist (0.23) |
| `counter_examples` | core | 6 | Optimize / stage-gate | 23 | 1 | examples (0.18) |
| `prerequisites` | core | 6 | Optimize / stage-gate | 19 | 2 | promotion_assessment.main_reasons (0.22) |
| `common_misunderstandings` | core | 5 | Optimize / stage-gate | 12 | 1 | my_words (0.27) |
| `needs_validation` | core | 4 | Redundant in default render | 12 | 1 | promotion_assessment.missing_evidence (0.18) |
| `my_words` | core | 3 | Redundant in default render | 5 | 1 | common_misunderstandings (0.27) |
| `local_position` | graph | 8 | Must keep | 44 | 3 | routing_and_dispatch.direct_routes (0.16) |
| `operational_links` | graph | 8 | Must keep | 58 | 4 | routing_and_dispatch.secondary_routes (0.21) |
| `routing_and_dispatch.direct_routes` | graph | 7 | Optimize / stage-gate | 33 | 2 | counter_examples (0.16) |
| `routing_and_dispatch.gap_signals` | graph | 5 | Optimize / stage-gate | 26 | 1 | promotion_assessment.next_rules (0.15) |
| `routing_and_dispatch.secondary_routes` | graph | 5 | Optimize / stage-gate | 25 | 1 | operational_links (0.21) |
| `routing_and_dispatch.stop_rules` | graph | 5 | Optimize / stage-gate | 19 | 1 | one_sentence_definition (0.16) |
| `next_goal` | progression | 5 | Optimize / stage-gate | 8 | 1 | expert_ready_checklist (0.25) |
| `promotion_assessment.current_recommendation` | progression | 5 | Optimize / stage-gate | 1 | 1 | - (0.00) |
| `promotion_assessment.main_reasons` | progression | 5 | Optimize / stage-gate | 18 | 2 | current_status_notes (0.24) |
| `promotion_assessment.missing_evidence` | progression | 5 | Optimize / stage-gate | 14 | 1 | needs_validation (0.18) |
| `promotion_assessment.next_rules` | progression | 5 | Optimize / stage-gate | 13 | 1 | one_sentence_definition (0.18) |
| `current_upgrade_tasks` | progression | 4 | Redundant in default render | 10 | 1 | my_words (0.17) |
| `expert_ready_checklist` | progression | 4 | Redundant in default render | 14 | 2 | next_goal (0.25) |
| `current_status_notes` | progression | 3 | Redundant in default render | 14 | 1 | promotion_assessment.main_reasons (0.24) |
| `growing_checklist` | progression | 3 | Redundant in default render | 10 | 1 | confusions (0.23) |
| `stable_checklist` | progression | 3 | Redundant in default render | 11 | 2 | current_status_notes (0.09) |
| `upgrade_history` | progression | 2 | Redundant in default render | 5 | 1 | next_goal (0.08) |

- Must keep focus: `one_sentence_definition`, `essence`, `question_answered`, `operational_links`, `local_position`
- Compression candidates: `routing_and_dispatch.direct_routes`, `examples`, `why_it_matters`, `counter_examples`, `prerequisites`
- Best move-out candidates: `expert_ready_checklist`, `needs_validation`, `current_upgrade_tasks`, `current_status_notes`, `stable_checklist`

## Mechanism Card

Sample spec: `analysis\learning-card-slimming\samples\mechanism-section-bloat-drift.json`
Rendered output: `analysis\learning-card-slimming\outputs\mechanism-section-bloat-drift.md`

| Section | Layer | Score | Classification | Words | Items | Highest Overlap |
| --- | --- | ---: | --- | ---: | ---: | --- |
| `causal_chain` | core | 10 | Must keep | 25 | 1 | routing_and_dispatch.gap_signals (0.17) |
| `phenomenon` | core | 10 | Must keep | 14 | 1 | expert_ready_checklist (0.09) |
| `core_variables` | core | 9 | Must keep | 8 | 4 | alternative_explanations (0.11) |
| `failure_boundaries` | core | 8 | Must keep | 21 | 1 | routing_and_dispatch.gap_signals (0.23) |
| `key_prerequisites` | core | 8 | Must keep | 17 | 1 | failure_boundaries (0.16) |
| `scope` | core | 8 | Must keep | 15 | 1 | current_status_notes (0.22) |
| `weakest_step` | core | 8 | Must keep | 14 | 1 | key_prerequisites (0.15) |
| `alternative_explanations` | core | 7 | Optimize / stage-gate | 13 | 1 | compressed_explanation (0.14) |
| `counter_cases` | core | 7 | Optimize / stage-gate | 15 | 1 | key_prerequisites (0.14) |
| `supporting_evidence` | core | 7 | Optimize / stage-gate | 25 | 1 | promotion_assessment.main_reasons (0.17) |
| `compressed_explanation` | core | 6 | Optimize / stage-gate | 13 | 1 | expert_ready_checklist (0.15) |
| `validation_question` | core | 4 | Redundant in default render | 16 | 1 | causal_chain (0.16) |
| `local_position` | graph | 8 | Must keep | 49 | 4 | key_prerequisites (0.14) |
| `operational_links` | graph | 8 | Must keep | 51 | 4 | routing_and_dispatch.secondary_routes (0.21) |
| `routing_and_dispatch.direct_routes` | graph | 7 | Optimize / stage-gate | 28 | 2 | routing_and_dispatch.secondary_routes (0.21) |
| `routing_and_dispatch.gap_signals` | graph | 5 | Optimize / stage-gate | 20 | 1 | failure_boundaries (0.23) |
| `routing_and_dispatch.secondary_routes` | graph | 5 | Optimize / stage-gate | 22 | 1 | operational_links (0.21) |
| `routing_and_dispatch.stop_rules` | graph | 5 | Optimize / stage-gate | 21 | 1 | counter_cases (0.13) |
| `next_goal` | progression | 5 | Optimize / stage-gate | 10 | 1 | expert_ready_checklist (0.36) |
| `promotion_assessment.current_recommendation` | progression | 5 | Optimize / stage-gate | 1 | 1 | - (0.00) |
| `promotion_assessment.main_reasons` | progression | 5 | Optimize / stage-gate | 10 | 1 | current_status_notes (0.21) |
| `promotion_assessment.missing_evidence` | progression | 5 | Optimize / stage-gate | 14 | 1 | next_goal (0.22) |
| `promotion_assessment.next_rules` | progression | 5 | Optimize / stage-gate | 14 | 1 | routing_and_dispatch.direct_routes (0.12) |
| `current_upgrade_tasks` | progression | 4 | Redundant in default render | 13 | 1 | routing_and_dispatch.direct_routes (0.13) |
| `expert_ready_checklist` | progression | 4 | Redundant in default render | 11 | 1 | next_goal (0.36) |
| `current_status_notes` | progression | 3 | Redundant in default render | 13 | 1 | scope (0.22) |
| `growing_checklist` | progression | 3 | Redundant in default render | 4 | 1 | stable_checklist (0.07) |
| `stable_checklist` | progression | 3 | Redundant in default render | 12 | 2 | failure_boundaries (0.07) |
| `upgrade_history` | progression | 2 | Redundant in default render | 5 | 1 | promotion_assessment.missing_evidence (0.06) |

- Must keep focus: `causal_chain`, `phenomenon`, `core_variables`, `operational_links`, `local_position`
- Compression candidates: `routing_and_dispatch.direct_routes`, `supporting_evidence`, `counter_cases`, `alternative_explanations`, `compressed_explanation`
- Best move-out candidates: `validation_question`, `current_upgrade_tasks`, `expert_ready_checklist`, `current_status_notes`, `stable_checklist`

## Method Card

Sample spec: `analysis\learning-card-slimming\samples\method-section-priority-compression.json`
Rendered output: `analysis\learning-card-slimming\outputs\method-section-priority-compression.md`

| Section | Layer | Score | Classification | Words | Items | Highest Overlap |
| --- | --- | ---: | --- | ---: | ---: | --- |
| `method_structure` | core | 10 | Must keep | 42 | 5 | failure_modes (0.10) |
| `problem_solved` | core | 10 | Must keep | 17 | 1 | routing_and_dispatch.gap_signals (0.21) |
| `core_idea` | core | 9 | Must keep | 14 | 1 | problem_solved (0.11) |
| `decision_criteria` | core | 8 | Must keep | 16 | 1 | routing_and_dispatch.stop_rules (0.19) |
| `failure_modes` | core | 8 | Must keep | 14 | 1 | routing_and_dispatch.direct_routes (0.12) |
| `fit_scenarios` | core | 8 | Must keep | 14 | 1 | non_fit_scenarios (0.17) |
| `non_fit_scenarios` | core | 8 | Must keep | 16 | 1 | validation_question (0.17) |
| `common_misuses` | core | 7 | Optimize / stage-gate | 17 | 2 | non_fit_scenarios (0.15) |
| `design_choices` | core | 7 | Optimize / stage-gate | 8 | 1 | operational_links (0.15) |
| `hidden_assumptions` | core | 7 | Optimize / stage-gate | 12 | 1 | problem_solved (0.12) |
| `comparison_with_alternatives` | core | 6 | Optimize / stage-gate | 17 | 1 | local_position (0.15) |
| `representative_examples` | core | 6 | Optimize / stage-gate | 22 | 1 | stable_checklist (0.14) |
| `validation_question` | core | 4 | Redundant in default render | 21 | 1 | routing_and_dispatch.gap_signals (0.23) |
| `local_position` | graph | 8 | Must keep | 34 | 3 | comparison_with_alternatives (0.15) |
| `operational_links` | graph | 8 | Must keep | 47 | 4 | routing_and_dispatch.direct_routes (0.17) |
| `routing_and_dispatch.direct_routes` | graph | 7 | Optimize / stage-gate | 29 | 2 | operational_links (0.17) |
| `routing_and_dispatch.gap_signals` | graph | 5 | Optimize / stage-gate | 25 | 1 | validation_question (0.23) |
| `routing_and_dispatch.secondary_routes` | graph | 5 | Optimize / stage-gate | 20 | 1 | local_position (0.14) |
| `routing_and_dispatch.stop_rules` | graph | 5 | Optimize / stage-gate | 16 | 1 | decision_criteria (0.19) |
| `next_goal` | progression | 5 | Optimize / stage-gate | 9 | 1 | routing_and_dispatch.gap_signals (0.10) |
| `promotion_assessment.current_recommendation` | progression | 5 | Optimize / stage-gate | 1 | 1 | - (0.00) |
| `promotion_assessment.main_reasons` | progression | 5 | Optimize / stage-gate | 8 | 1 | current_status_notes (0.31) |
| `promotion_assessment.missing_evidence` | progression | 5 | Optimize / stage-gate | 15 | 1 | expert_ready_checklist (0.29) |
| `promotion_assessment.next_rules` | progression | 5 | Optimize / stage-gate | 14 | 1 | routing_and_dispatch.gap_signals (0.16) |
| `current_upgrade_tasks` | progression | 4 | Redundant in default render | 8 | 1 | promotion_assessment.missing_evidence (0.10) |
| `expert_ready_checklist` | progression | 4 | Redundant in default render | 8 | 1 | promotion_assessment.missing_evidence (0.29) |
| `current_status_notes` | progression | 3 | Redundant in default render | 13 | 1 | promotion_assessment.main_reasons (0.31) |
| `growing_checklist` | progression | 3 | Redundant in default render | 5 | 1 | routing_and_dispatch.gap_signals (0.12) |
| `stable_checklist` | progression | 3 | Redundant in default render | 13 | 2 | representative_examples (0.14) |
| `upgrade_history` | progression | 2 | Redundant in default render | 5 | 1 | current_status_notes (0.12) |

- Must keep focus: `method_structure`, `problem_solved`, `core_idea`, `operational_links`, `local_position`
- Compression candidates: `routing_and_dispatch.direct_routes`, `common_misuses`, `hidden_assumptions`, `design_choices`, `representative_examples`
- Best move-out candidates: `validation_question`, `current_upgrade_tasks`, `expert_ready_checklist`, `current_status_notes`, `stable_checklist`

## Misconception Card

Sample spec: `analysis\learning-card-slimming\samples\misconception-more-sections-make-better-card.json`
Rendered output: `analysis\learning-card-slimming\outputs\misconception-more-sections-make-better-card.md`

| Section | Layer | Score | Classification | Words | Items | Highest Overlap |
| --- | --- | ---: | --- | ---: | ---: | --- |
| `mistaken_claim` | core | 10 | Must keep | 15 | 1 | correct_understanding (0.22) |
| `why_it_is_wrong` | core | 10 | Must keep | 25 | 2 | correct_understanding (0.16) |
| `correct_understanding` | core | 9 | Must keep | 19 | 1 | mistaken_claim (0.22) |
| `corrective_action` | core | 9 | Must keep | 19 | 1 | correct_understanding (0.12) |
| `why_it_seems_plausible` | core | 9 | Must keep | 15 | 1 | what_it_confuses (0.10) |
| `representative_counterexamples` | core | 8 | Must keep | 25 | 1 | correct_understanding (0.14) |
| `trigger_signals` | core | 8 | Must keep | 29 | 2 | promotion_assessment.next_rules (0.12) |
| `what_it_confuses` | core | 7 | Optimize / stage-gate | 7 | 1 | promotion_assessment.missing_evidence (0.11) |
| `local_position` | graph | 8 | Must keep | 38 | 3 | routing_and_dispatch.direct_routes (0.17) |
| `operational_links` | graph | 8 | Must keep | 44 | 4 | routing_and_dispatch.direct_routes (0.18) |
| `routing_and_dispatch.direct_routes` | graph | 7 | Optimize / stage-gate | 32 | 2 | promotion_assessment.next_rules (0.29) |
| `routing_and_dispatch.gap_signals` | graph | 5 | Optimize / stage-gate | 21 | 1 | correct_understanding (0.19) |
| `routing_and_dispatch.secondary_routes` | graph | 5 | Optimize / stage-gate | 23 | 1 | promotion_assessment.next_rules (0.18) |
| `routing_and_dispatch.stop_rules` | graph | 5 | Optimize / stage-gate | 20 | 1 | routing_and_dispatch.direct_routes (0.18) |
| `next_goal` | progression | 5 | Optimize / stage-gate | 13 | 1 | expert_ready_checklist (0.14) |
| `promotion_assessment.current_recommendation` | progression | 5 | Optimize / stage-gate | 1 | 1 | - (0.00) |
| `promotion_assessment.main_reasons` | progression | 5 | Optimize / stage-gate | 7 | 1 | current_status_notes (0.25) |
| `promotion_assessment.missing_evidence` | progression | 5 | Optimize / stage-gate | 14 | 1 | expert_ready_checklist (0.47) |
| `promotion_assessment.next_rules` | progression | 5 | Optimize / stage-gate | 20 | 1 | routing_and_dispatch.direct_routes (0.29) |
| `current_upgrade_tasks` | progression | 4 | Redundant in default render | 16 | 1 | routing_and_dispatch.secondary_routes (0.13) |
| `expert_ready_checklist` | progression | 4 | Redundant in default render | 11 | 1 | promotion_assessment.missing_evidence (0.47) |
| `current_status_notes` | progression | 3 | Redundant in default render | 13 | 1 | promotion_assessment.main_reasons (0.25) |
| `growing_checklist` | progression | 3 | Redundant in default render | 9 | 1 | promotion_assessment.next_rules (0.16) |
| `stable_checklist` | progression | 3 | Redundant in default render | 6 | 1 | local_position (0.09) |
| `upgrade_history` | progression | 2 | Redundant in default render | 5 | 1 | current_status_notes (0.06) |

- Must keep focus: `why_it_is_wrong`, `mistaken_claim`, `correct_understanding`, `corrective_action`, `why_it_seems_plausible`
- Compression candidates: `routing_and_dispatch.direct_routes`, `what_it_confuses`, `routing_and_dispatch.secondary_routes`, `routing_and_dispatch.gap_signals`, `promotion_assessment.next_rules`
- Best move-out candidates: `current_upgrade_tasks`, `expert_ready_checklist`, `current_status_notes`, `growing_checklist`, `stable_checklist`

## Global Findings

- Must-keep patterns: `local_position` x4, `operational_links` x4, `failure_boundaries` x2, `question_answered` x1, `one_sentence_definition` x1, `essence` x1, `core_logic` x1, `phenomenon` x1
- Compression-heavy patterns: `routing_and_dispatch.direct_routes` x4, `routing_and_dispatch.secondary_routes` x4, `routing_and_dispatch.gap_signals` x4, `routing_and_dispatch.stop_rules` x4, `next_goal` x4, `promotion_assessment.current_recommendation` x4, `promotion_assessment.main_reasons` x4, `promotion_assessment.missing_evidence` x4
- Default move-out patterns: `current_status_notes` x4, `growing_checklist` x4, `stable_checklist` x4, `expert_ready_checklist` x4, `current_upgrade_tasks` x4, `upgrade_history` x4, `validation_question` x2, `my_words` x1

## Structural Recommendation

- Keep the card-type explanation layer as the default visible body.
- Keep `local_position` and `operational_links` for stable cards because they carry real graph value.
- Reduce `routing_and_dispatch` in stable cards to a thin direct-route layer by default; gate secondary routes, gap signals, and stop rules behind mature cards or review mode.
- Collapse `current_status_notes`, `next_goal`, `promotion_assessment`, and `current_upgrade_tasks` into one compact `Upgrade Focus` block if you still want maintenance data in-body.
- Move `growing_checklist`, `stable_checklist`, `expert_ready_checklist`, and `upgrade_history` out of the default render.
- Treat `my_words`, `validation_question`, and similar reflection fields as optional study aids, not mandatory default sections.
