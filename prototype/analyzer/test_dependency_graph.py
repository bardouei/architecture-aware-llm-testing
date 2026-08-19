import unittest

from prototype.analyzer.dependency_graph import DependencyGraph


class DependencyGraphTests(unittest.TestCase):
    def test_builds_dependency_and_implementation_edges(self):
        components = [
            {
                "name": "LoginViewModel",
                "type": "class",
                "dependencies": ["LoginUseCase"],
            }
        ]
        mapping = [
            {"protocol": "LoginUseCase", "implementation": "DefaultLoginUseCase"}
        ]

        graph = DependencyGraph(components, mapping).build()

        self.assertIn(
            {
                "from": "LoginViewModel",
                "to": "LoginUseCase",
                "relationship": "depends_on",
            },
            graph["edges"],
        )
        self.assertIn(
            {
                "from": "LoginUseCase",
                "to": "DefaultLoginUseCase",
                "relationship": "implemented_by",
            },
            graph["edges"],
        )


if __name__ == "__main__":
    unittest.main()
