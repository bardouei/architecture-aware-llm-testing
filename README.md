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
