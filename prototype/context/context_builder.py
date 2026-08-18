from layer_detector import LayerDetector
from pattern_detector import PatternDetector


class ContextBuilder:


    def __init__(
        self,
        components,
        protocols,
        implementation_mapping=None
    ):

        self.components = components

        self.protocols = protocols

        self.implementation_mapping = (
            implementation_mapping or []
        )


        self.layer_detector = LayerDetector()

        self.pattern_detector = PatternDetector()



    def build(self):


        architecture_context = {

            "system": {

                "language": "Swift",

                "testing_framework": "XCTest"

            },


            "architecture": {

                "patterns":
                    self.pattern_detector.detect(
                        self.components,
                        []
                    )

            },


            "components": []

        }



        for component in self.components:


            enriched_component = (
                self.build_component_context(
                    component
                )
            )


            architecture_context[
                "components"
            ].append(
                enriched_component
            )


        return architecture_context



    # ---------------------------------
    # Component Context
    # ---------------------------------

    def build_component_context(
        self,
        component
    ):


        return {

            "name":
                component["name"],


            "type":
                component["type"],


            "file":
                component["file"],


            "layer":
                self.layer_detector.detect(
                    component["file"]
                ),


            "implements":
                component.get(
                    "implements",
                    []
                ),


            "responsibility":
                self.detect_responsibility(
                    component
                ),


            "dependencies":
                self.build_dependencies(
                    component
                ),


            "testing_strategy": {

                "framework":
                    "XCTest",

                "test_type":
                    "Unit Test",

                "mock_strategy":
                    "Protocol Mock"

            },


            "concurrency": {

                "main_actor":
                    "ViewModel"
                    in component["name"],


                "async_support":
                    "ViewModel"
                    in component["name"]

            }

        }



    # ---------------------------------
    # Dependency Mapping
    # ---------------------------------

    def build_dependencies(
        self,
        component
    ):


        dependencies = []


        for dependency in component.get(
            "dependencies",
            []
        ):


            dependency_info = {

                "name":
                    dependency,


                "type":
                    (
                        "Protocol"
                        if dependency in self.protocols
                        else "Concrete"
                    ),


                "mock_required":
                    dependency in self.protocols

            }



            implementations = (
                self.find_implementation(
                    dependency
                )
            )


            if implementations:


                dependency_info[
                    "implementation"
                ] = implementations



            dependencies.append(
                dependency_info
            )


        return dependencies



    # ---------------------------------
    # Find Concrete Implementations
    # ---------------------------------

    def find_implementation(
        self,
        protocol
    ):


        result = []


        for mapping in self.implementation_mapping:


            if mapping["protocol"] == protocol:

                result.append(
                    mapping["implementation"]
                )


        return result



    # ---------------------------------
    # Responsibility
    # ---------------------------------

    def detect_responsibility(
        self,
        component
    ):


        name = component["name"]



        if "ViewModel" in name:

            return (
                "Manages UI state "
                "and coordinates user actions"
            )



        if "UseCase" in name:

            return (
                "Contains business logic "
                "and application rules"
            )



        if "Repository" in name:

            return (
                "Provides data access abstraction"
            )



        return "Application component"