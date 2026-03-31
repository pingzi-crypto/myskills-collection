#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
ANALYSIS_DIR = REPO_ROOT / "analysis" / "learning-card-handoff-parser"
INPUT_DIR = ANALYSIS_DIR / "inputs"
OUTPUT_DIR = ANALYSIS_DIR / "outputs"
SCRIPT_PATH = (
    REPO_ROOT
    / "skills"
    / "shared"
    / "learning-card-core"
    / "scripts"
    / "build_execution_prompt_from_handoff.py"
)

CASES = [
    {
        "name": "concept-create-prompt",
        "input": "concept-create-handoff.txt",
        "output": "concept-create-prompt.txt",
    },
    {
        "name": "method-update-prompt",
        "input": "method-update-handoff.txt",
        "output": "method-update-prompt.txt",
    },
    {
        "name": "misconception-review-prompt",
        "input": "misconception-review-handoff.txt",
        "output": "misconception-review-prompt.txt",
    },
]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest().upper()


def run_case(case: dict[str, str]) -> tuple[str, str]:
    input_path = INPUT_DIR / case["input"]
    file_run = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "--handoff-file", str(input_path)],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    stdin_run = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "--stdin"],
        check=True,
        capture_output=True,
        input=input_path.read_text(encoding="utf-8"),
        text=True,
        encoding="utf-8",
    )
    if file_run.stdout != stdin_run.stdout:
        raise ValueError(f"{case['name']} produced different output for --handoff-file and --stdin")

    text = file_run.stdout
    if not text.endswith("\n"):
        text += "\n"
    return text, sha256_text(text)


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    manifest: list[dict[str, str]] = []

    for case in CASES:
        text, digest = run_case(case)
        output_path = OUTPUT_DIR / case["output"]
        output_path.write_text(text, encoding="utf-8")

        manifest.append(
            {
                "name": case["name"],
                "output": str(output_path.relative_to(REPO_ROOT)).replace("\\", "/"),
                "sha256": digest,
            }
        )

        if "Use $obsidian-" not in text:
            failures.append(f"{case['name']} missing downstream skill line")
        if "Mode:" not in text:
            failures.append(f"{case['name']} missing mode line")

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
