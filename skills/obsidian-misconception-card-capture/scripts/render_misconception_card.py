#!/usr/bin/env python3
"""
Render a Misconception Card markdown file from a JSON spec.

This renderer keeps the layout deterministic while supporting stage-aware
display of graph structure and promotion evidence.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
import re
from typing import Any


INVALID_FILENAME_RE = re.compile(r'[\\/:*?"<>|]')
ROUTING_SECTION_LABELS = [
    ("direct_routes", "Direct Routes"),
    ("secondary_routes", "Secondary Routes"),
    ("gap_signals", "Gap Signals"),
    ("stop_rules", "Stop Rules"),
]


def sanitize_filename(value: str) -> str:
    return INVALID_FILENAME_RE.sub("-", value.strip())


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def scalar(value: Any, default: str = "") -> str:
    if value is None:
        return default
    text = str(value).strip()
    return text if text else default


def bullet_lines(value: Any, default_blank: bool = True) -> list[str]:
    items = normalize_list(value)
    if items:
        return [f"- {item}" for item in items]
    return ["- "] if default_blank else []


def checkbox_lines(value: Any) -> list[str]:
    items = normalize_list(value)
    return [f"- [ ] {item}" for item in items] if items else ["- [ ] "]


def normalize_routing_sections(value: Any) -> dict[str, list[str]]:
    if isinstance(value, dict):
        mapping = value
    else:
        mapping = {"direct_routes": value}
    return {key: normalize_list(mapping.get(key)) for key, _ in ROUTING_SECTION_LABELS}


def has_routing_content(value: dict[str, list[str]]) -> bool:
    return any(value.get(key) for key, _ in ROUTING_SECTION_LABELS)


def routing_placeholder(key: str, status: str) -> str:
    stable_placeholders = {
        "direct_routes": "Direct routes are still emerging.",
        "secondary_routes": "Secondary routes are optional until multi-hop paths stabilize.",
        "gap_signals": "Gap signals are optional until promotion review begins.",
        "stop_rules": "Stop rules are optional until dispatch complexity increases.",
    }
    expert_placeholders = {
        "direct_routes": "Gap: expert-ready requires strong direct routes.",
        "secondary_routes": "Gap: expert-ready requires at least one bounded secondary route.",
        "gap_signals": "Gap: expert-ready requires at least one explicit gap signal.",
        "stop_rules": "Gap: expert-ready requires at least one explicit stop rule.",
    }
    if status == "expert-ready":
        return expert_placeholders[key]
    if status == "stable":
        return stable_placeholders[key]
    return "No rule recorded yet."


def render_routing_sections(routing: dict[str, list[str]], status: str) -> list[str]:
    lines: list[str] = []
    for key, label in ROUTING_SECTION_LABELS:
        lines.append(f"#### {label}")
        items = routing.get(key, [])
        if items:
            lines.extend([f"- {item}" for item in items])
        else:
            lines.append(f"- {routing_placeholder(key, status)}")
        lines.append("")
    return lines


def today_string() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def timestamp_string() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S%f")


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


def render_frontmatter(spec: dict[str, Any], title: str) -> list[str]:
    created = scalar(spec.get("created"), today_string())
    updated = scalar(spec.get("updated"), created)
    status = scalar(spec.get("status"), "seed")
    graph_maturity = scalar(spec.get("graph_maturity"), "none")
    card_id = scalar(spec.get("id"), f"{timestamp_string()}-misconception")
    domain = scalar(spec.get("domain"))
    subdomain = scalar(spec.get("subdomain"))
    source = scalar(spec.get("source"))
    confidence = scalar(spec.get("confidence"), "1")
    related = normalize_list(spec.get("related"))
    aliases = normalize_list(spec.get("aliases"))
    tags = normalize_list(spec.get("tags")) or ["misconception"]
    review_cycle = scalar(spec.get("review_cycle"), "30d")

    lines = [
        "---",
        f"id: {card_id}",
        f"title: {title}",
        "type: misconception",
        f"domain: {domain}",
        f"subdomain: {subdomain}",
        f"status: {status}",
        f"graph_maturity: {graph_maturity}",
        f"created: {created}",
        f"updated: {updated}",
        f"source: {source}",
        "tags:",
    ]
    lines.extend([f"  - {tag}" for tag in tags])
    lines.append("related: []" if not related else "related:")
    if related:
        lines.extend([f"  - {item}" for item in related])
    lines.append(f"confidence: {confidence}")
    lines.append(f"review_cycle: {review_cycle}")
    lines.append("aliases: []" if not aliases else "aliases:")
    if aliases:
        lines.extend([f"  - {item}" for item in aliases])
    lines.append("---")
    return lines


def lines_for_dict_entries(mapping: dict[str, Any], labels: list[tuple[str, str]]) -> tuple[list[str], bool]:
    rendered: list[str] = []
    has_content = False
    for key, label in labels:
        items = normalize_list(mapping.get(key))
        if items:
            rendered.append(f"- {label}: {items[0]}")
            rendered.extend([f"  - {item}" for item in items[1:]])
            has_content = True
        else:
            rendered.append(f"- {label}: ")
    return rendered, has_content


def should_show_graph(status: str, sections: dict[str, Any]) -> bool:
    if status in {"stable", "expert-ready"}:
        return True
    if status == "growing":
        return has_routing_content(sections["routing_and_dispatch"]) or any(
            normalize_list(value) for value in sections["local_position"].values()
        ) or any(normalize_list(value) for value in sections["operational_links"].values())
    return False


def should_show_promotion(status: str, assessment: dict[str, Any]) -> bool:
    if status in {"stable", "expert-ready"}:
        return True
    return any(scalar(assessment.get(key)) or normalize_list(assessment.get(key)) for key in assessment)


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
    show_routing = status in {"stable", "expert-ready"} or has_routing_content(routing_sections)
    show_promotion = should_show_promotion(status, sections["promotion_assessment"])

    lines: list[str] = []
    lines.extend(render_frontmatter(spec, title))
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")
    lines.append("## 1. 错误说法")
    lines.extend(sections["mistaken_claim"])
    lines.append("")
    lines.append("## 2. 为什么它看起来像对的？")
    lines.extend(sections["why_it_seems_plausible"])
    lines.append("")
    lines.append("## 3. 它错在哪里？")
    lines.extend(sections["why_it_is_wrong"])
    lines.append("")
    lines.append("## 4. 正确理解")
    lines.extend(sections["correct_understanding"])
    lines.append("")
    lines.append("## 5. 它混淆了什么？")
    lines.extend(sections["what_it_confuses"])
    lines.append("")
    lines.append("## 6. 代表性反例")
    lines.extend(sections["representative_counterexamples"])
    lines.append("")
    lines.append("## 7. 触发信号")
    lines.extend(sections["trigger_signals"])
    lines.append("")
    lines.append("## 8. 纠偏动作")
    lines.extend(sections["corrective_action"])
    lines.append("")

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

    lines.append("## Progression Layer")
    lines.append("")
    lines.append("### Current Status Notes")
    lines.append(f"- 当前阶段：{status}")
    lines.append(f"- 图谱成熟度：{graph_maturity}")
    lines.extend(sections["current_status_notes"])
    lines.append("")
    lines.append("### Next Goal")
    lines.extend(sections["next_goal"])
    lines.append("")
    lines.append("### Growing Checklist")
    lines.extend(sections["growing_checklist"])
    lines.append("")
    lines.append("### Stable Checklist")
    lines.extend(sections["stable_checklist"])
    lines.append("")
    lines.append("### Expert-Ready Checklist")
    lines.extend(sections["expert_ready_checklist"])
    lines.append("")
    if show_promotion:
        assessment = sections["promotion_assessment"]
        lines.append("### Promotion Assessment")
        lines.append(f"- 当前建议：{scalar(assessment.get('current_recommendation'), 'stay stable')}")
        main_reasons = bullet_lines(assessment.get("main_reasons"))
        missing_evidence = bullet_lines(assessment.get("missing_evidence"))
        next_rules = bullet_lines(assessment.get("next_rules"))
        lines.append("- 主要原因：")
        lines.extend([f"  {line}" for line in main_reasons])
        lines.append("- 缺失证据：")
        lines.extend([f"  {line}" for line in missing_evidence])
        lines.append("- 下一步最值得补的规则：")
        lines.extend([f"  {line}" for line in next_rules])
        lines.append("")
    lines.append("### Current Upgrade Tasks")
    lines.extend(sections["current_upgrade_tasks"])
    lines.append("")
    lines.append("## Upgrade History")
    lines.extend(sections["upgrade_history"])
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
