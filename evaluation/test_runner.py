from __future__ import annotations

import subprocess
import re
from pathlib import Path
from typing import Optional


class TestRunner:
    def __init__(
        self,
        project_path,
        scheme="SwiftSampleApp",
        destination="platform=iOS Simulator,name=iPhone 17",
        only_testing: Optional[str] = None,
        result_bundle: Optional[str | Path] = None,
        enable_coverage=False,
    ):
        self.project_path = str(project_path)
        self.scheme = scheme
        self.destination = destination
        self.only_testing = only_testing
        self.result_bundle = Path(result_bundle) if result_bundle else None
        self.enable_coverage = enable_coverage

    def command(self):
        command = [
            "xcodebuild",
            "test",
            "-project",
            self.project_path,
            "-scheme",
            self.scheme,
            "-destination",
            self.destination,
            "CODE_SIGNING_ALLOWED=NO",
        ]
        if self.only_testing:
            command.append(f"-only-testing:{self.only_testing}")
        if self.enable_coverage:
            command.extend(["-enableCodeCoverage", "YES"])
        if self.result_bundle:
            command.extend(["-resultBundlePath", str(self.result_bundle)])
        return command

    def run(self):
        if self.result_bundle and self.result_bundle.exists():
            return {
                "success": False,
                "error": f"Result bundle already exists: {self.result_bundle}",
            }

        try:
            result = subprocess.run(
                self.command(), capture_output=True, text=True, timeout=600
            )
            output = result.stdout + "\n" + result.stderr
            tests_executed = len(
                re.findall(
                    r"Test [Cc]ase .*? (?:passed|failed|skipped)",
                    output,
                )
            )
            compilation_failed = bool(
                re.search(r":\d+:\d+: error:", output)
                or "Testing cancelled because the build failed" in output
            )
            response = {
                "success": result.returncode == 0 and tests_executed > 0,
                "xcode_success": result.returncode == 0,
                "compilation_success": not compilation_failed,
                "tests_executed": tests_executed,
                "output": output[-5000:],
            }
            if result.returncode == 0 and tests_executed == 0:
                response["error"] = "Xcode succeeded but executed zero tests"
            if self.result_bundle:
                response["result_bundle"] = str(self.result_bundle)
            return response
        except Exception as error:
            return {"success": False, "error": str(error)}
