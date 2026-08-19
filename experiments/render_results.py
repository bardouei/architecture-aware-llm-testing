"""Rebuild the comparison JSON and Markdown table from condition results."""

from run_swift_sample_comparison import load_condition, save_comparison


if __name__ == "__main__":
    comparison = save_comparison(
        load_condition("baseline"), load_condition("architecture_aware")
    )
    metrics = comparison["comparison"]
    print("| Condition | Compile | Tests | Coverage | Mutation score |")
    print("|---|---:|---:|---:|---:|")
    for name in ("baseline", "architecture_aware"):
        result = metrics[name]
        print(
            f"| {name} | {result['compilation_success'] * 100:.0f}% "
            f"| {result['test_success'] * 100:.0f}% "
            f"| {result['coverage']:.2f}% "
            f"| {result['mutation_score']:.2f}% |"
        )
