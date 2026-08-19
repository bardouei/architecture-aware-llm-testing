"""Generate real baseline and architecture-aware Swift tests through Groq."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from prototype.llm.groq_client import GroqClient
from prototype.llm.output_cleaner import clean_generated_code
from prototype.llm.prompt_builder import PromptBuilder
from prototype.run_pipeline import run as build_architecture_context


DATASET_ID = "swift-sample-app"
PROJECT = ROOT / "datasets/fixtures/swift-sample-app"
SOURCE = PROJECT / "SwiftSampleApp/Feature/Login/LoginViewModel.swift"
TARGET = "LoginViewModel"
REQUEST_SETTINGS = {
    "temperature": 0.6,
    "max_completion_tokens": 4096,
    "reasoning_format": "hidden",
    "reasoning_effort": "none",
}
TEMPLATES = {
    "baseline": ROOT / "prototype/llm/templates/baseline_prompt.txt",
    "architecture_aware": ROOT / "prototype/llm/templates/architecture_prompt.txt",
}


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def build_prompt(condition: str, source: str, context: dict) -> tuple[str, str]:
    template = TEMPLATES[condition].read_text()
    prompt_context = context if condition == "architecture_aware" else {}
    return (
        PromptBuilder(template).build(
            prompt_context, source, module_name="SwiftSampleApp"
        ),
        template,
    )


def generate_run(
    client: GroqClient,
    condition: str,
    run_index: int,
    output: Path,
    source: str,
    context: dict,
) -> Path:
    prompt, template = build_prompt(condition, source, context)
    raw_output = client.generate(prompt)
    generated_code = clean_generated_code(raw_output)
    run_directory = output / condition / f"run-{run_index:03d}"
    run_directory.mkdir(parents=True, exist_ok=False)

    metadata = {
        "dataset_id": DATASET_ID,
        "target": TARGET,
        "condition": condition,
        "run": run_index,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "prompt_sha256": sha256(prompt),
        "template_sha256": sha256(template),
        "source_sha256": sha256(source),
        "client": client.last_metadata,
    }
    (run_directory / "prompt.txt").write_text(prompt)
    (run_directory / "raw-response.txt").write_text(raw_output)
    (run_directory / "generated-test.swift").write_text(generated_code)
    (run_directory / "metadata.json").write_text(json.dumps(metadata, indent=2))
    return run_directory


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--condition",
        choices=("baseline", "architecture_aware", "both"),
        default="both",
    )
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--experiment-id")
    return parser.parse_args()


def main() -> None:
    arguments = parse_args()
    if arguments.runs < 1:
        raise SystemExit("--runs must be at least 1")
    experiment_id = arguments.experiment_id or datetime.now(timezone.utc).strftime(
        "pilot-%Y%m%dT%H%M%SZ"
    )
    output = ROOT / "artifacts/generations" / experiment_id
    if output.exists():
        raise SystemExit(f"Experiment output already exists: {output}")

    conditions = (
        ("baseline", "architecture_aware")
        if arguments.condition == "both"
        else (arguments.condition,)
    )

    try:
        client = GroqClient(
            model=os.environ.get("AALLT_MODEL"),
            **REQUEST_SETTINGS,
        )
    except ValueError as error:
        raise SystemExit(f"Configuration error: {error}") from error

    context = {}
    if "architecture_aware" in conditions:
        context = build_architecture_context(
            PROJECT, TARGET, output / "architecture-context"
        )

    source = SOURCE.read_text()
    manifest = {
        "experiment_id": experiment_id,
        "dataset_id": DATASET_ID,
        "target": TARGET,
        "provider": "groq",
        "requested_model": client.model,
        "conditions": list(conditions),
        "runs_per_condition": arguments.runs,
        "request_settings": REQUEST_SETTINGS,
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2))

    for condition in conditions:
        for run_index in range(1, arguments.runs + 1):
            try:
                run_directory = generate_run(
                    client, condition, run_index, output, source, context
                )
            except Exception as error:
                raise SystemExit(
                    f"Generation failed for {condition} run {run_index}: {error}"
                ) from error
            print(f"Generated {run_directory.relative_to(ROOT)}")

    print(f"Pilot artifacts: {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
