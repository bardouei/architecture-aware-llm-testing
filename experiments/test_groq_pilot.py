import unittest

from experiments.generate_groq_pilot import REQUEST_SETTINGS, build_prompt, sha256


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


if __name__ == "__main__":
    unittest.main()
