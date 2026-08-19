from prototype.context.module_detector import ModuleDetector
from pathlib import Path



class ContextBuilder:


    def __init__(
        self,
        components,
        protocols,
        implementation_mapping=None,
        architecture_patterns=None
    ):

        self.components = components

        self.protocols = protocols

        self.implementation_mapping = (
            implementation_mapping or []
        )

        self.architecture_patterns = architecture_patterns or []

        self.module_detector = ModuleDetector()



    # ---------------------------------
    # Protocol implementation resolver
    # ---------------------------------

    def find_implementation(
        self,
        protocol
    ):

        result = []


        for item in self.implementation_mapping:

            if item["protocol"] == protocol:

                result.append(
                    item["implementation"]
                )


        return result



    # ---------------------------------
    # Protocol Context
    # ---------------------------------

    def build_protocols(self):

        result = []


        for protocol in self.protocols:

            implementations = (
                self.find_implementation(
                    protocol
                )
            )


            result.append(

                {

                    "name":
                        protocol,


                    "type":
                        "protocol",


                    "implemented_by":
                        implementations,


                    "mock_strategy":
                        "Protocol Mock"

                }

            )


        return result



    # ---------------------------------
    # Relative path resolver
    # ---------------------------------

    def get_relative_path(
        self,
        path
    ):

        parts = Path(path).parts


        try:

            index = parts.index(
                "SwiftSampleApp"
            )


            return "/".join(
                parts[index + 2:]
            )


        except ValueError:

            return str(path)



    # ---------------------------------
    # Dependency enrichment
    # ---------------------------------

    def enrich_dependencies(
        self,
        dependencies
    ):

        result = []


        for dependency in dependencies:


            if isinstance(
                dependency,
                dict
            ):

                name = dependency["name"]


            else:

                name = dependency



            item = {


                "name":
                    name,


                "type":

                    "Protocol"

                    if name in self.protocols

                    else "Concrete",


                "mock_required":

                    name in self.protocols

            }



            implementations = (
                self.find_implementation(
                    name
                )
            )


            if implementations:

                item[
                    "implementation"
                ] = implementations



            result.append(
                item
            )


        return result



    # ---------------------------------
    # Layer detector
    # ---------------------------------

    def detect_layer(
        self,
        component
    ):

        name = component["name"]


        if "ViewModel" in name:

            return "Presentation"


        if "UseCase" in name:

            return "Domain"


        if "Repository" in name:

            return "Data"


        if "View" in name:

            return "Presentation"


        return "Unknown"



    # ---------------------------------
    # Component builder
    # ---------------------------------

    def build_component(
        self,
        component
    ):

        file_path = component.get(
            "file",
            ""
        )


        return {


            "name":

                component["name"],


            "type":

                component.get(
                    "type",
                    "class"
                ),


            "file":

                Path(
                    file_path
                ).name,


            "path":

                self.get_relative_path(
                    file_path
                ),



            "layer":

                self.detect_layer(
                    component
                ),



            "module":

                self.module_detector.detect(
                    file_path
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

                self.enrich_dependencies(
                    component.get(
                        "dependencies",
                        []
                    )
                )

        }



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


        return "Unknown"



    # ---------------------------------
    # Final Context
    # ---------------------------------

    def build(self):

        return {


            "system": {

                "language":
                    "Swift",

                "testing_framework":
                    "XCTest"

            },


            "architecture": {

                "patterns": self.architecture_patterns

            },


            "protocols":

                self.build_protocols(),



            "components": [

                self.build_component(
                    component
                )

                for component in self.components

            ]

        }
