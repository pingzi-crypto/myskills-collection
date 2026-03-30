#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "analysis" / "learning-card-router-execution-contract-regression" / "outputs"

ROUTER_SKILL = REPO_ROOT / "skills" / "obsidian-learning-card-router" / "SKILL.md"
ROUTING_MODES = REPO_ROOT / "skills" / "obsidian-learning-card-router" / "references" / "routing-modes.md"
SKILL_FAMILY = REPO_ROOT / "skills" / "references" / "learning-card-skill-family.md"
SKILLS_README = REPO_ROOT / "skills" / "README.md"


REQUIRED_PHRASES = {
    ROUTER_SKILL: [
        "The minimum execution package already known at handoff time:",
        "Any still-missing write inputs that the downstream skill must collect before",
        "Execution package confirmed:",
        "Still needed before write:",
    ],
    ROUTING_MODES: [
        "And always include the minimum execution package:",
        "Mode-specific minimum follow-up:",
        "- `create`: if title, keywords, domain, or vault root are still missing, say so",
    ],
    SKILL_FAMILY: [
        "## Minimum Handoff Package",
        "- whether any write-critical inputs are still missing",
        "- marking still-missing write inputs instead of pretending the handoff is fully ready to write",
    ],
    SKILLS_README: [
        "minimum execution package already confirmed",
        "still-missing write inputs the downstream skill must collect",
    ],
}


SAMPLES = [
    {
        "name": "concept-create-minimum-package",
        "file": "concept-create-minimum-package.txt",
        "content": """Capture anchor: `windows系统有自带的截图功能吗？如果有快捷键是什么` -> first assistant reply after it
Route result: `Concept`
Mode: `create`
Use `$obsidian-concept-card-capture` for the next step.
Router status: routing complete only. No card file has been created or updated yet.
Execution package confirmed:
- Capture anchor: selected user message -> first assistant reply after it
- Card type: Concept
- Mode: create
- Downstream skill: $obsidian-concept-card-capture
Still needed before write:
- title
- keywords or thread points
- domain
- vault root
Next step: use `$obsidian-concept-card-capture` now to actually create the card.
Suggested reply: `继续创建`
Reason: 这段内容主要在解释截图方式的类型和边界，属于概念卡。
""",
    },
    {
        "name": "method-update-minimum-package",
        "file": "method-update-minimum-package.txt",
        "content": """Capture anchor: `把 router 的问题改成中英双语` -> first assistant reply after it
Route result: `Method`
Mode: `update`
Use `$obsidian-method-card-capture` for the next step.
Router status: routing complete only. No card file has been created or updated yet.
Execution package confirmed:
- Capture anchor: selected user message -> first assistant reply after it
- Card type: Method
- Mode: update
- Downstream skill: $obsidian-method-card-capture
Still needed before write:
- existing card title or path confirmation
- vault root
Next step: use `$obsidian-method-card-capture` now to actually update the card.
Suggested reply: `继续更新`
Reason: 当前任务是在已有方法卡上补充执行规则，不是新建卡。
""",
    },
    {
        "name": "misconception-review-minimum-package",
        "file": "misconception-review-minimum-package.txt",
        "content": """Capture anchor: `这个误解卡是否应该升到 expert-ready` -> first assistant reply after it
Route result: `Misconception`
Mode: `promotion review`
Use `$obsidian-misconception-card-capture` for the next step.
Router status: routing complete only. No card file has been created or updated yet.
Execution package confirmed:
- Capture anchor: selected user message -> first assistant reply after it
- Card type: Misconception
- Mode: promotion review
- Downstream skill: $obsidian-misconception-card-capture
Still needed before write:
- existing card title or path confirmation
- vault root
Next step: use `$obsidian-misconception-card-capture` now to actually review the card.
Suggested reply: `继续评审`
Reason: 当前线程在判断已有误解卡的成熟度，而不是首次创建。
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

    required_lines = [
        "Router status: routing complete only. No card file has been created or updated yet.",
        "Execution package confirmed:",
        "Still needed before write:",
        "Next step:",
        "Suggested reply:",
    ]
    forbidden_lines = [
        "Created file:",
        "Updated file:",
        "Still needed before write:\n- none\n- title",
    ]

    for sample in SAMPLES:
        text = sample["content"]
        out_path = OUTPUT_DIR / sample["file"]
        out_path.write_text(text, encoding="utf-8")

        for line in required_lines:
            if line not in text:
                failures.append(f"{sample['name']} missing line: {line}")
        for line in forbidden_lines:
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
