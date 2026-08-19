import tempfile
import unittest
from pathlib import Path

from prototype.analyzer.scanner import RepositoryScanner
from prototype.analyzer.swift_parser import SwiftParser


class RepositoryScannerTests(unittest.TestCase):
    def test_recognizes_xcode_test_target_directories(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "App" / "HomeViewModel.swift"
            test = root / "AppTests" / "HomeViewModelTests.swift"
            source.parent.mkdir()
            test.parent.mkdir()
            source.write_text("final class HomeViewModel {}")
            test.write_text("final class HomeViewModelTests {}")

            files = RepositoryScanner(root).scan_files(relative=True)

        self.assertEqual(files["source_files"], ["App/HomeViewModel.swift"])
        self.assertEqual(files["test_files"], ["AppTests/HomeViewModelTests.swift"])

    def test_ignores_dependency_and_generated_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "Sources/App/App.swift"
            dependency = root / ".build/checkouts/Dependency/Sources/Dependency.swift"
            generated = root / ".swiftpm/Generated.swift"
            manifest = root / "Package.swift"
            for path in (source, dependency, generated, manifest):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("struct Example {}")

            files = RepositoryScanner(root).scan_files(relative=True)

        self.assertEqual(files["source_files"], ["Sources/App/App.swift"])


class SwiftParserTests(unittest.TestCase):
    def test_extracts_classes_structs_and_actors_with_relative_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "Domain" / "Types.swift"
            source.parent.mkdir()
            source.write_text(
                """protocol Repository {}\nfinal class ViewModel {}\nstruct UseCase {}\nactor Store {}\n"""
            )

            result = SwiftParser([source], project_root=root).parse()

        self.assertEqual(
            {(item["name"], item["type"]) for item in result["components"]},
            {("ViewModel", "class"), ("UseCase", "struct"), ("Store", "actor")},
        )
        self.assertTrue(
            all(item["file"] == "Domain/Types.swift" for item in result["components"])
        )
        self.assertEqual(result["protocols"], ["Repository"])

    def test_extracts_tca_dependency_key(self):
        dependencies = SwiftParser([]).extract_dependencies(
            "@Dependency(\\.postsClient) var postsClient", "HomeFeature"
        )

        self.assertIn("postsClient", dependencies)

    def test_extracts_composed_tca_features(self):
        dependencies = SwiftParser([]).extract_dependencies(
            """struct AppFeature {
  var body: some ReducerOf<Self> {
    Scope(state: \.home, action: \.home) { HomeFeature() }
    Scope(state: \.splash, action: \.splash) { SplashFeature() }
  }
}
""",
            "AppFeature",
        )

        self.assertEqual(set(dependencies), {"HomeFeature", "SplashFeature"})


if __name__ == "__main__":
    unittest.main()
