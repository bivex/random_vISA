# Generated C++20 Emulator Architecture

This document describes the structure and execution model of the auto-generated C++20 Vector ISA emulator.

---

## 🏗 Generated Files Structure

When an ISA specification is emitted, the following standalone C++20 project files are generated:

| File | Purpose |
| :--- | :--- |
| `isa_state.hpp` | Register file (`v0-v31`, `x0-x31`), CSRs (`vl`, `vtype`), element accessors, bitmask checks |
| `decoder.hpp` | Bitfield instruction decoder matching 32-bit words to `(opcode, funct3, funct6)` |
| `instructions.hpp` | Declarations of instruction executors |
| `instructions.cpp` | Safe vector execution loops with masking and 2's complement wrapping math |
| `emulator.hpp` | Main `VectorEmulator` class (`step()`, `run_program()`) |
| `main.cpp` | Self-contained test verification suite executing test vectors |
| `CMakeLists.txt` | Standard CMake configuration for building the executable |

---

## ⚡ Arithmetic & UB Safety

The C++ code generator implements rigorous safety against **Undefined Behavior (UB)** and hardware traps:

1. **Division & Remainder Safety**:
   - Division by zero: returns `-1` (all bits set) as per RISC-V specification.
   - Remainder by zero: returns the dividend `op2`.
   - `INT32_MIN / -1`: handled safely to prevent hardware `SIGFPE` traps.
2. **Two's Complement Overflow Wrapping**:
   - `ADD`, `SUB`, `MUL`, `SLL`, `SRL` use unsigned casting `static_cast<elem_t>(static_cast<uint32_t>(op2) + static_cast<uint32_t>(op1))` to prevent signed integer overflow UB in standard C++.
3. **Shift Counts**:
   - Shift amounts are masked with `(op1 & 31u)` to ensure shifts are strictly in the range `[0, 31]`.
4. **Saturation Arithmetic**:
   - `SADD` and `SSUB` perform 64-bit intermediate calculations clamped to `[INT32_MIN, INT32_MAX]`.

---

## 🚀 Building and Running the C++ Emulator Manually

```bash
# Using Clang++
clang++ -std=c++20 -O3 -Wall -Wextra -I. main.cpp instructions.cpp -o visa_test_runner
./visa_test_runner

# Or using CMake
mkdir build && cd build
cmake ..
cmake --build .
./visa_test_runner
```
