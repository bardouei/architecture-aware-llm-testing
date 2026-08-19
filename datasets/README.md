# Dataset

The dataset is separated into two categories:

- `fixtures/`: controlled applications created for deterministic development and
  pipeline validation.
- `projects/`: externally sourced, real-world applications used as research
  subjects only after eligibility checks pass.

`registry.json` is the source of truth for project paths, provenance, Xcode
configuration, architecture labels, and eligibility state.

## Admission checklist

A real-world project is eligible for the comparative experiment only when:

1. its source URL and immutable commit are recorded;
2. its license permits the intended research use and redistribution;
3. the unmodified project builds reproducibly;
4. the selected test target runs before generated tests are injected;
5. candidate components and architectural labels are independently reviewed;
6. no project-authored tests are included in generated-test measurements;
7. generated tests can be isolated by condition.

The current `i2tocr-ios` snapshot is registered but not experiment-eligible: its
license is unknown and its Xcode project references a missing asset catalog.

## Adding Modular-TCA-App

`Modular-TCA-App` is a strong candidate because it adds a substantially different
architecture family (TCA), module boundaries, reducers/effects, dependency
injection, concurrency, and a mature test suite. Add an unmodified snapshot at:

```text
datasets/projects/modular-tca-app/
```

Do not copy its nested `.git` directory. After adding it, record its upstream URL,
immutable commit, license, Xcode workspace/project, scheme, test targets, Swift/TCA
versions, and clean-build command in `registry.json`. Its existing tests remain a
reference/oracle and must not be included in generated-test outcome measurements.

Because the project is large, begin with a stratified sample rather than the whole
application: select reducers/features of low, medium, and high dependency complexity
and record the selection rule before observing generated-test results.
