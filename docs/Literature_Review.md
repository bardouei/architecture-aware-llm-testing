# Literature Review

## Architecture-Aware Context Engineering for LLM-Based Unit Test Generation in Modular Software Systems

This document summarizes the key research papers that define the current
state of the art related to: - LLM-based unit test generation - Context
engineering for software engineering tasks - Repository-level code
understanding - Software architecture awareness - Test quality
evaluation

  --------------------------------------------------------------------------------------------------------------------------------------
  Paper              Year     Problem          Input           Method             Output             Evaluation     Limitation /
                                                                                                                    Research Gap
  ------------------ -------- ---------------- --------------- ------------------ ------------------ -------------- --------------------
  TestPilot: An      2023     Manual unit test Source code,    Uses LLMs to       Automated unit     Coverage       Focuses mainly on
  Empirical                   creation is      API             generate and       tests              metrics,       function/API level.
  Evaluation of               expensive and    information,    repair unit tests                     generated test Does not model
  Using Large                 time-consuming   documentation                                         execution      software
  Language Models                              examples                                                             architecture, module
  for Automated Unit                                                                                                boundaries, or
  Test Generation                                                                                                   dependency
                                                                                                                    relationships

  ChatUniTest: A     2023     LLM-generated    Source code     Context selection, Unit tests         Compilation    Uses code-level
  Framework for               tests often fail with adaptive   test generation,                      success,       context but lacks
  LLM-Based Test              compilation or   focal context   validation, and                       coverage       explicit
  Generation                  have low quality                 repair loop                           comparison     architecture
                                                                                                                    awareness

  MuTAP: Effective   2024     Code coverage    Program under   Uses mutation      Higher quality     Mutation       Improves quality
  Test Generation             alone is         test, generated testing feedback   unit tests         score, fault   evaluation but does
  Using Pre-trained           insufficient for tests, mutation to improve                            detection      not consider
  Large Language              evaluating test  information     generated tests                       capability     architecture context
  Models and                  quality                                                                               
  Mutation Testing                                                                                                  

  SWE-bench: Can     2023     LLM evaluation   Full            Repository-level   Code patches       Real GitHub    Focuses on bug
  Language Models             on isolated      repositories    problem solving                       issue          fixing rather than
  Resolve Real-World          files does not   and issue       using LLMs                            resolution     unit test
  GitHub Issues?              represent real   descriptions                                          rate           generation, but
                              software                                                                              highlights the
                              development                                                                           importance of
                                                                                                                    repository
                                                                                                                    understanding

  RepoCoder:         2023     LLMs struggle    Repository      Retrieval-based    Repository-level   Repository     Uses repository
  Repository-Level            when required    files           context selection  code completion    benchmarks     context but does not
  Code Completion             context exists                   combined with                                        explicitly represent
  Through Iterative           across many                      generation                                           software
  Retrieval and               files                                                                                 architecture
  Generation                                                                                                        

  RepoBench:         2023     Existing         Large           Repository-level   Generated code     Exact match    Does not include
  Benchmarking                benchmarks do    repositories    benchmarking                          and code       architecture-level
  Repository-Level            not evaluate                     methodology                           generation     understanding
  Code                        large project                                                          metrics        
  Auto-Completion             understanding                                                                         
  Systems                                                                                                           

  GraphCodeBERT:     2020     Source code      Code and data   Graph-based code   Improved code      Code           Not designed for LLM
  Pre-training Code           contains         flow            representation     representations    intelligence   test generation, but
  Representations             structural       information     learning                              benchmarks     demonstrates the
  with Data Flow              relationships                                                                         importance of
                              beyond plain                                                                          structural context
                              text                                                                                  

  CodeT5+: Open Code 2023     General language Code and        Code-specific      Code understanding Multiple code  Does not incorporate
  Large Language              models have      natural         pretraining and    and generation     benchmarks     software
  Models for Code             limited code     language        generation         tasks                             architecture
  Understanding and           understanding    descriptions                                                         knowledge
  Generation                                                                                                        

  SWE-agent:         2024     LLMs need tools  Repository,     Agent-based        Code modifications SWE-bench      Focuses on
  Agent-Computer              and interaction  issue           software                              evaluation     autonomous agents
  Interfaces Enable           capabilities for description,    engineering                                          rather than
  Automated Software          complex software development     workflow                                             architecture-aware
  Engineering                 tasks            tools                                                                test generation

  Context Matters:   2026     LLM test         Structured      Improved context   More reliable      Reliability    Shows the importance
  Improving                   generation       project context selection and      generated tests    and test       of context but does
  Practical                   reliability                      grounding                             quality        not fully explore
  Reliability of              decreases in                     strategies                            metrics        explicit
  LLM-Based Unit              real-world                                                                            architecture
  Test Generation             projects without                                                                      representations
                              proper context                                                                        
  --------------------------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# Research Gap Identified

Based on the reviewed literature, existing approaches mainly improve
LLM-based unit test generation through:

-   Better prompts
-   Retrieval mechanisms
-   Source-code context
-   Program analysis
-   Feedback loops

However, limited research investigates explicit software architecture
context as an input for LLM-based test generation.

The missing research direction is:

    Software Architecture Knowledge
            +
    Context Engineering
            +
    Large Language Models
            +
    Unit Test Generation

The proposed research aims to investigate whether architecture-aware
context, including:

-   module boundaries
-   dependency relationships
-   component responsibilities
-   interfaces
-   design patterns

can improve generated unit test quality in modular software systems.

------------------------------------------------------------------------

# Future Literature Expansion

The final literature review will expand this matrix to approximately 50
papers covering:

1.  LLM-based software testing
2.  Context engineering and retrieval
3.  Software architecture recovery
4.  Modular software systems
5.  Test quality evaluation
6.  Mobile and Swift software ecosystems
