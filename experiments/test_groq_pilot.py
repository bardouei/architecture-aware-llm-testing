import unittest

from experiments.generate_groq_pilot import (
    REQUEST_SETTINGS,
    PROTOCOL_VERSION,
    build_prompt,
    sha256,
    validate_resume_manifest,
)


class GroqPilotTests(unittest.TestCase):
    def test_baseline_prompt_does_not_include_architecture_context(self):
        prompt, _ = build_prompt("baseline", "class Target {}", {"secret": "fact"})
        self.assertNotIn("secret", prompt)
        self.assertIn("class Target {}", prompt)

    def test_architecture_prompt_includes_context(self):
        prompt, _ = build_prompt(
            "architecture_aware", "class Target {}", {"patterns": ["MVVM"]}
        )
        self.assertIn("MVVM", prompt)

    def test_sha256_is_stable(self):
        self.assertEqual(sha256("prompt"), sha256("prompt"))

    def test_pilot_uses_controlled_qwen_settings(self):
        self.assertEqual(REQUEST_SETTINGS["temperature"], 0.6)
        self.assertEqual(REQUEST_SETTINGS["reasoning_format"], "hidden")
        self.assertEqual(REQUEST_SETTINGS["reasoning_effort"], "none")
        self.assertEqual(PROTOCOL_VERSION, "qwen-pilot-v1")

    def test_resume_rejects_changed_controls(self):
        expected = {
            "experiment_id": "pilot",
            "dataset_id": "fixture",
            "provider": "groq",
            "requested_model": "model-a",
            "conditions": ["baseline"],
            "runs_per_condition": 1,
            "request_settings": {"temperature": 0.6},
            "protocol_version": "v1",
        }
        existing = dict(expected, requested_model="model-b")

        with self.assertRaisesRegex(ValueError, "requested_model"):
            validate_resume_manifest(existing, expected)

    def test_resume_accepts_identical_controls(self):
        manifest = {
            "experiment_id": "pilot",
            "dataset_id": "fixture",
            "provider": "groq",
            "requested_model": "model-a",
            "conditions": ["baseline", "architecture_aware"],
            "runs_per_condition": 1,
            "request_settings": REQUEST_SETTINGS,
            "protocol_version": PROTOCOL_VERSION,
        }

        validate_resume_manifest(manifest, manifest.copy())


if __name__ == "__main__":
    unittest.main()
