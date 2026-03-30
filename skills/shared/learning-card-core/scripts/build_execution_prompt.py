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


def render_prompt(args: argparse.Namespace) -> str:
    config = CARD_CONFIG[args.card_type]
    skill = config["skill"]
    lines: list[str] = [
        f"Use {skill} to work on one {config['label']} card from this thread.",
        f"Mode: {args.mode}",
    ]

    if args.capture_anchor:
        lines.append(f"Capture anchor: {args.capture_anchor.strip()}")

    if args.mode == "create":
        lines.append(f"{config['title_label']}: {placeholder(args.title, f'<single {config['label']}>')}")
        lines.extend(
            bullet_block(
                "Keywords or thread points to capture",
                args.point,
                "<keywords or short excerpts>",
            )
        )
        lines.append(f"Domain: {placeholder(args.domain, '<domain>')}")
        lines.append(f"Subdomain: {placeholder(args.subdomain, '<optional subdomain>')}")
        lines.append(f"Source: {placeholder(args.source, '<optional source>')}")
        lines.append(f"Vault root: {placeholder(args.vault_root, '<optional vault path>')}")
        return "\n".join(lines)

    lines.append(
        f"{config['existing_label']}: "
        f"{placeholder(args.existing_card or args.title, '<existing card path or title>')}"
    )
    if args.mode == "update":
        lines.extend(
            bullet_block(
                "Keywords or thread points to merge",
                args.point,
                "<keywords or short excerpts>",
            )
        )
    else:
        lines.extend(
            bullet_block(
                "Promotion evidence from this thread",
                args.point,
                "<evidence or short excerpts>",
            )
        )
    lines.append(f"Source: {placeholder(args.source, '<optional source>')}")
    lines.append(f"Vault root: {placeholder(args.vault_root, '<optional vault path>')}")
    return "\n".join(lines)


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
