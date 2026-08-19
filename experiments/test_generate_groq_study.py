import unittest
from unittest.mock import patch

from experiments.generate_groq_study import (
    build_generation_schedule,
    build_prompt,
    generate_with_retry,
    PROTOCOL_VERSION,
    rate_limit_delay,
)


class GenerateGroqStudyTests(unittest.TestCase):
    def test_uses_v3_protocol(self):
        self.assertEqual(PROTOCOL_VERSION, "three-condition-v3")

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
            {"framework_api_contract": {"allowed": ["VerifiedAPI()"]}},
        )

        self.assertIn("Dependency.swift", prompt)
        self.assertIn("VerifiedAPI()", prompt)
        self.assertNotIn('"TCA"', prompt)

    def test_every_condition_receives_identical_build_grounding(self):
        subject = {"module_name": "Feature"}
        build_context = {"resolved_dependencies": {"framework": "1.2.3"}}

        prompts = [
            build_prompt(
                condition,
                subject,
                "struct Target {}",
                [],
                {},
                build_context,
            )[0]
            for condition in ("source_only", "local_context", "architecture_aware")
        ]

        self.assertTrue(all('"framework": "1.2.3"' in prompt for prompt in prompts))
        self.assertTrue(
            all("empty or comment-only trailing closure" in prompt for prompt in prompts)
        )

    def test_parses_provider_retry_delay(self):
        error = RuntimeError("429 rate_limit: Please try again in 960ms")

        self.assertEqual(rate_limit_delay(error, 0.1), 1.21)

    @patch("experiments.generate_groq_study.time.sleep")
    def test_retries_rate_limit_without_replacing_request(self, sleep):
        class Client:
            calls = 0

            def generate(self, prompt):
                self.calls += 1
                if self.calls == 1:
                    raise RuntimeError("429 rate_limit: try again in 1s")
                return "generated"

        client = Client()

        result = generate_with_retry(client, "same prompt", 2, 0.1)

        self.assertEqual(result, "generated")
        self.assertEqual(client.calls, 2)
        sleep.assert_called_once_with(1.25)


if __name__ == "__main__":
    unittest.main()
