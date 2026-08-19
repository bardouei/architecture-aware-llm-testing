from pathlib import Path
import tempfile
import unittest

from prototype.run_pipeline import collect_source_evidence


class SourceEvidenceTests(unittest.TestCase):
    def test_collects_selected_non_target_declarations(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            (project / "Target.swift").write_text("final class Target {}")
            (project / "Dependency.swift").write_text(
                "protocol Dependency {}\nstruct Value {}"
            )
            selected = [
                {"name": "Target"},
                {"name": "Dependency"},
            ]

            evidence = collect_source_evidence(
                project,
                ["Target.swift", "Dependency.swift"],
                selected,
                "Target",
            )

            self.assertEqual(len(evidence), 1)
            self.assertEqual(evidence[0]["path"], "Dependency.swift")
            self.assertIn("protocol Dependency", evidence[0]["content"])


if __name__ == "__main__":
    unittest.main()
