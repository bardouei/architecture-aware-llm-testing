"""Retrieve exact nearby Swift definitions without architecture labels."""

from __future__ import annotations

from pathlib import Path
import re

from prototype.analyzer.scanner import RepositoryScanner


DECLARATION = re.compile(r"\b(?:class|struct|actor|protocol|enum)\s+(\w+)")
IDENTIFIER = re.compile(r"\b[A-Z][A-Za-z0-9_]+\b")
DEPENDENCY_KEY = re.compile(r"@Dependency\(\\\.(\w+)\)")
GENERIC_NESTED_TYPES = {"Action", "State", "Destination", "CancelID"}


def package_scope(relative_path: str) -> tuple[str, ...]:
    parts = Path(relative_path).parts
    if "Packages" in parts:
        index = parts.index("Packages")
        if len(parts) > index + 1:
            return tuple(parts[index : index + 2])
    return tuple(parts[:1])


def collect_local_context(
    project: Path,
    target_source: Path,
    target: str,
    max_files: int = 8,
) -> list[dict]:
    """Select declarations needed to understand a target's exact local API."""
    project = Path(project).resolve()
    target_source = Path(target_source).resolve()
    source = target_source.read_text()
    referenced = set(IDENTIFIER.findall(source))
    referenced_casefold = {name.casefold() for name in referenced}
    referenced_casefold.update(
        name.casefold() for name in DEPENDENCY_KEY.findall(source)
    )
    target_scope = package_scope(str(target_source.relative_to(project)))
    candidates = []
    files = RepositoryScanner(project).scan_files(relative=True)["source_files"]
    for relative_path in files:
        path = project / relative_path
        if path.resolve() == target_source or "Tests" in path.parts:
            continue
        content = path.read_text()
        declarations = set(DECLARATION.findall(content))
        matched_references = sorted(
            declaration
            for declaration in declarations
            if declaration.casefold() in referenced_casefold
        )
        extends_target = bool(re.search(rf"\bextension\s+{re.escape(target)}\b", content))
        same_scope = package_scope(relative_path) == target_scope
        matched_specific = [
            name for name in matched_references if name not in GENERIC_NESTED_TYPES
        ]
        if not (
            (same_scope and (matched_references or extends_target))
            or matched_specific
        ):
            continue
        score = 100 * extends_target + 40 * len(matched_references) + 10 * same_scope
        candidates.append(
            (
                -score,
                relative_path,
                {
                    "path": relative_path,
                    "selected_symbols": matched_references,
                    "extends_target": extends_target,
                    "content": content,
                },
            )
        )
    return [candidate for _, _, candidate in sorted(candidates)[:max_files]]
