# Architecture-Aware Context Engineering for LLM-Based Unit Test Generation in Modular Software Systems

## Overview

This repository contains the research project for investigating how
software architecture knowledge can improve Large Language Model
(LLM)-based unit test generation.

Current LLM-based test generation approaches mainly rely on source code
context. However, modern software systems are designed using
architectural patterns, modular boundaries, dependency relationships,
and abstraction layers.

This project explores whether providing structured architecture context
to LLMs can improve:

-   Unit test correctness
-   Dependency understanding
-   Mock generation
-   Fault detection capability
-   Test maintainability

------------------------------------------------------------------------

# Research Motivation

Large Language Models have demonstrated strong capabilities in software
engineering tasks such as:

-   Code generation
-   Code completion
-   Code explanation
-   Automated test generation

However, generated tests often lack awareness of:

-   Software architecture
-   Component responsibilities
-   Module boundaries
-   Dependency relationships
-   Design patterns

For example, an LLM may generate a test for a ViewModel but fail to
understand that:

    ViewModel
        |
        v
    UseCase
        |
        v
    Repository

requires dependency isolation and mock generation.

This research investigates whether architectural understanding can
improve generated tests.

------------------------------------------------------------------------

# Research Question

The main research question is:

> Does architecture-aware context improve the quality of LLM-generated
> unit tests compared with traditional source-code-only approaches?

Additional questions:

1.  Which architectural information contributes most to test generation
    quality?
2.  Can architecture-aware context improve maintainability and fault
    detection?
3.  How does architectural knowledge affect testing of modular software
    systems?

------------------------------------------------------------------------

# Proposed Approach

The proposed framework introduces an architecture-aware context
engineering pipeline:

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

    Large Language Model

            |
            v

    Generated Unit Tests

            |
            v

    Quality Evaluation

------------------------------------------------------------------------

# Architecture Context Schema

The project introduces a structured representation of software
architecture information.

The schema includes:

## System Context

General project information:

-   Programming language
-   Frameworks
-   Architecture style
-   Testing framework

------------------------------------------------------------------------

## Module Context

Information about:

-   Modules
-   Responsibilities
-   Dependencies
-   Architectural boundaries

Example:

    Authentication Module

    Depends on:

    Domain
    Network
    Storage

------------------------------------------------------------------------

## Component Context

Information about:

-   Component type
-   Architectural role
-   Responsibilities

Example:

    LoginViewModel

    Role:
    Presentation Layer

    Pattern:
    MVVM

------------------------------------------------------------------------

## Dependency Context

Represents relationships between components.

Example:

    LoginViewModel

    depends on

    LoginUseCase

    implemented through

    Protocol

------------------------------------------------------------------------

## Interface Context

Represents:

-   Protocols
-   Interfaces
-   Abstractions
-   Implementations

------------------------------------------------------------------------

## Design Pattern Context

Supports patterns such as:

-   MVVM
-   Clean Architecture
-   VIPER
-   TCA
-   Repository Pattern
-   Dependency Injection

------------------------------------------------------------------------

## Concurrency Context

Represents:

-   async/await usage
-   Actors
-   Concurrent operations

------------------------------------------------------------------------

## Testing Context

Defines:

-   Testing framework
-   Mocking strategy
-   Testing style

------------------------------------------------------------------------

# Experimental Design

The research compares three approaches.

## Baseline 1: Code Only

    Source Code

         |

        LLM

         |

    Generated Unit Tests

------------------------------------------------------------------------

## Baseline 2: Code + Local Context

    Source Code

    +

    Related Files

         |

        LLM

         |

    Generated Unit Tests

------------------------------------------------------------------------

## Proposed Approach: Architecture-Aware Context

    Source Code

    +

    Architecture Context

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

------------------------------------------------------------------------

# Evaluation Metrics

Generated tests are evaluated using:

  Metric                     Purpose
  -------------------------- ----------------------------------
  Compilation Success Rate   Can generated tests execute?
  Code Coverage              Tested code percentage
  Mutation Score             Ability to detect faults
  Fault Detection Rate       Real defect detection capability
  Test Maintainability       Quality and readability
  Mock Correctness           Dependency isolation quality

------------------------------------------------------------------------

# Supported Architecture Examples

Initial research focuses on modular software architectures:

## MVVM

    View
     |
    ViewModel
     |
    Repository

## Clean Architecture

    Presentation

    Domain

    Data

## TCA

    State

    Action

    Reducer

    Effect

    Dependency

------------------------------------------------------------------------

# Repository Structure

    architecture-aware-llm-testing

    ├── Research_Proposal.md
    ├── Literature_Review.md
    ├── Architecture_Context.md
    ├── Proposed_Framework.md
    ├── Experiment_Design.md
    ├── Research_Roadmap.md
    │
    └── Prototype

------------------------------------------------------------------------

# Research Status

## Completed

-   Research topic definition
-   Initial literature review
-   Research gap identification
-   Architecture Context Schema design
-   Proposed framework design
-   Experiment design

## Next Steps

1.  Design prototype architecture
2.  Implement architecture extraction
3.  Build LLM testing pipeline
4.  Run experiments
5.  Analyze results
6.  Prepare research paper

------------------------------------------------------------------------

# Goal

The goal of this project is not to train a new Large Language Model.

Instead, the research investigates how structured software architecture
knowledge can improve existing LLM capabilities for automated unit test
generation.
