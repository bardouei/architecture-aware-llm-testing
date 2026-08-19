from prototype.llm.llm_client import LLMClient



class TestGenerator:


    def __init__(
        self,
        client: LLMClient
    ):

        self.client = client



    def generate_test(
        self,
        prompt
    ):

        return self.client.generate(
            prompt
        )