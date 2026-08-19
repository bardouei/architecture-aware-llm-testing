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
        module_name="SwiftSampleApp",
        local_context=None,
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


        prompt = prompt.replace(

            "{{LOCAL_CONTEXT}}",

            json.dumps(
                local_context or [],
                indent=4
            )

        )


        return prompt
