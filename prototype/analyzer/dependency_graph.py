import json


class DependencyGraph:

    def __init__(
        self,
        components,
        implementation_mapping=None
    ):
        self.components = components
        self.implementation_mapping = (
            implementation_mapping or []
        )


    def build(self):

        nodes = []
        edges = []


        # -----------------------------
        # Components as Nodes
        # -----------------------------

        for component in self.components:

            nodes.append(
                {
                    "id": component["name"],
                    "type": component.get(
                        "type",
                        "component"
                    )
                }
            )


            # -----------------------------
            # Dependency Edges
            # -----------------------------

            for dependency in component.get(
                "dependencies",
                []
            ):

                if isinstance(
                    dependency,
                    dict
                ):
                    dependency_name = dependency["name"]

                else:
                    dependency_name = dependency


                edges.append(
                    {
                        "from": component["name"],

                        "to": dependency_name,

                        "relationship":
                            "depends_on"
                    }
                )



        # -----------------------------
        # Protocol Implementation Edges
        # -----------------------------

        for mapping in self.implementation_mapping:

            edges.append(
                {
                    "from":
                        mapping["protocol"],

                    "to":
                        mapping["implementation"],

                    "relationship":
                        "implemented_by"
                }
            )



        return {

            "nodes": nodes,

            "edges": edges

        }



    def save(
        self,
        output_path
    ):

        graph = self.build()


        with open(
            output_path,
            "w"
        ) as file:

            json.dump(
                graph,
                file,
                indent=4
            )


        return graph