# Domain Model Specification

This document formally specifies the Domain Entities, Value Objects, Aggregates, Invariants, and Lifecycle Events in **random_vISA**.

---

## 📐 Domain Entity-Relationship Overview

```mermaid
classDiagram
    class VectorIsaSpec {
        +String name
        +String version
        +VectorConfig config
        +List~VectorInstruction~ instructions
        +add_instruction(inst: VectorInstruction)
        +get_by_mnemonic(mnemonic: String)
        +decode(word: uint32) VectorInstruction
        +to_sail_specification() String
    }

    class VectorInstruction {
        +String mnemonic
        +InstructionFormat format
        +int funct6
        +int funct3
        +int opcode
        +BinaryOp binary_op
        +UnaryOp unary_op
        +ElementKind element_kind
        +SailFunctionDef sail_function
        +encode(vd, vs2, vs1, vm) uint32
    }

    class VectorConfig {
        +int vlen
        +int elen
        +SEW default_sew
        +LMUL default_lmul
        +TailPolicy tail_policy
        +MaskPolicy mask_policy
        +int num_vregs
        +calculate_vlmax(sew, lmul) int
    }

    class SailFunctionDef {
        +String name
        +List params
        +SailType return_type
        +List~SailStmt~ body
        +to_sail() String
    }

    VectorIsaSpec *-- VectorConfig : contains
    VectorIsaSpec o-- VectorInstruction : manages
    VectorInstruction *-- SailFunctionDef : defines
```

---

## 🔒 Domain Invariants & Constraints

1. **`VectorConfig` Invariants**:
   - `vlen > 0` and must be a power of 2: $vlen \in \{2^k \mid k \ge 6\}$.
   - `elen <= vlen`.
   - `num_vregs >= 8` and must be a power of 2: $num\_vregs \in \{8, 16, 32, 64, 128\}$.
   - `calculate_vlmax(sew, lmul) = (vlen / sew.value) * lmul.multiplier_val`.

2. **`VectorIsaSpec` Invariants**:
   - **No Encoding Collisions**: No two instructions may share the same triplet `(opcode, funct3, funct6)`.
   - **No Mnemonic Duplicates**: Every instruction in the aggregate must have a unique identifier string.

3. **`VectorInstruction` Invariants**:
   - `0 <= funct6 <= 63` (6-bit field).
   - `0 <= funct3 <= 7` (3-bit field).
   - `opcode == 0x57` (standard RISC-V vector opcode).
   - Encoding packing formula:
     $$\text{word} = (\text{funct6} \ll 26) \mid (\text{vm} \ll 25) \mid (\text{vs2} \ll 20) \mid (\text{vs1\_or\_rs1\_or\_imm} \ll 15) \mid (\text{funct3} \ll 12) \mid (\text{vd} \ll 7) \mid \text{opcode}$$

---

## 📣 Domain Events

- **`InstructionSynthesizedEvent`**: Emitted when a new valid instruction with verified encoding is generated.
- **`IsaSpecCompletedEvent`**: Emitted when an entire Vector ISA specification aggregate finishes synthesis.
- **`CppEmulatorEmittedEvent`**: Emitted when C++ emulator sources are successfully written to destination.
