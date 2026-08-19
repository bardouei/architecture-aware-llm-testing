# Project Status

Last reviewed: 2026-08-19

## Objective

Evaluate whether structured architecture context improves the correctness,
fault-detection ability, and architectural compliance of LLM-generated XCTest
suites compared with source-code-only prompting.

## Current evidence

One isolated experiment has been completed on the controlled `swift-sample-app`
fixture and its `LoginViewModel` component. Both conditions compiled and passed.
Architecture-aware tests improved target coverage from 91.67% to 100% and mutation
score from 33.33% to 100% across three identical mutants.

This validates the experiment pipeline only. With one component, one generated
suite per condition, one architecture family, and three hand-designed mutants, it
does not establish external validity or a publishable causal claim.

## Workstream readiness

Percentages are engineering/research-readiness estimates, not statistical results.

| Workstream | Readiness | Evidence | Main gap |
|---|---:|---|---|
| Research Idea | 90% | Clear question, hypothesis, and mechanism | Sharpen novelty against current literature |
| Experiment Design | 55% | Isolated A/B execution with identical mutants | Preregister protocol, repeated generations, controls, statistics |
| Prototype App | 80% | Controlled fixture builds and has deterministic tests | Generalize all pipeline stages beyond one target |
| Prompt Engineering | 40% | Baseline and architecture templates exist | Token-budget parity, ablations, prompt versioning, contamination controls |
| Test Generation | 25% | Client abstraction and deterministic mock exist | Real model integration, retries, seeds, raw-response provenance |
| Evaluation | 55% | Compile, execute, coverage, mutation implemented | Architecture compliance, flakiness, quality rubric, cost/time metrics |
| Dataset | 25% | One fixture and one registered real-world candidate | License/build qualification and substantially more diverse projects |
| Mutation Analysis | 45% | Restore-safe execution and three valid operators | Broader operators, equivalent-mutant review, multiple components/projects |
| Paper Writing | 0% | Intentionally deferred | Start only after protocol freeze and main study |

Simple overall readiness: **46% including the intentionally deferred paper**, or
**52% across active pre-paper workstreams**.

## Dataset

### swift-sample-app

- Type: controlled fixture
- Architecture: MVVM + Clean Architecture
- Status: experiment-eligible
- Current target: `LoginViewModel`

### i2tocr-ios

- Type: real-world candidate
- Architecture: MVVM + Clean Architecture + dependency injection
- Provenance: `https://github.com/i2tOCR/i2tocr-iOS.git`
- Pinned commit: `b35d9edeac0a95b74e1c9288b4af8dbdf7d3336a`
- Static scan: 25 source files, 8 test files, 35 components, 2 protocols
- Status: not experiment-eligible
- Blockers:
  - no license file is present in the imported commit;
  - the application build fails because `Resoures/Assets.xcassets` and `AppIcon`
    are referenced by the Xcode project but absent from the imported commit;
  - some tests reference types/frameworks not found in the current source tree;
  - `HomeViewModelTests.swift` is empty;
  - clean build and baseline-test execution still require validation.

## Implemented system

- Swift file and module scanning
- Class, struct, actor, protocol, dependency, and implementation extraction
- Context enrichment and dependency selection prototype
- Baseline and architecture-aware prompt templates
- Injectable LLM client interface with a mock implementation
- Xcode compilation and isolated XCTest execution
- Target-level Xcode coverage extraction
- Restore-safe, per-mutant compilation and execution
- Invalid-mutant exclusion from mutation-score denominator
- Compact, machine-readable experiment results

## Immediate next steps

1. Qualify or reject `i2tocr-ios`: establish license permission, fix or document its
   clean-build baseline, and select independently reviewable components.
2. Replace hard-coded context assumptions with project-derived architecture and
   concurrency facts; validate extraction precision/recall on a hand-labeled set.
3. Integrate at least two real LLM families and persist model/version, parameters,
   prompt hash, raw response, repair attempts, latency, and cost.
4. Freeze a paired experimental protocol with equal non-architecture context and
   comparable token budgets.
5. Run repeated generations per component and model; analyze paired outcomes with
   confidence intervals and effect sizes.
6. Add architecture-compliance and test-quality measures with blinded independent
   raters and inter-rater agreement.
7. Expand mutation operators and manually adjudicate equivalent mutants.
8. Expand to multiple architecture families and repositories before paper writing.

## Paper policy

Paper writing is deferred. Draft paper files were removed during the 2026-08-19
structure review because they implied maturity unsupported by the current evidence.
Writing should begin after protocol freeze, dataset qualification, and the main
experiment—not before.
