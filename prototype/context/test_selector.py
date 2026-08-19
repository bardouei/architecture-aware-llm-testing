import unittest

from prototype.context.context_selector import ContextSelector


class ContextSelectorTests(unittest.TestCase):
    def test_selects_target_protocol_and_implementation(self):
        context = {
            "architecture": {"patterns": ["MVVM"]},
            "components": [
                {
                    "name": "LoginViewModel",
                    "dependencies": [
                        {
                            "name": "LoginUseCase",
                            "implementation": ["DefaultLoginUseCase"],
                        },
                        {"name": "Clock"},
                    ],
                },
                {"name": "DefaultLoginUseCase", "dependencies": []},
                {"name": "Clock", "dependencies": []},
            ],
            "protocols": [{"name": "LoginUseCase"}],
        }

        selected = ContextSelector(context).select("LoginViewModel")

        self.assertEqual(selected["architecture"], {"patterns": ["MVVM"]})
        self.assertEqual(
            {item["name"] for item in selected["selected_components"]},
            {"LoginViewModel", "LoginUseCase", "DefaultLoginUseCase", "Clock"},
        )


if __name__ == "__main__":
    unittest.main()
