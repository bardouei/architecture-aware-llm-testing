from pathlib import Path

from prototype.llm.llm_client import MockLLMClient
from prototype.llm.prompt_builder import PromptBuilder
from prototype.llm.test_generator import TestGenerator


TEMPLATE = Path(__file__).resolve().parents[1] / "templates/baseline_prompt.txt"


class BaselineRunner:
    """Deterministic fixture runner; not a real-model experiment runner."""

    def __init__(self, client=None):
        self.generator = TestGenerator(client or MockLLMClient())

    def run(self, source_code):
        prompt = PromptBuilder(TEMPLATE.read_text()).build({}, source_code)
        return self.generator.generate_test(prompt)
