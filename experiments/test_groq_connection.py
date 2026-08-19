import unittest

from experiments.check_groq_connection import explain_api_error


class APIError(Exception):
    def __init__(self, code=None, status_code=None):
        self.code = code
        self.status_code = status_code


class GroqConnectionMessageTests(unittest.TestCase):
    def test_explains_invalid_key(self):
        self.assertIn("GROQ_API_KEY", explain_api_error(APIError(status_code=401)))

    def test_explains_rate_limit(self):
        self.assertIn("rate limit", explain_api_error(APIError(status_code=429)))

    def test_explains_unavailable_model(self):
        self.assertIn("AALLT_MODEL", explain_api_error(APIError(status_code=404)))


if __name__ == "__main__":
    unittest.main()
