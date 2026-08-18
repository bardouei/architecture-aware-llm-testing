# Implementation Plan

## Architecture-Aware Context Engineering for LLM-Based Unit Test Generation in Modular Software Systems

------------------------------------------------------------------------

# 1. Implementation Overview

This document defines the technical implementation plan for the research
prototype.

The objective is to build a proof-of-concept system that can:

1.  Analyze a software repository.
2.  Extract software architecture information.
3.  Convert architectural knowledge into structured context.
4.  Provide architecture-aware context to an LLM.
5.  Generate and evaluate unit tests.

The implementation focuses on validating the research hypothesis:

> Providing structured software architecture context improves the
> quality of LLM-generated unit tests.

------------------------------------------------------------------------

# 2. High-Level Architecture

The prototype consists of the following components:

                    Software Repository

                            |
                            v

                  Repository Analyzer

                            |
                            v

                Architecture Extraction Layer

                            |
                            v

              Architecture Context Generator

                            |
                            v

               Context Engineering Pipeline

                            |
                            v

                           LLM

                            |
                            v

                  Generated Unit Tests

                            |
                            v

                  Evaluation Framework

------------------------------------------------------------------------

# 3. Technology Stack Decision

## Core Implementation Language

Selected:

    Python

Reason:

-   Strong AI/LLM ecosystem
-   Fast experimentation
-   Easy integration with APIs
-   Rich code analysis libraries

------------------------------------------------------------------------

# 4. Target Language Support

Initial target:

    Swift

Reason:

-   Strong personal expertise
-   Mature testing ecosystem (XCTest)
-   Clear architectural patterns
-   Good case study for modular applications

Future support:

-   Java
-   Kotlin
-   TypeScript
-   Python

The framework design should remain language-independent.

------------------------------------------------------------------------

# 5. Component Implementation Plan

------------------------------------------------------------------------

# Component 1: Repository Analyzer

## Responsibility

Analyze the input software repository.

Input:

    Project Repository

Output:

    Repository Metadata

Extract:

-   Files
-   Modules
-   Folders
-   Source files
-   Test files
-   Dependencies

------------------------------------------------------------------------

Example:

Input:

    App

    ├── Features
    ├── Domain
    ├── Network
    └── Storage

Output:

``` json
{
 "modules": [
   "Features",
   "Domain",
   "Network",
   "Storage"
 ]
}
```

------------------------------------------------------------------------

# Component 2: Swift Code Analyzer

## Responsibility

Extract code-level information.

Possible technologies:

-   SwiftSyntax
-   SourceKit
-   Tree-sitter

------------------------------------------------------------------------

Extract:

## Classes

Example:

``` swift
final class LoginViewModel {

}
```

Output:

``` json
{
 "name":"LoginViewModel",
 "type":"class"
}
```

------------------------------------------------------------------------

## Protocols

Example:

``` swift
protocol UserRepository {

}
```

Output:

``` json
{
 "name":"UserRepository",
 "type":"protocol"
}
```

------------------------------------------------------------------------

## Initializers

Example:

``` swift
init(repository: UserRepository)
```

Output:

``` json
{
 "dependency":"UserRepository"
}
```

------------------------------------------------------------------------

# Component 3: Dependency Graph Generator

## Responsibility

Build relationships between components.

Example:

Input:

``` swift
LoginViewModel

depends on

LoginUseCase
```

Output:

    LoginViewModel

            |

            v

    LoginUseCase

Stored as:

``` json
{
 "source":"LoginViewModel",
 "target":"LoginUseCase"
}
```

------------------------------------------------------------------------

# Component 4: Architecture Pattern Detector

## Goal

Identify architectural patterns.

Initial supported patterns:

    MVVM

    Clean Architecture

    TCA

    VIPER

------------------------------------------------------------------------

## Detection Strategy

Combination of:

-   Folder structure
-   Naming conventions
-   Protocol relationships
-   Dependency patterns
-   Code structure

------------------------------------------------------------------------

Example:

Detected:

    LoginView.swift

    LoginViewModel.swift

    LoginRepository.swift

Possible output:

``` json
{
 "architecture":"MVVM"
}
```

------------------------------------------------------------------------

# Component 5: Architecture Context Generator

## Responsibility

Convert extracted information into the Architecture Context Schema.

Input:

    Raw Analysis Data

Output:

    architecture_context.json

Example:

``` json
{
 "component":"LoginViewModel",

 "architecture_role":
 "Presentation",

 "architecture_pattern":
 "MVVM",

 "dependencies":[
   {
    "name":"LoginUseCase",
    "mock_required":true
   }
 ],

 "testing_framework":
 "XCTest"
}
```

------------------------------------------------------------------------

# Component 6: Context Engineering Pipeline

## Responsibility

Select relevant context before sending information to the LLM.

Problem:

Sending the whole repository creates:

-   Large prompts
-   Irrelevant information
-   Reduced reliability

------------------------------------------------------------------------

Example:

Target:

    LoginViewModel

Selected:

    LoginViewModel Code

    +

    Dependencies

    +

    Interfaces

    +

    Architecture Role

    +

    Testing Strategy

------------------------------------------------------------------------

# Component 7: LLM Integration

## Initial Approach

Use API-based LLMs for prototype validation.

Possible models:

-   GPT models
-   Claude
-   Gemini

------------------------------------------------------------------------

Input:

    Source Code

    +

    Architecture Context

    +

    Testing Requirements

Output:

    Generated Unit Tests

------------------------------------------------------------------------

# Component 8: Test Evaluation System

## Responsibilities

Execute generated tests and collect metrics.

------------------------------------------------------------------------

## Metrics

### Compilation Success

Question:

Can generated tests build successfully?

------------------------------------------------------------------------

### Coverage

Measure:

-   Line coverage
-   Branch coverage

------------------------------------------------------------------------

### Mutation Testing

Measure:

Can generated tests detect injected faults?

------------------------------------------------------------------------

### Test Quality

Analyze:

-   Mock correctness
-   Assertion quality
-   Test smell
-   Maintainability

------------------------------------------------------------------------

# 6. Prototype Development Phases

------------------------------------------------------------------------

# Phase 1: Minimal Proof of Concept

Goal:

Validate the research idea.

Scope:

    One Swift Project

    One Feature

    One Architecture Pattern

    One LLM

Example:

    Login Feature

    MVVM

    LoginViewModelTests

------------------------------------------------------------------------

# Phase 2: Architecture Extraction

Implement:

-   Swift parser
-   Dependency extraction
-   Context generation

------------------------------------------------------------------------

# Phase 3: LLM Pipeline

Implement:

-   Prompt construction
-   Context injection
-   Test generation

------------------------------------------------------------------------

# Phase 4: Evaluation

Compare:

## Baseline

    Code Only

vs

## Proposed

    Code + Architecture Context

------------------------------------------------------------------------

# 7. Recommended First Implementation

Do not start with a complete framework.

First milestone:

    Swift Project

            |

    Extract:

    - Classes
    - Protocols
    - Dependencies

            |

    Generate:

    architecture_context.json

            |

    Send to LLM

            |

    Generate XCTest

------------------------------------------------------------------------

# 8. Expected Deliverables

The prototype should produce:

## 1. Architecture Context File

    architecture_context.json

------------------------------------------------------------------------

## 2. Generated Prompt

    prompt.txt

------------------------------------------------------------------------

## 3. Generated Tests

    GeneratedTests.swift

------------------------------------------------------------------------

## 4. Evaluation Report

    evaluation_report.md

------------------------------------------------------------------------

# 9. Long-Term Extension

Future versions can support:

-   Multiple languages
-   More architectures
-   Automatic architecture recovery
-   CI/CD integration
-   IDE plugins

------------------------------------------------------------------------

# Research Contribution

The implementation demonstrates a bridge between:

Traditional LLM testing:

    Code
     |
    LLM
     |
    Tests

and architecture-aware testing:

    Code

    +

    Software Architecture Knowledge

    +

    Context Engineering

     |

    LLM

     |

    Higher Quality Tests
