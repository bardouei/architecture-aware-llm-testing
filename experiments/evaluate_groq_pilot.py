"""Evaluate generated Groq pilot suites in isolated Xcode project copies."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evaluation.compilation_checker import CompilationChecker
from evaluation.coverage_analyzer import CoverageAnalyzer
from evaluation.mutation_testing import MutationTesting
from evaluation.test_runner import TestRunner


FIXTURE = ROOT / "datasets/fixtures/swift-sample-app"
PROJECT_NAME = "SwiftSampleApp.xcodeproj"
TEST_DIRECTORY = Path("SwiftSampleApp/Tests")
INJECTION_FILE = TEST_DIRECTORY / "GeneratedLoginViewModelTests.swift"
SOURCE_FILE = Path("SwiftSampleApp/Feature/Login/LoginViewModel.swift")
TEST_TARGET = "SwiftSampleAppTests"
CONDITIONS = ("baseline", "architecture_aware")


def prepare_workspace(fixture: Path, workspace: Path, generated_test: Path) -> Path:
    """Copy the fixture and leave exactly one non-empty generated test suite."""
    shutil.copytree(fixture, workspace)
    tests = workspace / TEST_DIRECTORY
    for test_file in tests.glob("*.swift"):
        test_file.write_text("")
    injection = workspace / INJECTION_FILE
    injection.write_text(generated_test.read_text())
    return injection


def compact_mutation(result: dict) -> dict:
    return {
        "success": result.get("success", False),
        "created": result.get("mutations_created", 0),
        "tested": result.get("mutations_tested", 0),
        "killed": result.get("mutations_killed", 0),
        "survived": result.get("mutations_survived", 0),
        "invalid": result.get("invalid_mutants", 0),
        "score": result.get("mutation_score", 0),
        "error": result.get("error"),
        "outcomes": {
            item["id"]: item["status"] for item in result.get("mutations", [])
        },
    }


def evaluate_generated_test(generated_test: Path, workspace_root: Path) -> dict:
    workspace = workspace_root / "project"
    prepare_workspace(FIXTURE, workspace, generated_test)
    project = workspace / PROJECT_NAME
    source = workspace / SOURCE_FILE
    result_bundle = workspace_root / "coverage.xcresult"
    test_runner = TestRunner(project, only_testing=TEST_TARGET)
    coverage_runner = TestRunner(
        project,
        only_testing=TEST_TARGET,
        result_bundle=result_bundle,
        enable_coverage=True,
    )

    application_build = CompilationChecker(project).check()
    suite = (
        coverage_runner.run()
        if application_build.get("success", False)
        else {"success": False, "skipped": True}
    )
    coverage = (
        CoverageAnalyzer(result_bundle, source.name).analyze()
        if suite.get("success", False)
        else {"success": False, "coverage": 0, "skipped": True}
    )
    mutation = MutationTesting(
        source,
        compilation_checker=CompilationChecker(project).check,
        test_runner=test_runner.run,
    ).run()
    suite_diagnostic = suite.get("output", suite.get("error", ""))
    return {
        "application_build_success": application_build.get("success", False),
        "generated_suite_success": suite.get("success", False),
        "tests_executed": suite.get("tests_executed", 0),
        "target_coverage": coverage.get("coverage", 0),
        "mutation": compact_mutation(mutation),
        "diagnostics": {
            "application_build": application_build.get("output", "")[-2000:],
            "generated_suite": str(suite_diagnostic)[-4000:],
        },
    }


def build_report(experiment: Path) -> str:
    rows = []
    for condition in CONDITIONS:
        evaluations = sorted((experiment / condition).glob("run-*/evaluation.json"))
        for evaluation_path in evaluations:
            result = json.loads(evaluation_path.read_text())
            rows.append(
                "| {condition} | {run} | {build} | {suite} | {count} | {coverage:.2f}% "
                "| {mutation:.2f}% |".format(
                    condition=condition,
                    run=evaluation_path.parent.name,
                    build="pass" if result["application_build_success"] else "fail",
                    suite="pass" if result["generated_suite_success"] else "fail",
                    count=result.get("tests_executed", 0),
                    coverage=result["target_coverage"],
                    mutation=result["mutation"]["score"],
                )
            )
    return """# Real Groq Pilot Evaluation

| Condition | Run | App build | Generated suite | Tests run | Coverage | Mutation score |
|---|---|---:|---:|---:|---:|---:|
{rows}

Results are per-generation observations. Failed or uncompilable suites remain in
the denominator and are not silently repaired or discarded.
""".format(rows="\n".join(rows))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-id", required=True)
    parser.add_argument(
        "--condition",
        choices=("baseline", "architecture_aware", "both"),
        default="both",
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_args()
    experiment = ROOT / "artifacts/generations" / arguments.experiment_id
    if not experiment.exists():
        raise SystemExit(f"Experiment does not exist: {experiment}")
    conditions = (
        CONDITIONS if arguments.condition == "both" else (arguments.condition,)
    )
    evaluated = 0
    for condition in conditions:
        generated_tests = sorted(
            (experiment / condition).glob("run-*/generated-test.swift")
        )
        if not generated_tests:
            raise SystemExit(f"No generated tests found for condition: {condition}")
        for generated_test in generated_tests:
            evaluation_path = generated_test.parent / "evaluation.json"
            with tempfile.TemporaryDirectory(prefix=f"aallt-{condition}-") as temporary:
                result = evaluate_generated_test(generated_test, Path(temporary))
            evaluation_path.write_text(json.dumps(result, indent=2))
            evaluated += 1
            print(
                f"{condition}/{generated_test.parent.name}: "
                f"tests={'pass' if result['generated_suite_success'] else 'fail'}, "
                f"executed={result['tests_executed']}, "
                f"coverage={result['target_coverage']:.2f}%, "
                f"mutation={result['mutation']['score']:.2f}%"
            )
    (experiment / "evaluation-report.md").write_text(build_report(experiment))
    print(f"Evaluated {evaluated} generated suite(s)")
    print(f"Report: {experiment.relative_to(ROOT)}/evaluation-report.md")


if __name__ == "__main__":
    main()
