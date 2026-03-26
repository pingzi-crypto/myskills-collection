#!/usr/bin/env python3
"""
Render a Concept Card markdown file from a JSON spec.

This script keeps the card structure deterministic while allowing the agent to
focus on content synthesis. It can print the rendered markdown to stdout or
write it directly to a target file.
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
        "related_cards_section": bullet_lines(sections.get("related_cards_section")),
        "needs_validation": bullet_lines(sections.get("needs_validation")),
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
    card_id = scalar(spec.get("id"), f"{timestamp_string()}-concept")
    domain = scalar(spec.get("domain"))
    subdomain = scalar(spec.get("subdomain"))
    source = scalar(spec.get("source"))
    confidence = scalar(spec.get("confidence"), "1")
    related = normalize_list(spec.get("related"))
    aliases = normalize_list(spec.get("aliases"))
    tags = normalize_list(spec.get("tags")) or ["concept"]

    lines = [
        "---",
        f"id: {card_id}",
        f"title: {title}",
        "type: concept",
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
    lines.append("## 1. 这张卡回答什么问题？")
    lines.extend(sections["question_answered"])
    lines.append("")
    lines.append("## 2. 一句话定义")
    lines.extend(sections["one_sentence_definition"])
    lines.append("")
    lines.append("## 3. 本质是什么？")
    lines.extend(sections["essence"])
    lines.append("")
    lines.append("## 4. 为什么重要？")
    lines.extend(sections["why_it_matters"])
    lines.append("")
    lines.append("## 5. 核心机制 / 逻辑链")
    lines.extend(sections["core_logic"])
    lines.append("")
    lines.append("## 6. 成立前提")
    lines.extend(sections["prerequisites"])
    lines.append("")
    lines.append("## 7. 失效边界")
    lines.extend(sections["failure_boundaries"])
    lines.append("")
    lines.append("## 8. 易混概念与区别")
    lines.extend(sections["confusions"])
    lines.append("")
    lines.append("## 9. 正例")
    lines.extend(sections["examples"])
    lines.append("")
    lines.append("## 10. 反例 / 误用")
    lines.extend(sections["counter_examples"])
    lines.append("")
    lines.append("## 11. 常见误区")
    lines.extend(sections["common_misunderstandings"])
    lines.append("")
    lines.append("## 12. 我的话版本")
    lines.extend(sections["my_words"])
    lines.append("")
    lines.append("## 13. 与哪些卡相关")
    lines.extend(sections["related_cards_section"])
    lines.append("")
    lines.append("## 14. 还待验证什么？")
    lines.extend(sections["needs_validation"])
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
    parser = argparse.ArgumentParser(description="Render an Obsidian Concept Card from JSON.")
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
