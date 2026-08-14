# Architecture & Domain-Driven Design (DDD) Guide

This document describes the architectural principles, layers, component boundaries, and design patterns used in **random_vISA**.

---

## 🏛 1. Hexagonal Architecture (Ports and Adapters) Overview

The project strictly follows Hexagonal Architecture principles to isolate core domain logic from input triggers, code generators, ANTLR4 parsers, and C++ compilers:

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

---

## 📦 2. Architectural Layers & Responsibilities Matrix

| Layer | Package Path | External Dependencies | Core Responsibility |
| :--- | :--- | :--- | :--- |
| **Domain Layer** | `random_visa.domain` | **None** (Pure Python standard library) | Encapsulates all domain entities, value objects, aggregates, invariants, events, and port interfaces |
| **Application Layer** | `random_visa.application` | Domain Layer | Coordinates use cases, orchestrates ports, handles DTO transformations, and executes business workflows |
| **Inbound Adapters** | `random_visa.adapters.inbound` | Application, Domain, `rich`, `antlr4` | Translates external input (CLI parameters, `.sail` file streams) into application use-case calls |
| **Outbound Adapters**| `random_visa.adapters.outbound`| Domain, `jinja2`, `subprocess` | Implements driven SPI ports: generates `.sail` files, renders C++ templates, and invokes compilers |

---

## 🔌 3. Ports & Adapters Mapping Matrix

| Port Name | Port Direction | Defined In | Implemented By (Adapter) | Primary Function |
| :--- | :---: | :--- | :--- | :--- |
| **`GenerateSpecPort`** | Inbound (Driving) | `domain.ports.inbound` | `GenerateRandomVisaUseCase` | Synthesizes randomized Vector ISA specifications |
| **`EmitEmulatorPort`** | Inbound (Driving) | `domain.ports.inbound` | `EmitCppEmulatorUseCase` | Emits C++ emulator source code for an ISA spec |
| **`RunPipelinePort`** | Inbound (Driving) | `domain.ports.inbound` | `RunFullPipelineUseCase` | Orchestrates complete synthesis, export, code generation, and test execution |
| **`SailParserPort`** | Inbound (Driving) | `domain.ports.inbound` | `AntlrSailParserAdapter` | Parses `.sail` source code via ANTLR4 into domain aggregates |
| **`SailSpecWriterPort`** | Outbound (Driven) | `domain.ports.outbound` | `SailFileAdapter` | Formats and writes domain `VectorIsaSpec` to `.sail` files |
| **`CppCodeEmitterPort`** | Outbound (Driven) | `domain.ports.outbound` | `CppEmulatorEmitterAdapter` | Generates standalone C++20 emulator headers, sources, and CMake files |
| **`CompilerRunnerPort`** | Outbound (Driven) | `domain.ports.outbound` | `ClangCompilerRunnerAdapter` | Compiles C++ emulator with `clang++` and executes test verification |

---

## 🧩 4. Domain Entities, Aggregates & Value Objects Matrix

| Component Name | Domain Classification | Location | Invariants / Validation Rules | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **`VectorIsaSpec`** | Aggregate Root | `domain.model.isa_spec` | No encoding slot collision `(funct6, funct3, opcode)`, unique mnemonics | Root entity managing the full vector architecture, register definitions, and instruction list |
| **`VectorInstruction`**| Entity / Aggregate | `domain.model.instruction` | Valid 6-bit `funct6`, 3-bit `funct3`, 7-bit opcode `0x57`, sound Sail AST | Encapsulates instruction format, encoding fields, operation semantics, and formal Sail function |
| **`VectorConfig`** | Value Object (Immutable) | `domain.model.vector_config`| `vlen` power-of-2 $\ge 64$, `elen <= vlen`, `num_vregs` power-of-2 $\ge 8$ | Represents immutable hardware parameters of the vector execution pipeline |
| **`SailAST` Nodes** | Value Objects | `domain.model.sail_ast` | Well-typed expressions, valid statement trees, parameter bindings | Pure AST modeling Sail types, expressions, vector loops, and let-bindings |
