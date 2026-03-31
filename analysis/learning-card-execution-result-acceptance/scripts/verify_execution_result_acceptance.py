#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
ANALYSIS_DIR = REPO_ROOT / "analysis" / "learning-card-execution-result-acceptance"
OUTPUT_DIR = ANALYSIS_DIR / "outputs"

MANUAL = REPO_ROOT / "skills" / "references" / "learning-card-standard-operating-manual.md"
END_TO_END = REPO_ROOT / "analysis" / "learning-card-end-to-end-examples" / "report.md"
CONCEPT_SKILL = REPO_ROOT / "skills" / "obsidian-concept-card-capture" / "SKILL.md"
METHOD_SKILL = REPO_ROOT / "skills" / "obsidian-method-card-capture" / "SKILL.md"
MISCONCEPTION_SKILL = REPO_ROOT / "skills" / "obsidian-misconception-card-capture" / "SKILL.md"

REQUIRED_PHRASES = {
    MANUAL: [
        "Expected execution result shape:",
        "Created file: <path>",
        "Updated file: <path>",
        "Reviewed file: <path>",
        "Promotion result: <promoted | watchlist | stay stable>",
    ],
    END_TO_END: [
        "Created file: C:\\Users\\pz\\Documents\\Obsidian Vault\\学习\\Cards\\Concepts\\Windows 自带截图方式.md",
        "Reviewed file: <path>",
        "Promotion result: watchlist",
    ],
    CONCEPT_SKILL: [
        "## Output Expectations",
        "The created or updated file path.",
    ],
    METHOD_SKILL: [
        "## Output Expectations",
        "The created or updated file path.",
    ],
    MISCONCEPTION_SKILL: [
        "## Output Expectations",
        "The created or updated file path.",
    ],
}

SAMPLES = [
    {
        "name": "concept-create-result",
        "file": "concept-create-result.txt",
        "content": """Concept captured: Windows 自带截图方式
Created file: C:\\Users\\pz\\Documents\\Obsidian Vault\\学习\\Cards\\Concepts\\Windows 自带截图方式.md
Summary: extracted the built-in screenshot options, their shortcuts, and their boundary differences.
Progression result: stay seed
""",
    },
    {
        "name": "method-update-result",
        "file": "method-update-result.txt",
        "content": """Method updated: Prompt Narrowing
Updated file: C:\\Users\\pz\\Documents\\Obsidian Vault\\学习\\Cards\\Methods\\Prompt Narrowing.md
Summary: merged new routing-precision guidance into the existing method card without changing its core identity.
""",
    },
    {
        "name": "misconception-review-result",
        "file": "misconception-review-result.txt",
        "content": """Reviewed file: C:\\Users\\pz\\Documents\\Obsidian Vault\\学习\\Cards\\Misconceptions\\More Cards Means Better Learning.md
Promotion result: watchlist
Summary: review recorded that the misconception remains useful but does not yet justify expert-ready promotion.
""",
    },
]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest().upper()


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    manifest: list[dict[str, str]] = []

    for path, phrases in REQUIRED_PHRASES.items():
        text = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                failures.append(f"{path.relative_to(REPO_ROOT)} missing phrase: {phrase}")

    for sample in SAMPLES:
        text = sample["content"]
        output_path = OUTPUT_DIR / sample["file"]
        output_path.write_text(text, encoding="utf-8")

        if sample["name"].endswith("create-result") and "Created file:" not in text:
            failures.append(f"{sample['name']} missing Created file line")
        if sample["name"].endswith("update-result") and "Updated file:" not in text:
            failures.append(f"{sample['name']} missing Updated file line")
        if sample["name"].endswith("review-result"):
            if "Reviewed file:" not in text:
                failures.append(f"{sample['name']} missing Reviewed file line")
            if "Promotion result:" not in text:
                failures.append(f"{sample['name']} missing Promotion result line")

        if "Router status: routing complete only" in text:
            failures.append(f"{sample['name']} should not contain router-only status")

        manifest.append(
            {
                "name": sample["name"],
                "output": str(output_path.relative_to(REPO_ROOT)).replace("\\", "/"),
                "sha256": sha256_text(text),
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
