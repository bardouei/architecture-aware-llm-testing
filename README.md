# Architecture-Aware LLM Test Generation

Research prototype for testing whether explicit software-architecture context
improves LLM-generated XCTest suites for iOS applications.

## Research question

Does adding structured information about layers, dependencies, protocols,
implementations, concurrency, and test constraints improve generated-test quality
over a source-code-only prompt?

The primary outcome is fault detection measured with mutation testing. Compilation,
test execution, target coverage, and architectural compliance are supporting
outcomes.

## Repository layout

```text
datasets/
  fixtures/                 controlled development subjects
  projects/                 real-world candidate subjects
  registry.json             provenance and eligibility source of truth
prototype/
  analyzer/                 Swift repository scanning and architecture extraction
  context/                  enrichment and target-context selection
  llm/                      prompt construction and client abstraction
evaluation/                 Xcode, coverage, and mutation evaluators
experiments/
  fixtures/                 deterministic/mock generation fixtures
  results/                  verified, compact experiment results
docs/                       research design, status, and reproducibility notes
```

Paper drafting is intentionally deferred until the experimental protocol and
dataset are mature.

## Dataset status

- `swift-sample-app`: controlled MVVM/Clean Architecture fixture; validated.
- `i2tocr-ios`: real-world MVVM/Clean Architecture candidate pinned to an immutable
  upstream commit; build and license eligibility are still pending.

See [datasets/registry.json](datasets/registry.json) for machine-readable metadata.

## Reproduce current checks

Create the project-local Python environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Configure a real OpenAI API connection without committing credentials:

```bash
export OPENAI_API_KEY="..."
export AALLT_MODEL="an-available-model-id"
python experiments/check_openai_connection.py
```

The OpenAI adapter uses the Responses API with remote response storage disabled and
captures request ID, resolved model, latency, and token usage for provenance. The
API smoke check is not an experimental generation and should be run only after the
two environment variables are set.

For the rate-limited Groq free tier, configure a Groq key and an active model:

```bash
export GROQ_API_KEY="..."
export AALLT_PROVIDER="groq"
export AALLT_MODEL="qwen/qwen3.6-27b"
python experiments/check_groq_connection.py
```

The Groq adapter uses its OpenAI-compatible chat-completions endpoint and records
request ID, resolved model, latency, token usage, provider, and endpoint metadata.
The Qwen pilot fixes temperature at `0.6`, disables reasoning for this constrained
code-only task, caps completion at 4096 tokens, and asks Groq to hide any reasoning
output. These settings and the response finish reason are persisted in every
experiment manifest and run metadata.

After the connection check succeeds, generate one real paired pilot:

```bash
python experiments/generate_groq_pilot.py \
  --condition both \
  --runs 1 \
  --experiment-id groq-smoke-001
```

If a rate limit interrupts a paired run after one condition was saved, resume it
without regenerating completed observations:

```bash
python experiments/generate_groq_pilot.py \
  --condition both \
  --runs 1 \
  --experiment-id groq-smoke-001 \
  --resume
```

The ignored `artifacts/generations/groq-smoke-001/` directory contains the exact
prompt, raw response, cleaned Swift test, hashes, usage, latency, selected
architecture context, and experiment manifest. Reasoning blocks such as
`<think>...</think>` and Markdown fences are removed only from
`generated-test.swift`; the raw response remains unchanged for provenance.
The post-calibration prompt protocol is frozen as `qwen-pilot-v1`; do not tune it
against individual measured runs. The generator pauses 2.1 seconds between API
requests by default, counterbalances condition order across paired runs, and
supports `--resume` after interruption.

Evaluate every generated suite in an isolated copy of the Xcode fixture:

```bash
python experiments/evaluate_groq_pilot.py \
  --experiment-id groq-smoke-001 \
  --condition both
```

Evaluation is checkpointed after every generated suite. Stop safely with `Ctrl+C`
and continue without rerunning completed suites:

```bash
python experiments/evaluate_groq_pilot.py \
  --experiment-id groq-smoke-001 \
  --condition both \
  --resume
```

The evaluator empties all fixture-authored test files inside the temporary copy,
injects exactly one generated suite, and then runs application build, XCTest,
target-file coverage, and the identical restore-safe mutant set. It writes
`evaluation.json` beside each generation and a combined `evaluation-report.md`.
Failed generations are retained as failures rather than discarded.
An Xcode exit code of zero is not sufficient: a suite passes only when at least one
XCTest case actually executes. Production-target build, generated-test compilation,
and test execution are reported separately.
Mutation is skipped when the unmodified generated suite does not compile and pass;
for a passing suite, its just-completed coverage run is reused as the verified
mutation baseline instead of executing it again.
The report includes both individual observations and unconditional aggregate rates;
failed generations contribute zero coverage and mutation score.

Run Python tests:

```bash
python3 -m unittest discover -v
```

Analyze either Swift project:

```bash
python3 -m prototype.analyzer.main \
  datasets/projects/i2tocr-ios \
  --output artifacts/analysis/i2tocr-ios
```

Run the validated isolated fixture comparison on macOS with Xcode and an iPhone 17
simulator:

```bash
python3 experiments/run_swift_sample_comparison.py
```

Run either condition independently:

```bash
# Existing/source-only method
python3 experiments/run_baseline_pipeline.py

# Proposed architecture-aware method
python3 experiments/run_architecture_pipeline.py
```

Rebuild and print the comparison table without rerunning Xcode:

```bash
python3 experiments/render_results.py
```

Each condition compiles the same production target, runs only its own XCTest suite,
measures target-file coverage, executes the same mutants, and writes a compact JSON
summary under `experiments/results/`. The current suites are frozen controlled-pilot
fixtures. Real-LLM generation and provenance capture are intentionally listed as
remaining research work rather than simulated by these evaluation commands.

## Current evidence

For the single validated `LoginViewModel` subject:

| Metric | Baseline | Architecture-aware |
|---|---:|---:|
| Compilation | 100% | 100% |
| Test execution | 100% | 100% |
| Target coverage | 91.67% | 100% |
| Mutation score | 33.33% | 100% |

This is a successful pipeline validation, not sufficient evidence for a general
research claim. See [docs/project-status.md](docs/project-status.md) for the full
readiness assessment, [docs/system-overview.md](docs/system-overview.md) for the
end-to-end method, and [docs/journal-readiness.md](docs/journal-readiness.md) for
the publication plan.
