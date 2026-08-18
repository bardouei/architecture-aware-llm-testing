# Proposed Framework

## Architecture-Aware Context Engineering for LLM-Based Unit Test Generation in Modular Software Systems

------------------------------------------------------------------------

# 1. Overview

This research proposes an architecture-aware context engineering
framework for Large Language Model (LLM)-based unit test generation.

Existing LLM-based test generation approaches mainly rely on
source-code-level information. However, modern software systems are
organized using architectural patterns, modular boundaries, dependency
relationships, and abstraction layers.

The proposed framework introduces an intermediate architecture
understanding layer that extracts software architecture knowledge and
provides structured context to LLMs during unit test generation.

The main objective is to investigate whether architecture-aware context
improves:

-   Test correctness
-   Dependency handling
-   Mock generation
-   Fault detection capability
-   Test maintainability

------------------------------------------------------------------------

# 2. System Architecture

The proposed system consists of the following pipeline:

                     Software Repository

                             |
                             v

                  Architecture Analyzer

                             |
                             v

                Architecture Context Schema

                             |
                             v

                  Context Engineering Layer

                             |
                             v

                             LLM

                             |
                             v

                  Generated Unit Tests

                             |
                             v

                  Quality Evaluation Pipeline

------------------------------------------------------------------------

# 3. Software Repository

## Input

The framework receives a software repository containing:

-   Source code
-   Project structure
-   Modules
-   Dependencies
-   Existing tests
-   Configuration files

Example:

    Application

    ├── Feature
    │   └── Authentication
    │
    ├── Domain
    │
    ├── Network
    │
    ├── Storage
    │
    └── Tests

The repository represents a real modular software system where
architectural understanding is required for effective testing.

------------------------------------------------------------------------

# 4. Architecture Analyzer

## Purpose

The Architecture Analyzer extracts architectural information from the
software repository.

It is responsible for identifying:

-   Module boundaries
-   Component relationships
-   Dependency graphs
-   Interfaces and abstractions
-   Design patterns
-   Concurrency characteristics

------------------------------------------------------------------------

## Module Extraction

Example:

    Authentication Module

    Responsibility:
    User authentication flow

    Dependencies:

    Authentication → Domain
    Authentication → Network

------------------------------------------------------------------------

## Dependency Graph Extraction

Example:

    LoginViewModel

            |
            v

    LoginUseCase

            |
            v

    UserRepository

The dependency graph helps the LLM understand:

-   Which dependencies exist
-   Which components should be mocked
-   Which boundaries should be tested

------------------------------------------------------------------------

## Interface Analysis

Example:

``` swift
protocol UserRepository {

    func fetchUser() async throws -> User

}
```

The analyzer identifies:

-   Protocol abstractions
-   Implementations
-   Injection points

------------------------------------------------------------------------

## Architecture Pattern Detection

Examples:

    MVVM

    Clean Architecture

    VIPER

    TCA

    Repository Pattern

    Dependency Injection

------------------------------------------------------------------------

# 5. Architecture Context Schema

The Architecture Analyzer produces a structured representation based on
the Architecture Context Schema.

Example:

``` json
{
  "component": {
    "name": "LoginViewModel",
    "layer": "Presentation"
  },

  "dependencies": [
    {
      "name": "LoginUseCase",
      "type": "Protocol"
    }
  ],

  "patterns": [
    "MVVM",
    "Dependency Injection"
  ],

  "testing": {
    "framework": "XCTest",
    "mock_strategy": "Protocol Mock"
  }
}
```

This representation acts as additional context for the LLM.

------------------------------------------------------------------------

# 6. Context Engineering Layer

## Purpose

The Context Engineering Layer decides which architectural information
should be provided to the LLM.

Providing the entire repository can introduce:

-   Excessive context size
-   Irrelevant information
-   Reduced model reliability

Therefore, the framework selects relevant architecture information based
on the target component.

------------------------------------------------------------------------

## Example

Target:

    LoginViewModel

Selected Context:

    Component Context

    +

    Dependency Context

    +

    Interface Context

    +

    Testing Context

------------------------------------------------------------------------

# 7. LLM Test Generation

The framework compares two approaches.

------------------------------------------------------------------------

## Baseline Approach

Traditional LLM test generation:

    Source Code

          |

         LLM

          |

    Generated Unit Tests

Input:

-   Class implementation
-   Method information

------------------------------------------------------------------------

## Proposed Approach

Architecture-aware generation:

    Source Code

    +

    Architecture Context

    +

    Dependency Information

    +

    Design Patterns

            |

           LLM

            |

    Generated Unit Tests

The generated tests should better understand:

-   Required mocks
-   Expected interactions
-   Correct testing boundaries

------------------------------------------------------------------------

# 8. Quality Evaluation Pipeline

Generated tests are evaluated using multiple metrics.

Coverage alone is insufficient because high coverage does not always
indicate high-quality tests.

------------------------------------------------------------------------

## Evaluation Metrics

  -----------------------------------------------------------------------
  Metric                              Purpose
  ----------------------------------- -----------------------------------
  Compilation Success Rate            Determines whether generated tests
                                      can execute

  Code Coverage                       Measures tested code percentage

  Mutation Score                      Evaluates fault detection
                                      capability

  Fault Detection Rate                Measures ability to identify real
                                      defects

  Test Maintainability                Evaluates readability and stability

  Mock Correctness                    Checks dependency isolation quality
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 9. Experimental Comparison

The research compares:

## Approach A

    Code Only

    ↓

    LLM

    ↓

    Unit Tests

------------------------------------------------------------------------

## Approach B

    Code

    +

    Local Context

    ↓

    LLM

    ↓

    Unit Tests

------------------------------------------------------------------------

## Approach C (Proposed)

    Code

    +

    Architecture Context

    +

    Dependency Graph

    +

    Design Patterns

    ↓

    LLM

    ↓

    Unit Tests

------------------------------------------------------------------------

# 10. Expected Outcome

The expected outcome is to demonstrate that architecture-aware context
can improve LLM-generated unit tests in modular software systems.

The research investigates whether architectural knowledge helps LLMs:

-   Understand software responsibilities
-   Generate appropriate mocks
-   Respect component boundaries
-   Produce maintainable tests

------------------------------------------------------------------------

# Future Extensions

Future versions of the framework may include:

-   Automatic architecture extraction tools
-   Static analysis integration
-   Repository-level retrieval systems
-   Support for multiple programming languages
-   Integration with CI/CD pipelines
