#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
ANALYSIS_DIR = REPO_ROOT / "analysis" / "learning-card-preflight-gate-acceptance"
INPUT_DIR = ANALYSIS_DIR / "inputs"
OUTPUT_DIR = ANALYSIS_DIR / "outputs"
PRECHECK_OUTPUT_DIR = REPO_ROOT / "analysis" / "learning-card-bridge-live-preflight" / "outputs"
WRAPPER = REPO_ROOT / "scripts" / "use_learning_card_preflight_gate.ps1"

GO_CASES = [
    ("concept-update-gate", PRECHECK_OUTPUT_DIR / "concept-update-bridge-packet-check.json"),
    ("method-promotion-review-gate", PRECHECK_OUTPUT_DIR / "method-promotion-review-bridge-packet-check.json"),
    ("misconception-ambiguous-create-gate", PRECHECK_OUTPUT_DIR / "misconception-ambiguous-create-bridge-packet-check.json"),
    ("misconception-bridge-create-gate", PRECHECK_OUTPUT_DIR / "misconception-bridge-create-bridge-packet-check.json"),
]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest().upper()


def resolve_powershell_executable() -> str:
    for candidate in ("pwsh", "powershell"):
        if shutil.which(candidate):
            return candidate
    raise RuntimeError("No PowerShell executable found. Install pwsh or make powershell available on PATH.")


def run_wrapper(shell: str, check_file: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [shell, "-File", str(WRAPPER), "-CheckFile", str(check_file)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shell = resolve_powershell_executable()
    failures: list[str] = []
    manifest: list[dict[str, str]] = []

    for name, check_file in GO_CASES:
        completed = run_wrapper(shell, check_file)
        if completed.returncode != 0:
            failures.append(f"{name} returned {completed.returncode}, expected 0")
        text = completed.stdout
        output_path = OUTPUT_DIR / f"{name}.txt"
        output_path.write_text(text, encoding="utf-8")
        manifest.append(
            {
                "name": name,
                "output": str(output_path.relative_to(REPO_ROOT)).replace("\\", "/"),
                "sha256": sha256_text(text),
            }
        )

        expected = json.loads(check_file.read_text(encoding="utf-8"))
        required_phrases = [
            "Bridge preflight gate ready.",
            "Gate: GO",
            f"Skill: {expected['expected_skill']}",
            f"Mode: {expected['mode']}",
            f"Target: {expected['expected_target_path']}",
            f"Prompt packet: {expected['prompt_output']}",
        ]
        for phrase in required_phrases:
            if phrase not in text:
                failures.append(f"{name} output missing phrase: {phrase}")

    no_go_file = INPUT_DIR / "synthetic-no-go-check.json"
    no_go_completed = run_wrapper(shell, no_go_file)
    if no_go_completed.returncode != 2:
        failures.append(f"synthetic-no-go-gate returned {no_go_completed.returncode}, expected 2")
    no_go_text = no_go_completed.stdout
    no_go_output_path = OUTPUT_DIR / "synthetic-no-go-gate.txt"
    no_go_output_path.write_text(no_go_text, encoding="utf-8")
    manifest.append(
        {
            "name": "synthetic-no-go-gate",
            "output": str(no_go_output_path.relative_to(REPO_ROOT)).replace("\\", "/"),
            "sha256": sha256_text(no_go_text),
        }
    )

    for phrase in (
        "Bridge preflight gate ready.",
        "Gate: NO-GO",
        "Placeholder free: False",
        "Blocking placeholders: <single concept>, <domain>",
    ):
        if phrase not in no_go_text:
            failures.append(f"synthetic-no-go-gate output missing phrase: {phrase}")

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
