# Journal Readiness and Novelty Strategy

Reviewed: 2026-08-19

This document is planning material, not a paper draft.

## Novelty risk

The broad claim that “more repository context improves LLM test generation” is no
longer sufficiently novel on its own. RATester injects language-server-derived
repository context, KTester combines project and testing knowledge, and recent
studies explicitly compare context and prompting strategies. Mutation-guided test
generation is also an active line of work (MUTGEN, GEM, and industrial work at
Meta).

Relevant primary sources:

- [RATester: precise repository context injection](https://arxiv.org/abs/2501.07425)
- [KTester: project and testing knowledge injection](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/241/Knowledge-Matters-Injecting-Project-and-Testing-Knowledge-into-LLM-based-Unit-Test-G)
- [Impact of code context and prompting strategies](https://arxiv.org/abs/2507.14256)
- [MUTGEN: mutation-guided LLM test generation](https://conf.researchr.org/details/ase-2026/ase-2026-journal-first/4/Mutation-Guided-Unit-Test-Generation-with-a-Large-Language-Model)
- [CODAMOSA: hybrid search-based and LLM generation](https://www.microsoft.com/en-us/research/?p=925401)
- [Large-scale prompt-engineering study](https://doi.org/10.1007/s10664-026-10840-4)

## Defensible contribution candidate

The strongest feasible contribution is narrower:

> A causally controlled, architecture-grounded context-selection method and
> benchmark for generating tests for Swift/iOS components, evaluated across
> architecture families using compilation, fault detection, and independently
> rated architecture compliance.

Potential contribution bundle:

1. A typed architecture-context representation for Swift/iOS concepts that are
   poorly represented by generic repository context: protocols and implementations,
   actor isolation, async effects, dependency-injection composition roots, MVVM,
   TCA reducers/effects, and module boundaries.
2. A context-selection algorithm that chooses architecture-relevant evidence rather
   than simply expanding the token window.
3. A versioned Swift/iOS benchmark mapping focal components to architecture facts,
   build/test commands, and reviewed mutants.
4. A paired empirical study that isolates the value of architecture facts from
   local code context, examples, token count, and iterative repair.
5. An architecture-compliance rubric with blinded human labels and inter-rater
   agreement, plus an automated metric validated against those labels.

Any one item alone is probably too weak for a strong journal submission; the bundle
can be substantive.

## Required experimental conditions

At minimum compare:

1. source only;
2. source + automatically retrieved local/repository definitions;
3. source + repository context + architecture labels/constraints;
4. architecture-aware context with one fact family removed at a time (ablation).

Use the same focal component, model, decoding parameters, repair policy, maximum
attempt count, and approximately matched input budget in paired conditions. Include
at least one current strong model and one reproducible open-weight model. A weak or
outdated baseline can exaggerate gains; recent ICST work explicitly warns that newer
plain models can outperform older proposed techniques.

## Dataset target

Before the main study, define power and sampling formally. A practical initial aim
is at least:

- 8–12 eligible repositories;
- 3 or more architecture families;
- 5–10 focal components per family;
- multiple component roles (ViewModel, use case, repository, reducer/effect,
  storage/network service);
- 10 or more independent generations per condition/model/component.

These are planning targets, not a substitute for a power analysis. Projects must be
license-compatible, pinned to immutable commits, cleanly buildable, and checked for
likely training-data contamination.

## Evaluation requirements

- Compilation and isolated execution rates, reported both unconditional and
  conditional on compilation.
- Line and branch coverage for the focal component.
- Mutation score using a documented Swift operator set.
- Manual adjudication or defensible filtering of equivalent and duplicate mutants;
  equivalent mutants bias mutation scores and cannot simply be counted as survivors.
- Real-defect or historical-bug evaluation where feasible.
- Architecture compliance, mock correctness, test smells/readability, flakiness,
  latency, token use, and monetary cost.
- Paired statistical analysis with effect sizes, confidence intervals, correction
  for multiple comparisons, and model/project random effects where appropriate.

## Reproducibility package

Freeze and publish:

- dataset registry, provenance, licenses, and exclusion reasons;
- prompt templates and hashes;
- extracted context and context-selection traces;
- model/provider/version, decoding configuration, seed when supported, and date;
- raw model outputs and all repair turns;
- generated tests before and after repair;
- build/test/coverage logs and environment versions;
- mutant definitions, diffs, outcomes, and equivalence decisions;
- analysis scripts and a one-command reproduction path.

## Stop/go criteria before paper writing

Do not start the main paper until all are true:

- the research questions and protocol are frozen;
- at least two real-world projects are fully eligible and a credible expansion plan
  is demonstrated;
- a real LLM, not the mock client, completes an end-to-end pilot;
- architecture extraction is evaluated against hand labels;
- mutation operators and equivalent-mutant procedure are reviewed;
- raw provenance is persisted for every generation;
- the statistical analysis plan is specified before seeing main-study results.
