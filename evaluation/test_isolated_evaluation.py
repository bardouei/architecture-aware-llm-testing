import subprocess
import unittest
from unittest.mock import patch

from evaluation.coverage_analyzer import CoverageAnalyzer
from evaluation.test_runner import TestRunner


class TestRunnerTests(unittest.TestCase):
    def test_builds_an_isolated_coverage_command(self):
        runner = TestRunner(
            "Sample.xcodeproj",
            only_testing="SampleTests/GeneratedTests",
            result_bundle="result.xcresult",
            enable_coverage=True,
        )

        command = runner.command()

        self.assertIn("-only-testing:SampleTests/GeneratedTests", command)
        self.assertIn("-enableCodeCoverage", command)
        self.assertIn("-resultBundlePath", command)

    @patch("evaluation.test_runner.subprocess.run")
    def test_reports_xcode_result(self, run):
        run.return_value = subprocess.CompletedProcess(
            [], 0, "Test case 'Example.testOne()' passed", ""
        )

        result = TestRunner("Sample.xcodeproj").run()

        self.assertTrue(result["success"])
        self.assertTrue(result["compilation_success"])
        self.assertIn("passed", result["output"])
        self.assertEqual(result["tests_executed"], 1)

    @patch("evaluation.test_runner.subprocess.run")
    def test_rejects_successful_xcode_run_with_zero_tests(self, run):
        run.return_value = subprocess.CompletedProcess([], 0, "Testing started", "")

        result = TestRunner("Sample.xcodeproj").run()

        self.assertFalse(result["success"])
        self.assertTrue(result["xcode_success"])
        self.assertEqual(result["tests_executed"], 0)
        self.assertIn("zero tests", result["error"])

    @patch("evaluation.test_runner.subprocess.run")
    def test_reports_generated_suite_compilation_failure(self, run):
        run.return_value = subprocess.CompletedProcess(
            [],
            65,
            "GeneratedTests.swift:10:2: error: actor isolation violation\n"
            "Testing cancelled because the build failed",
            "",
        )

        result = TestRunner("Sample.xcodeproj").run()

        self.assertFalse(result["success"])
        self.assertFalse(result["compilation_success"])


class CoverageAnalyzerTests(unittest.TestCase):
    def test_extracts_coverage_for_the_requested_source_file(self):
        report = """SwiftSampleApp.app 90.00% (9/10)\n  LoginViewModel.swift 75.00% (6/8)\n"""
        analyzer = CoverageAnalyzer("unused", "LoginViewModel.swift")

        coverage = analyzer.extract_file_percentage(report, "LoginViewModel.swift")

        self.assertEqual(coverage, 75.0)

    def test_missing_source_file_returns_zero(self):
        analyzer = CoverageAnalyzer("unused", "Other.swift")

        coverage = analyzer.extract_file_percentage(
            "LoginViewModel.swift 75.00% (6/8)", "Other.swift"
        )

        self.assertEqual(coverage, 0)


if __name__ == "__main__":
    unittest.main()
