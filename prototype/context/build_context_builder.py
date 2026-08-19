"""Build shared, architecture-neutral build and framework grounding."""

from __future__ import annotations

import json
from pathlib import Path
import re


TOOLS_VERSION = re.compile(r"swift-tools-version:\s*([0-9.]+)")
SWIFT_IMPORT = re.compile(
    r"^\s*(?:@\w+(?:\([^\n]*\))?\s+)?import\s+([A-Za-z_]\w*)",
    re.MULTILINE,
)


def resolved_versions(package: Path) -> dict[str, str]:
    resolved = package / "Package.resolved"
    if not resolved.is_file():
        return {}
    payload = json.loads(resolved.read_text())
    versions = {}
    for pin in payload.get("pins", []):
        identity = pin.get("identity")
        version = pin.get("state", {}).get("version")
        if identity and version:
            versions[identity] = version
    return dict(sorted(versions.items()))


def source_imports(source: Path) -> list[str]:
    """Extract explicit module imports without inferring architecture facts."""
    if not source.is_file():
        return []
    return sorted(set(SWIFT_IMPORT.findall(source.read_text())))


def build_shared_context(root: Path, subject: dict) -> dict:
    """Return build facts shared by every experimental condition."""
    project = (Path(root) / subject["project"]).resolve()
    context = {
        "build_system": subject.get("build_system", "unknown"),
        "module_name": subject["module_name"],
        "test_target": subject.get("test_target"),
        "test_framework": "XCTest",
        "source_imports": source_imports(project / subject["source"])
        if subject.get("source")
        else [],
    }
    if subject.get("build_system") == "swift_package":
        package = project / subject["package_path"]
        manifest = package / "Package.swift"
        manifest_text = manifest.read_text()
        version = TOOLS_VERSION.search(manifest_text)
        context.update(
            {
                "swift_tools_version": version.group(1) if version else None,
                "resolved_dependencies": resolved_versions(package),
            }
        )
    contract_path = subject.get("framework_contract")
    if contract_path:
        path = (Path(root) / contract_path).resolve()
        context["framework_api_contract"] = json.loads(path.read_text())
    return context
