"""Restore-safe mutation testing for Swift source files."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import re
from typing import Callable, Mapping, Optional


CheckResult = Mapping[str, object]
Check = Callable[[], CheckResult]


@dataclass(frozen=True)
class Mutant:
    id: str
    operator: str
    description: str
    line: int
    start: int
    end: int
    original: str
    replacement: str

    def public_dict(self) -> dict[str, object]:
        result = asdict(self)
        result.pop("start")
        result.pop("end")
        return result


class MutationTesting:
    """Discover, compile, and test deterministic Swift mutants.

    Check callables return mappings containing a Boolean ``success`` field.
    They are injected so this engine remains independent of Xcode.
    """

    def __init__(
        self,
        source_file: str | Path,
        compilation_checker: Optional[Check] = None,
        test_runner: Optional[Check] = None,
    ) -> None:
        self.source_file = Path(source_file)
        self.compilation_checker = compilation_checker
        self.test_runner = test_runner

    def discover_mutants(self) -> list[Mutant]:
        source = self.source_file.read_text()
        candidates = [
            (
                "remove_async_result_assignment",
                "Removed assignment of an async dependency result",
                re.compile(
                    r"(?P<indent>^[ \t]*)(?P<target>[A-Za-z_]\w*)\s*=\s*"
                    r"(?P<call>try\s+await\s+[^\n]+)",
                    re.MULTILINE,
                ),
                lambda match: f"{match.group('indent')}_ = {match.group('call')}",
            ),
            (
                "remove_nil_assignment",
                "Removed state clearing assignment",
                re.compile(
                    r"(?P<indent>^[ \t]*)(?P<target>[A-Za-z_]\w*)\s*=\s*nil\s*$",
                    re.MULTILINE,
                ),
                lambda match: f"{match.group('indent')}_ = {match.group('target')}",
            ),
            (
                "swap_credential_arguments",
                "Swapped username and password dependency arguments",
                re.compile(
                    r"username:\s*(?P<username>[A-Za-z_]\w*)\s*,\s*"
                    r"password:\s*(?P<password>[A-Za-z_]\w*)"
                ),
                lambda match: (
                    f"username: {match.group('password')}, "
                    f"password: {match.group('username')}"
                ),
            ),
            (
                "flip_boolean",
                "Flipped a Boolean literal",
                re.compile(r"\b(?:true|false)\b"),
                lambda match: "false" if match.group(0) == "true" else "true",
            ),
            (
                "remove_state_assignment",
                "Removed a reducer state update",
                re.compile(
                    r"(?P<indent>^[ \t]*)state\.(?P<target>[A-Za-z_]\w*)[ \t]*="
                    r"(?![ \t]*(?:true\b|false\b|nil\b))[ \t]*(?P<value>[^\n]+)$",
                    re.MULTILINE,
                ),
                lambda match: f"{match.group('indent')}_ = {match.group('value')}",
            ),
        ]

        mutants: list[Mutant] = []
        for operator, description, pattern, replacement_for in candidates:
            operator_index = 0
            for match in pattern.finditer(source):
                replacement = replacement_for(match)
                if replacement == match.group(0):
                    continue
                operator_index += 1
                mutants.append(
                    Mutant(
                        id=f"{operator}-{operator_index}",
                        operator=operator,
                        description=description,
                        line=source.count("\n", 0, match.start()) + 1,
                        start=match.start(),
                        end=match.end(),
                        original=match.group(0),
                        replacement=replacement,
                    )
                )
        return mutants

    def create_mutation(self) -> dict[str, object]:
        """Retain the original discovery API for callers that need a dry run."""
        mutants = self.discover_mutants()
        return {
            "mutations_created": len(mutants),
            "mutations": [mutant.public_dict() for mutant in mutants],
        }

    def run(self, baseline_verified: bool = False) -> dict[str, object]:
        if self.compilation_checker is None or self.test_runner is None:
            raise ValueError(
                "Mutation execution requires compilation_checker and test_runner"
            )

        original_source = self.source_file.read_text()
        mutants = self.discover_mutants()
        baseline = (
            {"success": True, "reused_verified_baseline": True}
            if baseline_verified
            else self._run_checks()
        )
        if not baseline["success"]:
            return {
                "success": False,
                "error": "The unmodified source did not compile and pass its tests",
                "baseline": baseline,
                "mutations_created": len(mutants),
                "mutations_tested": 0,
                "mutations_killed": 0,
                "mutations_survived": 0,
                "invalid_mutants": 0,
                "mutation_score": 0.0,
                "mutations": [],
            }

        results: list[dict[str, object]] = []
        try:
            for mutant in mutants:
                mutated_source = (
                    original_source[: mutant.start]
                    + mutant.replacement
                    + original_source[mutant.end :]
                )
                self.source_file.write_text(mutated_source)
                check = self._run_checks()
                if not check["compilation"]["success"]:
                    status = "invalid"
                elif check["tests"]["success"]:
                    status = "survived"
                else:
                    status = "killed"
                results.append(
                    {**mutant.public_dict(), "status": status, "check": check}
                )
                self.source_file.write_text(original_source)
        finally:
            self.source_file.write_text(original_source)

        killed = sum(result["status"] == "killed" for result in results)
        survived = sum(result["status"] == "survived" for result in results)
        invalid = sum(result["status"] == "invalid" for result in results)
        valid = killed + survived
        return {
            "success": True,
            "baseline": baseline,
            "mutations_created": len(mutants),
            "mutations_tested": len(results),
            "mutations_killed": killed,
            "mutations_survived": survived,
            "invalid_mutants": invalid,
            "mutation_score": round((killed / valid) * 100, 2) if valid else 0.0,
            "mutations": results,
        }

    def _run_checks(self) -> dict[str, object]:
        compilation = dict(self.compilation_checker())  # type: ignore[misc]
        if not compilation.get("success", False):
            return {
                "success": False,
                "compilation": self._summarize(compilation),
                "tests": {"success": False, "skipped": True},
            }
        tests = dict(self.test_runner())  # type: ignore[misc]
        return {
            "success": bool(tests.get("success", False)),
            "compilation": self._summarize(compilation),
            "tests": self._summarize(tests),
        }

    @staticmethod
    def _summarize(result: dict[str, object]) -> dict[str, object]:
        summary = dict(result)
        if isinstance(summary.get("output"), str):
            summary["output"] = summary["output"][-1000:]
        return summary
