import unittest
from types import SimpleNamespace
from unittest.mock import patch

from prototype.llm.openai_client import OpenAIResponsesClient


class Usage:
    def model_dump(self):
        return {"input_tokens": 10, "output_tokens": 2}


class FakeResponses:
    def __init__(self):
        self.arguments = None

    def create(self, **arguments):
        self.arguments = arguments
        return SimpleNamespace(
            id="response-1",
            model="test-model",
            output_text="OK",
            usage=Usage(),
        )


class OpenAIResponsesClientTests(unittest.TestCase):
    def test_generates_text_and_captures_provenance(self):
        responses = FakeResponses()
        sdk = SimpleNamespace(responses=responses)
        times = iter([10.0, 10.125])
        client = OpenAIResponsesClient(
            model="test-model", client=sdk, clock=lambda: next(times)
        )

        self.assertEqual(client.generate("ping"), "OK")
        self.assertEqual(
            responses.arguments,
            {"model": "test-model", "input": "ping", "store": False},
        )
        self.assertEqual(client.last_metadata["latency_ms"], 125.0)
        self.assertEqual(client.last_metadata["usage"]["input_tokens"], 10)

    def test_requires_explicit_model(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaisesRegex(ValueError, "AALLT_MODEL"):
                OpenAIResponsesClient(model=None, client=object())

    def test_requires_api_key_for_real_sdk_client(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaisesRegex(ValueError, "OPENAI_API_KEY"):
                OpenAIResponsesClient(model="test-model")


if __name__ == "__main__":
    unittest.main()
