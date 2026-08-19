import unittest

from prototype.llm.output_cleaner import clean_generated_code


class OutputCleanerTests(unittest.TestCase):
    def test_removes_thinking_and_swift_fence(self):
        raw = """<think>private reasoning</think>
```swift
import XCTest
```
"""
        self.assertEqual(clean_generated_code(raw), "import XCTest\n")

    def test_preserves_unfenced_code(self):
        self.assertEqual(
            clean_generated_code("import XCTest\nfinal class Tests {}"),
            "import XCTest\nfinal class Tests {}\n",
        )


if __name__ == "__main__":
    unittest.main()
