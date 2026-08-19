"""Build and run the existing oracle tests for registered SwiftPM subjects."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from experiments.generate_groq_study import load_subject


def count_xctests(output: str) -> int:
    return len(re.findall(r"Test [Cc]ase .*? (?:passed|failed|skipped)", output))


def smoke_subject(subject: dict, timeout: int = 900) -> dict:
    package = ROOT / subject["project"] / subject["package_path"]
    command = [
        "swift",
        "test",
        "--package-path",
        str(package),
        "--filter",
        subject["test_target"],
    ]
    try:
        process = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        output = process.stdout + "\n" + process.stderr
        result = {
            "subject_id": subject["id"],
            "target": subject["target"],
            "complexity_stratum": subject.get("complexity_stratum"),
            "package_path": subject["package_path"],
            "test_target": subject["test_target"],
            "success": process.returncode == 0,
            "tests_executed": count_xctests(output),
            "exit_code": process.returncode,
        }
        if process.returncode != 0:
            result["diagnostic"] = output[-3000:]
        return result
    except Exception as error:
        return {
            "subject_id": subject["id"],
            "target": subject["target"],
            "success": False,
            "tests_executed": 0,
            "error": str(error),
        }


def render(results: list[dict]) -> str:
    rows = [
        "# Modular TCA Subject Qualification",
        "",
        "| Subject | Stratum | Package tests | Status |",
        "|---|---|---:|---:|",
    ]
    for result in results:
        rows.append(
            f"| {result['target']} | {result.get('complexity_stratum', '-')} | "
            f"{result['tests_executed']} | {'pass' if result['success'] else 'fail'} |"
        )
    rows.extend(
        [
            "",
            "These are project-authored oracle tests used only to qualify the unmodified "
            "subjects. They are excluded when generated suites are evaluated.",
            "",
        ]
    )
    return "\n".join(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--subjects",
        nargs="+",
        default=["modular-tca-splash", "modular-tca-home", "modular-tca-app"],
    )
    parser.add_argument("--output-prefix", default="experiments/results/modular-tca-subject-smoke")
    arguments = parser.parse_args()
    results = [smoke_subject(load_subject(subject)) for subject in arguments.subjects]
    payload = {
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "results": results,
        "all_passed": all(result["success"] for result in results),
    }
    prefix = ROOT / arguments.output_prefix
    prefix.parent.mkdir(parents=True, exist_ok=True)
    prefix.with_suffix(".json").write_text(json.dumps(payload, indent=2) + "\n")
    prefix.with_suffix(".md").write_text(render(results))
    for result in results:
        print(
            f"{result['target']}: {'pass' if result['success'] else 'fail'}, "
            f"tests={result['tests_executed']}"
        )
    if not payload["all_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
