# Random Sail (V-ISA) -> C++ Emulator Generator

A synthesizer for randomized RISC-V Vector Extensions / Vector ISAs (V-ISA) specified in the formal **Sail** specification language with automatic code generation of high-performance **C++20 emulators**, built using **Hexagonal Architecture (Ports & Adapters)** and **Domain-Driven Design (DDD)** principles.

---

## 📚 Documentation

- [🏛 Architecture & DDD Design](docs/ARCHITECTURE.md) — In-depth breakdown of Domain, Application Use Cases, Ports, and Adapters.
- [💾 Vector Assembly & Bytecode Execution](docs/BYTECODE_AND_ASSEMBLER.md) — Assembly syntax, `.vbc` bytecode format, assembler service, and live VCPU execution.
- [🎯 Sail Jib IR Specification & Grammar](docs/JIB_IR_SPECIFICATION.md) — 3-Address Code IR, types, instructions, and ANTLR4 parser.
- [⛵ Sail Specification & ANTLR4 Grammar](docs/SAIL_SPECIFICATION.md) — Sail language syntax, AST model, and ANTLR4 parser integration.
- [⚡ C++20 Emulator Architecture](docs/CPP_EMULATOR.md) — Register file (`v0-v31`), bitfield decoder, and Undefined Behavior (UB) safety mechanisms.
- [🔧 CLI Reference Guide](docs/CLI_REFERENCE.md) — Detailed options and examples for `pipeline`, `synthesize`, `parse`, `assemble`, and `exec-bytecode`.
- [🌌 VCPU Theoretical Limits](docs/VCPU_THEORETICAL_LIMITS.md) — Combinatorial capacity ($> 10^{56}$ VCPUs), instruction encoding space, and throughput.
- [📐 Domain Model Specification](docs/DOMAIN_MODEL_SPEC.md) — Class diagram, Value Object invariants, and aggregate lifecycles.
- [🧪 Development & Testing Guide](docs/DEVELOPMENT_AND_TESTING.md) — Pytest suite, extending instructions, modifying ANTLR4 grammar, and contributing.

---

## 🏛 Project Architecture (Hexagonal + DDD)

```
random_visa/
├── domain/                         # DOMAIN LAYER (Pure business logic, zero framework dependencies)
│   ├── model/                      # Entities, Value Objects, Aggregates
│   │   ├── types.py                # SEW, LMUL, ElementKind, BinaryOp, UnaryOp, InstructionFormat
│   │   ├── vector_config.py        # VectorConfig (VLEN, ELEN, max_vl, tail/mask policies)
│   │   ├── sail_ast.py             # Sail AST (SailType, SailExpr, SailStmt, SailFunctionDef)
│   │   ├── instruction.py          # VectorInstruction Aggregate Root
│   │   └── isa_spec.py             # VectorIsaSpec Aggregate Root
│   ├── services/                   # Domain Services
│   │   └── random_generator.py     # Randomized non-colliding V-ISA synthesizer
│   ├── events/                     # Domain Events
│   │   └── events.py               # InstructionSynthesizedEvent, IsaSpecCompletedEvent
│   └── ports/                      # Ports (Decoupled interfaces)
│       ├── inbound/                # Driving Ports (Use Cases)
│       │   └── ports.py            # GenerateSpecPort, EmitEmulatorPort, RunPipelinePort, SailParserPort
│       └── outbound/               # Driven Ports (SPI / Infrastructure)
│           └── ports.py            # SailSpecWriterPort, CppCodeEmitterPort, CompilerRunnerPort
│
├── application/                    # APPLICATION LAYER (Orchestration & Use Cases)
│   ├── dtos.py                     # Request / Response DTOs
│   └── use_cases/                  # Use Case Implementations
│       └── pipeline.py             # GenerateRandomVisaUseCase, EmitCppEmulatorUseCase, RunFullPipelineUseCase
│
├── adapters/                       # ADAPTERS LAYER (Port Implementations)
│   ├── inbound/                    # Driving Adapters
│   │   ├── cli/main.py             # Rich & Argparse CLI Interface
│   │   └── parser/                 # ANTLR4 Sail Parser Adapter
│   │       ├── antlr/Sail.g4
│   │       └── sail_antlr_adapter.py
│   └── outbound/                   # Driven Adapters
│       ├── sail/                   # Sail Specification File Writer (.sail)
│       │   └── sail_file_adapter.py
│       ├── cpp_codegen/            # C++20 Emulator Project Code Generator (Jinja2)
│       │   └── cpp_emitter_adapter.py
│       └── compiler/               # Clang++/GCC Compiler and Verification Test Runner
│           └── clang_runner_adapter.py
│
└── tests/                          # Unit and Integration Test Suite
    ├── unit/
    └── integration/
```

---

## 🚀 Quick Start

### 1. Run the Full End-to-End Pipeline
Synthesize a random 12-instruction vector ISA, export `.sail` file, generate a standalone C++20 emulator, compile with `clang++`, and verify:

```bash
python3 -m random_visa.adapters.inbound.cli.main pipeline \
  --name RVV_Custom_ISA \
  --num-insts 12 \
  --vlen 128 \
  --seed 42 \
  --out-dir generated_emulator
```

### 2. Parse any `.sail` File via ANTLR4
Parse a Sail formal specification file into the domain model and inspect instruction encodings:

```bash
python3 -m random_visa.adapters.inbound.cli.main parse generated_emulator/rvv_custom_isa.sail
```

### 3. Direct Translation: Sail -> C++20 Emulator
Compile an existing `.sail` file into a C++20 emulator project and execute the verification suite:

```bash
python3 -m random_visa.adapters.inbound.cli.main compile-sail \
  generated_emulator/rvv_custom_isa.sail \
  --out-dir parsed_cpp_emulator
```

### 4. Assemble Vector Assembly into Binary Bytecode (`.vbc`)
Assemble a text assembly file into a 32-bit machine word binary file:

```bash
python3 -m random_visa.adapters.inbound.cli.main assemble \
  examples/sample_vector_program.asm \
  --spec generated_emulator/rvv_custom_isa.sail \
  -o program.vbc
```

### 5. Execute Custom Bytecode on the C++ VCPU Emulator
Run the assembled binary bytecode on the C++ emulator and inspect vector register writebacks:

```bash
python3 -m random_visa.adapters.inbound.cli.main exec-bytecode \
  program.vbc \
  --emu-dir generated_emulator
```

### 6. Run Test Suite
```bash
python3 -m pytest -v
```

---

## 🧩 Generated C++ Emulator Components

The generated emulator project contains:
- `isa_state.hpp`: Vector register file (`v0`..`v31` configurable by `VLEN`), scalar registers (`x0`..`x31`), CSR state (`vl`, `vtype`, `vstart`, `vxrm`).
- `decoder.hpp`: Bitfield table & mask decoder matching 32-bit words to `(opcode, funct3, funct6)`.
- `instructions.hpp` / `instructions.cpp`: Vector execution loops, masking checks (`vm`, `v0`), and UB-safe arithmetic.
- `emulator.hpp`: Vector emulator execution engine (`step()`, `run_program()`).
- `main.cpp`: Standalone verification test harness running synthesized instructions on test vectors.
- `CMakeLists.txt`: Standard CMake build file.
