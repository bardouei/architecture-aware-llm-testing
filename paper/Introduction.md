# Introduction


## 1. Background

Software systems have become increasingly complex due to the adoption of modular architectures, layered designs, and large-scale dependency structures. Modern software applications are no longer developed as isolated components; instead, they are composed of multiple modules, abstractions, and interconnected services that require careful design and maintenance.

Software testing, particularly unit testing, plays a critical role in ensuring software reliability and maintainability. However, writing comprehensive unit tests remains a time-consuming and challenging task, especially in large and modular software systems where developers must understand component responsibilities, dependency relationships, and architectural boundaries before creating effective tests.

Recently, Large Language Models (LLMs) have shown significant potential in software engineering tasks, including code completion, code generation, bug detection, and automated test generation. The ability of LLMs to understand programming languages and generate human-like code has created new opportunities for improving software development workflows.

However, despite their impressive capabilities, current LLM-based test generation approaches still face important limitations when applied to real-world software projects.


## 2. Challenges of LLM-Based Unit Test Generation

Most existing LLM-based unit test generation approaches primarily rely on source code as the main input. In these approaches, developers provide a class, function, or code fragment to an LLM and request the generation of corresponding unit tests.

Although this approach can generate syntactically valid tests, it often lacks deeper understanding of the software system's architecture.

For example, in a modular application following Clean Architecture or MVVM, a component may depend on abstractions rather than concrete implementations:

Presentation Layer
LoginViewModel
    |
    v
LoginUseCase (Protocol)
    |
    v
DefaultLoginUseCase

A code-only LLM may identify the dependency relationship but fail to understand:

- whether the dependency should be mocked,
- whether a protocol or concrete implementation should be used,
- which layer owns the responsibility,
- how dependency boundaries should be preserved,
- how concurrency requirements affect test implementation.

As a result, generated tests may compile incorrectly, violate architectural principles, or test implementation details instead of component behavior.


## 3. The Importance of Architectural Context

Software architecture contains valuable information that is often not explicitly represented in individual source files. Architectural decisions define how components communicate, how dependencies are managed, and how responsibilities are distributed across the system.

Important architectural knowledge includes:

- component responsibilities,
- module boundaries,
- abstraction relationships,
- protocol-implementation mappings,
- dependency directions,
- architectural patterns,
- concurrency requirements.

For example, knowing that:

LoginViewModel
    |
    depends on
    |
LoginUseCase Protocol
    |
implemented by
    |
DefaultLoginUseCase

provides essential information for generating an appropriate unit test.

With this knowledge, an LLM can generate a test using a protocol-based mock:

```swift
final class MockLoginUseCase: LoginUseCase {
    
}
instead of directly instantiating a concrete implementation.
Therefore, architectural knowledge can serve as an important context source for improving LLM-based software engineering tasks.
4. Research Gap
Although recent studies have explored LLM-based code generation and automated test generation, most existing approaches focus on source-code-level information and do not explicitly incorporate software architecture knowledge into the generation process.
Current limitations include:
Lack of architecture-aware representations
Existing approaches generally provide code snippets or repository content without structured architectural information.
Limited understanding of abstraction boundaries
LLMs may identify dependencies but often fail to distinguish between protocols, interfaces, and their concrete implementations.
Inefficient context usage
Providing an entire repository to an LLM is often impractical due to context limitations, high computational cost, and irrelevant information.
Lack of selective architectural context retrieval
Existing approaches rarely investigate which architectural information is necessary for generating tests for a specific component.
5. Research Objective
This research investigates the following question:
Can architecture-aware context engineering improve the quality and reliability of LLM-generated unit tests in modular software systems?
To address this question, we propose a framework that extracts architectural knowledge from software repositories and transforms it into structured context suitable for LLM-based test generation.
6. Research Contributions
The main contributions of this research are:
1. Architecture Context Representation
We introduce a structured architecture context model that represents:
software components,
architectural layers,
dependencies,
protocols,
implementations,
component responsibilities,
testing strategies,
concurrency requirements.
2. Architecture-Aware Context Engineering Framework
We propose a multi-stage framework consisting of:
architecture extraction,
context construction,
context enrichment,
context selection,
LLM prompt generation.
The framework provides relevant architectural information instead of exposing the LLM to unnecessary repository content.
3. Protocol-Aware Dependency Reasoning
The framework identifies abstraction relationships between protocols and concrete implementations.
This enables the LLM to better understand mocking requirements and maintain architectural boundaries during test generation.
4. Experimental Evaluation Methodology
We define an evaluation methodology comparing:
traditional code-only prompting,
architecture-aware context prompting.
The evaluation considers:
test compilation success,
generated test correctness,
code coverage,
dependency mocking accuracy,
architectural compliance.
7. Paper Organization
The remainder of this paper is organized as follows:
Section 2 discusses related work in LLM-based software engineering, automated test generation, and context engineering.
Section 3 presents the proposed architecture-aware context engineering framework.
Section 4 describes the experimental design and evaluation methodology.
Section 5 discusses experimental results and analysis.
Finally, Section 6 concludes the paper and presents future research directions.