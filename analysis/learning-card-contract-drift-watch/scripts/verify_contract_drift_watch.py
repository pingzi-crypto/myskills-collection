#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
ANALYSIS_DIR = REPO_ROOT / "analysis" / "learning-card-contract-drift-watch"
OUTPUT_DIR = ANALYSIS_DIR / "outputs"

ROUTER_EXECUTION_OUTPUTS = REPO_ROOT / "analysis" / "learning-card-router-execution-contract-regression" / "outputs"
OPERATOR_PACKET_OUTPUTS = REPO_ROOT / "analysis" / "learning-card-operator-packet-acceptance" / "outputs"
EXECUTION_RESULT_OUTPUTS = REPO_ROOT / "analysis" / "learning-card-execution-result-acceptance" / "outputs"
PREFLIGHT_OUTPUTS = REPO_ROOT / "analysis" / "learning-card-bridge-live-preflight" / "outputs"
LIVE_HARNESS_OUTPUTS = REPO_ROOT / "analysis" / "learning-card-live-acceptance-harness" / "outputs"

DAILY_OPERATOR_CASES = [
    {
        "name": "daily-operator-create-watch",
        "mode": "create",
        "router_file": ROUTER_EXECUTION_OUTPUTS / "concept-create-minimum-package.txt",
        "operator_packet_file": OPERATOR_PACKET_OUTPUTS / "concept-create-operator-packet.json",
        "execution_result_file": EXECUTION_RESULT_OUTPUTS / "concept-create-result.txt",
        "expected_skill": "$obsidian-concept-card-capture",
        "expected_markers": ["Created file:", "Summary:"],
    },
    {
        "name": "daily-operator-update-watch",
        "mode": "update",
        "router_file": ROUTER_EXECUTION_OUTPUTS / "method-update-minimum-package.txt",
        "operator_packet_file": OPERATOR_PACKET_OUTPUTS / "method-update-operator-packet.json",
        "execution_result_file": EXECUTION_RESULT_OUTPUTS / "method-update-result.txt",
        "expected_skill": "$obsidian-method-card-capture",
        "expected_markers": ["Updated file:", "Summary:"],
    },
    {
        "name": "daily-operator-review-watch",
        "mode": "promotion review",
        "router_file": ROUTER_EXECUTION_OUTPUTS / "misconception-review-minimum-package.txt",
        "operator_packet_file": OPERATOR_PACKET_OUTPUTS / "misconception-review-operator-packet.json",
        "execution_result_file": EXECUTION_RESULT_OUTPUTS / "misconception-review-result.txt",
        "expected_skill": "$obsidian-misconception-card-capture",
        "expected_markers": ["Reviewed file:", "Promotion result:", "Summary:"],
    },
]

BRIDGE_LIVE_CASES = [
    {
        "name": "bridge-live-update-watch",
        "preflight_check_file": PREFLIGHT_OUTPUTS / "concept-update-bridge-packet-check.json",
        "live_harness_file": LIVE_HARNESS_OUTPUTS / "concept-update-bridge-originated-check.json",
        "expected_skill": "$obsidian-concept-card-capture",
        "expected_markers": ["Updated file:", "Summary:"],
    },
    {
        "name": "bridge-live-review-watch",
        "preflight_check_file": PREFLIGHT_OUTPUTS / "method-promotion-review-bridge-packet-check.json",
        "live_harness_file": LIVE_HARNESS_OUTPUTS / "method-promotion-review-bridge-originated-check.json",
        "expected_skill": "$obsidian-method-card-capture",
        "expected_markers": ["Reviewed file:", "Promotion result:", "Summary:"],
    },
    {
        "name": "bridge-live-create-watch",
        "preflight_check_file": PREFLIGHT_OUTPUTS / "misconception-bridge-create-bridge-packet-check.json",
        "live_harness_file": LIVE_HARNESS_OUTPUTS / "misconception-bridge-originated-create-check.json",
        "expected_skill": "$obsidian-misconception-card-capture",
        "expected_markers": ["Created file:", "Summary:"],
    },
]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest().upper()


def write_json_output(name: str, payload: dict[str, object], manifest: list[dict[str, str]]) -> None:
    output_path = OUTPUT_DIR / f"{name}.json"
    output_text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    output_path.write_text(output_text, encoding="utf-8")
    manifest.append(
        {
            "name": name,
            "output": str(output_path.relative_to(REPO_ROOT)).replace("\\", "/"),
            "sha256": sha256_text(output_text),
        }
    )


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    manifest: list[dict[str, str]] = []

    for case in DAILY_OPERATOR_CASES:
        router_text = case["router_file"].read_text(encoding="utf-8")
        operator_packet = json.loads(case["operator_packet_file"].read_text(encoding="utf-8"))
        execution_result_text = case["execution_result_file"].read_text(encoding="utf-8")

        if f"Mode: {case['mode']}" not in router_text:
            failures.append(f"{case['name']} router file missing mode")
        if f"Downstream skill: {case['expected_skill']}" not in router_text:
            failures.append(f"{case['name']} router file missing downstream skill")
        if operator_packet["mode"] != case["mode"]:
            failures.append(f"{case['name']} operator packet mode mismatch")
        if operator_packet["skill"] != case["expected_skill"]:
            failures.append(f"{case['name']} operator packet skill mismatch")
        if operator_packet["completion_markers"] != case["expected_markers"]:
            failures.append(f"{case['name']} operator packet completion markers mismatch")
        if "Router status: routing complete only" in execution_result_text:
            failures.append(f"{case['name']} execution result still contains router-only status")
        for marker in case["expected_markers"]:
            if marker not in execution_result_text:
                failures.append(f"{case['name']} execution result missing marker: {marker}")

        payload = {
            "watch_line": "daily_operator",
            "mode": case["mode"],
            "expected_skill": case["expected_skill"],
            "router_file": str(case["router_file"].relative_to(REPO_ROOT)).replace("\\", "/"),
            "operator_packet_file": str(case["operator_packet_file"].relative_to(REPO_ROOT)).replace("\\", "/"),
            "execution_result_file": str(case["execution_result_file"].relative_to(REPO_ROOT)).replace("\\", "/"),
            "completion_markers": case["expected_markers"],
            "status": "ok",
        }
        write_json_output(str(case["name"]), payload, manifest)

    for case in BRIDGE_LIVE_CASES:
        preflight_check = json.loads(case["preflight_check_file"].read_text(encoding="utf-8"))
        live_harness = json.loads(case["live_harness_file"].read_text(encoding="utf-8"))
        evidence_chain = live_harness.get("evidence_chain", {})

        if preflight_check["expected_skill"] != case["expected_skill"]:
            failures.append(f"{case['name']} preflight expected_skill mismatch")
        if preflight_check["expected_completion_markers"] != case["expected_markers"]:
            failures.append(f"{case['name']} preflight completion markers mismatch")
        if preflight_check["go_no_go"] != "go":
            failures.append(f"{case['name']} preflight go_no_go is not go")
        if live_harness.get("expected_route") != case["expected_skill"]:
            failures.append(f"{case['name']} live harness expected_route mismatch")
        if live_harness.get("expected_result_markers") != case["expected_markers"]:
            failures.append(f"{case['name']} live harness result markers mismatch")
        if live_harness.get("bridge_originated") is not True:
            failures.append(f"{case['name']} live harness bridge_originated flag missing")
        if evidence_chain.get("preflight_go_no_go") != "go":
            failures.append(f"{case['name']} evidence chain preflight_go_no_go is not go")
        if evidence_chain.get("preflight_placeholder_free") is not True:
            failures.append(f"{case['name']} evidence chain preflight_placeholder_free is not true")

        payload = {
            "watch_line": "bridge_live",
            "expected_skill": case["expected_skill"],
            "preflight_check_file": str(case["preflight_check_file"].relative_to(REPO_ROOT)).replace("\\", "/"),
            "live_harness_file": str(case["live_harness_file"].relative_to(REPO_ROOT)).replace("\\", "/"),
            "expected_target_path": preflight_check["expected_target_path"],
            "completion_markers": case["expected_markers"],
            "status": "ok",
        }
        write_json_output(str(case["name"]), payload, manifest)

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
