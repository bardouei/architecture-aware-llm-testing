# Project Status

Last reviewed: 2026-08-19

## Objective

Evaluate whether structured architecture context improves the correctness,
fault-detection ability, and architectural compliance of LLM-generated XCTest
suites compared with source-code-only prompting.

## Current evidence

One isolated pipeline-validation comparison and one real repeated-generation pilot
have been completed on the controlled `swift-sample-app` fixture. In the real Qwen
pilot, source-only compiled and passed in 1/10 runs; architecture-aware compiled and
passed in 5/10. Unconditional mutation scores were 6.67% and 46.67%, respectively.
Architecture-aware won five discordant pairs and source-only won one, giving a
two-sided exact McNemar p-value of 0.21875.

This is promising pilot evidence, not a significant or externally valid result.
It uses one component, one model/provider, two conditions, and three mutants. The
new three-condition protocol is implemented to separate ordinary local-code context
from architecture-specific context, but its main study has not yet run.

## Workstream readiness

Percentages are engineering/research-readiness estimates, not statistical results.

| Workstream | Readiness | Evidence | Main gap |
|---|---:|---|---|
| Research Idea | 90% | Clear question, hypothesis, and mechanism | Sharpen novelty against current literature |
| Experiment Design | 75% | Repeated paired pilot plus source/local/architecture controlled protocol and counterbalanced order | Preregister sample size, token parity, ablations, and statistics |
| Prototype App | 85% | Generic Swift analysis plus Xcode and SwiftPM subject paths | Validate extraction accuracy on labeled projects |
| Prompt Engineering | 70% | Frozen v1 pilot and three-condition v2 prompts with equal local definitions | Token-budget parity, ablations, contamination controls |
| Test Generation | 75% | Real Groq generation, provenance, counterbalancing, and resume for registry-driven subjects | Run TCA study and add a second model family |
| Evaluation | 78% | Isolated Xcode and SwiftPM suite injection, zero-test rejection, checkpointing, and mutation | SwiftPM focal coverage, compliance rubric, flakiness, cost/time |
| Dataset | 40% | One fixture, one rejected candidate, and one build-qualified nine-package TCA candidate | Resolve license and add diverse eligible repositories |
| Mutation Analysis | 55% | Restore-safe operators plus reducer state mutations | More TCA operators and equivalent-mutant adjudication |
| Paper Writing | 0% | Intentionally deferred | Start only after protocol freeze and main study |

Simple overall readiness: **63% including the intentionally deferred paper**, or
**71% across active pre-paper workstreams**.

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

### Modular-TCA-App

- Type: real-world local candidate
- Architecture: TCA + modular SwiftPM + dependency injection
- Pinned commit: `3971ed4b667267fc45080a0bbd88c03df6f9bb59`
- Static scan: 101 source files and 46 test files, excluding package manifests and
  dependency/build caches
- Build qualification: all nine packages and 99 authored tests pass
- Frozen targets: `SplashFeature` (low), `HomeFeature` (medium), `AppFeature` (high)
- Status: locally experiment-qualified; public redistribution blocked because no
  license file is present

## Implemented system

- Swift file and module scanning
- Class, struct, actor, protocol, dependency, and implementation extraction
- Context enrichment and dependency selection prototype
- Baseline and architecture-aware prompt templates
- Injectable LLM client interface with mock, OpenAI, and Groq implementations
- Real paired Groq generation with controlled decoding and complete provenance
- Registry-driven three-condition generation with cyclic counterbalancing
- Automatically retrieved local-definition control without architecture labels
- SwiftPM subject qualification and isolated generated-suite evaluation
- Architecture-selected exact source evidence for dependency mocks and values
- Isolated generated-suite injection with failures retained in the denominator
- Xcode compilation and isolated XCTest execution
- Target-level Xcode coverage extraction
- Restore-safe, per-mutant compilation and execution
- Invalid-mutant exclusion from mutation-score denominator
- Compact, machine-readable experiment results

## Immediate next steps

1. Run a small three-condition TCA calibration on `SplashFeature` and `HomeFeature`
   without tuning prompts against measured outcomes.
2. Add SwiftPM focal-file coverage and broaden reducer/effect mutation operators.
3. Validate architecture extraction precision/recall on a hand-labeled set.
4. Freeze and preregister the main protocol with comparable token budgets.
5. Run repeated generations per component and at least two models; analyze with
   confidence intervals and effect sizes.
6. Add architecture-compliance and test-quality measures with blinded independent
   raters and inter-rater agreement.
7. Resolve Modular-TCA-App publication permission and qualify more repositories.
8. Manually adjudicate equivalent mutants before paper writing.

## Paper policy

Paper writing is deferred. Draft paper files were removed during the 2026-08-19
structure review because they implied maturity unsupported by the current evidence.
Writing should begin after protocol freeze, dataset qualification, and the main
experiment—not before.
