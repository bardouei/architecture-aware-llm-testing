import unittest

from prototype.context.module_detector import ModuleDetector
from prototype.context.pattern_detector import PatternDetector


class ModuleDetectorTests(unittest.TestCase):
    def test_detects_known_architecture_folders(self):
        detector = ModuleDetector()

        self.assertEqual(
            detector.detect("Feature/Login/LoginViewModel.swift"), "Feature/Login"
        )
        self.assertEqual(detector.detect("Domain/LoginUseCase.swift"), "Domain")
        self.assertEqual(detector.detect("Data/UserRepository.swift"), "Data")
        self.assertEqual(detector.detect("Core/Network/Client.swift"), "Core")


class PatternDetectorTests(unittest.TestCase):
    def test_detects_tca_feature_components(self):
        patterns = PatternDetector().detect(
            [{"name": "HomeFeature"}], {"source_files": []}
        )

        self.assertIn("Composable Architecture (TCA)", patterns)


if __name__ == "__main__":
    unittest.main()
