#!/usr/bin/env python3
"""
Render filled learning-card samples and generate a quantitative slimming report.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


TOKEN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*")

ROOT = Path(__file__).resolve().parents[3]
AUDIT_ROOT = ROOT / "analysis" / "learning-card-slimming"
SAMPLES_DIR = AUDIT_ROOT / "samples"
OUTPUTS_DIR = AUDIT_ROOT / "outputs"
REPORT_PATH = AUDIT_ROOT / "report.md"

CARD_CONFIGS = [
    {
        "card_type": "concept",
        "label": "Concept Card",
        "sample": SAMPLES_DIR / "concept-single-card-boundary.json",
        "renderer": ROOT / "skills" / "obsidian-concept-card-capture" / "scripts" / "render_concept_card.py",
        "output": OUTPUTS_DIR / "concept-single-card-boundary.md",
        "core_sections": [
            "question_answered",
            "one_sentence_definition",
            "essence",
            "why_it_matters",
            "core_logic",
            "prerequisites",
            "failure_boundaries",
            "confusions",
            "examples",
            "counter_examples",
            "common_misunderstandings",
            "my_words",
            "needs_validation",
        ],
    },
    {
        "card_type": "mechanism",
        "label": "Mechanism Card",
        "sample": SAMPLES_DIR / "mechanism-section-bloat-drift.json",
        "renderer": ROOT / "skills" / "obsidian-mechanism-card-capture" / "scripts" / "render_mechanism_card.py",
        "output": OUTPUTS_DIR / "mechanism-section-bloat-drift.md",
        "core_sections": [
            "phenomenon",
            "core_variables",
            "causal_chain",
            "key_prerequisites",
            "weakest_step",
            "alternative_explanations",
            "scope",
            "failure_boundaries",
            "supporting_evidence",
            "counter_cases",
            "compressed_explanation",
            "validation_question",
        ],
    },
    {
        "card_type": "method",
        "label": "Method Card",
        "sample": SAMPLES_DIR / "method-section-priority-compression.json",
        "renderer": ROOT / "skills" / "obsidian-method-card-capture" / "scripts" / "render_method_card.py",
        "output": OUTPUTS_DIR / "method-section-priority-compression.md",
        "core_sections": [
            "problem_solved",
            "core_idea",
            "method_structure",
            "design_choices",
            "hidden_assumptions",
            "fit_scenarios",
            "non_fit_scenarios",
            "comparison_with_alternatives",
            "common_misuses",
            "failure_modes",
            "decision_criteria",
            "representative_examples",
            "validation_question",
        ],
    },
    {
        "card_type": "misconception",
        "label": "Misconception Card",
        "sample": SAMPLES_DIR / "misconception-more-sections-make-better-card.json",
        "renderer": ROOT / "skills" / "obsidian-misconception-card-capture" / "scripts" / "render_misconception_card.py",
        "output": OUTPUTS_DIR / "misconception-more-sections-make-better-card.md",
        "core_sections": [
            "mistaken_claim",
            "why_it_seems_plausible",
            "why_it_is_wrong",
            "correct_understanding",
            "what_it_confuses",
            "representative_counterexamples",
            "trigger_signals",
            "corrective_action",
        ],
    },
]

COMMON_RUBRIC = {
    "local_position": (8, "must", "Stable cards need a reliable local graph anchor."),
    "operational_links": (8, "must", "Stable cards need functional connections, not just nearby nodes."),
    "routing_and_dispatch.direct_routes": (7, "optimize", "Useful after stability, but does not need many rules by default."),
    "routing_and_dispatch.secondary_routes": (5, "optimize", "Valuable later; default stable cards should keep this sparse."),
    "routing_and_dispatch.gap_signals": (5, "optimize", "Useful for mature cards, but not every stable card needs it fully expanded."),
    "routing_and_dispatch.stop_rules": (5, "optimize", "Important for dispatch-heavy cards, but can be gated by maturity."),
    "current_status_notes": (3, "redundant", "Often restates frontmatter status and can be folded into one shorter note."),
    "next_goal": (5, "optimize", "Useful for maintenance, but can be merged with upgrade tasks."),
    "growing_checklist": (3, "redundant", "Review metadata does not need to stay visible in the main card body."),
    "stable_checklist": (3, "redundant", "Review metadata does not need to stay visible in the main card body."),
    "expert_ready_checklist": (4, "redundant", "Useful during promotion review, but too heavy as an always-on section."),
    "promotion_assessment.current_recommendation": (5, "optimize", "Useful, but can be collapsed into a compact status line."),
    "promotion_assessment.main_reasons": (5, "optimize", "Useful, but should be shorter or review-only."),
    "promotion_assessment.missing_evidence": (5, "optimize", "Useful for maintenance, but can live in a shorter review summary."),
    "promotion_assessment.next_rules": (5, "optimize", "Action-oriented, but overlaps with next goal and upgrade tasks."),
    "current_upgrade_tasks": (4, "redundant", "Usually duplicates next goal and promotion assessment."),
    "upgrade_history": (2, "redundant", "Better kept in changelog or git, not in the default body."),
}

TYPE_RUBRIC = {
    "concept": {
        "question_answered": (9, "must", "A concept card must state the question it resolves."),
        "one_sentence_definition": (10, "must", "The compact definition is the retrieval anchor."),
        "essence": (9, "must", "The essence distinguishes the concept from a mere synonym."),
        "why_it_matters": (7, "optimize", "Useful, but can be merged with essence when short."),
        "core_logic": (8, "must", "Needed when the concept has internal structure or operating logic."),
        "prerequisites": (6, "optimize", "Helpful when misuse comes from missing setup, but not always mandatory."),
        "failure_boundaries": (8, "must", "Boundary clarity is core to concept quality."),
        "confusions": (6, "optimize", "Useful, but often overlaps with misunderstandings."),
        "examples": (7, "optimize", "Examples improve retrieval, but one strong example is enough."),
        "counter_examples": (6, "optimize", "Useful when boundary confusion is common, but not always essential."),
        "common_misunderstandings": (5, "optimize", "Useful, but usually mergeable with confusions."),
        "my_words": (3, "redundant", "Personal phrasing is nice-to-have but not core to a default shared card."),
        "needs_validation": (4, "redundant", "Open questions are useful in review mode, not always-on body content."),
    },
    "mechanism": {
        "phenomenon": (10, "must", "A mechanism card must state what it explains."),
        "core_variables": (9, "must", "Variables are core to causal understanding."),
        "causal_chain": (10, "must", "Without the chain, the card is not a mechanism card."),
        "key_prerequisites": (8, "must", "Mechanisms need enabling conditions to avoid over-generalization."),
        "weakest_step": (8, "must", "The likely break point is central to diagnosing failure."),
        "alternative_explanations": (7, "optimize", "Useful for disambiguation, but can be short."),
        "scope": (8, "must", "Mechanisms need a clear domain of validity."),
        "failure_boundaries": (8, "must", "Needed to avoid false causal overreach."),
        "supporting_evidence": (7, "optimize", "Evidence matters, but it can be concise."),
        "counter_cases": (7, "optimize", "Counter-cases sharpen scope, but one strong anomaly is enough."),
        "compressed_explanation": (6, "optimize", "Useful for recall, but can be merged into the lead if concise."),
        "validation_question": (4, "redundant", "Helpful in study mode, but not required in the default body."),
    },
    "method": {
        "problem_solved": (10, "must", "A method card must anchor to the problem it solves."),
        "core_idea": (9, "must", "This is the compression anchor for recall."),
        "method_structure": (10, "must", "The actionable procedure is the heart of the card."),
        "design_choices": (7, "optimize", "Important when tradeoffs matter, but can stay concise."),
        "hidden_assumptions": (7, "optimize", "Useful when transfer fails without them."),
        "fit_scenarios": (8, "must", "A method needs a clear fit boundary."),
        "non_fit_scenarios": (8, "must", "A method also needs anti-fit boundary clarity."),
        "comparison_with_alternatives": (6, "optimize", "Helpful, but only one meaningful contrast is usually enough."),
        "common_misuses": (7, "optimize", "Useful because methods are easy to misapply."),
        "failure_modes": (8, "must", "A strong method card should show how it breaks."),
        "decision_criteria": (8, "must", "Methods need a rule for when to apply them."),
        "representative_examples": (6, "optimize", "Helpful but compressible."),
        "validation_question": (4, "redundant", "Useful in study mode, not mandatory in every render."),
    },
    "misconception": {
        "mistaken_claim": (10, "must", "A misconception card must name the false claim cleanly."),
        "why_it_seems_plausible": (9, "must", "Without plausible appeal, the misconception is under-specified."),
        "why_it_is_wrong": (10, "must", "This is the correction core."),
        "correct_understanding": (9, "must", "The card should not only negate; it must redirect."),
        "what_it_confuses": (7, "optimize", "Useful, but can be folded into the correction when concise."),
        "representative_counterexamples": (8, "must", "A concrete counterexample makes correction stick."),
        "trigger_signals": (8, "must", "Misconceptions benefit from recognition cues."),
        "corrective_action": (9, "must", "The card should guide what to do after correction."),
    },
}

FRONTMATTER_MUST_KEEP = ["id", "title", "type", "domain", "status", "graph_maturity", "created", "updated"]
FRONTMATTER_OPTIMIZE = ["subdomain", "source", "tags", "confidence", "review_cycle"]
FRONTMATTER_REDUNDANT = ["related", "aliases"]


@dataclass
class SectionEvaluation:
    name: str
    layer: str
    word_count: int
    item_count: int
    score: int
    classification: str
    reason: str
    overlap_with: str
    overlap_score: float


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def flatten_value(value: Any) -> list[str]:
    if isinstance(value, dict):
        lines: list[str] = []
        for nested in value.values():
            lines.extend(flatten_value(nested))
        return lines
    return normalize_list(value)


def tokenize(text: str) -> set[str]:
    return {token.lower() for token in TOKEN_RE.findall(text)}


def jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def section_names(spec: dict[str, Any]) -> list[str]:
    sections = spec.get("sections", {})
    names: list[str] = []
    for key in sections:
        if key == "routing_and_dispatch":
            names.extend(
                [
                    "routing_and_dispatch.direct_routes",
                    "routing_and_dispatch.secondary_routes",
                    "routing_and_dispatch.gap_signals",
                    "routing_and_dispatch.stop_rules",
                ]
            )
        elif key == "promotion_assessment":
            names.extend(
                [
                    "promotion_assessment.current_recommendation",
                    "promotion_assessment.main_reasons",
                    "promotion_assessment.missing_evidence",
                    "promotion_assessment.next_rules",
                ]
            )
        else:
            names.append(key)
    return names


def extract_section_value(spec: dict[str, Any], name: str) -> list[str]:
    sections = spec.get("sections", {})
    if "." not in name:
        return flatten_value(sections.get(name))
    top, sub = name.split(".", 1)
    return flatten_value((sections.get(top) or {}).get(sub))


def layer_for_section(name: str, core_sections: list[str]) -> str:
    if name in core_sections:
        return "core"
    if name == "local_position" or name == "operational_links" or name.startswith("routing_and_dispatch."):
        return "graph"
    return "progression"


def overlap_summary(name: str, texts: dict[str, str]) -> tuple[str, float]:
    source_tokens = tokenize(texts[name])
    best_name = "-"
    best_score = 0.0
    for other_name, text in texts.items():
        if other_name == name:
            continue
        score = jaccard(source_tokens, tokenize(text))
        if score > best_score:
            best_name = other_name
            best_score = score
    return best_name, best_score


def render_sample(config: dict[str, Any]) -> None:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            sys.executable,
            str(config["renderer"]),
            "--spec",
            str(config["sample"]),
            "--output",
            str(config["output"]),
        ],
        check=True,
        cwd=str(ROOT),
    )


def evaluate_card(config: dict[str, Any]) -> list[SectionEvaluation]:
    spec = json.loads(config["sample"].read_text(encoding="utf-8"))
    texts = {name: " ".join(extract_section_value(spec, name)) for name in section_names(spec)}
    rubric = {**COMMON_RUBRIC, **TYPE_RUBRIC[config["card_type"]]}
    evaluations: list[SectionEvaluation] = []
    for name, text in texts.items():
        score, classification, reason = rubric[name]
        values = extract_section_value(spec, name)
        overlap_with, overlap_score = overlap_summary(name, texts)
        evaluations.append(
            SectionEvaluation(
                name=name,
                layer=layer_for_section(name, config["core_sections"]),
                word_count=len(TOKEN_RE.findall(text)),
                item_count=len(values),
                score=score,
                classification=classification,
                reason=reason,
                overlap_with=overlap_with,
                overlap_score=overlap_score,
            )
        )
    return evaluations


def summary_row(config: dict[str, Any], evaluations: list[SectionEvaluation]) -> dict[str, Any]:
    counts = Counter(item.classification for item in evaluations)
    words = Counter(item.layer for item in evaluations)
    word_totals = Counter()
    for item in evaluations:
        word_totals[item.layer] += item.word_count
    total_words = sum(item.word_count for item in evaluations) or 1
    trim_words = sum(item.word_count for item in evaluations if item.classification == "optimize")
    redundant_words = sum(item.word_count for item in evaluations if item.classification == "redundant")
    return {
        "card_type": config["label"],
        "sections": len(evaluations),
        "must": counts["must"],
        "optimize": counts["optimize"],
        "redundant": counts["redundant"],
        "avg_score": round(sum(item.score for item in evaluations) / len(evaluations), 2),
        "core_words": word_totals["core"],
        "graph_words": word_totals["graph"],
        "progression_words": word_totals["progression"],
        "reduction_opportunity": round((redundant_words + trim_words * 0.5) / total_words * 100, 1),
    }


def classification_label(name: str) -> str:
    labels = {
        "must": "Must keep",
        "optimize": "Optimize / stage-gate",
        "redundant": "Redundant in default render",
    }
    return labels[name]


def top_sections(evaluations: list[SectionEvaluation], classification: str) -> list[SectionEvaluation]:
    filtered = [item for item in evaluations if item.classification == classification]
    return sorted(filtered, key=lambda item: (-item.score, -item.word_count, item.name))[:5]


def render_summary_table(rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Card Type | Sections | Must | Optimize | Redundant | Avg Score | Core Words | Graph Words | Progression Words | Reduction Opportunity |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            "| {card_type} | {sections} | {must} | {optimize} | {redundant} | {avg_score} | {core_words} | {graph_words} | {progression_words} | {reduction_opportunity}% |".format(
                **row
            )
        )
    return lines


def render_frontmatter_note() -> list[str]:
    return [
        "## Frontmatter Baseline",
        "",
        "- Must keep: " + ", ".join(FRONTMATTER_MUST_KEEP),
        "- Keep but compress when possible: " + ", ".join(FRONTMATTER_OPTIMIZE),
        "- Redundant by default: " + ", ".join(FRONTMATTER_REDUNDANT),
        "",
    ]


def render_card_detail(config: dict[str, Any], evaluations: list[SectionEvaluation]) -> list[str]:
    lines = [
        f"## {config['label']}",
        "",
        f"Sample spec: `{config['sample'].relative_to(ROOT)}`",
        f"Rendered output: `{config['output'].relative_to(ROOT)}`",
        "",
        "| Section | Layer | Score | Classification | Words | Items | Highest Overlap |",
        "| --- | --- | ---: | --- | ---: | ---: | --- |",
    ]
    for item in sorted(evaluations, key=lambda value: (value.layer, -value.score, value.name)):
        overlap = f"{item.overlap_with} ({item.overlap_score:.2f})"
        lines.append(
            f"| `{item.name}` | {item.layer} | {item.score} | {classification_label(item.classification)} | "
            f"{item.word_count} | {item.item_count} | {overlap} |"
        )
    lines.append("")
    lines.append("- Must keep focus: " + ", ".join(f"`{item.name}`" for item in top_sections(evaluations, "must")))
    lines.append("- Compression candidates: " + ", ".join(f"`{item.name}`" for item in top_sections(evaluations, "optimize")))
    lines.append("- Best move-out candidates: " + ", ".join(f"`{item.name}`" for item in top_sections(evaluations, "redundant")))
    lines.append("")
    return lines


def render_global_findings(all_evaluations: dict[str, list[SectionEvaluation]]) -> list[str]:
    flat = [item for values in all_evaluations.values() for item in values]
    counts = {
        "must": Counter(item.name for item in flat if item.classification == "must"),
        "optimize": Counter(item.name for item in flat if item.classification == "optimize"),
        "redundant": Counter(item.name for item in flat if item.classification == "redundant"),
    }

    def common(counter: Counter[str]) -> str:
        return ", ".join(f"`{name}` x{count}" for name, count in counter.most_common(8))

    return [
        "## Global Findings",
        "",
        "- Must-keep patterns: " + common(counts["must"]),
        "- Compression-heavy patterns: " + common(counts["optimize"]),
        "- Default move-out patterns: " + common(counts["redundant"]),
        "",
        "## Structural Recommendation",
        "",
        "- Keep the card-type explanation layer as the default visible body.",
        "- Keep `local_position` and `operational_links` for stable cards because they carry real graph value.",
        "- Reduce `routing_and_dispatch` in stable cards to a thin direct-route layer by default; gate secondary routes, gap signals, and stop rules behind mature cards or review mode.",
        "- Collapse `current_status_notes`, `next_goal`, `promotion_assessment`, and `current_upgrade_tasks` into one compact `Upgrade Focus` block if you still want maintenance data in-body.",
        "- Move `growing_checklist`, `stable_checklist`, `expert_ready_checklist`, and `upgrade_history` out of the default render.",
        "- Treat `my_words`, `validation_question`, and similar reflection fields as optional study aids, not mandatory default sections.",
        "",
    ]


def write_report(rows: list[dict[str, Any]], all_evaluations: dict[str, list[SectionEvaluation]]) -> None:
    lines = [
        "# Learning Card Slimming Audit",
        "",
        "This audit judges the four-card family under one assumption:",
        "",
        "- target state: a default `stable` card render",
        "- goal: keep high-retrieval, high-boundary, high-graph value content visible",
        "- score rule: `8-10 = Must keep`, `5-7 = Optimize / stage-gate`, `0-4 = Redundant in default render`",
        "- test method: fill one realistic sample for each card type, render it, then score each body section",
        "",
        "## Summary",
        "",
    ]
    lines.extend(render_summary_table(rows))
    lines.append("")
    lines.extend(render_frontmatter_note())
    for config in CARD_CONFIGS:
        lines.extend(render_card_detail(config, all_evaluations[config["card_type"]]))
    lines.extend(render_global_findings(all_evaluations))
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    all_evaluations: dict[str, list[SectionEvaluation]] = {}
    for config in CARD_CONFIGS:
        render_sample(config)
        evaluations = evaluate_card(config)
        all_evaluations[config["card_type"]] = evaluations
        rows.append(summary_row(config, evaluations))
    write_report(rows, all_evaluations)
    print(f"Wrote report to {REPORT_PATH}")


if __name__ == "__main__":
    main()
