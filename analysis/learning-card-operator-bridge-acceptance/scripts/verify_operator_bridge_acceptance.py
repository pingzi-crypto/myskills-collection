#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
ANALYSIS_DIR = REPO_ROOT / "analysis" / "learning-card-operator-bridge-acceptance"
OUTPUT_DIR = ANALYSIS_DIR / "outputs"

WRAPPER_PATH = (
    REPO_ROOT
    / "skills"
    / "shared"
    / "learning-card-core"
    / "scripts"
    / "use_handoff_bridge.ps1"
)
PARSER_INPUT_DIR = REPO_ROOT / "analysis" / "learning-card-handoff-parser" / "inputs"
PARSER_OUTPUT_DIR = REPO_ROOT / "analysis" / "learning-card-handoff-parser" / "outputs"

CASES = [
    {
        "name": "concept-create-wrapper-printonly",
        "input": "concept-create-handoff.txt",
        "expected": "concept-create-prompt.txt",
        "output": "concept-create-wrapper-printonly.txt",
    },
    {
        "name": "method-update-wrapper-printonly",
        "input": "method-update-handoff.txt",
        "expected": "method-update-prompt.txt",
        "output": "method-update-wrapper-printonly.txt",
    },
    {
        "name": "misconception-review-wrapper-printonly",
        "input": "misconception-review-handoff.txt",
        "expected": "misconception-review-prompt.txt",
        "output": "misconception-review-wrapper-printonly.txt",
    },
]


def resolve_powershell_executable() -> str:
    for candidate in ("pwsh", "powershell"):
        if shutil.which(candidate):
            return candidate
    raise RuntimeError("No PowerShell executable found. Install pwsh or make powershell available on PATH.")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest().upper()


def run_wrapper_printonly(input_path: Path) -> str:
    shell = resolve_powershell_executable()
    completed = subprocess.run(
        [
            shell,
            "-File",
            str(WRAPPER_PATH),
            "-HandoffFile",
            str(input_path),
            "-PrintOnly",
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    text = completed.stdout
    if not text.endswith("\n"):
        text += "\n"
    return text


def run_wrapper_clipboard_smoke(input_path: Path) -> str:
    shell = resolve_powershell_executable()
    command = (
        f"$text = Get-Content -Path '{input_path}' -Raw -Encoding utf8; "
        "Set-Clipboard -Value $text; "
        "Start-Sleep -Milliseconds 300; "
        f"& '{shell}' -File '{WRAPPER_PATH}' | Out-Null; "
        "Start-Sleep -Milliseconds 300; "
        "Get-Clipboard -Raw"
    )
    completed = subprocess.run(
        [shell, "-NoProfile", "-Command", command],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return completed.stdout


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    manifest: list[dict[str, str]] = []

    for case in CASES:
        input_path = PARSER_INPUT_DIR / case["input"]
        expected_path = PARSER_OUTPUT_DIR / case["expected"]
        expected_text = expected_path.read_text(encoding="utf-8")
        if not expected_text.endswith("\n"):
            expected_text += "\n"

        actual_text = run_wrapper_printonly(input_path)
        output_path = OUTPUT_DIR / case["output"]
        output_path.write_text(actual_text, encoding="utf-8")

        if actual_text != expected_text:
            failures.append(f"{case['name']} print-only output does not match parser output")

        manifest.append(
            {
                "name": case["name"],
                "output": str(output_path.relative_to(REPO_ROOT)).replace("\\", "/"),
                "sha256": sha256_text(actual_text),
            }
        )

    concept_input = PARSER_INPUT_DIR / "concept-create-handoff.txt"
    concept_expected = (PARSER_OUTPUT_DIR / "concept-create-prompt.txt").read_text(encoding="utf-8")
    clipboard_text = run_wrapper_clipboard_smoke(concept_input)
    clipboard_output_path = OUTPUT_DIR / "concept-create-wrapper-clipboard.txt"
    clipboard_output_path.write_text(clipboard_text, encoding="utf-8")

    if "Use $obsidian-concept-card-capture" not in clipboard_text:
        failures.append("clipboard smoke test did not place execution prompt on clipboard")

    manifest.append(
        {
            "name": "concept-create-wrapper-clipboard",
            "output": str(clipboard_output_path.relative_to(REPO_ROOT)).replace("\\", "/"),
            "sha256": sha256_text(clipboard_text),
        }
    )

    if concept_expected.strip() != clipboard_text.strip():
        failures.append("clipboard smoke test output differs from expected concept prompt")

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
