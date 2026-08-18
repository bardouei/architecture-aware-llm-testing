# Architecture Context Schema

## Architecture-Aware Context Engineering for LLM-Based Unit Test Generation in Modular Software Systems

------------------------------------------------------------------------

# 1. Overview

Architecture Context Schema is a structured representation of software
architecture knowledge provided to Large Language Models (LLMs) during
automated unit test generation.

Traditional LLM-based test generation approaches mainly rely on source
code context. However, modern software systems are built using
architectural patterns, modular boundaries, dependency relationships,
and abstraction layers.

The goal of this schema is to provide LLMs with architectural
understanding, enabling them to generate more accurate, maintainable,
and context-aware unit tests.

The Architecture Context Schema represents:

-   System structure
-   Module boundaries
-   Component responsibilities
-   Dependency relationships
-   Interfaces and abstractions
-   Design patterns
-   Data flow
-   Concurrency model
-   Testing strategy

------------------------------------------------------------------------

# 2. Context Elements

The proposed architecture context consists of the following components:

    Architecture Context

    |
    ├── System Context
    |
    ├── Module Context
    |
    ├── Component Context
    |
    ├── Dependency Context
    |
    ├── Interface Context
    |
    ├── Design Pattern Context
    |
    ├── Data Flow Context
    |
    ├── Concurrency Context
    |
    └── Testing Context

------------------------------------------------------------------------

# 3. System Context

## Purpose

Provides high-level information about the software system.

Example:

``` json
{
  "system_name": "SampleApplication",
  "language": "Swift",
  "architecture_style": [
    "MVVM",
    "Clean Architecture"
  ],
  "frameworks": [
    "SwiftUI",
    "XCTest"
  ]
}
```

## Information Provided

-   Application type
-   Programming language
-   Architectural styles
-   Main frameworks
-   Testing frameworks

------------------------------------------------------------------------

# 4. Module Context

## Purpose

Represents logical boundaries and responsibilities of system modules.

Example:

``` json
{
  "module": "Authentication",
  "responsibility": "User authentication flow",
  "layer": "Feature",
  "dependencies": [
    "Domain",
    "Network"
  ]
}
```

## Information Provided

-   Module name
-   Module responsibility
-   Architectural layer
-   Dependencies with other modules

## Why It Matters

The LLM can understand whether a component belongs to:

-   Feature layer
-   Domain layer
-   Data layer
-   Infrastructure layer

------------------------------------------------------------------------

# 5. Component Context

## Purpose

Defines the role of individual software components.

Example:

``` json
{
  "name": "LoginViewModel",
  "type": "ViewModel",
  "architecture_role": "Presentation Layer",
  "responsibility": [
    "Validate user input",
    "Trigger authentication flow"
  ]
}
```

## Information Provided

-   Component name
-   Component type
-   Architectural responsibility
-   Business responsibility

------------------------------------------------------------------------

# 6. Dependency Context

## Purpose

Represents relationships between components.

Example:

``` json
{
  "component": "LoginViewModel",
  "dependencies": [
    {
      "name": "LoginUseCase",
      "type": "Protocol",
      "injection": "Constructor Injection"
    }
  ]
}
```

## Importance for Test Generation

This helps LLMs understand:

-   Which dependencies should be mocked
-   Which components should be isolated
-   How dependency injection works

------------------------------------------------------------------------

# 7. Interface Context

## Purpose

Represents abstractions and contracts.

Example:

``` json
{
  "interface": "UserRepository",
  "type": "Protocol",
  "implementation": "DefaultUserRepository"
}
```

## Information Provided

-   Protocols
-   Interfaces
-   Implementations
-   Abstraction boundaries

## Testing Impact

The LLM can generate:

-   Mock implementations
-   Fake objects
-   Dependency substitutes

------------------------------------------------------------------------

# 8. Design Pattern Context

## Purpose

Provides information about used software patterns.

Example:

``` json
{
  "patterns": [
    {
      "name": "Repository Pattern",
      "purpose": "Abstract data access"
    },
    {
      "name": "Dependency Injection",
      "purpose": "Improve testability"
    }
  ]
}
```

## Supported Patterns

Examples:

-   MVVM
-   VIPER
-   Clean Architecture
-   TCA
-   Repository Pattern
-   Dependency Injection
-   Observer Pattern

------------------------------------------------------------------------

# 9. Data Flow Context

## Purpose

Represents how data moves through the application.

Example:

    View
     |
    ViewModel
     |
    UseCase
     |
    Repository
     |
    Network

JSON:

``` json
{
  "flow": [
    "LoginView",
    "LoginViewModel",
    "LoginUseCase",
    "AuthRepository"
  ]
}
```

## Testing Impact

Helps identify:

-   Correct testing boundaries
-   Expected interactions
-   Mock locations

------------------------------------------------------------------------

# 10. Concurrency Context

## Purpose

Represents asynchronous and concurrent behavior.

Example:

``` json
{
  "concurrency_model": "Swift Concurrency",
  "async_operations": [
    "fetchUser()"
  ],
  "actors": [
    "NetworkManager"
  ]
}
```

## Information Provided

-   async/await usage
-   Actors
-   Thread safety requirements
-   Concurrent workflows

------------------------------------------------------------------------

# 11. Testing Context

## Purpose

Defines existing testing strategy.

Example:

``` json
{
  "framework": "XCTest",
  "style": "Given-When-Then",
  "mock_strategy": "Protocol-based mocking"
}
```

## Information Provided

-   Testing framework
-   Test style
-   Mocking strategy
-   Existing conventions

------------------------------------------------------------------------

# 12. Complete Architecture Context Example

``` json
{
  "system": {
    "language": "Swift",
    "architecture": "Clean Architecture + MVVM"
  },

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
    "Dependency Injection",
    "Repository Pattern"
  ],

  "testing": {
    "framework": "XCTest",
    "mocking": "Protocol Mock"
  }
}
```

------------------------------------------------------------------------

# Research Contribution

The proposed Architecture Context Schema aims to bridge the gap between:

    Traditional LLM Test Generation

    Code Context
          |
          v
         LLM
          |
          v
     Generated Tests

and:

    Architecture-Aware Test Generation

    Source Code

    +

    Architecture Knowledge

    +

    Dependency Relationships

    +

    Design Patterns

          |
          v

         LLM

          |
          v

    High Quality Unit Tests

------------------------------------------------------------------------

# Future Work

Future versions of this schema can include:

-   Automatic architecture extraction from source code
-   Dependency graph generation
-   Static analysis integration
-   Repository-level context retrieval
-   Support for multiple programming ecosystems
