import subprocess
import unittest
from unittest.mock import patch

from evaluation.swift_package_runner import SwiftPackageRunner


class SwiftPackageRunnerTests(unittest.TestCase):
    def test_targets_only_the_generated_test_target(self):
        runner = SwiftPackageRunner("Package", "FeatureTests")

        self.assertEqual(
            runner.test_command(),
            ["swift", "test", "--package-path", "Package", "--filter", "FeatureTests"],
        )

    @patch.object(SwiftPackageRunner, "_run")
    def test_rejects_zero_test_success(self, run):
        run.return_value = subprocess.CompletedProcess([], 0, "Build complete!", "")

        result = SwiftPackageRunner("Package", "FeatureTests").test()

        self.assertFalse(result["success"])
        self.assertTrue(result["compilation_success"])
        self.assertEqual(result["tests_executed"], 0)

    @patch.object(SwiftPackageRunner, "_run")
    def test_detects_generated_test_compilation_failure(self, run):
        run.return_value = subprocess.CompletedProcess(
            [], 1, "GeneratedTests.swift:4:2: error: cannot find X in scope", ""
        )

        result = SwiftPackageRunner("Package", "FeatureTests").test()

        self.assertFalse(result["success"])
        self.assertFalse(result["compilation_success"])


if __name__ == "__main__":
    unittest.main()
