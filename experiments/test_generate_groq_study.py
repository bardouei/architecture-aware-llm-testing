import unittest

from experiments.generate_groq_study import build_generation_schedule, build_prompt


class GenerateGroqStudyTests(unittest.TestCase):
    def test_rotates_three_condition_order(self):
        conditions = ("source_only", "local_context", "architecture_aware")

        schedule = build_generation_schedule(conditions, 3)

        self.assertEqual(
            schedule,
            [
                ("source_only", 1),
                ("local_context", 1),
                ("architecture_aware", 1),
                ("local_context", 2),
                ("architecture_aware", 2),
                ("source_only", 2),
                ("architecture_aware", 3),
                ("source_only", 3),
                ("local_context", 3),
            ],
        )

    def test_local_condition_does_not_receive_architecture_labels(self):
        subject = {"module_name": "Feature"}
        prompt, _ = build_prompt(
            "local_context",
            subject,
            "struct Target {}",
            [{"path": "Dependency.swift", "content": "struct Dependency {}"}],
            {"architecture": {"patterns": ["TCA"]}},
        )

        self.assertIn("Dependency.swift", prompt)
        self.assertNotIn('"TCA"', prompt)


if __name__ == "__main__":
    unittest.main()
