from pathlib import Path

from prototype.llm.llm_client import MockLLMClient
from prototype.llm.prompt_builder import PromptBuilder
from prototype.llm.test_generator import TestGenerator


TEMPLATE = Path(__file__).resolve().parents[1] / "templates/architecture_prompt.txt"


class ArchitectureRunner:
    """Architecture prompt runner with an injectable model client."""

    def __init__(self, client=None):
        self.generator = TestGenerator(client or MockLLMClient())

    def run(self, architecture_context, source_code):
        prompt = PromptBuilder(TEMPLATE.read_text()).build(
            architecture_context, source_code
        )
        return self.generator.generate_test(prompt)
