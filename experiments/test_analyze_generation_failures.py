import unittest

from experiments.analyze_generation_failures import (
    classify_diagnostic,
    exact_mcnemar_p_value,
)


class AnalyzeGenerationFailuresTests(unittest.TestCase):
    def test_classifies_multiple_compilation_causes(self):
        categories = classify_diagnostic(
            "Cannot convert value of type 'Int' to expected argument type 'String'\n"
            "requires that 'User' conform to 'Equatable'"
        )

        self.assertEqual(
            categories,
            ["non_equatable_assertion", "type_or_signature_hallucination"],
        )

    def test_computes_two_sided_exact_mcnemar_value(self):
        self.assertAlmostEqual(exact_mcnemar_p_value(5, 1), 0.21875)
        self.assertEqual(exact_mcnemar_p_value(0, 0), 1.0)


if __name__ == "__main__":
    unittest.main()
