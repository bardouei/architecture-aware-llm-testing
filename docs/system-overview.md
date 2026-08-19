# System Overview

Reviewed: 2026-08-19

## Purpose

The system tests whether selecting explicit software-architecture facts improves
LLM-generated Swift/XCTest suites over a source-code-only baseline.

## End-to-end method

1. **Dataset qualification** records provenance, license, immutable revision,
   architecture, build configuration, and eligibility in `datasets/registry.json`.
2. **Repository analysis** scans Swift sources and tests and extracts types,
   protocols, dependencies, implementation relationships, modules, and likely
   architecture patterns.
3. **Context construction** turns extracted facts into a typed architecture context.
4. **Target selection** keeps only architecture facts relevant to a focal component,
   including protocols and concrete implementations reached through dependencies.
5. **Prompt construction** creates either a source-only baseline prompt or an
   architecture-aware prompt. The experimental protocol must keep non-architecture
   information, model settings, repair budget, and approximately the token budget
   controlled.
6. **Test generation** sends the prompt to an injectable model client and stores the
   raw response and generated suite. The current repository has a deterministic mock
   client; a real provider and complete provenance capture remain to be implemented.
7. **Evaluation** compiles the application, runs only the condition-specific test
   suite, measures focal-file coverage, and runs identical restore-safe mutants.
8. **Comparison** reports compilation, execution, coverage, mutation score, and each
   mutant outcome as JSON and Markdown.

## Runnable controlled pilot

The current pilot uses one production component and two frozen test suites:

- `python3 experiments/run_baseline_pipeline.py` evaluates only the source-only
  baseline fixture.
- `python3 experiments/run_architecture_pipeline.py` evaluates only the proposed
  architecture-aware fixture.
- `python3 experiments/run_swift_sample_comparison.py` runs both sequentially.
- `python3 experiments/render_results.py` rebuilds the comparison table from saved
  condition summaries without rerunning Xcode.

Both conditions use the same `LoginViewModel.swift`, Xcode project, simulator,
coverage mechanism, mutant definitions, and mutation runner. XCTest isolation is
enforced with `xcodebuild -only-testing`.

## Current pilot result

| Metric | Baseline | Architecture-aware | Difference |
|---|---:|---:|---:|
| Compilation success | 100% | 100% | 0 pp |
| Test success | 100% | 100% | 0 pp |
| Target coverage | 91.67% | 100% | +8.33 pp |
| Mutation score | 33.33% | 100% | +66.67 pp |

The architecture-aware fixture exercises the success path, failure-state reset, and
dependency interaction. The baseline fixture checks only the success path. The
result validates the measurement pipeline and motivates the hypothesis; it does not
estimate the expected effect of real LLM generation across projects.

## Evidence boundary

Claims that are currently supported:

- architecture context can be extracted and selected for two Swift repositories;
- independently isolated suites can be evaluated under the same production code;
- the architecture-aware controlled fixture detects faults missed by the baseline;
- the evaluation is reproducible on the validated Xcode fixture.

Claims that are not yet supported:

- that an LLM reliably produces the architecture-aware fixture from the prompt;
- that the improvement generalizes to other components or architecture families;
- that architecture labels add value beyond ordinary repository retrieval;
- that the observed effect persists across models, runs, and token budgets.

## Dataset expansion

There are currently two registered projects but only one experiment-eligible
controlled fixture. A journal study should determine sample size with a formal power
analysis. The current planning target is 8–12 eligible repositories across at least
three architecture families, with multiple focal components and repeated generations
per condition. `Modular-TCA-App` is valuable as the next candidate because it adds
TCA and modular boundaries, but it should be sampled by component complexity rather
than evaluated monolithically.
