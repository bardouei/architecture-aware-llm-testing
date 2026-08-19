import unittest

from experiments.smoke_swiftpm_subjects import count_xctests


class SmokeSwiftPMSubjectsTests(unittest.TestCase):
    def test_counts_xctest_results(self):
        output = "\n".join(
            [
                "Test Case '-[FeatureTests testOne]' passed (0.1 seconds)",
                "Test case 'FeatureTests.testTwo()' failed (0.1 seconds)",
            ]
        )

        self.assertEqual(count_xctests(output), 2)


if __name__ == "__main__":
    unittest.main()
