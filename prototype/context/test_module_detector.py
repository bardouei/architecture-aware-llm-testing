import unittest

from prototype.context.module_detector import ModuleDetector


class ModuleDetectorTests(unittest.TestCase):
    def test_detects_known_architecture_folders(self):
        detector = ModuleDetector()

        self.assertEqual(
            detector.detect("Feature/Login/LoginViewModel.swift"), "Feature/Login"
        )
        self.assertEqual(detector.detect("Domain/LoginUseCase.swift"), "Domain")
        self.assertEqual(detector.detect("Data/UserRepository.swift"), "Data")
        self.assertEqual(detector.detect("Core/Network/Client.swift"), "Core")


if __name__ == "__main__":
    unittest.main()
