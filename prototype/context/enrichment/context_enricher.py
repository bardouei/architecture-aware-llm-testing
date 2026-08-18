from pathlib import Path


class ContextEnricher:


    def __init__(self, components, protocols):

        self.components = components
        self.protocols = protocols



    def enrich(self):

        enriched_components = []


        for component in self.components:

            enriched = component.copy()


            enriched["responsibility"] = (
                self.detect_responsibility(
                    component
                )
            )


            enriched["dependencies"] = (
                self.enrich_dependencies(
                    component
                )
            )


            enriched["concurrency"] = (
                self.detect_concurrency(
                    component
                )
            )


            enriched["testing_strategy"] = (
                self.generate_testing_strategy(
                    component
                )
            )


            enriched_components.append(
                enriched
            )


        return enriched_components



    # ----------------------------
    # Responsibility Detection
    # ----------------------------

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


        return (
            "Application component"
        )



    # ----------------------------
    # Dependency Enrichment
    # ----------------------------

    def enrich_dependencies(
        self,
        component
    ):

        result = []


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



            dependency_type = (
                "Protocol"
                if dependency_name in self.protocols
                else "Concrete"
            )


            enriched_dependency = {

                "name": dependency_name,

                "type": dependency_type,

                "mock_required":
                    dependency_type == "Protocol"

            }


            # Preserve implementation mapping
            if isinstance(
                dependency,
                dict
            ):

                if "implementation" in dependency:

                    enriched_dependency[
                        "implementation"
                    ] = dependency[
                        "implementation"
                    ]


            result.append(
                enriched_dependency
            )


        return result

    # ----------------------------
    # Concurrency Detection
    # ----------------------------

    def detect_concurrency(
        self,
        component
    ):

        file_name = component["file"]


        # نسخه اولیه
        # بعداً با Parser دقیق‌تر می‌شود

        if "ViewModel" in file_name:

            return {

                "main_actor": True,

                "async_support": True

            }


        return {

            "main_actor": False,

            "async_support": False

        }



    # ----------------------------
    # Testing Strategy
    # ----------------------------

    def generate_testing_strategy(
        self,
        component
    ):

        return {

            "framework":
                "XCTest",

            "test_type":
                "Unit Test",

            "mock_strategy":
                "Protocol Mock"

        }