import json
from pathlib import Path

from scanner import RepositoryScanner
from swift_parser import SwiftParser


PROJECT_PATH = "../../examples/SwiftSampleApp"


# Create output directory
output_path = Path("output")
output_path.mkdir(
    exist_ok=True
)


# -----------------------------
# Repository Scanning
# -----------------------------

scanner = RepositoryScanner(
    PROJECT_PATH
)


files = scanner.scan_files()


metadata = {

    "files": files,

    "modules": scanner.scan_modules()
}


with open(
    output_path / "repository_metadata.json",
    "w"
) as file:

    json.dump(
        metadata,
        file,
        indent=4
    )


print("Repository scanned successfully")


# -----------------------------
# Swift Parsing
# -----------------------------

parser = SwiftParser(
    files["source_files"]
)


architecture_components = parser.parse()


with open(
    output_path / "architecture_components.json",
    "w"
) as file:

    json.dump(
        architecture_components,
        file,
        indent=4
    )


print("Swift analysis completed")