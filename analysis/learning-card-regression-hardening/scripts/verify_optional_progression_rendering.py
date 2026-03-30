#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[3]
CORE_SCRIPTS = REPO_ROOT / "skills" / "shared" / "learning-card-core" / "scripts"

CONCEPT_SCRIPTS = REPO_ROOT / "skills" / "obsidian-concept-card-capture" / "scripts"
MECHANISM_SCRIPTS = REPO_ROOT / "skills" / "obsidian-mechanism-card-capture" / "scripts"
METHOD_SCRIPTS = REPO_ROOT / "skills" / "obsidian-method-card-capture" / "scripts"
MISCONCEPTION_SCRIPTS = REPO_ROOT / "skills" / "obsidian-misconception-card-capture" / "scripts"

for path in [
    str(CORE_SCRIPTS),
    str(CONCEPT_SCRIPTS),
    str(MECHANISM_SCRIPTS),
    str(METHOD_SCRIPTS),
    str(MISCONCEPTION_SCRIPTS),
]:
    if path not in sys.path:
        sys.path.insert(0, path)

import render_concept_card
import render_mechanism_card
import render_method_card
import render_misconception_card


OUTPUT_DIR = REPO_ROOT / "analysis" / "learning-card-regression-hardening" / "outputs"


CASES = [
    {
        "name": "concept",
        "renderer": render_concept_card.render_card,
        "output": OUTPUT_DIR / "concept-seed-no-optional-progression.md",
        "forbidden_lines": ["- 下一步重点：", "- 当前升级任务："],
        "required_lines": ["## Progression Layer", "- 当前阶段：seed", "- 图谱成熟度：none"],
        "spec": {
            "title": "Single Card Boundary",
            "domain": "AI协同",
            "subdomain": "Regression Hardening",
            "source": "Automated regression hardening check",
            "status": "seed",
            "graph_maturity": "none",
            "sections": {
                "question_answered": [
                    {
                        "zh": "为什么一个学习线程默认只应该先沉淀为一张卡？",
                        "en": "Why should one learning thread default to only one card first?",
                    }
                ],
                "one_sentence_definition": [
                    {
                        "zh": "单卡边界是先把线程压缩进一个主认知单位的约束。",
                        "en": "A single-card boundary is the constraint of compressing a thread into one primary learning unit first.",
                    }
                ],
                "current_status_notes": [
                    {
                        "zh": "这个 seed 样例只用于验证缺失可选进阶字段时的渲染边界。",
                        "en": "This seed sample only validates rendering boundaries when optional progression fields are absent.",
                    }
                ],
            },
        },
    },
    {
        "name": "mechanism",
        "renderer": render_mechanism_card.render_card,
        "output": OUTPUT_DIR / "mechanism-seed-no-optional-progression.md",
        "forbidden_lines": ["- Next goal:", "- Current upgrade tasks:"],
        "required_lines": ["## Progression Layer", "- Current status: seed", "- Graph maturity: none"],
        "spec": {
            "title": "Prompt Drift Feedback",
            "domain": "AI Collaboration",
            "subdomain": "Regression Hardening",
            "source": "Automated regression hardening check",
            "status": "seed",
            "graph_maturity": "none",
            "sections": {
                "phenomenon": ["Why does an initially clean prompt drift after repeated mixed-scope edits?"],
                "causal_chain": ["Each extra mixed objective weakens the original boundary and invites more drift."],
                "current_status_notes": [
                    "This seed sample exists only to ensure optional progression placeholders stay hidden when omitted."
                ],
            },
        },
    },
    {
        "name": "method",
        "renderer": render_method_card.render_card,
        "output": OUTPUT_DIR / "method-seed-no-optional-progression.md",
        "forbidden_lines": ["- 下一步重点：", "- 当前升级任务："],
        "required_lines": ["## Progression Layer", "- 当前阶段：seed", "- 图谱成熟度：none"],
        "spec": {
            "title": "Prompt Scope Reset",
            "domain": "AI协同",
            "subdomain": "Regression Hardening",
            "source": "Automated regression hardening check",
            "status": "seed",
            "graph_maturity": "none",
            "sections": {
                "problem_solved": [
                    {
                        "zh": "当当前工作线程已经开始混入过多目标时，如何重置成单一输出？",
                        "en": "How do you reset a working thread back to one output when too many goals have started to mix in?",
                    }
                ],
                "core_idea": [
                    {
                        "zh": "先停止扩张，再重建唯一主目标。",
                        "en": "Stop expansion first, then rebuild one primary target.",
                    }
                ],
                "current_status_notes": [
                    {
                        "zh": "这个 seed 样例用于验证 Method renderer 在缺失可选进阶字段时不会输出空占位。",
                        "en": "This seed sample verifies that the Method renderer does not emit empty placeholders when optional progression fields are absent.",
                    }
                ],
            },
        },
    },
    {
        "name": "misconception",
        "renderer": render_misconception_card.render_card,
        "output": OUTPUT_DIR / "misconception-seed-no-optional-progression.md",
        "forbidden_lines": ["- 下一步重点：", "- 当前升级任务："],
        "required_lines": ["## Progression Layer", "- 当前阶段：seed", "- 图谱成熟度：none"],
        "spec": {
            "title": "Visible In One Host Means Portable Everywhere",
            "domain": "AI协同",
            "subdomain": "Regression Hardening",
            "source": "Automated regression hardening check",
            "status": "seed",
            "graph_maturity": "none",
            "sections": {
                "mistaken_claim": [
                    {
                        "zh": "只要一个技能在一个宿主里可见，就等于它在所有宿主里都兼容。",
                        "en": "If a skill is visible in one host, it is therefore compatible in every host.",
                    }
                ],
                "why_it_is_wrong": [
                    {
                        "zh": "可见性只说明当前宿主接受了它，不说明其他宿主共享同一协议。",
                        "en": "Visibility only shows that the current host accepted it, not that other hosts share the same protocol.",
                    }
                ],
                "current_status_notes": [
                    {
                        "zh": "这个 seed 样例用于验证 Misconception renderer 在缺失可选进阶字段时不会渲染空块。",
                        "en": "This seed sample verifies that the Misconception renderer does not render empty blocks when optional progression fields are absent.",
                    }
                ],
            },
        },
    },
]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest().upper()


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    manifest: list[dict[str, str]] = []

    for case in CASES:
        markdown = case["renderer"](case["spec"])
        case["output"].write_text(markdown, encoding="utf-8")

        for line in case["required_lines"]:
            if line not in markdown:
                failures.append(f"{case['name']}: missing required line: {line}")

        for line in case["forbidden_lines"]:
            if line in markdown:
                failures.append(f"{case['name']}: found forbidden placeholder line: {line}")

        manifest.append(
            {
                "name": case["name"],
                "output": str(case["output"].relative_to(REPO_ROOT)).replace("\\", "/"),
                "sha256": sha256_text(markdown),
            }
        )

    manifest_path = OUTPUT_DIR / "manifest.json"
    manifest_path.write_text(
        json.dumps({"cases": manifest}, ensure_ascii=False, indent=2) + "\n",
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
