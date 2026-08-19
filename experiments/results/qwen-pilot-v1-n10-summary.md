# qwen-pilot-v1-n10 — Aggregated Results

| Condition | Compile success | Test success | Coverage (all runs) | Mutation (all runs) | Mutation (passing suites) |
|---|---:|---:|---:|---:|---:|
| baseline | 1/10 (10.00%) | 1/10 (10.00%) | 10.00% | 6.67% | 66.67% |
| architecture_aware | 5/10 (50.00%) | 5/10 (50.00%) | 50.00% | 46.67% | 93.33% |

## Paired comparison

Architecture-aware won 5 discordant pairs; baseline won 1. The two-sided exact McNemar p-value is 0.21875. This pilot is therefore directionally promising but not statistically conclusive.

## Compilation failure taxonomy

| Condition | Category | Runs affected |
|---|---|---:|
| baseline | non_equatable_assertion | 7 |
| baseline | type_or_signature_hallucination | 6 |
| baseline | undefined_symbol | 2 |
| architecture_aware | actor_isolation | 2 |
| architecture_aware | non_equatable_assertion | 3 |
| architecture_aware | xctest_lifecycle_override | 1 |

Failed suites remain in every unconditional denominator. A failure can have more than one category, so category counts need not sum to failed runs.
