# Project Status

Last reviewed: 2026-08-20

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
from architecture-specific context; calibration is still in progress before the
main study.

The first three-condition TCA calibration (`SplashFeature`, 3 runs per condition)
produced zero compilable suites in all conditions. Diagnostics showed systematic
hallucination of obsolete TCA testing APIs rather than application-build failures.
Protocol v2 then improved executable-suite yield to 6/9, but exposed one remaining
systematic TestStore trailing-closure error and had only one available mutant. Its
local-context condition retrieved zero files and therefore is not a meaningful
retrieval treatment. Protocol v3 then produced 9/9 compilable Splash suites, with
test-success rates of 66.67%, 100%, and 100% and unconditional mean mutation scores
of 50%, 75%, and 75% for source-only, local-context, and architecture-aware. Because
Splash retrieved zero local files, this does not establish a retrieval or
architecture effect. On the medium-complexity Home subject, all nine v3 suites
failed compilation; the dominant shared cause was the missing TCA rule requiring
case-key-path receipt for non-Equatable actions. Protocol v4 fixed that error: all
three architecture-aware suites compiled, and one of three local-context suites
compiled, passed, and killed five of seven mutants. However, no architecture-aware
suite passed because of semantic TestStore and async-stub errors, while local
retrieval omitted the transitive `EntityPost` declaration. Protocol
`three-condition-v5` supplies that exact transitive declaration equally to both
enriched conditions, adds generic expected-state and async-isolation rules, and
retains complete test and per-mutant diagnostics. Its isolated contract smoke test
passed three tests and killed all four mutants. Splash and Home are calibration-only
subjects and will be excluded from confirmatory evidence.

## Workstream readiness

Percentages are engineering/research-readiness estimates, not statistical results.

| Workstream | Readiness | Evidence | Main gap |
|---|---:|---|---|
| Research Idea | 90% | Clear question, hypothesis, and mechanism | Sharpen novelty against current literature |
| Experiment Design | 75% | Repeated paired pilot plus source/local/architecture controlled protocol and counterbalanced order | Preregister sample size, token parity, ablations, and statistics |
| Prototype App | 85% | Generic Swift analysis plus Xcode and SwiftPM subject paths | Validate extraction accuracy on labeled projects |
| Prompt Engineering | 80% | Frozen calibration protocols, transitive equal local definitions, and shared compile-validated framework grounding | Validate v5 on Home, token-budget parity, ablations, contamination controls |
| Test Generation | 82% | Real Groq generation, provenance, counterbalancing, robust resume, and automatic rate-limit retry | Run final v5 Home calibration and add a second model family |
| Evaluation | 78% | Isolated Xcode and SwiftPM suite injection, zero-test rejection, checkpointing, and mutation | SwiftPM focal coverage, compliance rubric, flakiness, cost/time |
| Dataset | 40% | One fixture, one rejected candidate, and one build-qualified nine-package TCA candidate | Resolve license and add diverse eligible repositories |
| Mutation Analysis | 55% | Restore-safe operators plus reducer state mutations | More TCA operators and equivalent-mutant adjudication |
| Paper Writing | 0% | Intentionally deferred | Start only after protocol freeze and main study |

Simple overall readiness: **64% including the intentionally deferred paper**, or
**72% across active pre-paper workstreams**.

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

1. Run the final v3 calibration on `SplashFeature`, then run all three conditions on
   `HomeFeature`, where local retrieval is non-empty.
2. Add SwiftPM focal-file coverage and manually review the expanded reducer/effect
   mutation operators.
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
