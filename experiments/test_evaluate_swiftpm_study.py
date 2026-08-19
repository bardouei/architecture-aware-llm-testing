import tempfile
import unittest
from pathlib import Path

from experiments.evaluate_swiftpm_study import prepare_workspace


class EvaluateSwiftPMStudyTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
