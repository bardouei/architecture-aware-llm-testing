import json
from pathlib import Path
import tempfile
import unittest

from experiments.evaluate_groq_pilot import (
    INJECTION_FILE,
    TEST_DIRECTORY,
    build_report,
    compact_mutation,
    prepare_workspace,
    skipped_mutation,
)


class GeneratedPilotEvaluationTests(unittest.TestCase):
    def test_workspace_contains_only_generated_suite_content(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = root / "fixture"
            tests = fixture / TEST_DIRECTORY
            tests.mkdir(parents=True)
            (tests / "ExistingTests.swift").write_text("existing")
            (tests / INJECTION_FILE.name).write_text("old generated")
            generated = root / "generated.swift"
            generated.write_text("new generated")
            workspace = root / "workspace"

            prepare_workspace(fixture, workspace, generated)

            self.assertEqual((workspace / INJECTION_FILE).read_text(), "new generated")
            existing = workspace / TEST_DIRECTORY / "ExistingTests.swift"
            self.assertEqual(existing.read_text(), "")

    def test_compacts_mutation_logs(self):
        compact = compact_mutation(
            {
                "success": True,
                "mutations_created": 1,
                "mutations_tested": 1,
                "mutations_killed": 1,
                "mutation_score": 100,
                "mutations": [{"id": "m1", "status": "killed", "check": "large"}],
            }
        )
        self.assertEqual(compact["outcomes"], {"m1": "killed"})
        self.assertNotIn("check", json.dumps(compact))

    def test_skips_mutation_after_invalid_generated_suite(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "Target.swift"
            source.write_text("final class Target { var enabled = true }")

            result = skipped_mutation(source, "suite failed")

            self.assertTrue(result["skipped"])
            self.assertEqual(result["mutations_tested"], 0)
            self.assertEqual(result["error"], "suite failed")

    def test_report_includes_saved_observations(self):
        with tempfile.TemporaryDirectory() as temporary:
            experiment = Path(temporary)
            for condition, score in (("baseline", 25), ("architecture_aware", 75)):
                run = experiment / condition / "run-001"
                run.mkdir(parents=True)
                (run / "evaluation.json").write_text(
                    json.dumps(
                        {
                            "application_build_success": True,
                            "generated_suite_compilation_success": True,
                            "generated_suite_success": True,
                            "tests_executed": 2,
                            "target_coverage": 90,
                            "mutation": {"score": score},
                        }
                    )
                )
            report = build_report(experiment)
            self.assertIn(
                "| baseline | run-001 | pass | pass | pass | 2 | 90.00% | 25.00% |",
                report,
            )
            self.assertIn("| architecture_aware | run-001", report)
            self.assertIn(
                "| baseline | 1 | 100.00% | 100.00% | 90.00% | 25.00% |",
                report,
            )


if __name__ == "__main__":
    unittest.main()
