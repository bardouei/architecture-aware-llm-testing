import json
import tempfile
import unittest
from pathlib import Path

from prototype.context.build_context_builder import build_shared_context


class BuildContextBuilderTests(unittest.TestCase):
    def test_reads_swiftpm_versions_and_framework_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / "Project/Package"
            package.mkdir(parents=True)
            (package / "Package.swift").write_text("// swift-tools-version: 6.2")
            (package / "Package.resolved").write_text(
                json.dumps(
                    {
                        "pins": [
                            {
                                "identity": "framework",
                                "state": {"version": "1.2.3"},
                            }
                        ]
                    }
                )
            )
            contract = root / "contract.json"
            contract.write_text(json.dumps({"allowed": ["VerifiedAPI()"]}))
            subject = {
                "project": "Project",
                "module_name": "Feature",
                "test_target": "FeatureTests",
                "build_system": "swift_package",
                "package_path": "Package",
                "framework_contract": "contract.json",
            }

            context = build_shared_context(root, subject)

        self.assertEqual(context["swift_tools_version"], "6.2")
        self.assertEqual(context["resolved_dependencies"], {"framework": "1.2.3"})
        self.assertEqual(context["framework_api_contract"]["allowed"], ["VerifiedAPI()"])


if __name__ == "__main__":
    unittest.main()
