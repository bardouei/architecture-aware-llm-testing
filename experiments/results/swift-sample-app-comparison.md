# Swift Sample App Comparison

Target: `LoginViewModel.swift`

## Results

| Metric | Baseline | Architecture-aware | Difference |
|---|---:|---:|---:|
| Compilation success | 100% | 100% | 0 pp |
| Test success | 100% | 100% | 0 pp |
| Target coverage | 91.67% | 100.00% | +8.33 pp |
| Mutation score | 33.33% | 100.00% | +66.67 pp |

## Mutant outcomes

| Mutant | Baseline | Architecture-aware |
|---|---|---|
| `remove_async_result_assignment-1` | killed | killed |
| `remove_nil_assignment-1` | survived | killed |
| `swap_credential_arguments-1` | survived | killed |

## Interpretation

Both isolated suites compile and pass. The architecture-aware suite covers the
target completely and kills all three seeded faults. This is pipeline-validation
evidence for one controlled component, not a general research conclusion.
