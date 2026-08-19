class ContextSelector:


    def __init__(
        self,
        context
    ):

        self.context = context



        self.components = {

            component["name"]:
                component

            for component in context.get(
                "components",
                []
            )

        }



        self.protocol_details = {

            protocol["name"]:
                protocol

            for protocol in context.get(
                "protocols",
                []
            )

        }



        self.protocols = set(

            self.protocol_details.keys()

        )



    # ---------------------------------
    # Find component
    # ---------------------------------

    def find_component(
        self,
        name
    ):

        exact_match = self.components.get(
            name
        )

        if exact_match:
            return exact_match

        normalized_name = name.casefold()

        return next(
            (
                component
                for component_name, component in self.components.items()
                if component_name.casefold() == normalized_name
            ),
            None,
        )



    # ---------------------------------
    # Check protocol
    # ---------------------------------

    def is_protocol(
        self,
        name
    ):

        return name in self.protocols



    # ---------------------------------
    # Dependencies
    # ---------------------------------

    def get_dependencies(
        self,
        component
    ):

        dependencies = []


        for dependency in component.get(
            "dependencies",
            []
        ):

            if isinstance(
                dependency,
                dict
            ):

                dependencies.append(
                    dependency
                )


            else:

                dependencies.append(

                    {
                        "name":
                            dependency
                    }

                )


        return dependencies



    # ---------------------------------
    # Add protocol node
    # ---------------------------------

    def add_protocol(
        self,
        protocol_name,
        selected,
        visited
    ):


        if protocol_name in visited:

            return



        protocol = self.protocol_details.get(
            protocol_name
        )


        if protocol:


            selected.append(

                {

                    "name":
                        protocol["name"],


                    "type":
                        "protocol",


                    "implemented_by":
                        protocol.get(
                            "implemented_by",
                            []
                        ),


                    "mock_strategy":
                        protocol.get(
                            "mock_strategy",
                            "Protocol Mock"
                        )

                }

            )


        else:


            selected.append(

                {

                    "name":
                        protocol_name,


                    "type":
                        "protocol"

                }

            )


        visited.add(
            protocol_name
        )



    # ---------------------------------
    # Select Context
    # ---------------------------------

    def select(
        self,
        target,
        depth=3
    ):


        selected = []

        visited = set()



        def traverse(
            name,
            level
        ):


            if level > depth:

                return



            if name in visited:

                return



            component = self.find_component(
                name
            )



            # Protocol

            if not component:


                if self.is_protocol(
                    name
                ):

                    self.add_protocol(
                        name,
                        selected,
                        visited
                    )


                return



            visited.add(
                name
            )


            selected.append(
                component
            )



            dependencies = (
                self.get_dependencies(
                    component
                )
            )



            for dependency in dependencies:


                dependency_name = (
                    dependency["name"]
                )


                # Add protocol

                if self.is_protocol(
                    dependency_name
                ):

                    self.add_protocol(
                        dependency_name,
                        selected,
                        visited
                    )


                else:

                    traverse(
                        dependency_name,
                        level + 1
                    )



                # Add implementation

                for implementation in dependency.get(
                    "implementation",
                    []
                ):


                    traverse(

                        implementation,

                        level + 1

                    )



        traverse(
            target,
            0
        )



        return {


            "target":

                target,


            "architecture":

                self.context.get(
                    "architecture",
                    {}
                ),


            "selected_components":

                selected

        }
