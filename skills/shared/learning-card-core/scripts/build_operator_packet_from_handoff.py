#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_execution_prompt import CARD_CONFIG
from build_execution_prompt_from_handoff import (
    build_from_handoff,
    parse_handoff,
    resolve_handoff_text,
)


COMPLETION_MARKERS = {
    "create": ["Created file:", "Summary:"],
    "update": ["Updated file:", "Summary:"],
    "promotion review": ["Reviewed file:", "Promotion result:", "Summary:"],
}


def build_packet(args: argparse.Namespace) -> dict[str, object]:
    handoff_text = resolve_handoff_text(args)
    if not handoff_text:
        raise ValueError(
            "Provide router handoff text with --handoff-file, --handoff-text, --stdin, or --from-clipboard."
        )

    parsed = parse_handoff(handoff_text)
    prompt = build_from_handoff(args)
    card_type = str(parsed["card_type"])
    mode = str(parsed["mode"])
    skill = CARD_CONFIG[card_type]["skill"]
    completion_markers = COMPLETION_MARKERS[mode]

    return {
        "card_type": card_type,
        "mode": mode,
        "skill": skill,
        "capture_anchor": str(parsed["capture_anchor"]),
        "missing_inputs": list(parsed["missing_inputs"]),
        "completion_markers": completion_markers,
        "next_action": (
            f"Paste the execution prompt into the next turn and continue with {skill} "
            f"until the result shows {', '.join(completion_markers)}."
        ),
        "prompt": prompt,
    }


def render_text(packet: dict[str, object]) -> str:
    completion_markers = ", ".join(packet["completion_markers"])
    missing_inputs = packet["missing_inputs"]

    lines = [
        "Operator packet ready.",
        f"Downstream skill: {packet['skill']}",
        f"Mode: {packet['mode']}",
        f"Completion proof: {completion_markers}",
    ]

    if missing_inputs:
        lines.append(f"Write-critical inputs now covered: {', '.join(str(item) for item in missing_inputs)}")

    lines.extend(
        [
            f"Next action: {packet['next_action']}",
            "",
            "Execution prompt:",
            str(packet["prompt"]),
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build an operator-facing packet from canonical router handoff text."
    )
    parser.add_argument("--handoff-file", help="Path to router handoff text.")
    parser.add_argument("--handoff-text", help="Inline router handoff text.")
    parser.add_argument("--stdin", action="store_true", help="Read router handoff text from stdin.")
    parser.add_argument(
        "--from-clipboard",
        action="store_true",
        help="Read router handoff text from the system clipboard.",
    )
    parser.add_argument("--capture-anchor", help="Optional override for capture anchor.")
    parser.add_argument("--title", help="Optional title override.")
    parser.add_argument("--existing-card", help="Optional existing-card override.")
    parser.add_argument("--point", action="append", default=[], help="Repeatable point or evidence line.")
    parser.add_argument("--domain", help="Optional domain override.")
    parser.add_argument("--subdomain", help="Optional subdomain override.")
    parser.add_argument("--source", help="Optional source string.")
    parser.add_argument("--vault-root", help="Optional vault-root override.")
    parser.add_argument("--output", help="Optional output file path.")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format for the operator packet.",
    )
    args = parser.parse_args()

    try:
        packet = build_packet(args)
    except (RuntimeError, ValueError) as exc:
        parser.error(str(exc))

    if args.format == "json":
        output_text = json.dumps(packet, ensure_ascii=False, indent=2) + "\n"
    else:
        output_text = render_text(packet) + "\n"

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output_text, encoding="utf-8")
    else:
        print(output_text, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
