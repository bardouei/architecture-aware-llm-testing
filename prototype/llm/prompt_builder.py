import json



class PromptBuilder:


    def __init__(
        self,
        template
    ):

        self.template = template




    def build(
        self,
        architecture_context,
        source_code,
        module_name="SwiftSampleApp"
    ):


        prompt = self.template.replace(

            "{{ARCHITECTURE_CONTEXT}}",

            json.dumps(
                architecture_context,
                indent=4
            )

        )


        prompt = prompt.replace(

            "{{SOURCE_CODE}}",

            source_code

        )


        prompt = prompt.replace(

            "{{MODULE_NAME}}",

            module_name

        )


        return prompt
