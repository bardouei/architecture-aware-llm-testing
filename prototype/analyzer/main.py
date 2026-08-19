"""Command-line entry point for Swift repository architecture analysis."""

import argparse
import json
from pathlib import Path

from prototype.analyzer.implementation_mapper import ImplementationMapper
from prototype.analyzer.scanner import RepositoryScanner
from prototype.analyzer.swift_parser import SwiftParser


def analyze_repository(project_path, output_path):
    project = Path(project_path).resolve()
    output = Path(output_path).resolve()
    if not project.exists():
        raise FileNotFoundError(f"Dataset project not found: {project}")
    output.mkdir(parents=True, exist_ok=True)

    scanner = RepositoryScanner(project)
    source_paths = scanner.scan_files()
    metadata = {
        "project": project.name,
        "files": scanner.scan_files(relative=True),
        "modules": scanner.scan_modules(),
    }
    architecture = SwiftParser(
        source_paths["source_files"], project_root=project
    ).parse()
    mapping = ImplementationMapper(architecture["components"]).build_mapping()

    artifacts = {
        "repository_metadata.json": metadata,
        "architecture_components.json": architecture,
        "implementation_mapping.json": mapping,
    }
    for filename, content in artifacts.items():
        (output / filename).write_text(json.dumps(content, indent=2))
    return artifacts


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract architecture metadata from a Swift project"
    )
    parser.add_argument("project", type=Path, help="Path to the dataset project")
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Directory for generated JSON artifacts",
    )
    return parser.parse_args()


def main():
    arguments = parse_args()
    result = analyze_repository(arguments.project, arguments.output)
    print(
        json.dumps(
            {
                "source_files": len(result["repository_metadata.json"]["files"]["source_files"]),
                "test_files": len(result["repository_metadata.json"]["files"]["test_files"]),
                "components": len(result["architecture_components.json"]["components"]),
                "protocols": len(result["architecture_components.json"]["protocols"]),
                "output": str(arguments.output.resolve()),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
