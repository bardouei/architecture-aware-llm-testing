"""Generate a registry-driven, three-condition Groq study."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from prototype.context.local_context_builder import collect_local_context
from prototype.llm.groq_client import GroqClient
from prototype.llm.output_cleaner import clean_generated_code
from prototype.llm.prompt_builder import PromptBuilder
from prototype.run_pipeline import run as build_architecture_context


CONDITIONS = ("source_only", "local_context", "architecture_aware")
PROTOCOL_VERSION = "three-condition-v1"
REQUEST_SETTINGS = {
    "temperature": 0.6,
    "max_completion_tokens": 4096,
    "reasoning_format": "hidden",
    "reasoning_effort": "none",
}
TEMPLATES = {
    "source_only": ROOT / "prototype/llm/templates/baseline_prompt.txt",
    "local_context": ROOT / "prototype/llm/templates/local_context_prompt.txt",
    "architecture_aware": ROOT / "prototype/llm/templates/architecture_local_prompt.txt",
}


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def load_subject(name_or_path: str) -> dict:
    path = Path(name_or_path)
    if not path.exists():
        path = ROOT / "experiments/subjects" / f"{name_or_path}.json"
    if not path.is_file():
        raise ValueError(f"Subject configuration not found: {name_or_path}")
    subject = json.loads(path.read_text())
    required = {"id", "dataset_id", "project", "target", "source", "module_name"}
    missing = sorted(required - subject.keys())
    if missing:
        raise ValueError("Subject configuration is missing: " + ", ".join(missing))
    return subject


def build_generation_schedule(conditions: tuple[str, ...], runs: int):
    """Use cyclic condition rotation to balance order across repeated runs."""
    schedule = []
    for run_index in range(1, runs + 1):
        offset = (run_index - 1) % len(conditions)
        order = conditions[offset:] + conditions[:offset]
        schedule.extend((condition, run_index) for condition in order)
    return schedule


def build_prompt(
    condition: str,
    subject: dict,
    source: str,
    local_context: list[dict],
    architecture_context: dict,
) -> tuple[str, str]:
    template = TEMPLATES[condition].read_text()
    architecture = architecture_context if condition == "architecture_aware" else {}
    evidence = local_context if condition != "source_only" else []
    return (
        PromptBuilder(template).build(
            architecture,
            source,
            module_name=subject["module_name"],
            local_context=evidence,
        ),
        template,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--condition", choices=(*CONDITIONS, "all"), default="all")
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--experiment-id")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--request-delay-seconds", type=float, default=2.1)
    return parser.parse_args()


def validate_resume(existing: dict, expected: dict) -> None:
    fields = (
        "experiment_id",
        "subject",
        "provider",
        "requested_model",
        "conditions",
        "runs_per_condition",
        "request_settings",
        "protocol_version",
    )
    mismatches = [field for field in fields if existing.get(field) != expected.get(field)]
    if mismatches:
        raise ValueError("Cannot resume with different settings: " + ", ".join(mismatches))


def main() -> None:
    arguments = parse_args()
    if arguments.runs < 1:
        raise SystemExit("--runs must be at least 1")
    if arguments.request_delay_seconds < 0:
        raise SystemExit("--request-delay-seconds cannot be negative")
    try:
        subject = load_subject(arguments.subject)
    except ValueError as error:
        raise SystemExit(str(error)) from error
    project = (ROOT / subject["project"]).resolve()
    source_path = (project / subject["source"]).resolve()
    if not source_path.is_file():
        raise SystemExit(f"Subject source not found: {source_path}")
    conditions = CONDITIONS if arguments.condition == "all" else (arguments.condition,)
    experiment_id = arguments.experiment_id or datetime.now(timezone.utc).strftime(
        f"{subject['id']}-%Y%m%dT%H%M%SZ"
    )
    output = ROOT / "artifacts/studies" / experiment_id
    if output.exists() and not arguments.resume:
        raise SystemExit(f"Experiment output already exists: {output}")
    try:
        client = GroqClient(model=os.environ.get("AALLT_MODEL"), **REQUEST_SETTINGS)
    except ValueError as error:
        raise SystemExit(f"Configuration error: {error}") from error

    manifest = {
        "experiment_id": experiment_id,
        "subject": subject,
        "provider": "groq",
        "requested_model": client.model,
        "conditions": list(conditions),
        "runs_per_condition": arguments.runs,
        "request_settings": REQUEST_SETTINGS,
        "protocol_version": PROTOCOL_VERSION,
        "generation_order": "cyclic_counterbalanced_by_run",
    }
    output.mkdir(parents=True, exist_ok=True)
    manifest_path = output / "manifest.json"
    if arguments.resume:
        if not manifest_path.exists():
            raise SystemExit(f"Cannot resume without manifest: {manifest_path}")
        try:
            validate_resume(json.loads(manifest_path.read_text()), manifest)
        except ValueError as error:
            raise SystemExit(str(error)) from error
    else:
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    source = source_path.read_text()
    context_path = output / "context/llm-context.json"
    if arguments.resume and context_path.exists():
        architecture_context = json.loads(context_path.read_text())
    else:
        architecture_context = build_architecture_context(
            project, subject["target"], output / "context"
        )
    # Exact definitions are a controlled input shared by the two enriched
    # conditions. Architecture labels cannot influence their retrieval.
    local_context = collect_local_context(
        project, source_path, subject["target"], max_files=subject.get("max_local_files", 8)
    )
    (output / "context/local-context.json").write_text(
        json.dumps(local_context, indent=2) + "\n"
    )
    architecture_context = dict(architecture_context)
    architecture_context.pop("source_evidence", None)

    requests_started = 0
    required = {"prompt.txt", "raw-response.txt", "generated-test.swift", "metadata.json"}
    for condition, run_index in build_generation_schedule(conditions, arguments.runs):
        run_directory = output / condition / f"run-{run_index:03d}"
        if arguments.resume and run_directory.exists():
            if not required.issubset({path.name for path in run_directory.iterdir()}):
                raise SystemExit(f"Cannot resume incomplete run: {run_directory}")
            print(f"Kept {run_directory.relative_to(ROOT)}")
            continue
        if requests_started:
            time.sleep(arguments.request_delay_seconds)
        prompt, template = build_prompt(
            condition, subject, source, local_context, architecture_context
        )
        try:
            requests_started += 1
            raw = client.generate(prompt)
        except Exception as error:
            raise SystemExit(
                f"Generation failed for {condition} run {run_index}: {error}"
            ) from error
        generated = clean_generated_code(raw)
        run_directory.mkdir(parents=True, exist_ok=False)
        metadata = {
            "dataset_id": subject["dataset_id"],
            "subject_id": subject["id"],
            "target": subject["target"],
            "condition": condition,
            "run": run_index,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "prompt_sha256": sha256(prompt),
            "template_sha256": sha256(template),
            "source_sha256": sha256(source),
            "local_context_sha256": sha256(json.dumps(local_context, sort_keys=True)),
            "client": client.last_metadata,
        }
        (run_directory / "prompt.txt").write_text(prompt)
        (run_directory / "raw-response.txt").write_text(raw)
        (run_directory / "generated-test.swift").write_text(generated)
        (run_directory / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
        print(f"Generated {run_directory.relative_to(ROOT)}")
    print(f"Study artifacts: {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
