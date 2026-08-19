# Modular Home Calibration — three-condition-v3

Subject: `HomeFeature`

Model: `qwen/qwen3.6-27b` through Groq

Runs: 3 per condition, 9 generated suites total

| Condition | N | Test compile | Test success | Mutants/run | Mean mutation |
|---|---:|---:|---:|---:|---:|
| source_only | 3 | 0% | 0% | 7 | 0% |
| local_context | 3 | 0% | 0% | 7 | 0% |
| architecture_aware | 3 | 0% | 0% | 7 | 0% |

All nine suites failed compilation. The dominant shared error was direct
`TestStore.receive(.postsResponse(...))` usage. `HomeFeature.Action` is not
`Equatable` because `postsResponse` carries a `TaskResult` whose failure contains
an `Error`; TCA 1.26.1 therefore requires case-key-path receipt such as
`await store.receive(\.postsResponse)`.

Secondary errors included missing imports for types named from `PostDetailFeature`,
inventing `Post` instead of the supplied `EntityPost`, and inventing state or
continuation initializers. Because the dominant framework rule was absent from the
shared v3 contract, this is a protocol-calibration failure rather than evidence
about the architecture treatment. Protocol `three-condition-v4` adds the generic
non-Equatable receive rule, explicit source-import facts, and a strict state
initializer rule equally to all three conditions. Original generations and failed
evaluations remain unchanged.
