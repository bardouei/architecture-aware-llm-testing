# Experiment Design

> Status: protocol draft. Source-only, automatically retrieved local context, and
> architecture-aware conditions are executable with counterbalanced repeated
> generation. The multi-project sampling plan, token-budget policy,
> architecture-compliance rubric, and statistical analysis plan are not frozen.
> See `project-status.md` and `journal-readiness.md` before treating this as a
> preregistered main-study protocol.

## Architecture-Aware Context Engineering for LLM-Based Unit Test Generation in Modular Software Systems

------------------------------------------------------------------------

# 1. Overview

This experiment evaluates whether providing structured software
architecture context improves the quality of Large Language Model
(LLM)-generated unit tests compared with traditional source-code-based
approaches.

The main hypothesis is that LLMs can generate more accurate and
maintainable unit tests when they understand:

-   Component responsibilities
-   Module boundaries
-   Dependency relationships
-   Interface abstractions
-   Design patterns
-   Existing testing strategies

------------------------------------------------------------------------

# 2. Research Questions

## RQ1

Does architecture-aware context improve the quality of LLM-generated
unit tests compared with source-code-only approaches?

------------------------------------------------------------------------

## RQ2

Which architectural information contributes most to generated test
quality?

Potential factors:

-   Module information
-   Dependency graph
-   Interface/protocol information
-   Design patterns
-   Existing tests
-   Concurrency information

------------------------------------------------------------------------

## RQ3

Can architecture-aware context improve test maintainability and fault
detection capability in modular software systems?

------------------------------------------------------------------------

# 3. Hypotheses

## H1

Architecture-aware context improves the compilation success rate of
generated unit tests.

## H2

Architecture-aware context improves mutation score and fault detection
capability.

## H3

Architecture-aware context produces more maintainable and understandable
unit tests.

------------------------------------------------------------------------

# 4. Experimental Setup

The experiment compares multiple LLM test generation strategies.

------------------------------------------------------------------------

# Baseline 1: Code-Only Generation

Input:

    Source Code

          |

         LLM

          |

    Generated Unit Tests

The LLM receives only the target class implementation.

All conditions additionally receive the same architecture-neutral execution
contract: module/test-target names, compiler/package version, resolved framework
versions, and compile-validated signatures for framework testing APIs. These facts
are required to make the test harness executable and are not architecture treatment.

Example:

    LoginViewModel.swift

------------------------------------------------------------------------

# Baseline 2: Code + Local Context

Input:

    Source Code

    +

    Related Files

          |

         LLM

          |

    Generated Unit Tests

Additional context may include:

-   Imported files
-   Related classes
-   Local dependencies

Existing project-authored test bodies are excluded. Framework API contracts are
derived from resolved public interfaces and validated with a separate smoke fixture.
If local retrieval returns zero files, that condition is marked as having no local
treatment and is excluded from claims about retrieval effectiveness for that target.

------------------------------------------------------------------------

# Proposed Approach: Architecture-Aware Context Generation

Input:

    Source Code

    +

    Architecture Context Schema

    +

    Dependency Graph

    +

    Design Patterns

    +

    Testing Strategy

          |

         LLM

          |

    Generated Unit Tests

The proposed approach provides structured architectural knowledge before
test generation.

------------------------------------------------------------------------

# 5. Dataset Strategy

## Option A: Open Source Swift Projects

Candidate dataset:

-   Modular Swift applications
-   Projects with XCTest tests
-   Projects using modern architectures

Selection criteria:

-   Open source
-   Active repository
-   Clear architecture
-   Testable components

------------------------------------------------------------------------

## Option B: Controlled Benchmark

Create controlled projects implementing:

-   MVVM
-   Clean Architecture
-   TCA

Advantages:

-   Controlled architecture
-   Known dependencies
-   Repeatable experiments

------------------------------------------------------------------------

## Recommended Strategy

Hybrid dataset:

    Open Source Swift Projects

    +

    Controlled Architecture Benchmarks

This provides both realism and experimental control.

------------------------------------------------------------------------

# 6. Architecture Styles for Evaluation

Initial evaluation:

## MVVM

    View
     |
    ViewModel
     |
    Repository

------------------------------------------------------------------------

## Clean Architecture

    Presentation

    Domain

    Data

------------------------------------------------------------------------

## TCA

    State

    Action

    Reducer

    Effect

    Dependency

------------------------------------------------------------------------

# 7. LLM Configuration

The experiment can evaluate:

## Closed Models

Examples:

-   GPT models
-   Claude models
-   Gemini models

## Open Models

Examples:

-   Code-focused open models

Initial prototype:

Use a high-quality API model to validate the research idea.

------------------------------------------------------------------------

# 8. Evaluation Metrics

## Compilation Success Rate

Measures whether generated tests can build and execute successfully.

------------------------------------------------------------------------

## Code Coverage

Metrics:

-   Line coverage
-   Branch coverage

------------------------------------------------------------------------

## Mutation Score

Measures the ability of generated tests to detect injected faults.

------------------------------------------------------------------------

## Fault Detection Rate

Evaluates whether generated tests identify real defects.

------------------------------------------------------------------------

## Test Maintainability

Evaluates:

-   Readability
-   Complexity
-   Stability
-   Test smells

------------------------------------------------------------------------

## Mock Correctness

Evaluates:

-   Correct dependency isolation
-   Proper use of abstractions
-   Appropriate mock generation

------------------------------------------------------------------------

# 9. Experimental Workflow

    Software Project

            |

    Architecture Analyzer

            |

    Architecture Context Schema

            |

    Context Engineering

            |

    LLM Test Generation

            |

    Test Execution

            |

    Quality Evaluation

            |

    Result Analysis

------------------------------------------------------------------------

# 10. Expected Results

The expected outcome is that architecture-aware context will improve:

-   Test compilation rate
-   Dependency handling
-   Mock generation
-   Mutation score
-   Maintainability

The research does not aim to create a new LLM model. Instead, it
investigates how structured architectural knowledge can improve existing
LLM capabilities.
