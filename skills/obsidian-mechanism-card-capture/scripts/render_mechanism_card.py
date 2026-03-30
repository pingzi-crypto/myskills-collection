#!/usr/bin/env python3
"""
Render a Mechanism Card markdown file from a JSON spec.

This renderer keeps the layout deterministic while supporting stage-aware
display of graph structure and promotion evidence.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


CORE_SCRIPTS = Path(__file__).resolve().parents[2] / "shared" / "learning-card-core" / "scripts"
if str(CORE_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(CORE_SCRIPTS))

from render_common import (
    SpecValidationError,
    append_section,
    bullet_lines,
    checkbox_lines,
    has_routing_content,
    lines_for_dict_entries,
    normalize_list,
    normalize_routing_sections,
    render_frontmatter,
    render_routing_sections,
    sanitize_filename,
    scalar,
    should_show_graph,
    should_show_progression,
    should_show_promotion,
    validate_learning_card_spec,
)

SECTION_KEYS = {
    "phenomenon",
    "core_variables",
    "causal_chain",
    "key_prerequisites",
    "weakest_step",
    "alternative_explanations",
    "scope",
    "failure_boundaries",
    "supporting_evidence",
    "counter_cases",
    "compressed_explanation",
    "validation_question",
    "current_status_notes",
    "next_goal",
    "growing_checklist",
    "stable_checklist",
    "expert_ready_checklist",
    "current_upgrade_tasks",
    "upgrade_history",
    "local_position",
    "operational_links",
    "routing_and_dispatch",
    "promotion_assessment",
}


def section_map(spec: dict[str, Any]) -> dict[str, Any]:
    sections = spec.get("sections", {}) or {}
    return {
        "phenomenon": bullet_lines(sections.get("phenomenon")),
        "core_variables": bullet_lines(sections.get("core_variables")),
        "causal_chain": bullet_lines(sections.get("causal_chain")),
        "key_prerequisites": bullet_lines(sections.get("key_prerequisites")),
        "weakest_step": bullet_lines(sections.get("weakest_step")),
        "alternative_explanations": bullet_lines(sections.get("alternative_explanations")),
        "scope": bullet_lines(sections.get("scope")),
        "failure_boundaries": bullet_lines(sections.get("failure_boundaries")),
        "supporting_evidence": bullet_lines(sections.get("supporting_evidence")),
        "counter_cases": bullet_lines(sections.get("counter_cases")),
        "compressed_explanation": bullet_lines(sections.get("compressed_explanation")),
        "validation_question": bullet_lines(sections.get("validation_question")),
        "current_status_notes": bullet_lines(sections.get("current_status_notes"), default_blank=False),
        "next_goal": bullet_lines(sections.get("next_goal")),
        "growing_checklist": checkbox_lines(sections.get("growing_checklist")),
        "stable_checklist": checkbox_lines(sections.get("stable_checklist")),
        "expert_ready_checklist": checkbox_lines(sections.get("expert_ready_checklist")),
        "current_upgrade_tasks": checkbox_lines(sections.get("current_upgrade_tasks")),
        "upgrade_history": bullet_lines(sections.get("upgrade_history")),
        "local_position": sections.get("local_position", {}) or {},
        "operational_links": sections.get("operational_links", {}) or {},
        "routing_and_dispatch": normalize_routing_sections(sections.get("routing_and_dispatch")),
        "promotion_assessment": sections.get("promotion_assessment", {}) or {},
    }


def render_card(spec: dict[str, Any]) -> str:
    validate_learning_card_spec(
        spec,
        card_type="mechanism",
        section_keys=SECTION_KEYS,
        mapping_sections={"local_position", "operational_links", "promotion_assessment"},
        routing_sections={"routing_and_dispatch"},
    )

    raw_title = scalar(spec.get("title"))
    title = sanitize_filename(raw_title)
    status = scalar(spec.get("status"), "seed")
    graph_maturity = scalar(spec.get("graph_maturity"), "none")
    sections = section_map(spec)

    local_labels = [
        ("upstream_concepts", "Upstream Concepts"),
        ("trigger_conditions", "Trigger Conditions"),
        ("downstream_results", "Downstream Results"),
        ("adjacent_mechanisms", "Adjacent Mechanisms"),
    ]
    operational_labels = [
        ("prerequisites", "Prerequisites"),
        ("enables", "Enables"),
        ("contrasts", "Contrasts"),
        ("corrections", "Corrections"),
    ]

    local_lines, local_has_content = lines_for_dict_entries(sections["local_position"], local_labels)
    operational_lines, operational_has_content = lines_for_dict_entries(
        sections["operational_links"], operational_labels
    )
    routing_sections = sections["routing_and_dispatch"]
    show_graph = should_show_graph(status, sections)
    show_routing = status == "expert-ready" or bool(routing_sections.get("direct_routes")) or (
        status == "growing" and has_routing_content(routing_sections)
    )
    show_promotion = should_show_promotion(status, sections["promotion_assessment"])
    show_progression = should_show_progression(status, sections)

    lines: list[str] = []
    lines.extend(render_frontmatter(spec, title, "mechanism", "mechanism", "mechanism"))
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")
    append_section(lines, status, "## 1. Phenomenon Explained", sections["phenomenon"])
    append_section(lines, status, "## 2. Core Variables", sections["core_variables"])
    append_section(lines, status, "## 3. Causal Chain", sections["causal_chain"])
    append_section(lines, status, "## 4. Key Preconditions", sections["key_prerequisites"])
    append_section(lines, status, "## 5. Weakest Link", sections["weakest_step"])
    append_section(lines, status, "## 6. Alternative Mechanisms", sections["alternative_explanations"])
    append_section(lines, status, "## 7. Scope", sections["scope"])
    append_section(lines, status, "## 8. Failure Boundaries", sections["failure_boundaries"])
    append_section(lines, status, "## 9. Supporting Evidence", sections["supporting_evidence"])
    append_section(lines, status, "## 10. Counter Cases", sections["counter_cases"])
    append_section(lines, status, "## 11. Compressed Explanation", sections["compressed_explanation"])
    append_section(lines, status, "## 12. Validation Question", sections["validation_question"])

    if show_graph:
        lines.append("## Knowledge Graph Relations")
        lines.append("")
        lines.append("### Local Position")
        lines.extend(local_lines)
        if status in {"stable", "expert-ready"} and not local_has_content:
            lines.append("- Note: local graph placement is still missing stable evidence.")
        lines.append("")
        lines.append("### Operational Links")
        lines.extend(operational_lines)
        if status in {"stable", "expert-ready"} and not operational_has_content:
            lines.append("- Note: operational relationships are still missing stable evidence.")
        lines.append("")
        if show_routing:
            lines.append("### Routing and Dispatch")
            lines.append("")
            lines.extend(render_routing_sections(routing_sections, status))
            lines.append("")

    if show_progression:
        lines.append("## Progression Layer")
        lines.append("")
        lines.append("### Upgrade Focus")
        lines.append(f"- Current status: {status}")
        lines.append(f"- Graph maturity: {graph_maturity}")
        lines.extend(sections["current_status_notes"])
        if sections["next_goal"]:
            lines.append("- Next goal:")
            lines.extend([f"  {line}" for line in sections["next_goal"]])
        if show_promotion:
            assessment = sections["promotion_assessment"]
            lines.append(f"- Current recommendation: {scalar(assessment.get('current_recommendation'), 'stay stable')}")
            missing_evidence = bullet_lines(assessment.get("missing_evidence"))
            next_rules = bullet_lines(assessment.get("next_rules"))
            if normalize_list(assessment.get("missing_evidence")):
                lines.append("- Missing evidence:")
                lines.extend([f"  {line}" for line in missing_evidence])
            if normalize_list(assessment.get("next_rules")):
                lines.append("- Next rules worth adding:")
                lines.extend([f"  {line}" for line in next_rules])
        elif sections["current_upgrade_tasks"]:
            lines.append("- Current upgrade tasks:")
            lines.extend([f"  {line}" for line in sections["current_upgrade_tasks"]])
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render an Obsidian Mechanism Card from JSON.")
    parser.add_argument("--spec", required=True, help="Path to the JSON spec file.")
    parser.add_argument("--output", help="Optional output markdown path. Prints to stdout when omitted.")
    args = parser.parse_args()

    try:
        spec_path = Path(args.spec)
        spec = json.loads(spec_path.read_text(encoding="utf-8-sig"))
        markdown = render_card(spec)
    except json.JSONDecodeError as exc:
        parser.exit(2, f"Invalid JSON spec: {exc}\n")
    except SpecValidationError as exc:
        parser.exit(2, f"Spec validation failed: {exc}\n")

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")
    else:
        print(markdown)


if __name__ == "__main__":
    main()
