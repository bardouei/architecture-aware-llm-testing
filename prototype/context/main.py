import json
from pathlib import Path

from context_builder import ContextBuilder
from enrichment.context_enricher import ContextEnricher


# ---------------------------------
# Paths
# ---------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent


ANALYZER_OUTPUT = (
    BASE_DIR /
    "analyzer" /
    "output"
)


COMPONENTS_FILE = (
    ANALYZER_OUTPUT /
    "architecture_components.json"
)


MAPPING_FILE = (
    ANALYZER_OUTPUT /
    "implementation_mapping.json"
)


OUTPUT_FILE = (
    Path(__file__).parent /
    "architecture_context.json"
)



# ---------------------------------
# Load Architecture Components
# ---------------------------------

with open(COMPONENTS_FILE) as file:

    architecture_data = json.load(file)



components = architecture_data["components"]

protocols = architecture_data["protocols"]



# ---------------------------------
# Load Implementation Mapping
# ---------------------------------

with open(MAPPING_FILE) as file:

    implementation_mapping = json.load(file)



print(
    "Architecture components loaded"
)



# ---------------------------------
# Build Architecture Context
# ---------------------------------

builder = ContextBuilder(

    components,

    protocols,

    implementation_mapping

)


context = builder.build()



print(
    "Architecture context built"
)



# ---------------------------------
# Context Enrichment
# ---------------------------------

enricher = ContextEnricher(

    context["components"],

    protocols

)


context["components"] = (
    enricher.enrich()
)



print(
    "Context enrichment completed"
)



# ---------------------------------
# Save Output
# ---------------------------------

with open(
    OUTPUT_FILE,
    "w"
) as file:

    json.dump(

        context,

        file,

        indent=4

    )


print(
    "Architecture context generated:"
)

print(
    OUTPUT_FILE
)