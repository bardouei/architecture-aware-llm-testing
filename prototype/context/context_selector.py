from typing import Dict, List


class ContextSelector:


    def __init__(
        self,
        architecture_context: Dict
    ):

        self.context = architecture_context

        self.components = (
            architecture_context.get(
                "components",
                []
            )
        )



    def select(
        self,
        target_component: str,
        depth: int = 1
    ) -> Dict:


        target = self.find_component(
            target_component
        )


        if not target:
            raise ValueError(
                f"Component '{target_component}' not found"
            )


        related_components = (
            self.find_related_components(
                target_component,
                depth
            )
        )


        return {

            "system":
                self.context.get(
                    "system",
                    {}
                ),


            "architecture":
                self.context.get(
                    "architecture",
                    {}
                ),


            "target_component":
                target,


            "related_components":
                related_components

        }



    # ---------------------------------
    # Find Target Component
    # ---------------------------------

    def find_component(
        self,
        name: str
    ):


        for component in self.components:

            if component["name"] == name:

                return component


        return None



    # ---------------------------------
    # Dependency Traversal
    # ---------------------------------

    def find_related_components(
        self,
        component_name: str,
        depth: int
    ) -> List[Dict]:


        visited = set()

        result = []


        self._collect_dependencies(

            component_name,

            depth,

            visited,

            result

        )


        return result



    def _collect_dependencies(
        self,
        component_name: str,
        depth: int,
        visited: set,
        result: list
    ):


        if depth == 0:
            return


        if component_name in visited:
            return


        visited.add(
            component_name
        )


        component = self.find_component(
            component_name
        )


        if not component:
            return



        for dependency in component.get(
            "dependencies",
            []
        ):


            dependency_name = (
                dependency["name"]
                if isinstance(
                    dependency,
                    dict
                )
                else dependency
            )


            dependency_component = (
                self.find_component(
                    dependency_name
                )
            )


            if dependency_component:


                result.append(
                    dependency_component
                )


                self._collect_dependencies(

                    dependency_name,

                    depth - 1,

                    visited,

                    result

                )