import json


class LLMContextBuilder:
    def __init__(self, selected_context):
        self.context = selected_context

    def extract_target(self):
        return self.context.get("target")

    @staticmethod
    def extract_dependencies(component):
        return [
            {
                "name": dependency["name"],
                "type": dependency.get("type", "Concrete"),
                "mock_required": dependency.get("mock_required", False),
                "implementation": dependency.get("implementation", []),
            }
            for dependency in component.get("dependencies", [])
        ]

    def simplify_component(self, component):
        return {
            "name": component.get("name"),
            "type": component.get("type"),
            "layer": component.get("layer"),
            "module": component.get("module"),
            "responsibility": component.get("responsibility"),
            "dependencies": self.extract_dependencies(component),
            "testing_strategy": component.get("testing_strategy", {}),
            "concurrency": component.get("concurrency", {}),
        }

    def build(self):
        components = [
            self.simplify_component(component)
            for component in self.context.get("selected_components", [])
        ]
        return {
            "target": self.extract_target(),
            "language": "Swift",
            "testing_framework": "XCTest",
            "architecture": self.context.get("architecture", {}),
            "test_generation_rules": {
                "generate_unit_tests": True,
                "use_protocol_mocks": True,
                "respect_main_actor": True,
                "test_async_code": True,
            },
            "components": components,
        }

    def save(self, path):
        with open(path, "w") as file:
            json.dump(self.build(), file, indent=4)
