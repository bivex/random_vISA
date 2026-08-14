# Pure C11 Vector Emulator & Official C ANTLR4 Parser

This document describes the architecture of the **Pure C11 / C99 Vector ISA Emulator** code generator and the official **ISO C ANTLR4 Parser** implementation.

---

## 🏛 1. High-Performance C11 Architecture

The pure C11 emulator generator eliminates modern C++ abstraction overhead by utilizing:
1. **$O(1)$ Direct Dispatch Table**: `visa_instruction_handler_t dispatch_table[64][8]` directly maps `(funct6, funct3)` to the execution handler without chained `switch` statements.
2. **64-Byte Cacheline Alignment (`_Alignas(64)`)**: Vector registers are explicitly aligned to 64-byte boundaries for maximum SIMD memory bandwidth.
3. **Loop Unswitching & Vectorization Pragmas**: Separates unmasked fast-paths (`inst->vm == 1`) with `#pragma clang loop vectorize(enable)` from masked paths.
4. **Direct Pointer Arithmetic**: Uses typed raw pointers (`int32_t* vd_ptr`) instead of `memcpy` and per-element bounds checking.

---

## 📦 2. Generated C11 Project Files Matrix

| File Name | Standard | Compiler Flags | Key Symbols | Responsibility |
| :--- | :---: | :--- | :--- | :--- |
| **`visa_emulator.h`** | ISO C11 | `-std=c11 -O3 -Wall` | `CSRState`, `VRegFile`, `EmulatorState`, `DecodedInstruction` | Architectural register structures, type definitions, and public API |
| **`visa_instructions.c`** | ISO C11 | `-std=c11 -O3` | `exec_<mnemonic>`, `dispatch_table[64][8]`, `visa_execute` | Static instruction execution functions, dispatch table, and UB-safe arithmetic |
| **`visa_emulator.c`** | ISO C11 | `-std=c11 -O3` | `visa_step`, `visa_decode`, `visa_dump_vregs`, `visa_run_program` | Bitfield instruction decoder and program execution loop |
| **`visa_main.c`** | ISO C11 | `-std=c11 -O3` | `main`, `run_bytecode_file` | Standalone verification test harness and bytecode runner |
| **`Makefile`** | GNU Make | `CC=clang` | `visa_c_runner` | Build automation targets |

---

## 🔍 3. ISO C ANTLR4 Parser (`C.g4`)

The project embeds the complete standard ISO C11 / C99 grammar:
- **Grammar File**: [`random_visa/adapters/inbound/parser/antlr/C.g4`](file:///Volumes/External/Code/random_vISA/random_visa/adapters/inbound/parser/antlr/C.g4)
- **Parser Adapter**: [`random_visa/adapters/inbound/parser/c_antlr_adapter.py`](file:///Volumes/External/Code/random_vISA/random_visa/adapters/inbound/parser/c_antlr_adapter.py)

### Supported C Constructs:
- `typedef`, `struct`, `union`, `enum` declarations.
- Function definitions with parameter type lists and compound statements.
- Preprocessor directives and attribute specifiers (`__attribute__`, `_Alignas`, `_Atomic`).
- Control flow (`if`, `switch`, `for`, `while`, `goto`).

---

## 🚀 4. CLI Usage Examples

### Compile a Sail Specification into Pure C11:
```bash
python3 -m random_visa.adapters.inbound.cli.main compile-c \
  my_spec.sail \
  -o c_emulator
```

### Parse and Inspect any C Source File with ANTLR4:
```python
from random_visa.adapters.inbound.parser.c_antlr_adapter import AntlrCParserAdapter

res = AntlrCParserAdapter.parse_c_file("c_emulator/visa_emulator.c")
print("Functions parsed:", res["functions"])
print("Structs parsed:", res["structs"])
```
