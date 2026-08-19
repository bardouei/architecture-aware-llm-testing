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

## Modular-TCA-App

`Modular-TCA-App` is a strong candidate because it adds a substantially different
architecture family (TCA), module boundaries, reducers/effects, dependency
injection, concurrency, and a mature test suite. Its current local snapshot is at:

```text
datasets/projects/Modular-TCA-App/
```

The pinned revision contains nine Swift packages. All packages build and all 99
project-authored tests pass with the recorded toolchain. The snapshot has no license
file, so it is qualified for local experiments but must not be redistributed as a
public benchmark until the owner supplies a compatible license or explicit
permission. For this reason the nested project directory is intentionally not
tracked by this repository.

Because the project is large, begin with a stratified sample rather than the whole
application: select reducers/features of low, medium, and high dependency complexity
before observing generated-test results. The frozen initial sample is
`SplashFeature` (low), `HomeFeature` (medium), and `AppFeature` (high).
