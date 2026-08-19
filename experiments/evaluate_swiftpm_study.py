"""Evaluate generated SwiftPM study suites in isolated project copies."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
from statistics import mean
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evaluation.mutation_testing import MutationTesting
from evaluation.swift_package_runner import SwiftPackageRunner
from experiments.generate_groq_study import CONDITIONS


def prepare_workspace(project: Path, workspace: Path, subject: dict, generated: Path) -> None:
    shutil.copytree(
        project,
        workspace,
        ignore=shutil.ignore_patterns(".git", ".build", ".swiftpm", ".DS_Store"),
    )
    tests = workspace / subject["package_path"] / "Tests" / subject["test_target"]
    if not tests.is_dir():
        raise ValueError(f"Test target directory not found: {tests}")
    for test_file in tests.rglob("*.swift"):
        test_file.write_text("")
    (tests / "GeneratedTests.swift").write_text(generated.read_text())


def compact_mutation(result: dict) -> dict:
    return {
        "success": result.get("success", False),
        "created": result.get("mutations_created", 0),
        "tested": result.get("mutations_tested", 0),
        "killed": result.get("mutations_killed", 0),
        "survived": result.get("mutations_survived", 0),
        "invalid": result.get("invalid_mutants", 0),
        "score": result.get("mutation_score", 0.0),
        "error": result.get("error"),
    }


def evaluate(generated: Path, subject: dict, temporary: Path) -> dict:
    source_project = ROOT / subject["project"]
    workspace = temporary / "project"
    prepare_workspace(source_project, workspace, subject, generated)
    package = workspace / subject["package_path"]
    source = workspace / subject["source"]
    runner = SwiftPackageRunner(package, subject["test_target"])
    application = runner.build()
    suite = runner.test() if application.get("success") else {"success": False}
    if suite.get("success"):
        mutation = MutationTesting(
            source, compilation_checker=runner.build, test_runner=runner.test
        ).run(baseline_verified=True)
    else:
        discovered = MutationTesting(source).create_mutation()
        mutation = {
            "success": False,
            "error": "Generated suite did not compile and pass",
            "mutations_created": discovered["mutations_created"],
        }
    return {
        "application_build_success": application.get("success", False),
        "generated_suite_compilation_success": suite.get("compilation_success", False),
        "generated_suite_success": suite.get("success", False),
        "tests_executed": suite.get("tests_executed", 0),
        "target_coverage": None,
        "mutation": compact_mutation(mutation),
        "diagnostics": {
            "application_build": application.get("output", application.get("error", "")),
            "generated_suite": suite.get("output", suite.get("error", "")),
        },
    }


def build_report(experiment: Path, conditions: tuple[str, ...]) -> str:
    rows = [
        "# SwiftPM Generated-Suite Evaluation",
        "",
        "| Condition | N | Compile rate | Test success | Mean mutation |",
        "|---|---:|---:|---:|---:|",
    ]
    for condition in conditions:
        results = [
            json.loads(path.read_text())
            for path in sorted((experiment / condition).glob("run-*/evaluation.json"))
        ]
        if not results:
            continue
        count = len(results)
        rows.append(
            f"| {condition} | {count} | "
            f"{100 * sum(r['generated_suite_compilation_success'] for r in results) / count:.2f}% | "
            f"{100 * sum(r['generated_suite_success'] for r in results) / count:.2f}% | "
            f"{mean(r['mutation']['score'] for r in results):.2f}% |"
        )
    rows.extend(
        [
            "",
            "Failed suites remain in every denominator. SwiftPM focal-file coverage is "
            "not yet reported by this evaluator; mutation score is the primary quality outcome.",
            "",
        ]
    )
    return "\n".join(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-id", required=True)
    parser.add_argument("--condition", choices=(*CONDITIONS, "all"), default="all")
    parser.add_argument("--resume", action="store_true")
    arguments = parser.parse_args()
    experiment = ROOT / "artifacts/studies" / arguments.experiment_id
    manifest_path = experiment / "manifest.json"
    if not manifest_path.is_file():
        raise SystemExit(f"Study manifest not found: {manifest_path}")
    manifest = json.loads(manifest_path.read_text())
    subject = manifest["subject"]
    if subject.get("build_system") != "swift_package":
        raise SystemExit("This evaluator supports only SwiftPM subjects")
    conditions = tuple(manifest["conditions"]) if arguments.condition == "all" else (arguments.condition,)
    evaluated = 0
    for condition in conditions:
        generated_tests = sorted((experiment / condition).glob("run-*/generated-test.swift"))
        if not generated_tests:
            raise SystemExit(f"No generated tests found for {condition}")
        for generated in generated_tests:
            evaluation_path = generated.parent / "evaluation.json"
            if arguments.resume and evaluation_path.exists():
                print(f"Kept {condition}/{generated.parent.name}")
                continue
            with tempfile.TemporaryDirectory(prefix=f"aallt-swiftpm-{condition}-") as directory:
                result = evaluate(generated, subject, Path(directory))
            evaluation_path.write_text(json.dumps(result, indent=2) + "\n")
            evaluated += 1
            print(
                f"{condition}/{generated.parent.name}: "
                f"compile={'pass' if result['generated_suite_compilation_success'] else 'fail'}, "
                f"tests={'pass' if result['generated_suite_success'] else 'fail'}, "
                f"executed={result['tests_executed']}, mutation={result['mutation']['score']:.2f}%"
            )
    (experiment / "evaluation-report.md").write_text(build_report(experiment, conditions))
    print(f"Evaluated {evaluated} generated suite(s)")


if __name__ == "__main__":
    main()
