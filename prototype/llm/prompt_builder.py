from pathlib import Path


class PromptBuilder:


    def __init__(self):

        self.template_path = (
            Path(__file__).parent /
            "templates"
        )



    def load_template(
        self,
        name
    ):

        path = (
            self.template_path /
            name
        )


        return path.read_text()



    def build_baseline_prompt(
        self,
        source_code
    ):


        template = self.load_template(
            "baseline_prompt.txt"
        )


        return template.format(
            source_code=source_code
        )



    def build_architecture_prompt(
        self,
        source_code,
        architecture_context
    ):


        template = self.load_template(
            "architecture_prompt.txt"
        )


        return template.format(

            source_code=source_code,

            architecture_context=
                architecture_context

        )