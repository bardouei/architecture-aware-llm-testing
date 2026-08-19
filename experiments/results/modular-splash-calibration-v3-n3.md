# Modular Splash Calibration — three-condition-v3

Subject: `SplashFeature`

Model: `qwen/qwen3.6-27b` through Groq

Runs: 3 per condition, 9 generated suites total

| Condition | N | Test compile | Test success | Mutants/run | Mean mutation |
|---|---:|---:|---:|---:|---:|
| source_only | 3 | 100% | 66.67% | 4 | 50% |
| local_context | 3 | 100% | 100% | 4 | 75% |
| architecture_aware | 3 | 100% | 100% | 4 | 75% |

Protocol v3 eliminated the systematic compilation failures observed under v2. The
failed source-only suite compiled but left an in-flight effect at the end of one
test, so it correctly remained a failed observation with zero mutation score.

Every passing suite killed three of four mutants. The surviving mutant changes
`cancelInFlight: true` to `false`; none of the generated suites sends `.onAppear`
twice while the first request is active, so this behavioral difference remains
untested.

Local-context retrieval returned zero files for this self-contained target.
Consequently, the identical local-context and architecture-aware results cannot be
used as evidence for either retrieval effectiveness or an architecture effect.
This is a calibration result with only three runs per condition.
