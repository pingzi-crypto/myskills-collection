#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
ANALYSIS_DIR = REPO_ROOT / "analysis" / "learning-card-operator-packet-acceptance"
OUTPUT_DIR = ANALYSIS_DIR / "outputs"
PACKET_BUILDER = REPO_ROOT / "skills" / "shared" / "learning-card-core" / "scripts" / "build_operator_packet_from_handoff.py"
WRAPPER = REPO_ROOT / "skills" / "shared" / "learning-card-core" / "scripts" / "use_operator_packet.ps1"
PROJECT_WRAPPER = REPO_ROOT / "scripts" / "use_learning_card_operator_packet.ps1"
HANDOFF_DIR = REPO_ROOT / "analysis" / "learning-card-handoff-parser" / "inputs"

CASES = [
    {
        "slug": "concept-create",
        "handoff_input": HANDOFF_DIR / "concept-create-handoff.txt",
        "skill": "$obsidian-concept-card-capture",
        "mode": "create",
        "completion_proof": "Created file:, Summary:",
        "missing_inputs": "title, keywords or thread points, domain, vault root",
        "prompt_line": "Use $obsidian-concept-card-capture to work on one concept card from this thread.",
    },
    {
        "slug": "method-update",
        "handoff_input": HANDOFF_DIR / "method-update-handoff.txt",
        "skill": "$obsidian-method-card-capture",
        "mode": "update",
        "completion_proof": "Updated file:, Summary:",
        "missing_inputs": "existing card title or path confirmation, vault root",
        "prompt_line": "Use $obsidian-method-card-capture to work on one method card from this thread.",
    },
    {
        "slug": "misconception-review",
        "handoff_input": HANDOFF_DIR / "misconception-review-handoff.txt",
        "skill": "$obsidian-misconception-card-capture",
        "mode": "promotion review",
        "completion_proof": "Reviewed file:, Promotion result:, Summary:",
        "missing_inputs": "existing card title or path confirmation, vault root",
        "prompt_line": "Use $obsidian-misconception-card-capture to work on one misconception card from this thread.",
    },
]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest().upper()


def resolve_powershell_executable() -> str:
    for candidate in ("pwsh", "powershell"):
        if shutil.which(candidate):
            return candidate
    raise RuntimeError("No PowerShell executable found. Install pwsh or make powershell available on PATH.")


def set_clipboard_text(shell: str, text: str) -> None:
    subprocess.run(
        [shell, "-NoProfile", "-Command", "Set-Clipboard -Value @'\n" + text + "\n'@"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def get_clipboard_text(shell: str) -> str:
    completed = subprocess.run(
        [shell, "-NoProfile", "-Command", "Get-Clipboard -Raw"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return completed.stdout


def run_command(arguments: list[str]) -> str:
    completed = subprocess.run(
        arguments,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return completed.stdout


def verify_case(case: dict[str, str | Path], shell: str) -> tuple[list[str], list[dict[str, str]]]:
    failures: list[str] = []
    manifest: list[dict[str, str]] = []
    slug = str(case["slug"])
    handoff_input = Path(case["handoff_input"])
    handoff_text = handoff_input.read_text(encoding="utf-8")

    packet_text = run_command(
        [
            sys.executable,
            str(PACKET_BUILDER),
            "--handoff-file",
            str(handoff_input),
            "--format",
            "json",
        ]
    )
    packet = json.loads(packet_text)

    if packet["skill"] != case["skill"]:
        failures.append(f"{slug}: packet json skill mismatch")
    if packet["mode"] != case["mode"]:
        failures.append(f"{slug}: packet json mode mismatch")
    if packet["completion_markers"] != str(case["completion_proof"]).split(", "):
        failures.append(f"{slug}: packet json completion markers mismatch")

    packet_json_path = OUTPUT_DIR / f"{slug}-operator-packet.json"
    packet_json_path.write_text(packet_text, encoding="utf-8")
    manifest.append(
        {
            "name": f"{slug}-operator-packet-json",
            "output": str(packet_json_path.relative_to(REPO_ROOT)).replace("\\", "/"),
            "sha256": sha256_text(packet_text),
        }
    )

    set_clipboard_text(shell, handoff_text)
    run_command([shell, "-File", str(WRAPPER), "-HandoffFile", str(handoff_input)])
    shared_clipboard_text = get_clipboard_text(shell)
    if "Operator packet ready." in shared_clipboard_text:
        failures.append(f"{slug}: shared wrapper clipboard should contain prompt only, not packet summary")
    if str(case["prompt_line"]) not in shared_clipboard_text:
        failures.append(f"{slug}: shared wrapper clipboard prompt missing downstream skill line")

    wrapper_text = run_command(
        [
            shell,
            "-File",
            str(WRAPPER),
            "-HandoffFile",
            str(handoff_input),
            "-PrintOnly",
        ]
    )
    wrapper_output_path = OUTPUT_DIR / f"{slug}-operator-packet.txt"
    wrapper_output_path.write_text(wrapper_text, encoding="utf-8")
    manifest.append(
        {
            "name": f"{slug}-operator-packet-text",
            "output": str(wrapper_output_path.relative_to(REPO_ROOT)).replace("\\", "/"),
            "sha256": sha256_text(wrapper_text),
        }
    )

    required_phrases = [
        "Operator packet ready.",
        "Status: Execution prompt ready only. No card file has been created, updated, or reviewed yet.",
        f"Downstream skill: {case['skill']}",
        f"Mode: {case['mode']}",
        f"Completion proof: {case['completion_proof']}",
        f"Still needed: {case['missing_inputs']}",
        "Next action:",
        "Execution prompt preview:",
        str(case["prompt_line"]),
    ]
    for phrase in required_phrases:
        if phrase not in wrapper_text:
            failures.append(f"{slug}: wrapper output missing phrase: {phrase}")

    project_wrapper_text = run_command(
        [
            shell,
            "-File",
            str(PROJECT_WRAPPER),
            "-HandoffFile",
            str(handoff_input),
            "-PrintOnly",
        ]
    )
    if project_wrapper_text != wrapper_text:
        failures.append(f"{slug}: project wrapper output mismatch")

    set_clipboard_text(shell, handoff_text)
    run_command([shell, "-File", str(PROJECT_WRAPPER), "-HandoffFile", str(handoff_input)])
    project_clipboard_text = get_clipboard_text(shell)
    if "Operator packet ready." in project_clipboard_text:
        failures.append(f"{slug}: project wrapper clipboard should contain prompt only, not packet summary")
    if project_clipboard_text != shared_clipboard_text:
        failures.append(f"{slug}: project wrapper clipboard prompt mismatch")

    return failures, manifest


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    manifest: list[dict[str, str]] = []
    shell = resolve_powershell_executable()

    for case in CASES:
        case_failures, case_manifest = verify_case(case, shell)
        failures.extend(case_failures)
        manifest.extend(case_manifest)

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
