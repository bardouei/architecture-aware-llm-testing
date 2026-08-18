import re


class ImplementationMapper:


    def __init__(self, components):

        self.components = components



    def build_mapping(self):

        mappings = []


        for component in self.components:

            implementations = component.get(
                "implements",
                []
            )


            for protocol in implementations:

                mappings.append({

                    "implementation":
                        component["name"],

                    "protocol":
                        protocol

                })


        return mappings



    def find_implementation(
        self,
        protocol_name
    ):


        results = []


        for component in self.components:


            if protocol_name in component.get(
                "implements",
                []
            ):

                results.append(
                    component["name"]
                )


        return results