# Modular Home Calibration — three-condition-v4

Subject: `HomeFeature`

Model: `qwen/qwen3.6-27b` through Groq

Runs: 3 per condition, 9 generated suites total

| Condition | N | Test compile | Test success | Mutants/run | Mean mutation |
|---|---:|---:|---:|---:|---:|
| source_only | 3 | 0% | 0% | 7 | 0% |
| local_context | 3 | 33.33% | 33.33% | 7 | 23.81% |
| architecture_aware | 3 | 100% | 0% | 7 | 0% |

Protocol v4 eliminated the shared non-Equatable `TestStore.receive` compilation
error. All architecture-aware suites compiled, and one local-context suite compiled,
passed three tests, and killed five of seven mutants. The source-only condition
continued to invent declarations unavailable from the focal file.

The two failed local-context suites invented an unsupported `userId` argument for
`EntityPost`; transitive local retrieval had supplied references to `EntityPost` but
not its declaration. The architecture context named that component, but this is not
a controlled substitute for giving both enriched conditions the same exact source
definition.

The architecture-aware suites exposed semantic test errors rather than compiler API
drift: XCTest assertions were placed inside expected-state mutation closures, async
dependencies were driven with clocks not used by production, unrelated load actions
were used to prepare navigation tests, and cancellation scenarios used real
`Task.sleep` or uncontrolled immediate responses. The original outputs and failed
observations remain unchanged.

This calibration is excluded from confirmatory evidence. Protocol
`three-condition-v5` adds transitive exact-definition retrieval, generic TestStore
state-assertion and async-isolation rules, preserved stdout/stderr diagnostics, and
per-mutant result retention. No v4 generation is repaired or reclassified.
