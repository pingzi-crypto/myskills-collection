#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


CARD_CONFIG = {
    "concept": {
        "skill": "$obsidian-concept-card-capture",
        "label": "concept",
        "title_label": "Concept title",
        "existing_label": "Existing concept card",
    },
    "mechanism": {
        "skill": "$obsidian-mechanism-card-capture",
        "label": "mechanism",
        "title_label": "Mechanism title",
        "existing_label": "Existing mechanism card",
    },
    "method": {
        "skill": "$obsidian-method-card-capture",
        "label": "method",
        "title_label": "Method title",
        "existing_label": "Existing method card",
    },
    "misconception": {
        "skill": "$obsidian-misconception-card-capture",
        "label": "misconception",
        "title_label": "Misconception title",
        "existing_label": "Existing misconception card",
    },
}


def normalize_mode(value: str) -> str:
    text = " ".join(value.strip().lower().replace("-", " ").split())
    if text not in {"create", "update", "promotion review"}:
        raise argparse.ArgumentTypeError("mode must be one of: create, update, promotion review")
    return text


def bullet_block(header: str, points: list[str], placeholder: str) -> list[str]:
    lines = [f"{header}:"]
    if points:
        lines.extend([f"- {point}" for point in points])
    else:
        lines.append(f"- {placeholder}")
    return lines


def placeholder(value: str | None, default: str) -> str:
    text = (value or "").strip()
    return text if text else default


def render_prompt_from_values(
    *,
    card_type: str,
    mode: str,
    capture_anchor: str | None = None,
    title: str | None = None,
    existing_card: str | None = None,
    points: list[str] | None = None,
    domain: str | None = None,
    subdomain: str | None = None,
    source: str | None = None,
    vault_root: str | None = None,
) -> str:
    config = CARD_CONFIG[card_type]
    skill = config["skill"]
    point_values = points or []
    lines: list[str] = [
        f"Use {skill} to work on one {config['label']} card from this thread.",
        f"Mode: {mode}",
    ]

    if capture_anchor:
        lines.append(f"Capture anchor: {capture_anchor.strip()}")

    if mode == "create":
        lines.append(f"{config['title_label']}: {placeholder(title, f'<single {config['label']}>')}")
        lines.extend(
            bullet_block(
                "Keywords or thread points to capture",
                point_values,
                "<keywords or short excerpts>",
            )
        )
        lines.append(f"Domain: {placeholder(domain, '<domain>')}")
        lines.append(f"Subdomain: {placeholder(subdomain, '<optional subdomain>')}")
        lines.append(f"Source: {placeholder(source, '<optional source>')}")
        lines.append(f"Vault root: {placeholder(vault_root, '<optional vault path>')}")
        return "\n".join(lines)

    lines.append(
        f"{config['existing_label']}: "
        f"{placeholder(existing_card or title, '<existing card path or title>')}"
    )
    if mode == "update":
        lines.extend(
            bullet_block(
                "Keywords or thread points to merge",
                point_values,
                "<keywords or short excerpts>",
            )
        )
    else:
        lines.extend(
            bullet_block(
                "Promotion evidence from this thread",
                point_values,
                "<evidence or short excerpts>",
            )
        )
    lines.append(f"Source: {placeholder(source, '<optional source>')}")
    lines.append(f"Vault root: {placeholder(vault_root, '<optional vault path>')}")
    return "\n".join(lines)


def render_prompt(args: argparse.Namespace) -> str:
    return render_prompt_from_values(
        card_type=args.card_type,
        mode=args.mode,
        capture_anchor=args.capture_anchor,
        title=args.title,
        existing_card=args.existing_card,
        points=args.point,
        domain=args.domain,
        subdomain=args.subdomain,
        source=args.source,
        vault_root=args.vault_root,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a downstream learning-card execution prompt from a router result."
    )
    parser.add_argument(
        "--card-type",
        required=True,
        choices=sorted(CARD_CONFIG),
        help="One of: concept, mechanism, method, misconception.",
    )
    parser.add_argument(
        "--mode",
        required=True,
        type=normalize_mode,
        help="One of: create, update, promotion review.",
    )
    parser.add_argument("--capture-anchor", help="Optional resolved capture anchor text.")
    parser.add_argument("--title", help="Create title, or fallback existing card label for update/review.")
    parser.add_argument("--existing-card", help="Existing card path or title for update/review.")
    parser.add_argument(
        "--point",
        action="append",
        default=[],
        help="Repeatable thread point, keyword, or evidence line.",
    )
    parser.add_argument("--domain", help="Optional domain, mainly used for create.")
    parser.add_argument("--subdomain", help="Optional subdomain, mainly used for create.")
    parser.add_argument("--source", help="Optional source string.")
    parser.add_argument("--vault-root", help="Optional Obsidian vault root.")
    parser.add_argument("--output", help="Optional output file path. Prints to stdout when omitted.")
    args = parser.parse_args()

    prompt = render_prompt(args)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(prompt + "\n", encoding="utf-8")
    else:
        print(prompt)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
