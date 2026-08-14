# Generated C++20 Emulator Architecture

This document describes the internal structure, memory layout, register state, bitfield decoding, and execution model of the auto-generated C++20 Vector ISA emulator.

---

## 🏗 1. Generated Project Files & Responsibilities Matrix

| File Name | Language / Standard | Dependencies | Key Classes / Structs | Architectural Responsibility |
| :--- | :---: | :--- | :--- | :--- |
| **`isa_state.hpp`** | C++20 | `<cstdint>`, `<array>`, `<cstring>`, `<iostream>` | `CSRState`, `VRegFile`, `EmulatorState` | Manages vector register array `v0..v31`, scalar `x0..x31`, CSR registers (`vl`, `vtype`), element typecast get/set accessors, and vector mask bit inspection |
| **`decoder.hpp`** | C++20 | `<cstdint>`, `<string_view>`, `<optional>` | `InstId`, `DecodedInstruction`, `Decoder` | Fast table and bitmask decoding of 32-bit words into structured opcode fields (`funct6`, `funct3`, `vd`, `vs2`, `vs1`, `imm`, `vm`) |
| **`instructions.hpp`** | C++20 | `"isa_state.hpp"`, `"decoder.hpp"` | `InstructionExecutor` | Static class declaring the master `execute()` dispatch method and private handlers `exec_<mnemonic>()` |
| **`instructions.cpp`** | C++20 | `"instructions.hpp"`, `<algorithm>` | `InstructionExecutor` implementation | Vector execution loops over `0 <= i < vl`, mask checks, and UB-safe arithmetic implementations |
| **`emulator.hpp`** | C++20 | `"instructions.hpp"`, `<vector>` | `VectorEmulator` | Main high-level emulator engine providing `reset()`, `step(uint32_t)`, and batch `run_program()` execution |
| **`main.cpp`** | C++20 | `"emulator.hpp"` | `main()` verification harness | Test fixture initializing source registers (`v1`, `v2`, `x1`), executing encoded test words, and verifying output vectors |
| **`CMakeLists.txt`** | CMake $\ge$ 3.16 | C++20 Compiler (Clang/GCC) | Target `visa_test_runner` | Build automation with `-O3 -Wall -Wextra` optimization flags |

---

## 🗄 2. Emulator State & Vector Register Layout Matrix

| Register Group | Count | Size per Register | Total Memory Layout | Accessor Method | Description |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **Vector Registers (`v0..v31`)** | 32 | `VLEN / 8` bytes (16 B @ 128b, 64 B @ 512b) | `std::array<std::array<uint8_t, VLEN_BYTES>, 32>` | `get_elem<T>(reg, idx)`, `set_elem<T>(reg, idx, val)` | General-purpose vector register file with byte-level precision |
| **Scalar Registers (`x0..x31`)** | 32 | 64 bits (8 bytes) | `std::array<uint64_t, 32>` | `get_xreg(idx)`, `set_xreg(idx, val)` | General-purpose integer scalar registers (`x0` hardwired to 0) |
| **Vector Length (`vl`)** | 1 | 64 bits | Part of `CSRState` | `state.csr.vl` | Number of active elements processed by each vector instruction |
| **Vector Type (`vtype`)** | 1 | 64 bits | Part of `CSRState` | `state.csr.vtype` | Encodes selected element width (`SEW`), multiplier (`LMUL`), and policies |
| **Vector Start (`vstart`)** | 1 | 64 bits | Part of `CSRState` | `state.csr.vstart` | Specifies the element index from which a vector instruction starts execution |
| **Rounding Mode (`vxrm`)** | 1 | 64 bits | Part of `CSRState` | `state.csr.vxrm` | Fixed-point rounding mode |
| **Saturation Flag (`vxsat`)** | 1 | 64 bits | Part of `CSRState` | `state.csr.vxsat` | Sticky bit set when any saturating instruction overflows/clamps |
| **Program Counter (`pc`)** | 1 | 64 bits | Part of `CSRState` | `state.csr.pc` | Current execution instruction address (starts at `0x80000000`) |

---

## 🔍 3. Instruction Word Bitfield Decoding Matrix

| Field | Bit Range | Width | Mask / Shift Formula | Field Type | Target in `DecodedInstruction` |
| :--- | :---: | :---: | :--- | :--- | :--- |
| **`opcode`** | `[6:0]` | 7 bits | `word & 0x7F` | Unsigned | `dec.opcode` (Fixed to `0x57`) |
| **`vd`** | `[11:7]` | 5 bits | `(word >> 7) & 0x1F` | Unsigned | `dec.vd` (Destination vector register index $0\dots 31$) |
| **`funct3`** | `[14:12]` | 3 bits | `(word >> 12) & 0x7` | Unsigned | `dec.funct3` (Format discriminator $0\dots 7$) |
| **`vs1 / rs1`** | `[19:15]` | 5 bits | `(word >> 15) & 0x1F` | Unsigned | `dec.vs1`, `dec.rs1` (Source vector or scalar register index) |
| **`imm`** | `[19:15]` | 5 bits | `sign_extend_5((word >> 15) & 0x1F)` | Signed 8-bit | `dec.imm` (Sign-extended immediate value in $[-16, 15]$) |
| **`vs2`** | `[24:20]` | 5 bits | `(word >> 20) & 0x1F` | Unsigned | `dec.vs2` (Source vector register index 2) |
| **`vm`** | `[25]` | 1 bit | `(word >> 25) & 0x1` | Flag | `dec.vm` (`1` = unmasked, `0` = masked by `v0`) |
| **`funct6`** | `[31:26]` | 6 bits | `(word >> 26) & 0x3F` | Unsigned | `dec.funct6` (Operation code $0\dots 63$) |

---

## ⚡ 4. Arithmetic Safety & UB Prevention Matrix

| Hazard / Undefined Behavior | Standard C++ Risk | RISC-V Specification Mandate | C++20 Emulator Implementation Guard |
| :--- | :--- | :--- | :--- |
| **Division by Zero (`/ 0`)** | `SIGFPE` hardware exception / crash | Returns all-ones (`-1` for signed `int32_t`) | `if (op1 == 0) result = -1; else result = op2 / op1;` |
| **Remainder by Zero (`% 0`)** | `SIGFPE` hardware exception / crash | Returns the dividend `op2` | `if (op1 == 0) result = op2; else result = op2 % op1;` |
| **Signed Division Overflow (`INT32_MIN / -1`)** | `SIGFPE` on x86/ARM hardware | Returns `INT32_MIN` without trapping | `if (op2 == INT32_MIN && op1 == -1) result = INT32_MIN;` |
| **Signed Remainder Overflow (`INT32_MIN % -1`)** | `SIGFPE` on x86/ARM hardware | Returns `0` | `if (op2 == INT32_MIN && op1 == -1) result = 0;` |
| **Signed Integer Overflow (`+`, `-`, `*`)** | Undefined Behavior (UB) in C++ standard | Two's complement wrapping modulo $2^{32}$ | `static_cast<elem_t>(static_cast<uint32_t>(op2) + (uint32_t)op1)` |
| **Shift Count Out of Range (`<< 32`, `<< -1`)** | Undefined Behavior / CPU-dependent | Mask shift count to lowest 5 bits ($[0, 31]$) | `static_cast<elem_t>(static_cast<uint32_t>(op2) << (op1 & 31u))` |
| **Absolute Value of Minimum (`std::abs(INT32_MIN)`)** | Undefined Behavior in `std::abs` | Returns `INT32_MIN` | `(op2 == INT32_MIN) ? INT32_MIN : ((op2 < 0) ? -op2 : op2)` |
| **Count Leading/Trailing Zeros on Zero Input** | `__builtin_clz(0)` is undefined | Returns element bitwidth (32) | `(op2 == 0) ? 32 : __builtin_clz((uint32_t)op2)` |
| **Fixed-Point Saturation (`+_sat`, `-_sat`)** | Integer overflow / wraparound | Clamps result to `[INT32_MIN, INT32_MAX]` | `std::clamp<int64_t>((int64_t)op2 + op1, INT32_MIN, INT32_MAX)` |

---

## 🚀 5. Manual Build & Execution Recipes

```bash
# Direct single-command compilation via Clang++
clang++ -std=c++20 -O3 -Wall -Wextra -I. main.cpp instructions.cpp -o visa_test_runner
./visa_test_runner

# CMake automated build
mkdir -p build && cd build
cmake ..
cmake --build .
./visa_test_runner
```
