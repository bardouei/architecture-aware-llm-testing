# Related Work


## 1. Large Language Models in Software Engineering

Large Language Models (LLMs) have recently demonstrated significant capabilities in software engineering tasks, including code completion, code generation, program repair, and software documentation.

Models such as GPT-based systems and other code-oriented language models have shown that large-scale pre-trained models can learn programming patterns and generate syntactically valid code from natural language descriptions.

However, software engineering tasks differ from general code generation because successful solutions require understanding software structure, design decisions, and relationships between multiple components.

In particular, tasks such as automated unit test generation require more than local code understanding. A generated test must respect dependency boundaries, abstraction levels, and architectural constraints defined by the original software system.


## 2. LLM-Based Unit Test Generation

Recent research has investigated the application of LLMs for automated unit test generation. These approaches typically provide source code elements such as classes, methods, or functions as input and ask the model to generate corresponding test cases.

The main advantage of these approaches is their ability to produce human-like test code with limited manual effort. However, many existing approaches focus primarily on code-level information and evaluate generated tests based on syntactic correctness, compilation success, or code coverage.

A major limitation of code-only approaches is the lack of architectural awareness.

For example, when testing a component that depends on an abstraction:

ViewModel
    |
    v
Repository Protocol

a test generator must understand that the dependency should usually be replaced with a mock implementation rather than a concrete production object.

Without architectural information, LLMs may generate tests that:

- instantiate concrete implementations,
- violate dependency inversion principles,
- create tightly coupled tests,
- ignore concurrency constraints,
- test implementation details instead of behavior.


## 3. Retrieval-Augmented Generation for Software Engineering

Retrieval-Augmented Generation (RAG) approaches have been introduced to improve LLM performance by providing additional relevant information from external sources.

In software engineering, RAG-based methods commonly retrieve relevant source files, documentation, or repository fragments and provide them as additional context to the LLM.

Although retrieval improves context availability, most existing approaches focus on textual or semantic similarity between code fragments.

However, software architecture relationships are not always captured through textual similarity.

For example:

LoginViewModel
depends on
LoginUseCase Protocol
implemented by
DefaultLoginUseCase

The relationship between these components represents architectural knowledge rather than simple textual similarity.

Therefore, retrieving files alone may not provide the architectural reasoning required for high-quality test generation.


## 4. Context Engineering for LLM Applications

Context engineering has emerged as an important research direction for improving the effectiveness of LLM-based systems.

Instead of only increasing the amount of information provided to a model, context engineering focuses on designing structured, relevant, and task-specific information representations.

In software engineering scenarios, effective context engineering requires answering questions such as:

- What information should be provided to the LLM?
- How should software knowledge be represented?
- Which parts of a repository are relevant for a specific task?
- How can irrelevant information be removed?

Existing approaches demonstrate the importance of context selection; however, architecture-specific context engineering for automated testing remains underexplored.


## 5. Software Architecture Recovery and Analysis

Software architecture recovery techniques aim to extract architectural information from existing source code.

Previous research has explored approaches for identifying:

- components,
- dependencies,
- architectural layers,
- design patterns,
- module relationships.

These techniques provide valuable information for understanding large software systems.

However, traditional architecture recovery methods are generally designed for software maintenance, visualization, or reverse engineering purposes rather than serving as context providers for LLM-based generation tasks.

Our work connects software architecture analysis with LLM-based test generation by transforming recovered architectural knowledge into an LLM-compatible context representation.


## 6. Limitations of Existing Approaches

Based on existing research directions, several limitations remain:

| Research Area | Existing Capability | Remaining Limitation |
|---|---|---|
| LLM Code Generation | Generates code from prompts | Limited architectural understanding |
| LLM Test Generation | Produces unit tests from source code | Weak dependency and abstraction reasoning |
| RAG for Software Engineering | Retrieves relevant code | Does not explicitly model architecture |
| Context Engineering | Improves prompt information quality | Limited focus on software architecture |
| Architecture Recovery | Extracts system structure | Not designed for LLM test generation |


## 7. Research Gap

The main research gap identified in this work is the absence of a systematic approach for incorporating software architecture knowledge into LLM-based unit test generation.

Existing methods generally treat source code as the primary context, while architectural information such as:

- component responsibilities,
- abstraction boundaries,
- protocol-implementation relationships,
- module structures,
- dependency directions,

is rarely represented explicitly.

This research addresses this gap by proposing an architecture-aware context engineering framework that transforms software architecture knowledge into structured context for LLM-based unit test generation.


## 8. Summary

Previous research has demonstrated the potential of LLMs for software engineering tasks and automated test generation. However, achieving reliable test generation for modular software systems requires deeper understanding of software architecture.

This work builds upon existing research in LLM-based software engineering, retrieval-based