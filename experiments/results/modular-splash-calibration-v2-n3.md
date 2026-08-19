# Modular Splash Calibration — three-condition-v2

Subject: `SplashFeature`

Model: `qwen/qwen3.6-27b` through Groq

Runs: 3 per condition, 9 generated suites total

| Condition | N | Application build | Test compile | Test success | Mean mutation |
|---|---:|---:|---:|---:|---:|
| source_only | 3 | 100% | 33.33% | 33.33% | 0% |
| local_context | 3 | 100% | 100% | 100% | 33.33% |
| architecture_aware | 3 | 100% | 66.67% | 66.67% | 0% |

Protocol v2 improved executable-suite yield from 0/9 in v1 to 6/9. All three
remaining compilation failures used an empty or comment-only trailing assertion
closure with `TestStore.send` or `TestStore.receive`; the resolved TCA 1.26.1 API
requires a state parameter in such a closure. When no state mutation is expected,
the closure must be omitted.

Only one mutant was available (`cancelInFlight: true` changed to `false`). It was
killed only by `local_context/run-003`, making per-run mutation scores binary and
unstable. The local-context retrieval contained zero files for this self-contained
target, so its observed 3/3 success cannot be attributed to additional local code.

With three paired runs, none of the condition differences is statistically
conclusive. These observations are a calibration result, not a test of the research
hypothesis. Protocol `three-condition-v3` freezes the follow-up API-contract and
mutation improvements under a new experiment identifier.
