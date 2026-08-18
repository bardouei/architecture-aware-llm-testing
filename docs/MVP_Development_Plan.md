# MVP Development Plan

## Architecture-Aware Context Engineering for LLM-Based Unit Test Generation in Modular Software Systems

------------------------------------------------------------------------

# 1. MVP Goal

The goal of the Minimum Viable Prototype (MVP) is to validate the core
research hypothesis:

> Providing structured software architecture context improves the
> quality of LLM-generated unit tests.

The MVP is not intended to build a complete production tool.

The objective is to create a small but measurable research prototype
that demonstrates:

    Software Project

            |

    Architecture Context Extraction

            |

    Architecture-Aware Prompt

            |

    LLM Test Generation

            |

    Evaluation

------------------------------------------------------------------------

# 2. MVP Scope

The first version intentionally focuses on a limited scenario.

## Included

-   One programming language
-   One architecture style
-   One testing framework
-   One LLM provider
-   One evaluation scenario

## Excluded

-   Full multi-language support
-   Autonomous AI agents
-   Model training
-   IDE plugin
-   Complete architecture recovery system

------------------------------------------------------------------------

# 3. MVP Technology Selection

## Analyzer Language

Selected:

    Python

Reason:

-   Strong AI ecosystem
-   Easy experimentation
-   Good integration with LLM APIs
-   Fast iteration

------------------------------------------------------------------------

## Case Study Language

Selected:

    Swift

Reason:

-   Existing expertise
-   Mature testing ecosystem
-   Strong modular architecture usage
-   Clear dependency patterns

------------------------------------------------------------------------

## Testing Framework

Selected:

    XCTest

------------------------------------------------------------------------

# 4. MVP Target Project

The first experiment should use a small controlled Swift project.

Example:

    SampleApp

    ├── Feature
    │
    │   └── Authentication
    │
    ├── Domain
    │
    ├── Data
    │
    └── Tests

------------------------------------------------------------------------

Architecture:

    MVVM + Clean Architecture

Example flow:

    LoginView

        |

        v

    LoginViewModel

        |

        v

    LoginUseCase

        |

        v

    UserRepository

------------------------------------------------------------------------

# 5. MVP Components

## Component 1: Swift Project Scanner

Responsibility:

Read project files.

Extract:

-   Swift files
-   Modules
-   Classes
-   Protocols
-   Test files

Output:

    repository_metadata.json

Example:

``` json
{
 "files": [
   "LoginViewModel.swift",
   "LoginUseCase.swift"
 ]
}
```

------------------------------------------------------------------------

# Component 2: Basic Dependency Extractor

Responsibility:

Identify relationships.

Example:

Swift:

``` swift
init(useCase: LoginUseCase)
```

Output:

``` json
{
 "component":"LoginViewModel",
 "depends_on":[
   "LoginUseCase"
 ]
}
```

------------------------------------------------------------------------

# Component 3: Architecture Context Generator

Convert extracted information into the research schema.

Output:

    architecture_context.json

Example:

``` json
{
 "component":"LoginViewModel",

 "architecture":"MVVM",

 "role":"Presentation",

 "dependencies":[
   {
    "name":"LoginUseCase",
    "mock_required":true
   }
 ]
}
```

------------------------------------------------------------------------

# Component 4: Prompt Builder

Creates two prompts for comparison.

------------------------------------------------------------------------

## Baseline Prompt

    Generate XCTest for this Swift class.

    Source Code:

    {code}

------------------------------------------------------------------------

## Architecture-Aware Prompt

    Generate XCTest for this Swift class.

    Source Code:

    {code}

    Architecture Context:

    {architecture_context}

------------------------------------------------------------------------

# Component 5: LLM Interface

Responsibilities:

-   Send prompt
-   Receive generated tests
-   Save output

Output:

    GeneratedTests.swift

------------------------------------------------------------------------

# Component 6: Evaluation Runner

Evaluate generated tests.

Initial metrics:

## Compilation

Does the generated test build?

------------------------------------------------------------------------

## Coverage

Measure:

-   Line coverage

------------------------------------------------------------------------

## Mock Quality

Check:

-   Correct dependency mocking
-   Proper isolation

------------------------------------------------------------------------

# 6. MVP Experiment Flow

    Swift Project

            |

    Scanner

            |

    Architecture Context

            |

    +-----------------------+
    |                       |
    v                       v

    Code Only Prompt    Architecture Prompt

    |                       |

    LLM                     LLM

    |                       |

    Tests A              Tests B

    |                       |

    Evaluation          Evaluation

------------------------------------------------------------------------

# 7. MVP Success Criteria

The MVP is successful if architecture-aware generation demonstrates
improvement in at least one area:

-   Higher compilation success
-   Better dependency mocking
-   Better test structure
-   Higher mutation score
-   Better maintainability

------------------------------------------------------------------------

# 8. MVP Development Order

## Step 1

Create sample Swift modular project.

------------------------------------------------------------------------

## Step 2

Implement Swift source scanner.

------------------------------------------------------------------------

## Step 3

Generate first architecture_context.json.

------------------------------------------------------------------------

## Step 4

Create LLM prompt pipeline.

------------------------------------------------------------------------

## Step 5

Generate baseline tests.

------------------------------------------------------------------------

## Step 6

Generate architecture-aware tests.

------------------------------------------------------------------------

## Step 7

Compare results.

------------------------------------------------------------------------

# 9. Future Improvements After MVP

After validating the idea:

-   Support more architectures:

    -   TCA
    -   VIPER
    -   Pure MVVM

-   Add automatic pattern detection.

-   Add dependency graph visualization.

-   Support more languages.

-   Integrate with CI/CD.

------------------------------------------------------------------------

# Final MVP Architecture

                  Swift Project

                        |

                        v

              Swift Architecture Scanner

                        |

                        v

              Architecture Context JSON

                        |

              +----------------+
              |                |
              v                v

         Code Prompt     Architecture Prompt

              |                |

              v                v

                  LLM Test Generation

                        |

                        v

                 XCTest Comparison

                        |

                        v

                  Research Results
