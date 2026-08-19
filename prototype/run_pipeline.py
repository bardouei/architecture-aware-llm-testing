"""Build architecture and LLM context artifacts for any registered Swift project."""

import argparse
import json
from pathlib import Path
import re

from prototype.analyzer.main import analyze_repository
from prototype.context.context_builder import ContextBuilder
from prototype.context.context_selector import ContextSelector
from prototype.context.enrichment.context_enricher import ContextEnricher
from prototype.context.llm_context_builder import LLMContextBuilder
from prototype.context.pattern_detector import PatternDetector


DECLARATION = re.compile(r"\b(?:class|struct|actor|protocol|enum)\s+(\w+)")


def collect_source_evidence(project, source_files, selected_components, target):
    """Collect exact files declaring architecture-selected non-target symbols."""
    selected_names = {
        component["name"]
        for component in selected_components
        if component.get("name") != target
    }
    evidence = []
    for relative_path in source_files:
        path = project / relative_path
        content = path.read_text()
        declared = set(DECLARATION.findall(content))
        matched = sorted(declared & selected_names)
        if matched:
            evidence.append(
                {
                    "path": relative_path,
                    "selected_symbols": matched,
                    "content": content,
                }
            )
    return evidence


def run(project, target, output):
    project = Path(project).resolve()
    output = Path(output).resolve()
    analysis_output = output / "analysis"
    analysis = analyze_repository(project, analysis_output)
    architecture = analysis["architecture_components.json"]
    mapping = analysis["implementation_mapping.json"]

    patterns = PatternDetector().detect(
        architecture["components"],
        analysis["repository_metadata.json"]["files"],
    )
    context = ContextBuilder(
        architecture["components"],
        architecture["protocols"],
        mapping,
        architecture_patterns=patterns,
    ).build()
    context["components"] = ContextEnricher(
        context["components"], architecture["protocols"]
    ).enrich()
    selected = ContextSelector(context).select(target)
    llm_context = LLMContextBuilder(selected).build()
    llm_context["source_evidence"] = collect_source_evidence(
        project,
        analysis["repository_metadata.json"]["files"]["source_files"],
        selected["selected_components"],
        target,
    )

    artifacts = {
        "architecture-context.json": context,
        "selected-context.json": selected,
        "llm-context.json": llm_context,
    }
    output.mkdir(parents=True, exist_ok=True)
    for filename, content in artifacts.items():
        (output / filename).write_text(json.dumps(content, indent=2))

    if not selected["selected_components"]:
        raise ValueError(f"Target component was not found: {target}")
    return llm_context


def parse_args():
    parser = argparse.ArgumentParser(description="Build focused LLM architecture context")
    parser.add_argument("project", type=Path)
    parser.add_argument("--target", required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main():
    arguments = parse_args()
    context = run(arguments.project, arguments.target, arguments.output)
    print(
        json.dumps(
            {
                "target": context["target"],
                "patterns": context["architecture"].get("patterns", []),
                "selected_components": len(context["components"]),
                "output": str(arguments.output.resolve()),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
