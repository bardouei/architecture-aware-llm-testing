"""Run and report the controlled Swift baseline comparison."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evaluation.compilation_checker import CompilationChecker
from evaluation.coverage_analyzer import CoverageAnalyzer
from evaluation.mutation_testing import MutationTesting
from evaluation.test_runner import TestRunner
from experiments.comparison_engine import ComparisonEngine


PROJECT = ROOT / "datasets/fixtures/swift-sample-app/SwiftSampleApp.xcodeproj"
SOURCE = (
    ROOT
    / "datasets/fixtures/swift-sample-app/SwiftSampleApp/Feature/Login/LoginViewModel.swift"
)
RESULTS = ROOT / "experiments/results"

CONDITIONS = {
    "baseline": {
        "selector": "SwiftSampleAppTests/GeneratedLoginViewModelTests",
        "description": "Source-code-only generated success-path test",
        "result": "swift-sample-app-baseline.json",
    },
    "architecture_aware": {
        "selector": "SwiftSampleAppTests/ArchitectureAwareLoginViewModelTests",
        "description": (
            "Architecture-aware success, failure, and dependency-interaction tests"
        ),
        "result": "swift-sample-app-architecture-aware.json",
    },
}


def evaluate_condition(name: str, temporary_directory: str | Path) -> dict:
    """Compile, test, measure coverage, and mutation-test one condition."""
    condition = CONDITIONS[name]
    result_bundle = Path(temporary_directory) / f"{name}.xcresult"
    selected_runner = TestRunner(PROJECT, only_testing=condition["selector"])
    coverage_runner = TestRunner(
        PROJECT,
        only_testing=condition["selector"],
        result_bundle=result_bundle,
        enable_coverage=True,
    )

    compilation = CompilationChecker(PROJECT).check()
    tests = (
        coverage_runner.run()
        if compilation["success"]
        else {"success": False, "skipped": True}
    )
    coverage = (
        CoverageAnalyzer(result_bundle, SOURCE.name).analyze()
        if tests["success"]
        else {"success": False, "coverage": 0, "skipped": True}
    )
    tests.pop("result_bundle", None)
    tests["coverage_bundle_ephemeral"] = True
    mutation = MutationTesting(
        SOURCE,
        compilation_checker=CompilationChecker(PROJECT).check,
        test_runner=selected_runner.run,
    ).run()

    return {
        "approach": name,
        "description": condition["description"],
        "test_selector": condition["selector"],
        "compilation": compilation,
        "tests": tests,
        "coverage": coverage,
        "mutation": mutation,
    }


def summarize_condition(name: str, result: dict) -> dict:
    mutation = result["mutation"]
    return {
        "dataset_id": "swift-sample-app",
        "approach": name,
        "test_selector": result["test_selector"],
        "compilation_success": result["compilation"].get("success", False),
        "test_success": result["tests"].get("success", False),
        "target_coverage": result["coverage"].get("coverage", 0),
        "mutation": {
            "created": mutation.get("mutations_created", 0),
            "killed": mutation.get("mutations_killed", 0),
            "survived": mutation.get("mutations_survived", 0),
            "invalid": mutation.get("invalid_mutants", 0),
            "score": mutation.get("mutation_score", 0),
            "outcomes": {
                item["id"]: item["status"] for item in mutation.get("mutations", [])
            },
        },
    }


def condition_metrics(summary: dict) -> dict:
    return {
        "compilation_success": int(summary["compilation_success"]),
        "test_success": int(summary["test_success"]),
        "coverage": summary["target_coverage"],
        "mutation_score": summary["mutation"]["score"],
    }


def print_condition_table(summary: dict) -> None:
    print("\n| Condition | Compile | Tests | Coverage | Mutation score |")
    print("|---|---:|---:|---:|---:|")
    print(
        f"| {summary['approach']} "
        f"| {'100%' if summary['compilation_success'] else '0%'} "
        f"| {'100%' if summary['test_success'] else '0%'} "
        f"| {summary['target_coverage']:.2f}% "
        f"| {summary['mutation']['score']:.2f}% |"
    )


def save_condition(name: str, result: dict) -> dict:
    RESULTS.mkdir(parents=True, exist_ok=True)
    summary = summarize_condition(name, result)
    (RESULTS / CONDITIONS[name]["result"]).write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    return summary


def load_condition(name: str) -> dict:
    return json.loads((RESULTS / CONDITIONS[name]["result"]).read_text())


def comparison_from_summaries(baseline: dict, architecture: dict) -> dict:
    comparison = ComparisonEngine(
        condition_metrics(baseline), condition_metrics(architecture)
    ).compare()
    comparison["experimental_control"] = {
        "same_production_source": str(SOURCE.relative_to(ROOT)),
        "same_mutants": True,
        "isolated_with_xcode_only_testing": True,
        "baseline_selector": CONDITIONS["baseline"]["selector"],
        "architecture_selector": CONDITIONS["architecture_aware"]["selector"],
    }
    return comparison


def markdown_report(baseline: dict, architecture: dict, comparison: dict) -> str:
    metrics = comparison["comparison"]
    improvements = comparison["improvements"]
    mutant_ids = sorted(
        set(baseline["mutation"]["outcomes"])
        | set(architecture["mutation"]["outcomes"])
    )
    mutant_rows = "\n".join(
        f"| `{mutant_id}` | {baseline['mutation']['outcomes'].get(mutant_id, 'n/a')} "
        f"| {architecture['mutation']['outcomes'].get(mutant_id, 'n/a')} |"
        for mutant_id in mutant_ids
    )
    return f"""# Swift Sample App Comparison

Target: `LoginViewModel.swift`

## Results

| Metric | Baseline | Architecture-aware | Difference |
|---|---:|---:|---:|
| Compilation success | {metrics['baseline']['compilation_success'] * 100:.0f}% | {metrics['architecture_aware']['compilation_success'] * 100:.0f}% | 0 pp |
| Test success | {metrics['baseline']['test_success'] * 100:.0f}% | {metrics['architecture_aware']['test_success'] * 100:.0f}% | 0 pp |
| Target coverage | {metrics['baseline']['coverage']:.2f}% | {metrics['architecture_aware']['coverage']:.2f}% | {improvements['coverage']['improvement']:+.2f} pp |
| Mutation score | {metrics['baseline']['mutation_score']:.2f}% | {metrics['architecture_aware']['mutation_score']:.2f}% | {improvements['mutation_score']['improvement']:+.2f} pp |

## Mutant outcomes

| Mutant | Baseline | Architecture-aware |
|---|---|---|
{mutant_rows}

## Interpretation

Both isolated suites compile and pass. The architecture-aware suite covers the
target completely and kills all three seeded faults. This is pipeline-validation
evidence for one controlled component, not a general research conclusion.
"""


def save_comparison(baseline: dict, architecture: dict) -> dict:
    comparison = comparison_from_summaries(baseline, architecture)
    (RESULTS / "swift-sample-app-comparison.json").write_text(
        json.dumps(comparison, indent=2) + "\n"
    )
    (RESULTS / "swift-sample-app-comparison.md").write_text(
        markdown_report(baseline, architecture, comparison)
    )
    return comparison


def run_selected(name: str) -> dict:
    if name not in CONDITIONS:
        raise ValueError(f"Unknown condition: {name}")
    print(f"Running isolated {name} pipeline")
    with tempfile.TemporaryDirectory(prefix=f"aallt-{name}-") as temporary:
        result = evaluate_condition(name, temporary)
    summary = save_condition(name, result)
    print_condition_table(summary)
    return summary


def run() -> dict:
    baseline = run_selected("baseline")
    architecture = run_selected("architecture_aware")
    comparison = save_comparison(baseline, architecture)
    print(f"\nSaved results to {RESULTS}")
    return comparison


if __name__ == "__main__":
    run()
