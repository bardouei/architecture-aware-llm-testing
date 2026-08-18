# Prototype Design

## Architecture-Aware Context Engineering for LLM-Based Unit Test Generation in Modular Software Systems

------------------------------------------------------------------------

# 1. Prototype Overview

This prototype implements the practical validation of the proposed
architecture-aware context engineering framework.

The goal is not to train a new Large Language Model or build an
autonomous AI agent.

Instead, the prototype introduces an intermediate software architecture
understanding layer that extracts architectural knowledge from an
existing software project and provides structured context to an LLM
during unit test generation.

The prototype follows this workflow:

    Software Repository

            |

            v

    Architecture Analyzer

            |

            v

    Architecture Context Generator

            |

            v

    LLM Context Engineering Layer

            |

            v

    Unit Test Generation

            |

            v

    Test Evaluation

------------------------------------------------------------------------

# 2. Design Goals

The prototype should:

1.  Extract meaningful architectural information from software projects.
2.  Convert architecture knowledge into a structured representation.
3.  Provide relevant context to LLMs.
4.  Compare architecture-aware generation against traditional
    approaches.
5.  Measure improvements in generated test quality.

------------------------------------------------------------------------

# 3. Technology Strategy

## General Framework

The proposed approach is language-independent.

The architecture context model should not depend on a specific
programming language or framework.

Conceptually:

    Any Software Project

            |

    Architecture Analysis

            |

    Architecture Context

            |

    LLM Test Generation

------------------------------------------------------------------------

# 4. Case Study Implementation

Although the framework is general, the initial prototype will use Swift
applications as a case study.

Reasons:

-   Strong modular architecture ecosystem
-   Clear architectural patterns
-   Mature testing framework (XCTest)
-   Availability of real-world projects
-   Existing experience with MVVM, Clean Architecture, VIPER, and TCA

Initial target:

    Swift Modular Applications

------------------------------------------------------------------------

# 5. Prototype Technology Stack

## Core Analyzer

Language:

    Python

Reasons:

-   Strong ecosystem for AI integration
-   Easy experimentation
-   Available parsing and analysis libraries
-   Easy integration with LLM APIs

------------------------------------------------------------------------

## Target Language

Initial analysis target:

    Swift

Future extensions:

-   Java
-   Kotlin
-   TypeScript
-   Python

------------------------------------------------------------------------

# 6. Prototype Components

## Component 1: Source Repository Parser

Purpose:

Read and analyze the software repository.

Input:

    Swift Project

    ├── Sources
    ├── Modules
    ├── Tests
    └── Configuration

Responsibilities:

-   Discover files
-   Identify modules
-   Extract source code information

------------------------------------------------------------------------

# Component 2: Architecture Analyzer

Purpose:

Extract architecture-related information.

Responsibilities:

## Module Detection

Example:

    Authentication

    Feature Module

    Depends on:

    Domain
    Network
    Storage

------------------------------------------------------------------------

## Component Detection

Example:

    LoginViewModel

    Type:
    ViewModel

    Layer:
    Presentation

------------------------------------------------------------------------

## Dependency Analysis

Example:

Source:

``` swift
init(
    useCase: LoginUseCase
)
```

Extracted:

    LoginViewModel

            |

            v

    LoginUseCase

------------------------------------------------------------------------

## Interface Detection

Example:

``` swift
protocol UserRepository {

}
```

Extracted:

    Interface:

    UserRepository

    Implementation:

    DefaultUserRepository

------------------------------------------------------------------------

## Pattern Detection

Initial supported patterns:

    MVVM

    Clean Architecture

    TCA

    VIPER

    Repository Pattern

    Dependency Injection

------------------------------------------------------------------------

# Component 3: Architecture Context Generator

Purpose:

Convert extracted information into structured context.

Output:

Example:

``` json
{
 "component": "LoginViewModel",

 "architecture_role": "Presentation",

 "pattern": "MVVM",

 "dependencies": [
    {
      "name": "LoginUseCase",
      "mock_required": true
    }
 ],

 "testing_strategy": {
    "framework": "XCTest",
    "style": "Given-When-Then"
 }
}
```

------------------------------------------------------------------------

# Component 4: Context Engineering Layer

Purpose:

Select the most relevant architecture information for the target
component.

Problem:

Providing the complete repository creates:

-   Excessive context
-   Irrelevant information
-   Lower LLM reliability

Solution:

Generate focused context.

Example:

Target:

    LoginViewModel

Selected context:

    Component Context

    +

    Dependency Context

    +

    Interface Context

    +

    Testing Context

------------------------------------------------------------------------

# Component 5: LLM Test Generator

Two generation modes are compared.

------------------------------------------------------------------------

## Traditional Mode

    Source Code

          |

         LLM

          |

    Generated Unit Test

------------------------------------------------------------------------

## Architecture-Aware Mode

    Source Code

    +

    Architecture Context

    +

    Dependency Graph

    +

    Design Patterns

          |

         LLM

          |

    Generated Unit Test

------------------------------------------------------------------------

# Component 6: Test Evaluation

Generated tests are evaluated through:

## Build Validation

Question:

Does the generated test compile?

------------------------------------------------------------------------

## Coverage Analysis

Metrics:

-   Line Coverage
-   Branch Coverage

------------------------------------------------------------------------

## Mutation Testing

Question:

Can generated tests detect injected faults?

------------------------------------------------------------------------

## Quality Analysis

Evaluate:

-   Mock correctness
-   Assertion quality
-   Maintainability
-   Test smells

------------------------------------------------------------------------

# 7. Initial Prototype Scope

The first prototype should remain small.

Target:

    One Swift Modular Application

    +

    One Architecture Pattern

    +

    One LLM

    +

    One Test Generation Scenario

Example:

    MVVM Login Feature

    Input:

    LoginViewModel

    Output:

    LoginViewModelTests

------------------------------------------------------------------------

# 8. Future Expansion

After validating the concept:

Expand to:

    MVVM

    +

    Clean Architecture

    +

    TCA

    +

    Multiple Projects

    +

    Multiple Languages

------------------------------------------------------------------------

# 9. Expected Research Contribution

The prototype validates the following research idea:

Current approach:

    Code

     |

    LLM

     |

    Tests

Proposed approach:

    Code

    +

    Architecture Knowledge

    +

    Context Engineering

     |

    LLM

     |

    Higher Quality Tests

The prototype demonstrates how software architecture knowledge can
improve LLM-based unit test generation without requiring model training.
