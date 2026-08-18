# Project Structure

## Architecture-Aware Context Engineering for LLM-Based Unit Test Generation in Modular Software Systems

------------------------------------------------------------------------

# 1. Overview

This document defines the initial repository structure for the prototype
implementation.

The goal is to keep the implementation modular, testable, and aligned
with the research architecture:

    Software Repository

            |

            v

    Architecture Analyzer

            |

            v

    Architecture Context Generator

            |

            v

    LLM Context Engineering

            |

            v

    Test Generation

            |

            v

    Evaluation

The prototype should follow separation of responsibilities so that each
research component can be evaluated independently.

------------------------------------------------------------------------

# 2. Repository Structure

Proposed structure:

    architecture-aware-llm-testing

    │
    ├── README.md
    ├── Research_Proposal.md
    ├── Literature_Review.md
    ├── Architecture_Context.md
    ├── Proposed_Framework.md
    ├── Experiment_Design.md
    ├── Implementation_Plan.md
    ├── MVP_Development_Plan.md
    │
    ├── prototype
    │
    │   ├── analyzer
    │   │   ├── repository_scanner
    │   │   ├── swift_parser
    │   │   ├── dependency_analyzer
    │   │   └── pattern_detector
    │   │
    │   ├── context
    │   │   ├── schema
    │   │   ├── context_builder
    │   │   └── context_validator
    │   │
    │   ├── llm
    │   │   ├── prompt_builder
    │   │   ├── client
    │   │   └── generators
    │   │
    │   ├── evaluation
    │   │   ├── test_runner
    │   │   ├── coverage
    │   │   ├── mutation_testing
    │   │   └── quality_analysis
    │   │
    │   ├── examples
    │   │   └── swift_samples
    │   │
    │   └── tests
    │
    └── experiments
        ├── datasets
        ├── results
        └── reports

------------------------------------------------------------------------

# 3. Component Responsibilities

------------------------------------------------------------------------

# Analyzer Module

Path:

    prototype/analyzer

Responsibility:

Analyze software repositories and extract architecture information.

Components:

## Repository Scanner

Responsibilities:

-   Discover files
-   Identify modules
-   Detect source and test files

Output:

    repository_metadata.json

------------------------------------------------------------------------

## Swift Parser

Responsibilities:

Extract:

-   Classes
-   Structs
-   Protocols
-   Functions
-   Initializers

Possible technologies:

-   SwiftSyntax
-   SourceKit
-   Tree-sitter

------------------------------------------------------------------------

## Dependency Analyzer

Responsibilities:

Build dependency relationships.

Example:

    LoginViewModel

            |

            v

    LoginUseCase

Output:

    dependency_graph.json

------------------------------------------------------------------------

## Pattern Detector

Responsibilities:

Detect architectural patterns.

Initial support:

-   MVVM
-   Clean Architecture
-   TCA
-   VIPER

------------------------------------------------------------------------

# Context Module

Path:

    prototype/context

Responsibility:

Convert extracted information into Architecture Context Schema.

------------------------------------------------------------------------

## Schema

Contains:

-   System Context
-   Module Context
-   Component Context
-   Dependency Context
-   Interface Context
-   Pattern Context
-   Testing Context

Output:

    architecture_context.json

------------------------------------------------------------------------

## Context Builder

Responsibilities:

Create the final context sent to the LLM.

Example:

Input:

    LoginViewModel

Output:

    Component Information

    +

    Dependencies

    +

    Interfaces

    +

    Testing Strategy

------------------------------------------------------------------------

## Context Validator

Responsibilities:

Verify:

-   Required fields exist
-   JSON format is valid
-   Context is consistent

------------------------------------------------------------------------

# LLM Module

Path:

    prototype/llm

Responsibility:

Handle interaction with Large Language Models.

------------------------------------------------------------------------

## Prompt Builder

Creates prompts for:

## Baseline

    Source Code

    ↓

    LLM

    ↓

    Tests

------------------------------------------------------------------------

## Proposed

    Source Code

    +

    Architecture Context

    ↓

    LLM

    ↓

    Tests

------------------------------------------------------------------------

## LLM Client

Responsibilities:

-   API communication
-   Request handling
-   Response storage

------------------------------------------------------------------------

## Test Generator

Responsibilities:

Save generated tests.

Output:

    GeneratedTests.swift

------------------------------------------------------------------------

# Evaluation Module

Path:

    prototype/evaluation

Responsibility:

Measure generated test quality.

------------------------------------------------------------------------

## Test Runner

Responsibilities:

-   Execute generated tests
-   Collect execution results

------------------------------------------------------------------------

## Coverage Analyzer

Measures:

-   Line coverage
-   Branch coverage

------------------------------------------------------------------------

## Mutation Testing

Measures:

-   Fault detection capability

------------------------------------------------------------------------

## Quality Analyzer

Analyzes:

-   Mock correctness
-   Assertion quality
-   Test maintainability
-   Test smells

------------------------------------------------------------------------

# 4. Example Workflow

    Swift Project

            |

            v

    Repository Scanner

            |

            v

    Swift Parser

            |

            v

    Dependency Analyzer

            |

            v

    Architecture Context JSON

            |

            v

    Prompt Builder

            |

            v

    LLM

            |

            v

    Generated XCTest

            |

            v

    Evaluation

------------------------------------------------------------------------

# 5. Development Milestones

## Milestone 1: Basic Analyzer

Goal:

Extract:

-   Files
-   Classes
-   Protocols
-   Dependencies

------------------------------------------------------------------------

## Milestone 2: Context Generation

Goal:

Generate:

    architecture_context.json

------------------------------------------------------------------------

## Milestone 3: LLM Integration

Goal:

Generate tests using:

-   Code only
-   Architecture context

------------------------------------------------------------------------

## Milestone 4: Evaluation Pipeline

Goal:

Compare:

Baseline vs Proposed Approach

------------------------------------------------------------------------

# 6. Design Principles

The prototype follows:

## Modularity

Each component can be replaced independently.

## Extensibility

New languages and architectures can be added.

## Reproducibility

Experiments should be repeatable.

## Research Focus

The prototype exists to validate the research hypothesis, not to become
a commercial testing tool.

------------------------------------------------------------------------

# 7. Initial Implementation Target

First working version:

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

    Generate XCTest with LLM

            |

    Compare Results

This provides the minimum required evidence for validating the proposed
research direction.
