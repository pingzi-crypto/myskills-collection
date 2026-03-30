#!/usr/bin/env python3
"""
Render a Method Card markdown file from a JSON spec.

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
    "problem_solved",
    "core_idea",
    "method_structure",
    "design_choices",
    "hidden_assumptions",
    "fit_scenarios",
    "non_fit_scenarios",
    "comparison_with_alternatives",
    "common_misuses",
    "failure_modes",
    "decision_criteria",
    "representative_examples",
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
        "problem_solved": bullet_lines(sections.get("problem_solved")),
        "core_idea": bullet_lines(sections.get("core_idea")),
        "method_structure": bullet_lines(sections.get("method_structure")),
        "design_choices": bullet_lines(sections.get("design_choices")),
        "hidden_assumptions": bullet_lines(sections.get("hidden_assumptions")),
        "fit_scenarios": bullet_lines(sections.get("fit_scenarios")),
        "non_fit_scenarios": bullet_lines(sections.get("non_fit_scenarios")),
        "comparison_with_alternatives": bullet_lines(sections.get("comparison_with_alternatives")),
        "common_misuses": bullet_lines(sections.get("common_misuses")),
        "failure_modes": bullet_lines(sections.get("failure_modes")),
        "decision_criteria": bullet_lines(sections.get("decision_criteria")),
        "representative_examples": bullet_lines(sections.get("representative_examples")),
        "validation_question": bullet_lines(sections.get("validation_question")),
        "current_status_notes": bullet_lines(sections.get("current_status_notes"), default_blank=False),
        "next_goal": bullet_lines(sections.get("next_goal"), default_blank=False),
        "growing_checklist": checkbox_lines(sections.get("growing_checklist")),
        "stable_checklist": checkbox_lines(sections.get("stable_checklist")),
        "expert_ready_checklist": checkbox_lines(sections.get("expert_ready_checklist")),
        "current_upgrade_tasks": checkbox_lines(sections.get("current_upgrade_tasks"), default_blank=False),
        "upgrade_history": bullet_lines(sections.get("upgrade_history")),
        "local_position": sections.get("local_position", {}) or {},
        "operational_links": sections.get("operational_links", {}) or {},
        "routing_and_dispatch": normalize_routing_sections(sections.get("routing_and_dispatch")),
        "promotion_assessment": sections.get("promotion_assessment", {}) or {},
    }


def render_card(spec: dict[str, Any]) -> str:
    validate_learning_card_spec(
        spec,
        card_type="method",
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
        ("upstream_concepts", "上游概念"),
        ("upstream_mechanisms", "上游机制"),
        ("adjacent_methods", "相邻或替代方法"),
    ]
    operational_labels = [
        ("prerequisites", "前提依赖"),
        ("enables", "下游支撑"),
        ("contrasts", "关键对比"),
        ("corrections", "纠偏关联"),
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
    lines.extend(render_frontmatter(spec, title, "method", "method", "method"))
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")
    append_section(lines, status, "## 1. 这个方法解决什么问题？", sections["problem_solved"])
    append_section(lines, status, "## 2. 核心思路", sections["core_idea"])
    append_section(lines, status, "## 3. 步骤结构", sections["method_structure"])
    append_section(lines, status, "## 4. 关键设计选择", sections["design_choices"])
    append_section(lines, status, "## 5. 隐含假设", sections["hidden_assumptions"])
    append_section(lines, status, "## 6. 适用场景", sections["fit_scenarios"])
    append_section(lines, status, "## 7. 不适用场景", sections["non_fit_scenarios"])
    append_section(lines, status, "## 8. 与替代方法的比较", sections["comparison_with_alternatives"])
    append_section(lines, status, "## 9. 常见误用", sections["common_misuses"])
    append_section(lines, status, "## 10. 失败模式", sections["failure_modes"])
    append_section(lines, status, "## 11. 决策标准", sections["decision_criteria"])
    append_section(lines, status, "## 12. 代表性例子", sections["representative_examples"])
    append_section(lines, status, "## 13. 验证问题", sections["validation_question"])

    if show_graph:
        lines.append("## Knowledge Graph Relations")
        lines.append("")
        lines.append("### Local Position")
        lines.extend(local_lines)
        if status in {"stable", "expert-ready"} and not local_has_content:
            lines.append("- 说明：当前阶段仍缺少稳定的局部定位关系。")
        lines.append("")
        lines.append("### Operational Links")
        lines.extend(operational_lines)
        if status in {"stable", "expert-ready"} and not operational_has_content:
            lines.append("- 说明：当前阶段仍缺少稳定的功能连接关系。")
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
        lines.append(f"- 当前阶段：{status}")
        lines.append(f"- 图谱成熟度：{graph_maturity}")
        lines.extend(sections["current_status_notes"])
        if sections["next_goal"]:
            lines.append("- 下一步重点：")
            lines.extend([f"  {line}" for line in sections["next_goal"]])
        if show_promotion:
            assessment = sections["promotion_assessment"]
            lines.append(f"- 当前建议：{scalar(assessment.get('current_recommendation'), 'stay stable')}")
            missing_evidence = bullet_lines(assessment.get("missing_evidence"))
            next_rules = bullet_lines(assessment.get("next_rules"))
            if normalize_list(assessment.get("missing_evidence")):
                lines.append("- 缺失证据：")
                lines.extend([f"  {line}" for line in missing_evidence])
            if normalize_list(assessment.get("next_rules")):
                lines.append("- 下一步行动规则：")
                lines.extend([f"  {line}" for line in next_rules])
        elif sections["current_upgrade_tasks"]:
            lines.append("- 当前升级任务：")
            lines.extend([f"  {line}" for line in sections["current_upgrade_tasks"]])
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render an Obsidian Method Card from JSON.")
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
