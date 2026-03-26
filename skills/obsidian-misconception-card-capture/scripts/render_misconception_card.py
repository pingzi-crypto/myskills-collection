#!/usr/bin/env python3
"""
Render a Misconception Card markdown file from a JSON spec.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
import re
from typing import Any


INVALID_FILENAME_RE = re.compile(r'[\\/:*?"<>|]')


def sanitize_filename(value: str) -> str:
    return INVALID_FILENAME_RE.sub("-", value.strip())


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def bullet_lines(value: Any) -> list[str]:
    items = normalize_list(value)
    return [f"- {item}" for item in items] if items else ["- "]


def checkbox_lines(value: Any) -> list[str]:
    items = normalize_list(value)
    return [f"- [ ] {item}" for item in items] if items else ["- [ ] "]


def nonempty_bullets(value: Any) -> list[str]:
    items = normalize_list(value)
    return [f"- {item}" for item in items]


def scalar(value: Any, default: str = "") -> str:
    if value is None:
        return default
    text = str(value).strip()
    return text if text else default


def today_string() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def timestamp_string() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S")


def section_map(spec: dict[str, Any]) -> dict[str, list[str]]:
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
        "related_cards_section": bullet_lines(sections.get("related_cards_section")),
        "current_status_notes": nonempty_bullets(sections.get("current_status_notes")),
        "next_goal": bullet_lines(sections.get("next_goal")),
        "growing_checklist": checkbox_lines(sections.get("growing_checklist")),
        "stable_checklist": checkbox_lines(sections.get("stable_checklist")),
        "expert_ready_checklist": checkbox_lines(sections.get("expert_ready_checklist")),
        "current_upgrade_tasks": checkbox_lines(sections.get("current_upgrade_tasks")),
        "upgrade_history": bullet_lines(sections.get("upgrade_history")),
    }


def render_frontmatter(spec: dict[str, Any], title: str) -> list[str]:
    created = scalar(spec.get("created"), today_string())
    updated = scalar(spec.get("updated"), created)
    status = scalar(spec.get("status"), "seed")
    card_id = scalar(spec.get("id"), f"{timestamp_string()}-misconception")
    domain = scalar(spec.get("domain"))
    subdomain = scalar(spec.get("subdomain"))
    source = scalar(spec.get("source"))
    confidence = scalar(spec.get("confidence"), "1")
    related = normalize_list(spec.get("related"))
    aliases = normalize_list(spec.get("aliases"))
    tags = normalize_list(spec.get("tags")) or ["misconception"]

    lines = [
        "---",
        f"id: {card_id}",
        f"title: {title}",
        "type: misconception",
        f"domain: {domain}",
        f"subdomain: {subdomain}",
        f"status: {status}",
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
    lines.append("review_cycle: 30d")
    lines.append("aliases: []" if not aliases else "aliases:")
    if aliases:
        lines.extend([f"  - {item}" for item in aliases])
    lines.append("---")
    return lines


def render_card(spec: dict[str, Any]) -> str:
    raw_title = scalar(spec.get("title"))
    if not raw_title:
        raise ValueError("Missing required field: title")

    domain = scalar(spec.get("domain"))
    if not domain:
        raise ValueError("Missing required field: domain")

    title = sanitize_filename(raw_title)
    status = scalar(spec.get("status"), "seed")
    sections = section_map(spec)

    lines: list[str] = []
    lines.extend(render_frontmatter(spec, title))
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")
    lines.append("## 1. 错误说法")
    lines.extend(sections["mistaken_claim"])
    lines.append("")
    lines.append("## 2. 为什么它看起来合理")
    lines.extend(sections["why_it_seems_plausible"])
    lines.append("")
    lines.append("## 3. 它错在哪里")
    lines.extend(sections["why_it_is_wrong"])
    lines.append("")
    lines.append("## 4. 正确理解")
    lines.extend(sections["correct_understanding"])
    lines.append("")
    lines.append("## 5. 它混淆了什么")
    lines.extend(sections["what_it_confuses"])
    lines.append("")
    lines.append("## 6. 典型反例")
    lines.extend(sections["representative_counterexamples"])
    lines.append("")
    lines.append("## 7. 我的触发信号")
    lines.extend(sections["trigger_signals"])
    lines.append("")
    lines.append("## 8. 修正动作")
    lines.extend(sections["corrective_action"])
    lines.append("")
    lines.append("## 9. 与哪些卡相关")
    lines.extend(sections["related_cards_section"])
    lines.append("")
    lines.append("## 当前状态")
    lines.append(f"- 当前等级：{status}")
    next_goal_lines = sections["next_goal"]
    next_goal = next_goal_lines[0][2:] if next_goal_lines and next_goal_lines[0].startswith("- ") else ""
    lines.append(f"- 下一目标：{next_goal}")
    lines.extend(sections["current_status_notes"])
    lines.append("")
    lines.append("## 升级门槛")
    lines.append("### 升到 growing 前自检")
    lines.extend(sections["growing_checklist"])
    lines.append("")
    lines.append("### 升到 stable 前自检")
    lines.extend(sections["stable_checklist"])
    lines.append("")
    lines.append("### 升到 expert-ready 前自检")
    lines.extend(sections["expert_ready_checklist"])
    lines.append("")
    lines.append("## 当前升级任务")
    lines.extend(sections["current_upgrade_tasks"])
    lines.append("")
    lines.append("## 升级记录")
    lines.extend(sections["upgrade_history"])
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render an Obsidian Misconception Card from JSON.")
    parser.add_argument("--spec", required=True, help="Path to the JSON spec file.")
    parser.add_argument("--output", help="Optional output markdown path. Prints to stdout when omitted.")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    markdown = render_card(spec)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")
    else:
        print(markdown)


if __name__ == "__main__":
    main()
