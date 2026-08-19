"""Compile-test a framework contract fixture outside measured LLM outcomes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evaluation.swift_package_runner import SwiftPackageRunner
from evaluation.mutation_testing import MutationTesting
from experiments.evaluate_swiftpm_study import prepare_workspace
from experiments.generate_groq_study import PROTOCOL_VERSION, load_subject


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subject", default="modular-tca-splash")
    parser.add_argument(
        "--fixture",
        type=Path,
        default=ROOT / "experiments/fixtures/tca-1.26-contract-smoke.swift",
    )
    arguments = parser.parse_args()
    subject = load_subject(arguments.subject)
    if subject.get("build_system") != "swift_package":
        raise SystemExit("Framework contract smoke currently supports SwiftPM subjects")
    fixture = arguments.fixture.resolve()
    if not fixture.is_file():
        raise SystemExit(f"Contract fixture not found: {fixture}")
    with tempfile.TemporaryDirectory(prefix="aallt-contract-smoke-") as directory:
        workspace = Path(directory) / "project"
        prepare_workspace(ROOT / subject["project"], workspace, subject, fixture)
        runner = SwiftPackageRunner(
            workspace / subject["package_path"], subject["test_target"]
        )
        build = runner.build()
        test = runner.test() if build.get("success") else {"success": False}
        source = workspace / subject["source"]
        mutation = (
            MutationTesting(
                source,
                compilation_checker=runner.build,
                test_runner=runner.test,
            ).run(baseline_verified=True)
            if test.get("success")
            else {"success": False}
        )
    result = {
        "subject": subject["id"],
        "protocol": PROTOCOL_VERSION,
        "application_build_success": build.get("success", False),
        "contract_compilation_success": test.get("compilation_success", False),
        "contract_test_success": test.get("success", False),
        "tests_executed": test.get("tests_executed", 0),
        "mutations_created": mutation.get("mutations_created", 0),
        "mutations_tested": mutation.get("mutations_tested", 0),
        "mutations_killed": mutation.get("mutations_killed", 0),
        "mutations_survived": mutation.get("mutations_survived", 0),
        "invalid_mutants": mutation.get("invalid_mutants", 0),
        "mutation_score": mutation.get("mutation_score", 0.0),
    }
    print(json.dumps(result, indent=2))
    mutation_valid = (
        mutation.get("success", False)
        and result["mutations_created"] == result["mutations_tested"]
        and result["invalid_mutants"] == 0
    )
    if not result["contract_test_success"] or not mutation_valid:
        diagnostic = test.get("output", test.get("error", build.get("output", "")))
        print(str(diagnostic)[-5000:])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
