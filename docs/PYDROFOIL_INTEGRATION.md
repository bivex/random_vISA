# Pydrofoil JIT Emulator Integration in random_vISA

## 1. Overview

[**Pydrofoil**](https://github.com/pydrofoil/pydrofoil) is a high-performance, JIT-accelerated instruction set emulator framework developed for RISC-V and ARM formal Sail models.

`random_vISA` now provides direct support for synthesizing and compiling any Sail V-ISA specification into a **Pydrofoil-compatible / RPython JIT vector emulator**.

---

## 2. Architecture & Emitted Modules

When `compile-pydrofoil` is executed, the `PydrofoilEmitterAdapter` generates a modular Python/RPython emulator package:

| File | Purpose |
| :--- | :--- |
| [`pydrofoil_state.py`](file:///Volumes/External/Code/random_vISA/generated_emulator/pydrofoil_emulator/pydrofoil_state.py) | Full architectural state: `v0..v31` vector registers, CSRs (`vl`, `vtype`, `vstart`), scalar `x0..x31`, and little-endian bitvector accessors. |
| [`pydrofoil_decoder.py`](file:///Volumes/External/Code/random_vISA/generated_emulator/pydrofoil_emulator/pydrofoil_decoder.py) | 32-bit RISC-V Vector bitfield decoder (`funct6`, `vm`, `vs2`, `vs1_or_imm`, `funct3`, `vd`, `opcode`). |
| [`pydrofoil_instructions.py`](file:///Volumes/External/Code/random_vISA/generated_emulator/pydrofoil_emulator/pydrofoil_instructions.py) | JIT-friendly semantic execution functions with saturation handling and unmasked fast paths. |
| [`pydrofoil_emulator.py`](file:///Volumes/External/Code/random_vISA/generated_emulator/pydrofoil_emulator/pydrofoil_emulator.py) | Stepping engine and bytecode stream loader. |
| [`pydrofoil_main.py`](file:///Volumes/External/Code/random_vISA/generated_emulator/pydrofoil_emulator/pydrofoil_main.py) | Standalone verification test harness (16/16 test vectors) and CLI bytecode executor (`--bin <file.vbc>`). |

---

## 3. Submodule & Internal Architecture (`third_party/pydrofoil`)

The official [**Pydrofoil**](https://github.com/pydrofoil/pydrofoil) codebase is included as a git submodule in:
[`third_party/pydrofoil/`](file:///Volumes/External/Code/random_vISA/third_party/pydrofoil)

### Key Submodule Components:
1. **`pydrofoil/parse.py`**:
   - Parses Sail Jib IR (`.ir` 3-address code text format) into internal AST nodes (`ast.Definition`, `ast.Function`, `ast.Instruction`).
2. **`pydrofoil/makecode.py` (`parse_and_make_code`)**:
   - Specializes, inlines, and compiles Jib IR into RPython/Python AST with SSA representation.
3. **`pydrofoil/bitvector.py`**:
   - Highly optimized bitvector operations (`SmallBitVector`, `BigBitVector`).
4. **`riscv/`**:
   - Pre-generated RISC-V Sail IR models (`riscv_model_RV32.ir`, `riscv_model_RV64.ir`) and support library (`supportcoderiscv.py`).

---

## 4. Dual-Mode Execution Model in `random_vISA`

Because the full RPython meta-tracing JIT framework is based on the PyPy2/RPython bootstrap toolchain, `random_vISA` provides a **Dual-Mode** architecture:

```
                          ┌───────────────────────────┐
                          │   Sail V-ISA Specification │
                          │     (hypervector_isa.sail)│
                          └─────────────┬─────────────┘
                                        │
                         random_vISA ANTLR4 Parser & Jib IR
                                        │
                  ┌─────────────────────┴─────────────────────┐
                  ▼                                           ▼
      [Mode 1: Python 3 JIT-Ready]                 [Mode 2: PyPy2 / RPython JIT]
        (PydrofoilEmitterAdapter)                    (third_party/pydrofoil)
                  │                                           │
  • Zero external dependencies               • Uses pydrofoil.makecode.parse_and_make_code
  • Standalone v0..v31 bitvector engine       • Generates C binary with tracing JIT
  • Runs anywhere on modern Python 3.9+       • Requires PyPy2 + RPython toolchain
  • 16/16 instruction verification suite      • Ideal for maximum production throughput
```

---

## 5. CLI Usage

### 5.1. Compile Sail to Pydrofoil Emulator & Run Verification (Mode 1)
```bash
python3 -m random_visa.adapters.inbound.cli.main compile-pydrofoil \
  generated_emulator/hypervector_isa.sail \
  -o generated_emulator/pydrofoil_emulator
```

### 5.2. Run Bytecode Program on Pydrofoil Emulator
```bash
python3 generated_emulator/pydrofoil_emulator/pydrofoil_main.py \
  --bin generated_emulator/program.vbc
```

---

## 6. Multi-VLEN Support

The Pydrofoil generator adapts seamlessly across vector register lengths:
- **`VLEN = 64`** (2 $\times$ 32-bit elements / register)
- **`VLEN = 128`** (4 $\times$ 32-bit elements / register)
- **`VLEN = 256`** (8 $\times$ 32-bit elements / register)
- **`VLEN = 512`** (16 $\times$ 32-bit elements / register)
