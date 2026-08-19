import unittest

from prototype.context.enrichment.context_enricher import ContextEnricher


class ContextEnricherTests(unittest.TestCase):
    def test_uses_parser_concurrency_facts_for_non_view_model(self):
        component = {
            "name": "SplashFeature",
            "file": "SplashFeature.swift",
            "dependencies": [],
            "source_facts": {"main_actor": False, "async_support": True},
        }

        enriched = ContextEnricher([component], []).enrich()[0]

        self.assertEqual(
            enriched["concurrency"],
            {"main_actor": False, "async_support": True},
        )


if __name__ == "__main__":
    unittest.main()
