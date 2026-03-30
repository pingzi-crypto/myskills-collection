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


OUTPUT_DIR = REPO_ROOT / "analysis" / "learning-card-stage-visibility-regression" / "outputs"


def bilingual(zh: str, en: str) -> dict[str, str]:
    return {"zh": zh, "en": en}


CASES = [
    {
        "name": "concept-stable",
        "renderer": render_concept_card.render_card,
        "output": OUTPUT_DIR / "concept-stable-routing-visibility.md",
        "required_lines": [
            "## Knowledge Graph Relations",
            "### Routing and Dispatch",
            "#### Direct Routes",
            "When the term boundary drifts, route back to [[Single Card Boundary]].",
        ],
        "forbidden_lines": [
            "#### Secondary Routes",
            "#### Gap Signals",
            "#### Stop Rules",
        ],
        "spec": {
            "title": "Single Card Boundary",
            "domain": "AI协同",
            "subdomain": "Stage Visibility Regression",
            "source": "Automated stage-aware routing visibility check",
            "status": "stable",
            "graph_maturity": "local",
            "sections": {
                "question_answered": [bilingual("什么情况下应该只保留一张卡？", "When should only one card be kept?")],
                "one_sentence_definition": [
                    bilingual("单卡边界是防止线程失焦的第一道约束。", "A single-card boundary is the first constraint against thread drift.")
                ],
                "local_position": {
                    "parent_concepts": ["[[Task Scope]] | 单卡边界依赖任务边界先被说明。"]
                },
                "operational_links": {
                    "enables": ["[[Learning Card Routing]] | 稳定单卡边界后，路由才更可靠。"]
                },
                "routing_and_dispatch": {
                    "direct_routes": [
                        "When the term boundary drifts, route back to [[Single Card Boundary]]."
                    ],
                    "secondary_routes": [
                        "If [[Task Scope]] is clear but the concept still overlaps, continue to [[Learning Card Routing]]."
                    ],
                    "gap_signals": [
                        "If many cards fail for the same boundary reason, add a new Concept card for the missing distinction."
                    ],
                    "stop_rules": [
                        "Stop if the problem is no longer conceptual and has become procedural."
                    ],
                },
                "current_status_notes": [
                    bilingual("该稳定态样例用于验证 stable 只显示 Direct Routes。", "This stable sample verifies that stable only exposes Direct Routes.")
                ],
                "promotion_assessment": {
                    "current_recommendation": "watchlist",
                    "missing_evidence": ["Still lacks stronger dispatch rules."],
                },
            },
        },
    },
    {
        "name": "concept-expert",
        "renderer": render_concept_card.render_card,
        "output": OUTPUT_DIR / "concept-expert-routing-visibility.md",
        "required_lines": [
            "### Routing and Dispatch",
            "#### Direct Routes",
            "#### Secondary Routes",
            "#### Gap Signals",
            "#### Stop Rules",
            "- Gap: expert-ready requires at least one bounded secondary route.",
            "- Gap: expert-ready requires at least one explicit gap signal.",
            "- Gap: expert-ready requires at least one explicit stop rule.",
        ],
        "forbidden_lines": [],
        "spec": {
            "title": "Definition Boundary Recovery",
            "domain": "AI协同",
            "subdomain": "Stage Visibility Regression",
            "source": "Automated stage-aware routing visibility check",
            "status": "expert-ready",
            "graph_maturity": "dispatchable",
            "sections": {
                "question_answered": [bilingual("定义边界漂移后应该如何回到主概念？", "How should a definition return to the main concept after drift?")],
                "one_sentence_definition": [
                    bilingual("定义边界恢复是把偏离主轴的解释重新拉回核心概念。", "Definition boundary recovery pulls explanations back to the core concept after drift.")
                ],
                "local_position": {
                    "parent_concepts": ["[[Single Card Boundary]] | 先有单卡边界，才有恢复动作。"]
                },
                "operational_links": {
                    "enables": ["[[Learning Card Routing]] | 概念恢复后，路由更稳定。"]
                },
                "routing_and_dispatch": {
                    "direct_routes": [
                        "When the explanation drifts into unrelated terms, route to [[Single Card Boundary]] because boundary recovery comes first."
                    ]
                },
                "current_status_notes": [
                    bilingual("该 expert-ready 样例用于验证缺失 routing 子块时仍显示占位。", "This expert-ready sample verifies that missing routing sub-blocks still render placeholders.")
                ],
                "promotion_assessment": {
                    "current_recommendation": "worth promoting",
                    "next_rules": ["Add stronger multi-hop recovery rules."]
                },
            },
        },
    },
    {
        "name": "mechanism-stable",
        "renderer": render_mechanism_card.render_card,
        "output": OUTPUT_DIR / "mechanism-stable-routing-visibility.md",
        "required_lines": [
            "## Knowledge Graph Relations",
            "### Routing and Dispatch",
            "#### Direct Routes",
            "If the failure cause is still local, inspect [[Prompt Drift Feedback]] before adding another mechanism.",
        ],
        "forbidden_lines": [
            "#### Secondary Routes",
            "#### Gap Signals",
            "#### Stop Rules",
        ],
        "spec": {
            "title": "Prompt Drift Feedback",
            "domain": "AI Collaboration",
            "subdomain": "Stage Visibility Regression",
            "source": "Automated stage-aware routing visibility check",
            "status": "stable",
            "graph_maturity": "local",
            "sections": {
                "phenomenon": ["Why does a prompt get noisier after each mixed-scope edit?"],
                "causal_chain": ["Each extra goal weakens the original selection filter and increases drift."],
                "local_position": {
                    "upstream_concepts": ["[[Task Scope]] | Scope boundaries determine whether drift starts."],
                },
                "operational_links": {
                    "enables": ["[[Prompt Scope Reset]] | Once drift is diagnosed, reset can follow."]
                },
                "routing_and_dispatch": {
                    "direct_routes": [
                        "If the failure cause is still local, inspect [[Prompt Drift Feedback]] before adding another mechanism."
                    ],
                    "secondary_routes": [
                        "If the cause remains unclear after local inspection, continue to [[Task Scope]]."
                    ],
                    "gap_signals": [
                        "If drift appears repeatedly without a causal variable card, add a new Mechanism card."
                    ],
                    "stop_rules": [
                        "Stop if the issue is no longer causal and has become a method-selection problem."
                    ],
                },
                "current_status_notes": [
                    "This stable sample verifies that only Direct Routes remain visible even when the other routing blocks are populated."
                ],
                "promotion_assessment": {
                    "current_recommendation": "watchlist"
                },
            },
        },
    },
    {
        "name": "mechanism-expert",
        "renderer": render_mechanism_card.render_card,
        "output": OUTPUT_DIR / "mechanism-expert-routing-visibility.md",
        "required_lines": [
            "### Routing and Dispatch",
            "#### Direct Routes",
            "#### Secondary Routes",
            "#### Gap Signals",
            "#### Stop Rules",
            "- Gap: expert-ready requires at least one bounded secondary route.",
            "- Gap: expert-ready requires at least one explicit gap signal.",
            "- Gap: expert-ready requires at least one explicit stop rule.",
        ],
        "forbidden_lines": [],
        "spec": {
            "title": "Failure Cause Arbitration",
            "domain": "AI Collaboration",
            "subdomain": "Stage Visibility Regression",
            "source": "Automated stage-aware routing visibility check",
            "status": "expert-ready",
            "graph_maturity": "dispatchable",
            "sections": {
                "phenomenon": ["How should competing mechanism candidates be resolved?"],
                "causal_chain": ["Start with the strongest trigger variable, then compare alternatives only if that path fails."],
                "local_position": {
                    "upstream_concepts": ["[[Prompt Drift Feedback]] | Arbitration starts only after drift is recognized."]
                },
                "operational_links": {
                    "enables": ["[[Prompt Scope Reset]] | Once the cause is chosen, execution can reset safely."]
                },
                "routing_and_dispatch": {
                    "direct_routes": [
                        "When one trigger variable dominates, inspect that variable first before comparing adjacent mechanisms."
                    ]
                },
                "current_status_notes": [
                    "This expert-ready sample verifies that the full routing frame stays visible even when only direct routes are present."
                ],
                "promotion_assessment": {
                    "current_recommendation": "worth promoting",
                    "missing_evidence": ["Needs explicit secondary and stop-rule coverage."]
                },
            },
        },
    },
    {
        "name": "method-stable",
        "renderer": render_method_card.render_card,
        "output": OUTPUT_DIR / "method-stable-routing-visibility.md",
        "required_lines": [
            "## Knowledge Graph Relations",
            "### Routing and Dispatch",
            "#### Direct Routes",
            "When scope drift appears mid-execution, route to [[Prompt Scope Reset]] before continuing the current method.",
        ],
        "forbidden_lines": [
            "#### Secondary Routes",
            "#### Gap Signals",
            "#### Stop Rules",
        ],
        "spec": {
            "title": "Prompt Scope Reset",
            "domain": "AI协同",
            "subdomain": "Stage Visibility Regression",
            "source": "Automated stage-aware routing visibility check",
            "status": "stable",
            "graph_maturity": "local",
            "sections": {
                "problem_solved": [bilingual("线程已混入多个目标时，如何回到单一输出？", "How do you return to one output after a thread has mixed multiple goals?")],
                "core_idea": [bilingual("先停，再缩，再重定主目标。", "Pause, shrink, then re-anchor the primary target.")],
                "local_position": {
                    "upstream_concepts": ["[[Single Card Boundary]] | 重置前先需要边界概念。"]
                },
                "operational_links": {
                    "enables": ["[[Learning Card Routing]] | 重置后才能重新路由。"]
                },
                "routing_and_dispatch": {
                    "direct_routes": [
                        "When scope drift appears mid-execution, route to [[Prompt Scope Reset]] before continuing the current method."
                    ],
                    "secondary_routes": [
                        "If reset clarifies the target but not the sequence, continue to [[Learning Card Routing]]."
                    ],
                    "gap_signals": [
                        "If reset keeps recurring without a choice rule, add a new Method card for method arbitration."
                    ],
                    "stop_rules": [
                        "Stop if the problem is not execution drift but a mistaken belief about card count."
                    ],
                },
                "current_status_notes": [
                    bilingual("该稳定态样例用于验证 Method 卡在 stable 时仅显示 Direct Routes。", "This stable sample verifies that Method cards in stable show only Direct Routes.")
                ],
                "promotion_assessment": {
                    "current_recommendation": "watchlist"
                },
            },
        },
    },
    {
        "name": "method-expert",
        "renderer": render_method_card.render_card,
        "output": OUTPUT_DIR / "method-expert-routing-visibility.md",
        "required_lines": [
            "### Routing and Dispatch",
            "#### Direct Routes",
            "#### Secondary Routes",
            "#### Gap Signals",
            "#### Stop Rules",
            "- Gap: expert-ready requires at least one bounded secondary route.",
            "- Gap: expert-ready requires at least one explicit gap signal.",
            "- Gap: expert-ready requires at least one explicit stop rule.",
        ],
        "forbidden_lines": [],
        "spec": {
            "title": "Method Arbitration Reset",
            "domain": "AI协同",
            "subdomain": "Stage Visibility Regression",
            "source": "Automated stage-aware routing visibility check",
            "status": "expert-ready",
            "graph_maturity": "dispatchable",
            "sections": {
                "problem_solved": [bilingual("多个方法都像可行时，如何先做一次重置裁决？", "How do you perform a reset arbitration when several methods all seem viable?")],
                "core_idea": [bilingual("先用最小重置规则排除噪声，再进入真正执行。", "Use the smallest reset rule to remove noise before real execution.")],
                "local_position": {
                    "upstream_concepts": ["[[Prompt Scope Reset]] | 当前方法是更高阶的重置裁决。"]
                },
                "operational_links": {
                    "enables": ["[[Learning Card Routing]] | 裁决后再进入下游路由。"]
                },
                "routing_and_dispatch": {
                    "direct_routes": [
                        "When several methods compete, run the smallest reset first before expanding into full execution."
                    ]
                },
                "current_status_notes": [
                    bilingual("该 expert-ready 样例用于验证 Method 卡缺失子块时仍保留完整 routing 框架。", "This expert-ready sample verifies that Method cards keep the full routing frame even when sub-blocks are missing.")
                ],
                "promotion_assessment": {
                    "current_recommendation": "worth promoting"
                },
            },
        },
    },
    {
        "name": "misconception-stable",
        "renderer": render_misconception_card.render_card,
        "output": OUTPUT_DIR / "misconception-stable-routing-visibility.md",
        "required_lines": [
            "## Knowledge Graph Relations",
            "### Routing and Dispatch",
            "#### Direct Routes",
            "When the user mistakes visibility for portability, correct this misconception before resuming compatibility planning.",
        ],
        "forbidden_lines": [
            "#### Secondary Routes",
            "#### Gap Signals",
            "#### Stop Rules",
        ],
        "spec": {
            "title": "Visible In One Host Means Portable Everywhere",
            "domain": "AI协同",
            "subdomain": "Stage Visibility Regression",
            "source": "Automated stage-aware routing visibility check",
            "status": "stable",
            "graph_maturity": "local",
            "sections": {
                "mistaken_claim": [bilingual("一个宿主中可见就等于所有宿主都兼容。", "Visibility in one host means compatibility in every host.")],
                "why_it_is_wrong": [bilingual("这只说明当前宿主接受了它，不说明其他宿主共享同一协议。", "This only shows the current host accepted it, not that other hosts share the same protocol.")],
                "local_position": {
                    "common_confusions": ["[[Learning Card Routing]] | 可见性和兼容性经常在路由层被混淆。"]
                },
                "operational_links": {
                    "corrections": ["[[Prompt Scope Reset]] | 纠偏后才适合回到执行层。"]
                },
                "routing_and_dispatch": {
                    "direct_routes": [
                        "When the user mistakes visibility for portability, correct this misconception before resuming compatibility planning."
                    ],
                    "secondary_routes": [
                        "If compatibility remains unclear after correction, continue to [[Learning Card Routing]]."
                    ],
                    "gap_signals": [
                        "If many host-specific failures exist without a reusable compatibility card, add a new Misconception or Method card."
                    ],
                    "stop_rules": [
                        "Stop treating the issue as a misconception once the user already accepts the correction."
                    ],
                },
                "current_status_notes": [
                    bilingual("该稳定态样例用于验证 Misconception 卡在 stable 时只显示 Direct Routes。", "This stable sample verifies that Misconception cards in stable show only Direct Routes.")
                ],
                "promotion_assessment": {
                    "current_recommendation": "watchlist"
                },
            },
        },
    },
    {
        "name": "misconception-expert",
        "renderer": render_misconception_card.render_card,
        "output": OUTPUT_DIR / "misconception-expert-routing-visibility.md",
        "required_lines": [
            "### Routing and Dispatch",
            "#### Direct Routes",
            "#### Secondary Routes",
            "#### Gap Signals",
            "#### Stop Rules",
            "- Gap: expert-ready requires at least one bounded secondary route.",
            "- Gap: expert-ready requires at least one explicit gap signal.",
            "- Gap: expert-ready requires at least one explicit stop rule.",
        ],
        "forbidden_lines": [],
        "spec": {
            "title": "Correction Before Compatibility Planning",
            "domain": "AI协同",
            "subdomain": "Stage Visibility Regression",
            "source": "Automated stage-aware routing visibility check",
            "status": "expert-ready",
            "graph_maturity": "dispatchable",
            "sections": {
                "mistaken_claim": [bilingual("兼容问题可以在不先纠正前提误解的情况下直接规划。", "Compatibility planning can proceed without first correcting the underlying misconception.")],
                "why_it_is_wrong": [bilingual("如果前提误解不先修正，后续规划会建立在错误假设上。", "If the misconception is not corrected first, later planning is built on a false assumption.")],
                "local_position": {
                    "correct_return_nodes": ["[[Learning Card Routing]] | 纠偏后应回到正确的路由节点。"]
                },
                "operational_links": {
                    "enables": ["[[Prompt Scope Reset]] | 纠偏后执行层才适合重置。"]
                },
                "routing_and_dispatch": {
                    "direct_routes": [
                        "When the planning thread depends on a false premise, correct that premise before attempting any compatibility design."
                    ]
                },
                "current_status_notes": [
                    bilingual("该 expert-ready 样例用于验证 Misconception 卡在缺少子块时仍暴露完整 routing 层。", "This expert-ready sample verifies that Misconception cards still expose the full routing layer when sub-blocks are missing.")
                ],
                "promotion_assessment": {
                    "current_recommendation": "worth promoting"
                },
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
                failures.append(f"{case['name']}: found forbidden line: {line}")

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
