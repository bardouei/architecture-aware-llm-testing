import json
import tempfile
import unittest
from pathlib import Path

from experiments.result_analyzer import ResultAnalyzer


class ResultAnalyzerTests(unittest.TestCase):
    def test_excludes_invalid_mutants_from_denominator(self):
        with tempfile.TemporaryDirectory() as directory:
            result_file = Path(directory) / "result.json"
            result_file.write_text(
                json.dumps(
                    {
                        "mutation": {
                            "mutations_created": 4,
                            "mutations_killed": 2,
                            "invalid_mutants": 1,
                        }
                    }
                )
            )

            metrics = ResultAnalyzer(result_file).calculate_metrics()

        self.assertEqual(metrics["mutation_score"], 66.67)

    def test_uses_score_emitted_by_mutation_engine(self):
        with tempfile.TemporaryDirectory() as directory:
            result_file = Path(directory) / "result.json"
            result_file.write_text(
                json.dumps(
                    {
                        "mutation": {
                            "mutations_created": 3,
                            "mutations_killed": 3,
                            "mutation_score": 100.0,
                        }
                    }
                )
            )

            metrics = ResultAnalyzer(result_file).calculate_metrics()

        self.assertEqual(metrics["mutation_score"], 100.0)


if __name__ == "__main__":
    unittest.main()
