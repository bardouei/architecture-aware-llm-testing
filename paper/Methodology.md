
# Methodology


## 1. Overview

This section presents the proposed Architecture-Aware Context Engineering framework for LLM-based unit test generation in modular software systems.

The main objective of the proposed framework is to provide Large Language Models with structured architectural knowledge instead of relying only on raw source code.

The proposed approach is based on the assumption that software architecture contains essential information required for generating reliable and maintainable unit tests, including component responsibilities, dependency relationships, abstraction boundaries, and implementation mappings.

The framework consists of four main stages:

1. Architecture Extraction
2. Architecture Context Construction
3. Context Enrichment
4. Context Selection and LLM Context Generation


The overall workflow is illustrated as follows:

Software Repository
    |
    v
Architecture Extraction
    |
    v
Architecture Context Model
    |
    v
Context Enrichment
    |
    v
Relevant Context Selection
    |
    v
LLM-Based Unit Test Generation


---

# 2. Architecture Extraction Layer


The first stage analyzes the software repository to extract architectural information from the existing source code.

Unlike traditional code retrieval approaches that only collect relevant files based on textual similarity, the proposed framework attempts to recover architectural relationships between software components.


The architecture extraction layer consists of three main components:

- Repository Scanner
- Source Code Parser
- Implementation Relationship Analyzer


## 2.1 Repository Scanner

The repository scanner identifies the structure of the software project.

The extracted information includes:

- source files,
- test files,
- project modules,
- feature boundaries.


This information provides the initial representation of the software system structure.


Example:

SwiftSampleApp
├── Feature
│   └── Login
├── Domain
├── Data
└── Tests


## 2.2 Source Code Analysis

The source code analysis component extracts software entities from source files.

The extracted entities include:

- classes,
- protocols,
- dependencies,
- inheritance relationships.


For example, the following Swift relationship:

```swift
final class DefaultLoginUseCase: LoginUseCase
is transformed into an architectural relationship:
DefaultLoginUseCase

        implements

        |

        v

LoginUseCase
2.3 Protocol-Implementation Mapping
Modern modular software systems frequently rely on abstractions such as protocols or interfaces.
Therefore, understanding the relationship between abstractions and implementations is essential for automated test generation.
The proposed framework explicitly models these relationships.
Example:
LoginUseCase (Protocol)

          |

          implements

          |

DefaultLoginUseCase
This information helps an LLM determine whether a dependency should be mocked or directly instantiated during test generation.
3. Architecture Context Construction
After extracting architectural information, the framework constructs a structured architecture context representation.
Instead of providing the complete repository to the LLM, the framework converts architectural information into a compact machine-readable representation.
The architecture context contains:
3.1 System Information
General project information:
programming language,
testing framework,
supported environment.
Example:
{
    "language": "Swift",
    "testing_framework": "XCTest"
}
3.2 Architectural Pattern Information
The framework represents detected architectural patterns.
Examples:
MVVM,
Clean Architecture,
Modular Architecture.
Example:
{
    "patterns": [
        "MVVM",
        "Clean Architecture"
    ]
}
3.3 Component Representation
Each software component is represented with architectural metadata:
component name,
responsibility,
architectural layer,
dependencies,
implemented protocols.
Example:
{
    "name": "LoginViewModel",

    "layer": "Presentation",

    "dependencies": [
        "LoginUseCase"
    ]
}
4. Context Enrichment
Raw architectural information is insufficient for effective LLM reasoning.
Therefore, the framework enriches the extracted context with additional semantic information.
The enrichment stage adds:
4.1 Component Responsibility
The framework identifies the responsibility of each component.
Examples:
ViewModel:

Manages UI state and coordinates user actions


UseCase:

Contains business logic and application rules


Repository:

Provides data access abstraction
This information helps the LLM understand the purpose of each component.
4.2 Testing Strategy Information
The framework adds testing-related knowledge:
testing framework,
test type,
mocking strategy.
Example:
{
    "framework":"XCTest",

    "test_type":"Unit Test",

    "mock_strategy":"Protocol Mock"
}
4.3 Concurrency Context
Modern applications frequently use asynchronous programming models.
The framework captures concurrency-related requirements:
MainActor usage,
async support.
Example:
{
    "main_actor":true,

    "async_support":true
}
This information allows generated tests to respect concurrency constraints.
5. Architecture-Aware Context Selection
Providing the entire architecture context to an LLM can introduce unnecessary information and increase context complexity.
Therefore, the proposed framework introduces a context selection mechanism.
The context selector identifies the minimal architectural context required for a target component.
Example:
For generating tests for:
LoginViewModel
the framework selects:
LoginViewModel

        |

        v

LoginUseCase

        |

        v

UserRepository
instead of providing unrelated components from the entire repository.
The selected context contains:
target component information,
related dependencies,
protocol relationships,
concrete implementations.
This reduces irrelevant information while preserving architectural knowledge required for test generation.
6. LLM Context Generation
The final stage transforms the selected architecture context into an LLM-compatible prompt.
Two approaches are considered:
Baseline Approach
The LLM receives only source code.
Source Code

      |

      v

LLM

      |

      v

Generated Unit Test
Proposed Architecture-Aware Approach
The LLM receives source code combined with architectural context.
Source Code

      +

Architecture Context

      |

      v

LLM

      |

      v

Generated Unit Test
The proposed approach aims to improve:
dependency mocking accuracy,
architectural compliance,
generated test maintainability.
7. Summary
The proposed methodology introduces an architecture-aware context engineering pipeline that bridges the gap between software architecture analysis and LLM-based test generation.
Unlike code-only approaches, the framework provides structured architectural knowledge including component responsibilities, dependency relationships, abstraction mappings, and testing requirements.
By selecting and injecting relevant architectural context, the proposed method aims to enable LLMs to generate more reliable and maintainable unit tests for modular software systems.