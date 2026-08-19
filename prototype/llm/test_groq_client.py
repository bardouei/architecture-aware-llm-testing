import unittest
from types import SimpleNamespace
from unittest.mock import patch

from prototype.llm.groq_client import GroqClient


class Usage:
    def model_dump(self):
        return {"prompt_tokens": 8, "completion_tokens": 2}


class FakeCompletions:
    def __init__(self):
        self.arguments = None

    def create(self, **arguments):
        self.arguments = arguments
        return SimpleNamespace(
            id="groq-response-1",
            model="test-model",
            choices=[SimpleNamespace(message=SimpleNamespace(content="OK"))],
            usage=Usage(),
        )


class GroqClientTests(unittest.TestCase):
    def test_generates_text_and_captures_provenance(self):
        completions = FakeCompletions()
        sdk = SimpleNamespace(chat=SimpleNamespace(completions=completions))
        times = iter([20.0, 20.25])
        client = GroqClient(
            model="test-model", client=sdk, clock=lambda: next(times)
        )

        self.assertEqual(client.generate("ping"), "OK")
        self.assertEqual(
            completions.arguments,
            {
                "model": "test-model",
                "messages": [{"role": "user", "content": "ping"}],
            },
        )
        self.assertEqual(client.last_metadata["provider"], "groq")
        self.assertEqual(client.last_metadata["latency_ms"], 250.0)

    def test_requires_model(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaisesRegex(ValueError, "AALLT_MODEL"):
                GroqClient(client=object())

    def test_sends_controlled_generation_settings(self):
        completions = FakeCompletions()
        sdk = SimpleNamespace(chat=SimpleNamespace(completions=completions))
        client = GroqClient(
            model="test-model",
            client=sdk,
            temperature=0.6,
            max_completion_tokens=4096,
            reasoning_format="hidden",
        )

        client.generate("generate")

        self.assertEqual(completions.arguments["temperature"], 0.6)
        self.assertEqual(completions.arguments["max_completion_tokens"], 4096)
        self.assertEqual(
            completions.arguments["extra_body"], {"reasoning_format": "hidden"}
        )
        self.assertEqual(
            client.last_metadata["request_settings"], client.request_settings
        )

    def test_requires_api_key_for_real_client(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaisesRegex(ValueError, "GROQ_API_KEY"):
                GroqClient(model="test-model")


if __name__ == "__main__":
    unittest.main()
