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


if __name__ == "__main__":
    unittest.main()
