from __future__ import annotations

from datetime import datetime
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


def normalize_content_items(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        items: list[Any] = []
        for item in value:
            if isinstance(item, dict):
                zh = scalar(item.get("zh"))
                en = scalar(item.get("en"))
                if zh or en:
                    items.append({"zh": zh, "en": en})
            else:
                text = scalar(item)
                if text:
                    items.append(text)
        return items
    if isinstance(value, dict):
        zh = scalar(value.get("zh"))
        en = scalar(value.get("en"))
        if zh or en:
            return [{"zh": zh, "en": en}]
        return []
    text = scalar(value)
    return [text] if text else []


def render_item_lines(item: Any, prefix: str = "- ", translation_prefix: str = "  - EN: ") -> list[str]:
    if isinstance(item, dict):
        zh = scalar(item.get("zh"))
        en = scalar(item.get("en"))
        lines: list[str] = []
        if zh:
            lines.append(f"{prefix}{zh}")
        if en:
            if zh:
                lines.append(f"{translation_prefix}{en}")
            else:
                lines.append(f"{prefix}EN: {en}")
        return lines
    text = scalar(item)
    return [f"{prefix}{text}"] if text else []


def bullet_lines(value: Any, default_blank: bool = True) -> list[str]:
    items = normalize_content_items(value)
    if items:
        lines: list[str] = []
        for item in items:
            lines.extend(render_item_lines(item))
        return lines
    return ["- "] if default_blank else []


def checkbox_lines(value: Any) -> list[str]:
    items = normalize_content_items(value)
    if items:
        lines: list[str] = []
        for item in items:
            lines.extend(render_item_lines(item, prefix="- [ ] ", translation_prefix="  - EN: "))
        return lines
    return ["- [ ] "]


def has_meaningful_lines(lines: list[str]) -> bool:
    return any(line.strip() not in {"-", "- [ ]"} for line in lines)


def append_section(lines: list[str], status: str, heading: str, section_lines: list[str]) -> None:
    if status not in {"stable", "expert-ready"} and not has_meaningful_lines(section_lines):
        return
    lines.append(heading)
    lines.extend(section_lines)
    lines.append("")


def normalize_routing_sections(value: Any) -> dict[str, list[str]]:
    if isinstance(value, dict):
        mapping = value
    else:
        mapping = {"direct_routes": value}
    return {key: normalize_content_items(mapping.get(key)) for key, _ in ROUTING_SECTION_LABELS}


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
    visible_labels = ROUTING_SECTION_LABELS if status == "expert-ready" else [ROUTING_SECTION_LABELS[0]]
    for key, label in visible_labels:
        lines.append(f"#### {label}")
        items = routing.get(key, [])
        if items:
            for item in items:
                lines.extend(render_item_lines(item))
        else:
            lines.append(f"- {routing_placeholder(key, status)}")
        lines.append("")
    return lines


def today_string() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def timestamp_string() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S%f")


def render_frontmatter(
    spec: dict[str, Any],
    title: str,
    card_type: str,
    default_tag: str,
    id_suffix: str,
) -> list[str]:
    created = scalar(spec.get("created"), today_string())
    updated = scalar(spec.get("updated"), created)
    status = scalar(spec.get("status"), "seed")
    graph_maturity = scalar(spec.get("graph_maturity"), "none")
    card_id = scalar(spec.get("id"), f"{timestamp_string()}-{id_suffix}")
    domain = scalar(spec.get("domain"))
    subdomain = scalar(spec.get("subdomain"))
    source = scalar(spec.get("source"))
    confidence = scalar(spec.get("confidence"), "1")
    related = normalize_list(spec.get("related"))
    aliases = normalize_list(spec.get("aliases"))
    tags = normalize_list(spec.get("tags")) or [default_tag]
    review_cycle = scalar(spec.get("review_cycle"), "30d")

    lines = [
        "---",
        f"id: {card_id}",
        f"title: {title}",
        f"type: {card_type}",
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
        items = normalize_content_items(mapping.get(key))
        if items:
            first_item = items[0]
            if isinstance(first_item, dict):
                zh = scalar(first_item.get("zh"))
                en = scalar(first_item.get("en"))
                if zh:
                    rendered.append(f"- {label}: {zh}")
                    if en:
                        rendered.append(f"  - EN: {en}")
                elif en:
                    rendered.append(f"- {label}: EN: {en}")
            else:
                rendered.append(f"- {label}: {first_item}")
            for item in items[1:]:
                if isinstance(item, dict):
                    zh = scalar(item.get("zh"))
                    en = scalar(item.get("en"))
                    if zh:
                        rendered.append(f"  - {zh}")
                        if en:
                            rendered.append(f"    - EN: {en}")
                    elif en:
                        rendered.append(f"  - EN: {en}")
                else:
                    rendered.append(f"  - {item}")
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
    if status == "expert-ready":
        return True
    if status == "stable":
        return bool(scalar(assessment.get("current_recommendation"))) or bool(normalize_list(assessment.get("next_rules")))
    return any(scalar(assessment.get(key)) or normalize_list(assessment.get(key)) for key in assessment)


def should_show_progression(status: str, sections: dict[str, Any]) -> bool:
    if status in {"stable", "expert-ready"}:
        return True
    return any(
        has_meaningful_lines(sections[key])
        for key in ["current_status_notes", "next_goal", "current_upgrade_tasks", "upgrade_history"]
    )
