import unittest

from experiments.run_swift_sample_comparison import (
    comparison_from_summaries,
    markdown_report,
    summarize_condition,
)


class ExperimentReportingTests(unittest.TestCase):
    def result(self, killed=1, score=33.33):
        return {
            "test_selector": "Target/TestClass",
            "compilation": {"success": True},
            "tests": {"success": True},
            "coverage": {"coverage": 90.0},
            "mutation": {
                "mutations_created": 3,
                "mutations_killed": killed,
                "mutations_survived": 3 - killed,
                "invalid_mutants": 0,
                "mutation_score": score,
                "mutations": [{"id": "mutant-1", "status": "killed"}],
            },
        }

    def test_summarizes_without_build_logs(self):
        summary = summarize_condition("baseline", self.result())
        self.assertEqual(summary["target_coverage"], 90.0)
        self.assertNotIn("output", summary)

    def test_builds_comparison_and_markdown_table(self):
        baseline = summarize_condition("baseline", self.result())
        architecture = summarize_condition(
            "architecture_aware", self.result(killed=3, score=100.0)
        )
        comparison = comparison_from_summaries(baseline, architecture)
        report = markdown_report(baseline, architecture, comparison)
        self.assertEqual(
            comparison["improvements"]["mutation_score"]["improvement"], 66.67
        )
        self.assertIn("| Mutation score | 33.33% | 100.00% | +66.67 pp |", report)


if __name__ == "__main__":
    unittest.main()
