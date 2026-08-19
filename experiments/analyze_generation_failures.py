"""Aggregate repeated-generation outcomes and classify compilation failures."""

from __future__ import annotations

import argparse
from collections import Counter
from math import comb
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
CONDITIONS = ("baseline", "architecture_aware")
FAILURE_PATTERNS = (
    (
        "actor_isolation",
        re.compile(r"main actor-isolated|actor isolated|actor-isolated", re.I),
    ),
    (
        "xctest_lifecycle_override",
        re.compile(r"overriding a throwing ['‘]?@objc['’]? method", re.I),
    ),
    (
        "non_equatable_assertion",
        re.compile(r"requires that ['‘].+['’] conform to ['‘]Equatable['’]", re.I),
    ),
    (
        "undefined_symbol",
        re.compile(r"cannot find .+ in scope", re.I),
    ),
    (
        "type_or_signature_hallucination",
        re.compile(
            r"cannot convert value of type|extra argument|missing argument|incorrect argument label",
            re.I,
        ),
    ),
)


def classify_diagnostic(diagnostic: str) -> list[str]:
    labels = [label for label, pattern in FAILURE_PATTERNS if pattern.search(diagnostic)]
    return labels or ["other_compilation_failure"]


def exact_mcnemar_p_value(left_wins: int, right_wins: int) -> float:
    """Two-sided exact binomial test for paired discordant outcomes."""
    discordant = left_wins + right_wins
    if not discordant:
        return 1.0
    smaller = min(left_wins, right_wins)
    tail = sum(comb(discordant, value) for value in range(smaller + 1)) / (2**discordant)
    return min(1.0, 2 * tail)


def load_runs(experiment: Path, condition: str) -> list[dict]:
    runs = []
    for evaluation_path in sorted((experiment / condition).glob("run-*/evaluation.json")):
        evaluation = json.loads(evaluation_path.read_text())
        diagnostic = evaluation.get("diagnostics", {}).get("generated_suite", "")
        evaluation["run"] = evaluation_path.parent.name
        evaluation["failure_categories"] = (
            []
            if evaluation.get("generated_suite_compilation_success")
            else classify_diagnostic(diagnostic)
        )
        runs.append(evaluation)
    return runs


def summarize_condition(runs: list[dict]) -> dict:
    count = len(runs)
    if not count:
        return {"runs": 0}
    compile_count = sum(bool(run.get("generated_suite_compilation_success")) for run in runs)
    test_count = sum(bool(run.get("generated_suite_success")) for run in runs)
    failures = Counter(
        category for run in runs for category in run.get("failure_categories", [])
    )
    passing = [run for run in runs if run.get("generated_suite_success")]
    return {
        "runs": count,
        "compilation_success_count": compile_count,
        "compilation_success_rate": compile_count / count,
        "test_success_count": test_count,
        "test_success_rate": test_count / count,
        "unconditional_mean_coverage": sum(run.get("target_coverage", 0) for run in runs) / count,
        "unconditional_mean_mutation_score": sum(
            run.get("mutation", {}).get("score", 0) for run in runs
        )
        / count,
        "conditional_mean_coverage": (
            sum(run.get("target_coverage", 0) for run in passing) / len(passing)
            if passing
            else 0.0
        ),
        "conditional_mean_mutation_score": (
            sum(run.get("mutation", {}).get("score", 0) for run in passing) / len(passing)
            if passing
            else 0.0
        ),
        "failure_categories": dict(sorted(failures.items())),
    }


def analyze(experiment: Path) -> dict:
    runs = {condition: load_runs(experiment, condition) for condition in CONDITIONS}
    by_run = {
        condition: {run["run"]: run for run in condition_runs}
        for condition, condition_runs in runs.items()
    }
    common = sorted(set(by_run["baseline"]) & set(by_run["architecture_aware"]))
    architecture_wins = sum(
        not by_run["baseline"][name].get("generated_suite_success", False)
        and by_run["architecture_aware"][name].get("generated_suite_success", False)
        for name in common
    )
    baseline_wins = sum(
        by_run["baseline"][name].get("generated_suite_success", False)
        and not by_run["architecture_aware"][name].get("generated_suite_success", False)
        for name in common
    )
    return {
        "experiment_id": experiment.name,
        "conditions": {
            condition: summarize_condition(condition_runs)
            for condition, condition_runs in runs.items()
        },
        "paired_test_success": {
            "pairs": len(common),
            "architecture_aware_wins": architecture_wins,
            "baseline_wins": baseline_wins,
            "ties": len(common) - architecture_wins - baseline_wins,
            "exact_mcnemar_p_value": exact_mcnemar_p_value(
                architecture_wins, baseline_wins
            ),
        },
        "failed_runs": {
            condition: [
                {"run": run["run"], "categories": run["failure_categories"]}
                for run in condition_runs
                if not run.get("generated_suite_compilation_success")
            ]
            for condition, condition_runs in runs.items()
        },
    }


def percentage(value: float) -> str:
    return f"{value * 100:.2f}%"


def render_markdown(result: dict) -> str:
    lines = [
        f"# {result['experiment_id']} — Aggregated Results",
        "",
        "| Condition | Compile success | Test success | Coverage (all runs) | Mutation (all runs) | Mutation (passing suites) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for condition in CONDITIONS:
        summary = result["conditions"][condition]
        lines.append(
            f"| {condition} | {summary['compilation_success_count']}/{summary['runs']} "
            f"({percentage(summary['compilation_success_rate'])}) | "
            f"{summary['test_success_count']}/{summary['runs']} "
            f"({percentage(summary['test_success_rate'])}) | "
            f"{summary['unconditional_mean_coverage']:.2f}% | "
            f"{summary['unconditional_mean_mutation_score']:.2f}% | "
            f"{summary['conditional_mean_mutation_score']:.2f}% |"
        )
    paired = result["paired_test_success"]
    lines.extend(
        [
            "",
            "## Paired comparison",
            "",
            f"Architecture-aware won {paired['architecture_aware_wins']} discordant pairs; "
            f"baseline won {paired['baseline_wins']}. The two-sided exact McNemar "
            f"p-value is {paired['exact_mcnemar_p_value']:.5f}. This pilot is therefore "
            "directionally promising but not statistically conclusive.",
            "",
            "## Compilation failure taxonomy",
            "",
            "| Condition | Category | Runs affected |",
            "|---|---|---:|",
        ]
    )
    for condition in CONDITIONS:
        for category, count in result["conditions"][condition]["failure_categories"].items():
            lines.append(f"| {condition} | {category} | {count} |")
    lines.extend(
        [
            "",
            "Failed suites remain in every unconditional denominator. A failure can have "
            "more than one category, so category counts need not sum to failed runs.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-id", required=True)
    parser.add_argument("--output-prefix", type=Path)
    arguments = parser.parse_args()
    experiment = ROOT / "artifacts/generations" / arguments.experiment_id
    if not experiment.is_dir():
        raise SystemExit(f"Experiment not found: {experiment}")
    result = analyze(experiment)
    prefix = arguments.output_prefix or ROOT / "experiments/results" / arguments.experiment_id
    if not prefix.is_absolute():
        prefix = ROOT / prefix
    prefix.parent.mkdir(parents=True, exist_ok=True)
    json_path = prefix.with_name(prefix.name + "-summary.json")
    markdown_path = prefix.with_name(prefix.name + "-summary.md")
    json_path.write_text(json.dumps(result, indent=2) + "\n")
    markdown_path.write_text(render_markdown(result))
    print(markdown_path.relative_to(ROOT))


if __name__ == "__main__":
    main()
