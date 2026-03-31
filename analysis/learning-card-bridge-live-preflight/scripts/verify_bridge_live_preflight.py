#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
ANALYSIS_DIR = REPO_ROOT / "analysis" / "learning-card-bridge-live-preflight"
CASE_DIR = ANALYSIS_DIR / "cases"
OUTPUT_DIR = ANALYSIS_DIR / "outputs"
BRIDGE_SCRIPT = (
    REPO_ROOT
    / "skills"
    / "shared"
    / "learning-card-core"
    / "scripts"
    / "build_execution_prompt_from_handoff.py"
)

CARD_TYPE_DIR = {
    "concept": "Concepts",
    "mechanism": "Mechanisms",
    "method": "Methods",
    "misconception": "Misconceptions",
}

PLACEHOLDER_RE = re.compile(r"<[^>\n]+>")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest().upper()


def build_prompt(case: dict[str, object]) -> str:
    command = [
        sys.executable,
        str(BRIDGE_SCRIPT),
        "--handoff-file",
        str(ANALYSIS_DIR / str(case["handoff_file"])),
    ]

    if case.get("title"):
        command += ["--title", str(case["title"])]
    if case.get("existing_card"):
        command += ["--existing-card", str(case["existing_card"])]
    if case.get("domain"):
        command += ["--domain", str(case["domain"])]
    if case.get("subdomain"):
        command += ["--subdomain", str(case["subdomain"])]
    if case.get("source"):
        command += ["--source", str(case["source"])]
    if case.get("vault_root"):
        command += ["--vault-root", str(case["vault_root"])]

    for point in case.get("points", []):
        command += ["--point", str(point)]

    completed = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    text = completed.stdout
    if not text.endswith("\n"):
        text += "\n"
    return text


def expected_target_path(case: dict[str, object]) -> str:
    mode = str(case["mode"])
    if mode == "create":
        vault_root = str(case["vault_root"])
        title = str(case["title"])
        card_dir = CARD_TYPE_DIR[str(case["card_type"])]
        return str(Path(vault_root) / "学习" / "Cards" / card_dir / f"{title}.md")
    return str(case["existing_card"])


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    manifest: list[dict[str, str]] = []

    for case_path in sorted(CASE_DIR.glob("*.json")):
        case = json.loads(case_path.read_text(encoding="utf-8"))
        prompt = build_prompt(case)
        output_path = OUTPUT_DIR / str(case["output"])
        output_path.write_text(prompt, encoding="utf-8")

        linked_live_case_path = REPO_ROOT / str(case["linked_live_case"])
        if not linked_live_case_path.exists():
            failures.append(f"{case['name']} linked live case missing: {linked_live_case_path}")
            linked_live_case = {}
        else:
            linked_live_case = json.loads(linked_live_case_path.read_text(encoding="utf-8"))

        if str(case["expected_skill"]) not in prompt:
            failures.append(f"{case['name']} prompt missing expected downstream skill")

        if f"Mode: {case['mode']}" not in prompt:
            failures.append(f"{case['name']} prompt missing expected mode")

        for phrase in case.get("required_prompt_phrases", []):
            if phrase not in prompt:
                failures.append(f"{case['name']} prompt missing phrase: {phrase}")

        placeholders = sorted(set(PLACEHOLDER_RE.findall(prompt)))
        if placeholders:
            failures.append(
                f"{case['name']} prompt still contains unresolved placeholders: {', '.join(placeholders)}"
            )

        expected_path = expected_target_path(case)
        linked_target = str(linked_live_case.get("target_path", ""))
        if linked_target and linked_target != expected_path:
            failures.append(
                f"{case['name']} expected target {expected_path} does not match linked live case {linked_target}"
            )

        linked_markers = list(linked_live_case.get("expected_result_markers", []))
        expected_primary_marker = {
            "create": "Created file:",
            "update": "Updated file:",
            "promotion review": "Reviewed file:",
        }[str(case["mode"])]
        if linked_markers and expected_primary_marker not in linked_markers:
            failures.append(
                f"{case['name']} linked live case markers do not include {expected_primary_marker}"
            )

        check = {
            "name": case["name"],
            "mode": case["mode"],
            "card_type": case["card_type"],
            "expected_skill": case["expected_skill"],
            "expected_target_path": expected_path,
            "linked_live_case": case["linked_live_case"],
            "linked_live_target_path": linked_target or expected_path,
            "linked_live_result_markers": linked_markers,
            "go_no_go": "go" if not placeholders else "no-go",
            "placeholder_free": not placeholders,
            "placeholder_markers": placeholders,
            "manual_next_step": (
                f"Copy {output_path.name} into the next turn and run {case['expected_skill']} until "
                f"the result shows {', '.join(linked_markers or [expected_primary_marker])}."
            ),
            "expected_completion_markers": linked_markers or [expected_primary_marker],
            "prompt_output": str(output_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        }
        check_path = OUTPUT_DIR / f"{output_path.stem}-check.json"
        check_text = json.dumps(check, ensure_ascii=False, indent=2) + "\n"
        check_path.write_text(check_text, encoding="utf-8")

        manifest.append(
            {
                "name": str(case["name"]),
                "output": str(output_path.relative_to(REPO_ROOT)).replace("\\", "/"),
                "sha256": sha256_text(prompt),
            }
        )
        manifest.append(
            {
                "name": f"{case['name']}-check",
                "output": str(check_path.relative_to(REPO_ROOT)).replace("\\", "/"),
                "sha256": sha256_text(check_text),
            }
        )

    manifest_path = OUTPUT_DIR / "manifest.json"
    manifest_path.write_text(
        json.dumps({"outputs": manifest}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    for item in manifest:
        print(f"PASS: {item['name']} -> {item['sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
