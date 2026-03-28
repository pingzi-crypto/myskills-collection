#!/usr/bin/env python3
"""
Render a Misconception Card markdown file from a JSON spec.

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
    append_section,
    bullet_lines,
    checkbox_lines,
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
)


def section_map(spec: dict[str, Any]) -> dict[str, Any]:
    sections = spec.get("sections", {}) or {}
    return {
        "mistaken_claim": bullet_lines(sections.get("mistaken_claim")),
        "why_it_seems_plausible": bullet_lines(sections.get("why_it_seems_plausible")),
        "why_it_is_wrong": bullet_lines(sections.get("why_it_is_wrong")),
        "correct_understanding": bullet_lines(sections.get("correct_understanding")),
        "what_it_confuses": bullet_lines(sections.get("what_it_confuses")),
        "representative_counterexamples": bullet_lines(sections.get("representative_counterexamples")),
        "trigger_signals": bullet_lines(sections.get("trigger_signals")),
        "corrective_action": bullet_lines(sections.get("corrective_action")),
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
    raw_title = scalar(spec.get("title"))
    if not raw_title:
        raise ValueError("Missing required field: title")

    domain = scalar(spec.get("domain"))
    if not domain:
        raise ValueError("Missing required field: domain")

    title = sanitize_filename(raw_title)
    status = scalar(spec.get("status"), "seed")
    graph_maturity = scalar(spec.get("graph_maturity"), "none")
    sections = section_map(spec)

    local_labels = [
        ("common_confusions", "常混淆节点"),
        ("correct_return_nodes", "正确回接节点"),
        ("adjacent_misconceptions", "同层误区"),
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
        status == "growing" and any(routing_sections.values())
    )
    show_promotion = should_show_promotion(status, sections["promotion_assessment"])
    show_progression = should_show_progression(status, sections)

    lines: list[str] = []
    lines.extend(render_frontmatter(spec, title, "misconception", "misconception", "misconception"))
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")
    append_section(lines, status, "## 1. 错误说法", sections["mistaken_claim"])
    append_section(lines, status, "## 2. 为什么它看起来像对的？", sections["why_it_seems_plausible"])
    append_section(lines, status, "## 3. 它错在哪里？", sections["why_it_is_wrong"])
    append_section(lines, status, "## 4. 正确理解", sections["correct_understanding"])
    append_section(lines, status, "## 5. 它混淆了什么？", sections["what_it_confuses"])
    append_section(lines, status, "## 6. 代表性反例", sections["representative_counterexamples"])
    append_section(lines, status, "## 7. 触发信号", sections["trigger_signals"])
    append_section(lines, status, "## 8. 纠偏动作", sections["corrective_action"])

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
    parser = argparse.ArgumentParser(description="Render an Obsidian Misconception Card from JSON.")
    parser.add_argument("--spec", required=True, help="Path to the JSON spec file.")
    parser.add_argument("--output", help="Optional output markdown path. Prints to stdout when omitted.")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    spec = json.loads(spec_path.read_text(encoding="utf-8-sig"))
    markdown = render_card(spec)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")
    else:
        print(markdown)


if __name__ == "__main__":
    main()
