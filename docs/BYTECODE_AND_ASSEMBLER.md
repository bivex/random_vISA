# Vector Assembly & Bytecode Execution Guide

This document explains the vector assembly syntax, 32-bit binary bytecode format (`.vbc`), the built-in Vector Assembler (`VectorAssemblerService`), and how to execute custom binary programs on synthesized C++ VCPUs.

---

## 🏗 1. Vector Assembly & Bytecode Workflow

```
+---------------------------+
|  Vector Assembly Source   |  e.g.  vmul_vv_5  v4, v2, v1
|       (program.asm)       |        vsll_vx_2  v5, v2, x1
+---------------------------+
              │
              ▼
+---------------------------+
|  VectorAssemblerService   |  Matches mnemonics against .sail specification
|    (Domain Assembler)     |  Encodes 32-bit RISC-V Vector instruction words
+---------------------------+
              │
              ▼
+---------------------------+
|   Binary Bytecode File    |  Little-Endian 32-bit packed words
|       (program.vbc)       |  +0x0000: 0x16208257 ...
+---------------------------+
              │
              ▼
+---------------------------+
|    C++ VCPU Emulator      |  Loads binary / hex words into memory
|   (visa_test_runner)      |  Executes instruction step-by-step with register dump
+---------------------------+
```

---

## ✍️ 2. Vector Assembly Language Syntax

The assembly syntax follows standard RISC-V Vector convention adapted for synthesized V-ISAs:

```asm
# Line comments start with '#' or '//'
# Format: <mnemonic> <destination>, <source2>, <source1_or_immediate>, [mask_option]

# Vector-Vector Arithmetic (OP_VV)
vmul_vv_5  v4, v2, v1          # v4[i] = v2[i] * v1[i]

# Vector-Scalar Arithmetic (OP_VX)
vsll_vx_2  v5, v2, x1          # v5[i] = v2[i] << (x1 & 31)

# Vector-Immediate Arithmetic (OP_VI)
vadd_vi_0  v3, v2, -4          # v3[i] = v2[i] + (-4)

# Unary / Mask Operations (OP_MVV)
vneg_m_0   v7, v6              # v7[i] = -v6[i]
vclz_m_4   v8, v2              # v8[i] = clz(v2[i])

# Masked execution (vm = 0, enabled only where v0[i] == 1)
vadd_vv_3  v6, v4, v5, v0.t    # Masked execution using v0 as mask register
```

### Operand Types:
- **`v0`..`v31`**: Vector registers (width = $VLEN$ bits).
- **`x0`..`x31`**: Scalar General-Purpose Registers (64-bit).
- **`simm5`**: 5-bit signed integer immediate in range $[-16, 15]$.
- **`v0.t` / `masked`**: Optional mask flag (sets `vm=0`). Default is unmasked (`vm=1`).

---

## 💾 3. Binary Bytecode Format (`.vbc` / `.bin`)

The bytecode file is a raw binary stream of **32-bit Little-Endian words**:

| Byte Offset | Field Range | Size | Description |
| :---: | :---: | :---: | :--- |
| `0x00 - 0x03` | Instruction 0 | 4 Bytes (32-bit LE) | Machine instruction word for `PC = 0x80000000` |
| `0x04 - 0x07` | Instruction 1 | 4 Bytes (32-bit LE) | Machine instruction word for `PC = 0x80000004` |
| `0x08 - 0x0B` | Instruction 2 | 4 Bytes (32-bit LE) | Machine instruction word for `PC = 0x80000008` |
| `+4 * N` | Instruction N | 4 Bytes (32-bit LE) | Machine instruction word for `PC = 0x80000000 + 4*N` |

---

## 🚀 4. Step-by-Step Practical Walkthrough

### Step 1: Synthesize a Target VCPU
```bash
python3 -m random_visa.adapters.inbound.cli.main pipeline \
  --name My_VCPU \
  -n 8 \
  --vlen 128 \
  --seed 123 \
  --out-dir my_vcpu_emu
```

### Step 2: Write Vector Assembly Program (`examples/sample_vector_program.asm`)
```asm
vmul_vv_5  v4, v2, v1
vsll_vx_2  v5, v2, x1
vadd_vv_3  v6, v4, v5
vneg_m_0   v7, v6
```

### Step 3: Assemble into Binary Bytecode
```bash
python3 -m random_visa.adapters.inbound.cli.main assemble \
  examples/sample_vector_program.asm \
  --spec my_vcpu_emu/my_vcpu.sail \
  -o program.vbc
```

### Step 4: Execute Bytecode on the C++ Emulator
```bash
python3 -m random_visa.adapters.inbound.cli.main exec-bytecode \
  program.vbc \
  --emu-dir my_vcpu_emu
```

### Or Execute Raw Hex Words Directly:
```bash
python3 -m random_visa.adapters.inbound.cli.main exec-bytecode \
  --emu-dir my_vcpu_emu \
  --hex 0x16208257 0x0A20C2D7 0x0E428357 0x026023D7
```
