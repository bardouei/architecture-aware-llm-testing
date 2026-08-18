# Architecture-Aware Context Engineering for LLM-Based Unit Test Generation in Modular Software Systems


## 1. Abstract


## 2. Background


## 3. Problem Statement


## 4. Research Gap


## 5. Research Objectives


## 6. Research Questions


## 7. Proposed Approach


## 8. Expected Contributions


## 9. Evaluation Strategy


Background
Large Language Models (LLMs) have recently demonstrated strong capabilities in software engineering tasks, including code generation, code completion, and automated unit test generation.

However, most existing approaches rely mainly on source-code-level context. They have limited understanding of software architecture, module boundaries, dependency relationships, and design patterns that define how modern software systems are structured.


Problem Statement
Modern software systems are increasingly built using modular architectures such as Clean Architecture, MVVM, VIPER, and other layered approaches.

Generating high-quality unit tests for these systems requires understanding not only individual classes but also their architectural roles and relationships.

Current LLM-based test generation approaches often fail to correctly identify dependencies, generate appropriate mocks, and maintain testing boundaries because architectural knowledge is missing from the provided context.

Research Gap
Existing studies have explored LLM-based unit test generation using source code, documentation, retrieval mechanisms, and program analysis.

However, limited research has investigated how explicit software architecture context can improve LLM-based unit test generation, particularly for modular software systems.

Research Questions
RQ1:
Does architecture-aware context improve the quality of LLM-generated unit tests compared with source-code-only approaches?


RQ2:
Which architectural information provides the highest impact on generated test quality?


RQ3:
Can architecture-aware context improve test maintainability and fault detection capability in modular software systems?
