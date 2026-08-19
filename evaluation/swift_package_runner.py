"""Build and test a Swift package with machine-readable outcome fields."""

from __future__ import annotations

from pathlib import Path
import re
import subprocess


class SwiftPackageRunner:
    def __init__(self, package_path: str | Path, test_target: str | None = None):
        self.package_path = Path(package_path)
        self.test_target = test_target

    def build_command(self) -> list[str]:
        return ["swift", "build", "--package-path", str(self.package_path)]

    def test_command(self) -> list[str]:
        command = ["swift", "test", "--package-path", str(self.package_path)]
        if self.test_target:
            command.extend(["--filter", self.test_target])
        return command

    @staticmethod
    def _run(command: list[str], timeout: int) -> subprocess.CompletedProcess:
        return subprocess.run(command, capture_output=True, text=True, timeout=timeout)

    def build(self) -> dict:
        try:
            process = self._run(self.build_command(), 900)
            output = process.stdout + "\n" + process.stderr
            return {"success": process.returncode == 0, "output": output[-5000:]}
        except Exception as error:
            return {"success": False, "error": str(error)}

    def test(self) -> dict:
        try:
            process = self._run(self.test_command(), 900)
            output = process.stdout + "\n" + process.stderr
            tests_executed = len(
                re.findall(r"Test [Cc]ase .*? (?:passed|failed|skipped)", output)
            )
            compilation_failed = bool(
                re.search(r"\.swift:\d+:\d+: error:", output)
                or "emit-module command failed" in output
            )
            result = {
                "success": process.returncode == 0 and tests_executed > 0,
                "swift_success": process.returncode == 0,
                "compilation_success": not compilation_failed,
                "tests_executed": tests_executed,
                "output": output[-5000:],
            }
            if process.returncode == 0 and tests_executed == 0:
                result["error"] = "SwiftPM succeeded but executed zero XCTest cases"
            return result
        except Exception as error:
            return {"success": False, "compilation_success": False, "error": str(error)}
