#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "analysis" / "learning-card-router-handoff-contract-regression" / "outputs"

ROUTER_SKILL = REPO_ROOT / "skills" / "obsidian-learning-card-router" / "SKILL.md"
ROUTING_MODES = REPO_ROOT / "skills" / "obsidian-learning-card-router" / "references" / "routing-modes.md"
SKILL_FAMILY = REPO_ROOT / "skills" / "references" / "learning-card-skill-family.md"
SKILLS_README = REPO_ROOT / "skills" / "README.md"


REQUIRED_PHRASES = {
    ROUTER_SKILL: [
        "The router must explicitly tell the user when routing is finished but no card",
        "An explicit status line saying routing is complete but no card file has been",
        "One exact next-step instruction for actual execution by the downstream",
        "Router status: routing complete only. No card file has been created or updated yet.",
        "Next step: use $<target-skill> now to actually <create | update | review> the card.",
        "Suggested reply: <继续创建 | 继续更新 | 继续评审>",
        "Do not stop with a handoff that sounds like a card already exists on disk when",
    ],
    ROUTING_MODES: [
        "routing alone did not write any card file yet",
        "the user still needs the downstream execution skill to actually create,",
    ],
    SKILL_FAMILY: [
        "explicitly stating when the result is routing only and no card file exists yet",
        "pointing to one exact downstream next step for actual execution",
        "3. explicitly state that routing did not create or update a card file yet",
    ],
    SKILLS_README: [
        "Let the router explicitly say whether it only classified the thread or an execution skill has actually written a card.",
    ],
}


SAMPLE_HANDOFFS = [
    {
        "name": "concept-create",
        "file": "concept-create-handoff.txt",
        "content": """Capture anchor: `windows系统有自带的截图功能吗？如果有快捷键是什么` -> first assistant reply after it
Route result: `Concept`
Mode: `create`
Use `$obsidian-concept-card-capture` for the next step.
Router status: routing complete only. No card file has been created or updated yet.
Next step: use `$obsidian-concept-card-capture` now to actually create the card.
Suggested reply: `继续创建`
Reason: 这段内容主要在回答截图功能的定义、边界和分类，主轴是概念说明而不是单一步骤执行。
""",
    },
    {
        "name": "method-update",
        "file": "method-update-handoff.txt",
        "content": """Capture anchor: `把 router 的问题改成中英双语` -> first assistant reply after it
Route result: `Method`
Mode: `update`
Use `$obsidian-method-card-capture` for the next step.
Router status: routing complete only. No card file has been created or updated yet.
Next step: use `$obsidian-method-card-capture` now to actually update the card.
Suggested reply: `继续更新`
Reason: 现有方法卡已经在讨论范围内，这次内容是在补充执行规则，而不是新建概念卡。
""",
    },
    {
        "name": "misconception-promotion-review",
        "file": "misconception-promotion-review-handoff.txt",
        "content": """Capture anchor: `这个误解卡是否应该升到 expert-ready` -> first assistant reply after it
Route result: `Misconception`
Mode: `promotion review`
Use `$obsidian-misconception-card-capture` for the next step.
Router status: routing complete only. No card file has been created or updated yet.
Next step: use `$obsidian-misconception-card-capture` now to actually review the card.
Suggested reply: `继续评审`
Reason: 当前线程在判断已有误解卡的成熟度与调度价值，属于晋升评审而不是首次写卡。
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

    required_sample_lines = [
        "Router status: routing complete only. No card file has been created or updated yet.",
        "Next step:",
        "Suggested reply:",
    ]
    forbidden_sample_lines = [
        "Created file:",
        "Updated file:",
    ]

    for sample in SAMPLE_HANDOFFS:
        text = sample["content"]
        out_path = OUTPUT_DIR / sample["file"]
        out_path.write_text(text, encoding="utf-8")

        for line in required_sample_lines:
            if line not in text:
                failures.append(f"{sample['name']} missing line: {line}")
        for line in forbidden_sample_lines:
            if line in text:
                failures.append(f"{sample['name']} contains forbidden line: {line}")

        manifest.append(
            {
                "name": sample["name"],
                "output": str(out_path.relative_to(REPO_ROOT)).replace("\\", "/"),
                "sha256": sha256_text(text),
            }
        )

    manifest_path = OUTPUT_DIR / "manifest.json"
    manifest_path.write_text(
        json.dumps({"samples": manifest}, ensure_ascii=False, indent=2) + "\n",
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
