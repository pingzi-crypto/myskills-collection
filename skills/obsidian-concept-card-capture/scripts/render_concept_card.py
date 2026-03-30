#!/usr/bin/env python3
"""
Render a Concept Card markdown file from a JSON spec.

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
    "question_answered",
    "one_sentence_definition",
    "essence",
    "why_it_matters",
    "core_logic",
    "prerequisites",
    "failure_boundaries",
    "confusions",
    "examples",
    "counter_examples",
    "common_misunderstandings",
    "my_words",
    "needs_validation",
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
        "question_answered": bullet_lines(sections.get("question_answered")),
        "one_sentence_definition": bullet_lines(sections.get("one_sentence_definition")),
        "essence": bullet_lines(sections.get("essence")),
        "why_it_matters": bullet_lines(sections.get("why_it_matters")),
        "core_logic": bullet_lines(sections.get("core_logic")),
        "prerequisites": bullet_lines(sections.get("prerequisites")),
        "failure_boundaries": bullet_lines(sections.get("failure_boundaries")),
        "confusions": bullet_lines(sections.get("confusions")),
        "examples": bullet_lines(sections.get("examples")),
        "counter_examples": bullet_lines(sections.get("counter_examples")),
        "common_misunderstandings": bullet_lines(sections.get("common_misunderstandings")),
        "my_words": bullet_lines(sections.get("my_words")),
        "needs_validation": bullet_lines(sections.get("needs_validation")),
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
        card_type="concept",
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
        ("parent_concepts", "上位概念"),
        ("child_concepts", "下位概念"),
        ("adjacent_concepts", "相邻概念"),
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
    lines.extend(render_frontmatter(spec, title, "concept", "concept", "concept"))
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")
    append_section(lines, status, "## 1. 这个概念在回答什么问题？", sections["question_answered"])
    append_section(lines, status, "## 2. 一句话定义", sections["one_sentence_definition"])
    append_section(lines, status, "## 3. 核心本质", sections["essence"])
    append_section(lines, status, "## 4. 为什么重要", sections["why_it_matters"])
    append_section(lines, status, "## 5. 核心逻辑", sections["core_logic"])
    append_section(lines, status, "## 6. 成立前提", sections["prerequisites"])
    append_section(lines, status, "## 7. 失效边界", sections["failure_boundaries"])
    append_section(lines, status, "## 8. 易混概念与区别", sections["confusions"])
    append_section(lines, status, "## 9. 正例", sections["examples"])
    append_section(lines, status, "## 10. 反例或误用", sections["counter_examples"])
    append_section(lines, status, "## 11. 常见误解", sections["common_misunderstandings"])
    append_section(lines, status, "## 12. 我的表达", sections["my_words"])
    append_section(lines, status, "## 13. 待验证问题", sections["needs_validation"])

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
    parser = argparse.ArgumentParser(description="Render an Obsidian Concept Card from JSON.")
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
