#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_execution_prompt import render_prompt_from_values


CARD_TYPE_MAP = {
    "concept": "concept",
    "mechanism": "mechanism",
    "method": "method",
    "misconception": "misconception",
}


def clean_value(value: str) -> str:
    text = value.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in {"`", '"', "'"}:
        return text[1:-1].strip()
    return text


def normalize_mode(value: str) -> str:
    return " ".join(value.strip().lower().replace("-", " ").split())


def parse_handoff(text: str) -> dict[str, object]:
    card_type = None
    mode = None
    capture_anchor = None
    missing_inputs: list[str] = []

    in_missing = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            if in_missing:
                in_missing = False
            continue

        if line.startswith("Capture anchor:"):
            capture_anchor = clean_value(line.split(":", 1)[1])
            continue

        if line.startswith("Route result:"):
            route_value = clean_value(line.split(":", 1)[1]).lower()
            route_value = route_value.strip("`")
            if route_value not in CARD_TYPE_MAP:
                raise ValueError(f"Unsupported route result: {route_value}")
            card_type = CARD_TYPE_MAP[route_value]
            continue

        if line.startswith("Mode:"):
            mode_value = clean_value(line.split(":", 1)[1]).strip("`")
            mode = normalize_mode(mode_value)
            if mode not in {"create", "update", "promotion review"}:
                raise ValueError(f"Unsupported mode: {mode_value}")
            continue

        if line.startswith("Still needed before write:"):
            in_missing = True
            continue

        if in_missing and line.startswith("- "):
            missing_inputs.append(clean_value(line[2:]))
            continue

        if in_missing and not line.startswith("- "):
            in_missing = False

    if not card_type:
        raise ValueError("Handoff text is missing Route result.")
    if not mode:
        raise ValueError("Handoff text is missing Mode.")

    return {
        "card_type": card_type,
        "mode": mode,
        "capture_anchor": capture_anchor or "",
        "missing_inputs": missing_inputs,
    }


def infer_placeholders(mode: str, missing_inputs: list[str]) -> dict[str, str]:
    joined = " | ".join(item.lower() for item in missing_inputs)
    values: dict[str, str] = {}

    if mode == "create":
        if "title" in joined:
            values["title"] = ""
        if "domain" in joined:
            values["domain"] = ""
        if "subdomain" in joined:
            values["subdomain"] = ""
        if "vault root" in joined:
            values["vault_root"] = ""
    else:
        if "existing card" in joined or "title or path" in joined or "path confirmation" in joined:
            values["existing_card"] = ""
        if "vault root" in joined:
            values["vault_root"] = ""

    return values


def extract_points(args: argparse.Namespace, mode: str) -> list[str]:
    if args.point:
        return args.point
    if mode == "promotion review":
        return ["<evidence or short excerpts>"]
    if mode == "update":
        return ["<keywords or short excerpts>"]
    return ["<keywords or short excerpts>"]


def build_from_handoff(args: argparse.Namespace) -> str:
    handoff_text = Path(args.handoff_file).read_text(encoding="utf-8") if args.handoff_file else args.handoff_text
    if not handoff_text:
        raise ValueError("Provide either --handoff-file or --handoff-text.")

    parsed = parse_handoff(handoff_text)
    inferred = infer_placeholders(parsed["mode"], parsed["missing_inputs"])

    return render_prompt_from_values(
        card_type=parsed["card_type"],
        mode=parsed["mode"],
        capture_anchor=args.capture_anchor or str(parsed["capture_anchor"]),
        title=args.title if args.title is not None else inferred.get("title"),
        existing_card=args.existing_card if args.existing_card is not None else inferred.get("existing_card"),
        points=extract_points(args, str(parsed["mode"])),
        domain=args.domain if args.domain is not None else inferred.get("domain"),
        subdomain=args.subdomain if args.subdomain is not None else inferred.get("subdomain"),
        source=args.source,
        vault_root=args.vault_root if args.vault_root is not None else inferred.get("vault_root"),
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build an execution prompt skeleton from router handoff text."
    )
    parser.add_argument("--handoff-file", help="Path to router handoff text.")
    parser.add_argument("--handoff-text", help="Inline router handoff text.")
    parser.add_argument("--capture-anchor", help="Optional override for capture anchor.")
    parser.add_argument("--title", help="Optional title override.")
    parser.add_argument("--existing-card", help="Optional existing-card override.")
    parser.add_argument("--point", action="append", default=[], help="Repeatable point or evidence line.")
    parser.add_argument("--domain", help="Optional domain override.")
    parser.add_argument("--subdomain", help="Optional subdomain override.")
    parser.add_argument("--source", help="Optional source string.")
    parser.add_argument("--vault-root", help="Optional vault-root override.")
    parser.add_argument("--output", help="Optional output file path.")
    args = parser.parse_args()

    if not args.handoff_file and not args.handoff_text:
        parser.error("Provide either --handoff-file or --handoff-text.")

    prompt = build_from_handoff(args)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(prompt + "\n", encoding="utf-8")
    else:
        print(prompt)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
