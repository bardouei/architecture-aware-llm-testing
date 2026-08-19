import unittest

from experiments.check_openai_connection import explain_api_error


class APIError(Exception):
    def __init__(self, code):
        self.code = code


class OpenAIConnectionMessageTests(unittest.TestCase):
    def test_explains_insufficient_quota(self):
        message = explain_api_error(APIError("insufficient_quota"))
        self.assertIn("no available quota", message)

    def test_explains_unavailable_model(self):
        message = explain_api_error(APIError("model_not_found"))
        self.assertIn("AALLT_MODEL", message)


if __name__ == "__main__":
    unittest.main()
