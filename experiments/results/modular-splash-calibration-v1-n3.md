# Modular Splash Calibration — three-condition-v1

Subject: `SplashFeature`

Model: `qwen/qwen3.6-27b` through Groq

Runs: 3 per condition, 9 generated suites total

| Condition | N | Application build | Test compile | Test success | Mean mutation |
|---|---:|---:|---:|---:|---:|
| source_only | 3 | 100% | 0% | 0% | 0% |
| local_context | 3 | 100% | 0% | 0% | 0% |
| architecture_aware | 3 | 100% | 0% | 0% | 0% |

The shared failure mechanism was framework API drift and hallucination. Generated
suites used unavailable TCA forms including `SplashFeature().reducer`,
`SplashFeature.reducer`, `TestScheduler`, `DispatchQueue.test`,
`ContinuousClock.test()`, scheduler-erasure helpers, and `store.advance(...)`.
The local-context retrieval was empty because this self-contained reducer declares
its state and action in the focal file.

This is a calibration failure, not evidence of equal treatment effectiveness. It
identified missing architecture-neutral build/framework grounding. The observations
remain frozen under `three-condition-v1`; the resulting fixes are versioned as
`three-condition-v2` and must use a new experiment ID.
