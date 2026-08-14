# Sail Jib IR Specification & ANTLR4 Grammar

This document provides a formal specification of **Jib IR**, the linear typed Intermediate Representation (IR) used by the **Sail** compiler, along with its ANTLR4 grammar implementation in `random_vISA`.

---

## 🎯 What is Jib IR?

**Jib** is Sail's internal lower-level intermediate representation. Before generating C, C++, OCaml, Lem, or SMT code, the Sail compiler transforms the high-level dependent-typed AST into Jib IR:

$$\text{Sail DSL} \xrightarrow{\text{Monomorphization}} \mathbf{\text{Jib IR (3-Address Code)}} \xrightarrow{\text{Codegen}} \text{C++ / JIT / SMT}$$

### Key Properties of Jib IR:
1. **Linear Control Flow**: Control flow is represented with explicit labels (`label name:`), jumps (`jump target;`), and conditional branches (`jump_if cond target;` or `if cond goto L1 else goto L2;`).
2. **Explicit Variables**: All variables must be declared with types (`var %name : type;`).
3. **Monomorphized Bitvectors & Vectors**: Sized bitvectors (`bv(128)`, `bits(64)`) and fixed vectors (`vector(N, T)`).
4. **Three-Address Code Operations**: Primitives and calls have explicit destination targets (`%res = call get_velem(vs2, %i);`).

---

## 📑 2. Jib IR Language Grammar Overview

The full ANTLR4 grammar is located at [`random_visa/adapters/inbound/parser/antlr/Jib.g4`](file:///Volumes/External/Code/random_vISA/random_visa/adapters/inbound/parser/antlr/Jib.g4).

### Top-Level Declarations Matrix:

| Construct | Syntax | Description | Example |
| :--- | :--- | :--- | :--- |
| **`struct`** | `struct ID = { field: type, ... }` | Composite record type | `struct VState = { vl: i(64), v0: bv(128) }` |
| **`enum`** | `enum ID = { VAL1, VAL2, ... }` | Enumeration type | `enum RoundingMode = { RNE, RTZ, RDN, RUP }` |
| **`union`** | `union ID = { ctor: type, ... }` | Tagged union / variant | `union Value = { Int: i(64), Bits: bv(128) }` |
| **`register`**| `register ID : type;` | Architectural register declaration | `register v0 : bv(128);` |
| **`val`** | `val ID : (type, ...) -> type;` | Function prototype declaration | `val get_velem : (bv(128), i(64)) -> i(32);` |
| **`fn`** | `fn ID(param: type, ...) -> type { ... }` | Function definition with 3AC body | `fn execute_vadd_vv(...) -> unit { ... }` |

---

## 🔧 3. Jib IR Instructions Matrix

| Instruction Class | Syntax | Semantic Action |
| :--- | :--- | :--- |
| **Variable Declaration** | `var %x : type;` or `local %x : type;` | Allocates a local variable with static Jib type |
| **Assignment / Copy** | `%dest = %src;` or `copy %dest = %src;` | Copies value from source to destination |
| **Primitive Operation** | `%dest = %op1 + %op2;` | Computes binary/unary arithmetic or bitwise operation |
| **Function Call** | `%dest = call func(%arg1, %arg2);` | Invokes function and assigns return value to `%dest` |
| **Type Cast / Slice** | `%dest = (type) %src;` | Casts, sign-extends, zero-extends, or slices bitvectors |
| **Unconditional Jump** | `goto label;` or `jump label;` | Transfers control unconditionally to target label |
| **Conditional Branch** | `jump_if %cond label;` | Transfers control to target label if `%cond` is true |
| **If-Then-Else Jump** | `if %cond goto L1 else goto L2;` | Two-way conditional branch |
| **Return** | `return %val;` or `return ();` | Returns value from current function |
| **End / Trap** | `end;` or `fail "message";` | Normal termination or architectural trap |

---

## 🧪 4. Complete Jib IR Code Example

```c
#pragma sail target c

struct VRegState = {
    v0: bv(128),
    vl: i(64)
}

register v0 : bv(128);
register vl : i(64);

val get_velem : (bv(128), i(64)) -> i(32);
val set_velem : (bv(5), i(64), i(32)) -> unit;

fn execute_vadd_vv(vd: bv(5), vs2: bv(5), vs1: bv(5), vm: bit) -> unit {
    var %i : i(64);
    var %op2 : i(32);
    var %op1 : i(32);
    var %res : i(32);
    var %cond : bool;

    %i = 0;
label loop_head:
    %cond = %i < vl;
    jump_if %cond loop_body;
    goto loop_end;

label loop_body:
    %op2 = call get_velem(vs2, %i);
    %op1 = call get_velem(vs1, %i);
    %res = %op2 + %op1;
    call set_velem(vd, %i, %res);
    %i = %i + 1;
    goto loop_head;

label loop_end:
    return ();
}
```
