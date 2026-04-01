#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
ANALYSIS_DIR = REPO_ROOT / "analysis" / "learning-card-live-acceptance-harness"
CASE_DIR = ANALYSIS_DIR / "cases"
OUTPUT_DIR = ANALYSIS_DIR / "outputs"

CARD_TYPE_DIR = {
    "concept": "Concepts",
    "mechanism": "Mechanisms",
    "method": "Methods",
    "misconception": "Misconceptions",
}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest().upper()


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    manifest: list[dict[str, str]] = []

    for case_path in sorted(CASE_DIR.glob("*.json")):
        case = json.loads(case_path.read_text(encoding="utf-8"))
        name = case["name"]
        target_path = Path(case["target_path"])
        duplicate_dir = Path(case["duplicate_dir"])
        report_path = REPO_ROOT / case["source_report"]
        expected_dir_name = CARD_TYPE_DIR[case["card_type"]]
        bridge_originated = bool(case.get("bridge_originated", False))

        if not target_path.exists():
            failures.append(f"{name} target path missing: {target_path}")

        if not duplicate_dir.exists():
            failures.append(f"{name} duplicate dir missing: {duplicate_dir}")

        if target_path.exists() and target_path.parent.name != expected_dir_name:
            failures.append(
                f"{name} target path is in {target_path.parent.name}, expected {expected_dir_name}"
            )

        duplicate_matches = []
        if duplicate_dir.exists():
            duplicate_matches = sorted(path.name for path in duplicate_dir.glob(case["duplicate_glob"]))
            if len(duplicate_matches) != case["expected_duplicate_count"]:
                failures.append(
                    f"{name} duplicate count {len(duplicate_matches)} != {case['expected_duplicate_count']}"
                )

        if not report_path.exists():
            failures.append(f"{name} source report missing: {report_path}")
            report_text = ""
        else:
            report_text = report_path.read_text(encoding="utf-8")
            if case["target_path"] not in report_text:
                failures.append(f"{name} source report does not mention target path")
            for phrase in case["required_report_phrases"]:
                if phrase not in report_text:
                    failures.append(f"{name} source report missing phrase: {phrase}")

        evidence_chain: dict[str, object] | None = None
        if bridge_originated:
            handoff_path = REPO_ROOT / case["handoff_source"]
            preflight_packet_path = REPO_ROOT / case["preflight_packet"]
            preflight_check_path = REPO_ROOT / case["preflight_check"]

            if not handoff_path.exists():
                failures.append(f"{name} handoff source missing: {handoff_path}")
            if not preflight_packet_path.exists():
                failures.append(f"{name} preflight packet missing: {preflight_packet_path}")
            if not preflight_check_path.exists():
                failures.append(f"{name} preflight check missing: {preflight_check_path}")

            preflight_check = {}
            if preflight_check_path.exists():
                preflight_check = json.loads(preflight_check_path.read_text(encoding="utf-8"))
                if preflight_check.get("expected_skill") != case["expected_route"]:
                    failures.append(f"{name} preflight check expected_skill mismatch")
                if preflight_check.get("expected_target_path") != case["target_path"]:
                    failures.append(f"{name} preflight check expected_target_path mismatch")
                if preflight_check.get("linked_live_target_path") != case["target_path"]:
                    failures.append(f"{name} preflight check linked_live_target_path mismatch")
                if preflight_check.get("expected_completion_markers") != case["expected_result_markers"]:
                    failures.append(f"{name} preflight check completion markers mismatch")
                if preflight_check.get("go_no_go") != "go":
                    failures.append(f"{name} preflight check go_no_go is not go")
                if preflight_check.get("placeholder_free") is not True:
                    failures.append(f"{name} preflight check is not placeholder_free")
                prompt_output = preflight_check.get("prompt_output")
                if not prompt_output:
                    failures.append(f"{name} preflight check missing prompt_output")
                elif not (REPO_ROOT / str(prompt_output)).exists():
                    failures.append(f"{name} preflight check prompt_output missing on disk")

            if report_text:
                for linked_path in (
                    case["handoff_source"],
                    case["preflight_packet"],
                    case["preflight_check"],
                ):
                    if linked_path not in report_text:
                        failures.append(f"{name} source report does not mention {linked_path}")

            evidence_chain = {
                "handoff_source": case["handoff_source"],
                "handoff_exists": handoff_path.exists(),
                "preflight_packet": case["preflight_packet"],
                "preflight_packet_exists": preflight_packet_path.exists(),
                "preflight_check": case["preflight_check"],
                "preflight_check_exists": preflight_check_path.exists(),
                "preflight_go_no_go": preflight_check.get("go_no_go") if preflight_check else None,
                "preflight_placeholder_free": preflight_check.get("placeholder_free") if preflight_check else None,
            }

        result = {
            "name": name,
            "validation_kind": case["validation_kind"],
            "card_type": case["card_type"],
            "target_path": case["target_path"],
            "target_exists": target_path.exists(),
            "expected_route": case["expected_route"],
            "expected_result_markers": case["expected_result_markers"],
            "duplicate_glob": case["duplicate_glob"],
            "duplicate_matches": duplicate_matches,
            "source_report": case["source_report"],
            "bridge_originated": bridge_originated,
        }
        if evidence_chain is not None:
            result["evidence_chain"] = evidence_chain

        output_path = OUTPUT_DIR / f"{case_path.stem}-check.json"
        output_text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        output_path.write_text(output_text, encoding="utf-8")

        manifest.append(
            {
                "name": name,
                "output": str(output_path.relative_to(REPO_ROOT)).replace("\\", "/"),
                "sha256": sha256_text(output_text),
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
