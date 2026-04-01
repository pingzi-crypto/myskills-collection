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
HANDOFF_INPUT = REPO_ROOT / "analysis" / "learning-card-handoff-parser" / "inputs" / "concept-create-handoff.txt"
PACKET_BUILDER = REPO_ROOT / "skills" / "shared" / "learning-card-core" / "scripts" / "build_operator_packet_from_handoff.py"
WRAPPER = REPO_ROOT / "skills" / "shared" / "learning-card-core" / "scripts" / "use_operator_packet.ps1"
PROJECT_WRAPPER = REPO_ROOT / "scripts" / "use_learning_card_operator_packet.ps1"


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


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    manifest: list[dict[str, str]] = []

    json_run = subprocess.run(
        [
            sys.executable,
            str(PACKET_BUILDER),
            "--handoff-file",
            str(HANDOFF_INPUT),
            "--format",
            "json",
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    packet_text = json_run.stdout
    packet = json.loads(packet_text)

    if packet["skill"] != "$obsidian-concept-card-capture":
        failures.append("packet json skill mismatch")
    if packet["mode"] != "create":
        failures.append("packet json mode mismatch")
    if "Created file:" not in packet["completion_markers"]:
        failures.append("packet json missing create completion marker")

    packet_json_path = OUTPUT_DIR / "concept-create-operator-packet.json"
    packet_json_path.write_text(packet_text, encoding="utf-8")
    manifest.append(
        {
            "name": "concept-create-operator-packet-json",
            "output": str(packet_json_path.relative_to(REPO_ROOT)).replace("\\", "/"),
            "sha256": sha256_text(packet_text),
        }
    )

    shell = resolve_powershell_executable()
    handoff_text = HANDOFF_INPUT.read_text(encoding="utf-8")
    set_clipboard_text(shell, handoff_text)
    subprocess.run(
        [shell, "-File", str(WRAPPER)],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    clipboard_text = get_clipboard_text(shell)
    if "Operator packet ready." in clipboard_text:
        failures.append("shared wrapper clipboard should contain prompt only, not packet summary")
    if "Use $obsidian-concept-card-capture" not in clipboard_text:
        failures.append("shared wrapper clipboard prompt missing downstream skill line")

    wrapper_run = subprocess.run(
        [
            shell,
            "-File",
            str(WRAPPER),
            "-HandoffFile",
            str(HANDOFF_INPUT),
            "-PrintOnly",
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    wrapper_text = wrapper_run.stdout
    wrapper_output_path = OUTPUT_DIR / "concept-create-operator-packet.txt"
    wrapper_output_path.write_text(wrapper_text, encoding="utf-8")
    manifest.append(
        {
            "name": "concept-create-operator-packet-text",
            "output": str(wrapper_output_path.relative_to(REPO_ROOT)).replace("\\", "/"),
            "sha256": sha256_text(wrapper_text),
        }
    )

    required_phrases = [
        "Operator packet ready.",
        "Status: Execution prompt ready only. No card file has been created, updated, or reviewed yet.",
        "Downstream skill: $obsidian-concept-card-capture",
        "Mode: create",
        "Completion proof: Created file:, Summary:",
        "Still needed: title, keywords or thread points, domain, vault root",
        "Next action:",
        "Execution prompt preview:",
        "Use $obsidian-concept-card-capture to work on one concept card from this thread.",
    ]
    for phrase in required_phrases:
        if phrase not in wrapper_text:
            failures.append(f"wrapper output missing phrase: {phrase}")

    project_wrapper_run = subprocess.run(
        [
            shell,
            "-File",
            str(PROJECT_WRAPPER),
            "-HandoffFile",
            str(HANDOFF_INPUT),
            "-PrintOnly",
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    project_wrapper_text = project_wrapper_run.stdout
    if project_wrapper_text != wrapper_text:
        failures.append("project wrapper output mismatch")

    set_clipboard_text(shell, handoff_text)
    subprocess.run(
        [shell, "-File", str(PROJECT_WRAPPER)],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    project_clipboard_text = get_clipboard_text(shell)
    if "Operator packet ready." in project_clipboard_text:
        failures.append("project wrapper clipboard should contain prompt only, not packet summary")
    if project_clipboard_text != clipboard_text:
        failures.append("project wrapper clipboard prompt mismatch")

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
