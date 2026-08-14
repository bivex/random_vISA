# Architecture & Domain-Driven Design (DDD) Guide

This document describes the architectural principles and design patterns used in **random_vISA**.

---

## 🏛 Hexagonal Architecture (Ports and Adapters)

The project strictly follows Hexagonal Architecture principles to isolate business logic from input triggers, code generators, parsers, and compilers:

```
                      +-------------------------------------------------+
                      |                  DOMAIN LAYER                   |
                      |                                                 |
[Inbound Adapters]    |  [Entities & Aggregates]                        |   [Outbound Adapters]
  - CLI (Rich/Arg)  -->    * VectorIsaSpec (Aggregate Root)             | --> - SailFileAdapter
  - Python API        |    * VectorInstruction (Aggregate)              |     - CppEmulatorEmitter
  - ANTLR4 Parser     |    * VectorConfig (Value Object)                |     - ClangCompilerRunner
                      |    * Sail AST Nodes                             |
                      |                                                 |
                      |  [Domain Services]                              |
                      |    * RandomVisaGeneratorService                 |
                      |                                                 |
                      |  [Inbound Ports]        [Outbound Ports]        |
                      |    * GenerateSpecPort     * SailSpecWriterPort  |
                      |    * EmitEmulatorPort     * CppCodeEmitterPort  |
                      |    * RunPipelinePort      * CompilerRunnerPort  |
                      |    * SailParserPort                             |
                      +-------------------------------------------------+
```

### 1. Domain Layer (`random_visa/domain/`)
- **No external framework dependencies**. Pure Python standard library & domain logic.
- **Model**:
  - `VectorIsaSpec`: Aggregate root encapsulating the complete ISA, register configuration, and instruction collision detection.
  - `VectorInstruction`: Aggregate root representing a single instruction with its encoding parameters (`funct6`, `funct3`, `opcode`), format, and synthesized Sail AST.
  - `VectorConfig`: Immutable Value Object enforcing powers-of-2 constraints on `VLEN`, `ELEN`, and register counts.
  - `SailAst`: Pure AST representing Sail formal language elements (`SailType`, `SailExpr`, `SailStmt`, `SailFunctionDef`).
- **Domain Services**:
  - `RandomVisaGeneratorService`: Handles non-colliding opcode allocation, diversified arithmetic/bitwise/mask operation selection, and AST synthesis.
- **Domain Events**:
  - `InstructionSynthesizedEvent`, `IsaSpecCompletedEvent`, `CppEmulatorEmittedEvent`.
- **Ports**:
  - Abstract interfaces decoupling core domain logic from I/O mechanisms.

### 2. Application Layer (`random_visa/application/`)
- Orchestrates use cases and maps DTOs to domain aggregates:
  - `GenerateRandomVisaUseCase`: Coordinates spec synthesis.
  - `EmitCppEmulatorUseCase`: Coordinates C++ generation.
  - `RunFullPipelineUseCase`: Complete workflow pipeline.

### 3. Adapters Layer (`random_visa/adapters/`)
- **Inbound Adapters (Driving)**:
  - `cli/main.py`: Command-line interface with Rich tables, colored terminal formatting, and error handling.
  - `parser/sail_antlr_adapter.py`: ANTLR4-based parser that translates `.sail` DSL into domain aggregates.
- **Outbound Adapters (Driven)**:
  - `sail/sail_file_adapter.py`: Serializes domain models into `.sail` formal specs.
  - `cpp_codegen/cpp_emitter_adapter.py`: Generates clean C++20 emulator headers, sources, and CMake files.
  - `compiler/clang_runner_adapter.py`: Invokes `clang++` / `g++` and executes the verification harness.
