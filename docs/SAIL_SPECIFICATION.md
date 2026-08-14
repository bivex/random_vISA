# Sail Formal Specification & ANTLR4 Parser Guide

This document describes how Sail formal ISA specifications are generated, structured, and parsed.

---

## ⛵ What is Sail?

**Sail** is a formal specification language developed by the University of Cambridge and University of Edinburgh to formally define processor instruction set architectures (such as RISC-V, ARM, and CHERI).

### Generated Sail Spec Structure

A synthesized Vector ISA specification in `.sail` contains:

```sail
/* ========================================================================= */
/* Sail Formal Specification for RVV_Custom_ISA (V-ISA)                      */
/* Version: 1.0-synth                                                        */
/* ========================================================================= */

default Order dec
$include <prelude.sail>

let VLEN : int = 128
let ELEN : int = 64
let NUM_VREGS : int = 32

type vreg_idx = range(0, 31)
type vreg_t = bits(VLEN)

register v0  : vreg_t
register v1  : vreg_t
register v2  : vreg_t
register v3  : vreg_t
register vl  : bits(64)
register vtype : bits(64)

val get_velem : (vreg_t, int, int) -> bits(32)
val set_velem : (vreg_t, int, int, bits(32)) -> unit
val get_vmask_bit : (vreg_t, int) -> bits(1)

/* Instruction: vadd_vv_0 (OPIVV) */
val execute_vadd_vv_0 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vadd_vv_0(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = (op2 + op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}
```

---

## 🔍 ANTLR4 Grammar (`Sail.g4`)

The ANTLR4 grammar is located at [`random_visa/adapters/inbound/parser/antlr/Sail.g4`](file:///Volumes/External/Code/random_vISA/random_visa/adapters/inbound/parser/antlr/Sail.g4).

### Key Grammar Rules:
- **Top Level**: Directives (`$include`, `default Order`), Constants (`let`), Types (`type`), Registers (`register`), Function Prototypes (`val`), and Function Bodies (`function`).
- **Statements**:
  - `let ID [: type] = expr;`
  - `foreach (i from start to end) { stmts };`
  - `if cond then { ... } else { ... }`
  - Function calls (`set_velem(...)`, `get_velem(...)`).
- **Expressions**:
  - Binary arithmetic: `+`, `-`, `*`, `/`, `%`, `&`, `|`, `^`, `<<`, `>>`, `min`, `max`, `+_sat`, `-_sat`.
  - Unary operations: `~`, `-`, `clz`, `ctz`, `cpop`, `abs`.

### Parsing Workflow

1. `AntlrSailParserAdapter` feeds `.sail` text to `SailLexer` and `SailParser`.
2. `SailToDomainVisitor` walks the AST and builds domain `VectorInstruction` entities.
3. The resulting `VectorIsaSpec` aggregate can then be passed to the C++ Code Emitter for immediate emulation.
