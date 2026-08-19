import tempfile
import unittest
from pathlib import Path

import json

from experiments.evaluate_swiftpm_study import (
    build_report,
    compact_mutation,
    prepare_workspace,
)


class EvaluateSwiftPMStudyTests(unittest.TestCase):
    def test_compact_mutation_retains_per_mutant_status(self):
        compact = compact_mutation(
            {
                "success": True,
                "mutations": [
                    {
                        "id": "flip_boolean-1",
                        "operator": "flip_boolean",
                        "description": "Flipped Boolean",
                        "line": 12,
                        "status": "killed",
                        "check": {"large": "diagnostics"},
                    }
                ],
            }
        )

        self.assertEqual(compact["results"][0]["status"], "killed")
        self.assertNotIn("check", compact["results"][0])

    def test_replaces_authored_tests_with_one_generated_suite(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "source"
            test_dir = project / "Packages/Feature/Tests/FeatureTests"
            test_dir.mkdir(parents=True)
            (project / "Packages/Feature/Package.swift").write_text("// package")
            (test_dir / "AuthoredTests.swift").write_text("authored")
            generated = root / "Generated.swift"
            generated.write_text("generated")
            workspace = root / "workspace"
            subject = {
                "package_path": "Packages/Feature",
                "test_target": "FeatureTests",
            }

            prepare_workspace(project, workspace, subject, generated)

            copied = workspace / "Packages/Feature/Tests/FeatureTests"
            self.assertEqual((copied / "AuthoredTests.swift").read_text(), "")
            self.assertEqual((copied / "GeneratedTests.swift").read_text(), "generated")

    def test_report_warns_when_local_retrieval_is_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            experiment = Path(directory)
            (experiment / "context").mkdir()
            (experiment / "context/local-context.json").write_text("[]")
            evaluation = experiment / "local_context/run-001/evaluation.json"
            evaluation.parent.mkdir(parents=True)
            evaluation.write_text(
                json.dumps(
                    {
                        "generated_suite_compilation_success": True,
                        "generated_suite_success": True,
                        "mutation": {"created": 4, "score": 25.0},
                    }
                )
            )

            report = build_report(experiment, ("local_context",))

        self.assertIn("| local_context | 1 |", report)
        self.assertIn("4.00", report)
        self.assertIn("returned zero files", report)


if __name__ == "__main__":
    unittest.main()
