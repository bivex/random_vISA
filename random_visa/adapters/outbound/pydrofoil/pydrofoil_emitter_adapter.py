"""Outbound Adapter: Pydrofoil / RPython / JIT-Compatible Emulator Code Emitter."""

import os
from typing import Dict, List, Any
from jinja2 import Environment, DictLoader
from random_visa.domain.model.types import InstructionFormat, BinaryOp, UnaryOp
from random_visa.domain.model.isa_spec import VectorIsaSpec
from random_visa.domain.ports.outbound.ports import PydrofoilCodeEmitterPort


PYDROFOIL_TEMPLATES = {
"pydrofoil_state.py": r"""# Pydrofoil / RPython Architectural Vector State Representation
from typing import List

VLEN = {{ config.vlen }}
VLEN_BYTES = VLEN // 8
NUM_VREGS = {{ config.num_vregs }}
NUM_XREGS = 32

class CSRState:
    def __init__(self):
        self.vl = {{ config.vlen // config.default_sew.value }}
        self.vtype = 0
        self.vstart = 0
        self.vxrm = 0
        self.vxsat = 0
        self.pc = 0x80000000

class VRegFile:
    def __init__(self):
        self.regs = [bytearray(VLEN_BYTES) for _ in range(NUM_VREGS)]

    def reset(self):
        for r in self.regs:
            for b in range(VLEN_BYTES):
                r[b] = 0

    def get_elem(self, reg_idx: int, elem_idx: int, sew: int = 32) -> int:
        if not (0 <= reg_idx < NUM_VREGS):
            return 0
        byte_offset = elem_idx * (sew // 8)
        if byte_offset + (sew // 8) > VLEN_BYTES:
            return 0
        raw = self.regs[reg_idx][byte_offset : byte_offset + (sew // 8)]
        val = int.from_bytes(raw, byteorder="little", signed=True)
        return val

    def set_elem(self, reg_idx: int, elem_idx: int, val: int, sew: int = 32):
        if not (0 <= reg_idx < NUM_VREGS):
            return
        byte_offset = elem_idx * (sew // 8)
        if byte_offset + (sew // 8) > VLEN_BYTES:
            return
        # Normalize to signed 32-bit integer range
        val = ((val + 0x80000000) & 0xFFFFFFFF) - 0x80000000
        raw = val.to_bytes(sew // 8, byteorder="little", signed=True)
        self.regs[reg_idx][byte_offset : byte_offset + (sew // 8)] = raw

    def is_mask_set(self, mask_reg: int, elem_idx: int) -> bool:
        if not (0 <= mask_reg < NUM_VREGS):
            return False
        byte_idx = elem_idx // 8
        bit_idx = elem_idx % 8
        if byte_idx >= VLEN_BYTES:
            return False
        return bool(self.regs[mask_reg][byte_idx] & (1 << bit_idx))

    def dump(self):
        lines = []
        for i in range(NUM_VREGS):
            hex_bytes = " ".join(f"{b:02x}" for b in reversed(self.regs[i]))
            lines.append(f"v{i:02d}: [ {hex_bytes} ]")
        return "\n".join(lines)


class PydrofoilState:
    def __init__(self):
        self.vregs = VRegFile()
        self.xregs = [0] * NUM_XREGS
        self.csr = CSRState()

    def reset(self):
        self.vregs.reset()
        self.xregs = [0] * NUM_XREGS
        self.csr = CSRState()

    def get_xreg(self, idx: int) -> int:
        if idx == 0 or not (0 <= idx < NUM_XREGS):
            return 0
        return self.xregs[idx]

    def set_xreg(self, idx: int, val: int):
        if 0 < idx < NUM_XREGS:
            self.xregs[idx] = val & 0xFFFFFFFFFFFFFFFF
""",

"pydrofoil_decoder.py": r"""# Pydrofoil / Jib IR 32-bit Vector Instruction Decoder
from typing import Optional, NamedTuple

class DecodedInstruction(NamedTuple):
    mnemonic: str
    funct6: int
    funct3: int
    vd: int
    vs2: int
    vs1: int
    rs1: int
    imm: int
    vm: int
    raw_word: int


DECODE_TABLE = {
{% for inst in instructions %}
    ({{ inst.funct6 }}, {{ inst.funct3 }}): "{{ inst.mnemonic }}",
{% endfor %}
}


def decode(word: int) -> Optional[DecodedInstruction]:
    opcode = word & 0x7F
    if opcode != 0x57:
        return None

    vd = (word >> 7) & 0x1F
    funct3 = (word >> 12) & 0x7
    vs1 = (word >> 15) & 0x1F
    rs1 = vs1

    # 5-bit sign extension
    imm5 = (word >> 15) & 0x1F
    if imm5 & 0x10:
        imm5 -= 0x20

    vs2 = (word >> 20) & 0x1F
    vm = (word >> 25) & 0x1
    funct6 = (word >> 26) & 0x3F

    mnemonic = DECODE_TABLE.get((funct6, funct3))
    if not mnemonic:
        return None

    return DecodedInstruction(
        mnemonic=mnemonic,
        funct6=funct6,
        funct3=funct3,
        vd=vd,
        vs2=vs2,
        vs1=vs1,
        rs1=rs1,
        imm=imm5,
        vm=vm,
        raw_word=word,
    )
""",

"pydrofoil_instructions.py": r"""# Pydrofoil / RPython JIT Instruction Semantics
import math
try:
    from .pydrofoil_state import PydrofoilState
    from .pydrofoil_decoder import DecodedInstruction
except (ImportError, ValueError):
    from pydrofoil_state import PydrofoilState
    from pydrofoil_decoder import DecodedInstruction

INT32_MIN = -2147483648
INT32_MAX = 2147483647

def clamp_i32(val: int) -> int:
    if val < INT32_MIN:
        return INT32_MIN
    if val > INT32_MAX:
        return INT32_MAX
    return val

{% for inst in instructions %}
def exec_{{ inst.mnemonic }}(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
{% if inst.binary_op %}
    {% if inst.format.value == "OPIVX" %}
        op1 = state.get_xreg(inst.rs1)
    {% elif inst.format.value == "OPIVI" %}
        op1 = inst.imm
    {% else %}
        op1 = state.vregs.get_elem(inst.vs1, i, 32)
    {% endif %}
{% endif %}

        res = 0
{% if inst.binary_op %}
    {% if inst.binary_op.name == "ADD" %}
        res = (op2 + op1) & 0xFFFFFFFF
        if res & 0x80000000: res -= 0x100000000
    {% elif inst.binary_op.name == "SUB" %}
        res = (op2 - op1) & 0xFFFFFFFF
        if res & 0x80000000: res -= 0x100000000
    {% elif inst.binary_op.name == "MUL" %}
        res = (op2 * op1) & 0xFFFFFFFF
        if res & 0x80000000: res -= 0x100000000
    {% elif inst.binary_op.name == "DIV" %}
        if op1 == 0:
            res = -1
        elif op2 == INT32_MIN and op1 == -1:
            res = INT32_MIN
        else:
            res = int(op2 / op1)
    {% elif inst.binary_op.name == "REM" %}
        if op1 == 0:
            res = op2
        elif op2 == INT32_MIN and op1 == -1:
            res = 0
        else:
            res = op2 - int(op2 / op1) * op1
    {% elif inst.binary_op.name == "AND" %}
        res = op2 & op1
    {% elif inst.binary_op.name == "OR" %}
        res = op2 | op1
    {% elif inst.binary_op.name == "XOR" %}
        res = op2 ^ op1
    {% elif inst.binary_op.name == "SLL" %}
        res = (op2 << (op1 & 31)) & 0xFFFFFFFF
        if res & 0x80000000: res -= 0x100000000
    {% elif inst.binary_op.name == "SRL" %}
        u_op2 = op2 & 0xFFFFFFFF
        res = (u_op2 >> (op1 & 31)) & 0xFFFFFFFF
        if res & 0x80000000: res -= 0x100000000
    {% elif inst.binary_op.name == "SRA" %}
        res = op2 >> (op1 & 31)
    {% elif inst.binary_op.name == "MIN" %}
        res = min(op2, op1)
    {% elif inst.binary_op.name == "MAX" %}
        res = max(op2, op1)
    {% elif inst.binary_op.name == "SADD" %}
        res = clamp_i32(op2 + op1)
    {% elif inst.binary_op.name == "SSUB" %}
        res = clamp_i32(op2 - op1)
    {% else %}
        res = (op2 + op1) & 0xFFFFFFFF
        if res & 0x80000000: res -= 0x100000000
    {% endif %}
{% elif inst.unary_op %}
    {% if inst.unary_op.name == "NEG" %}
        res = (0 - op2) & 0xFFFFFFFF
        if res & 0x80000000: res -= 0x100000000
    {% elif inst.unary_op.name == "NOT" %}
        res = ~op2
    {% elif inst.unary_op.name == "ABS" %}
        res = INT32_MIN if op2 == INT32_MIN else abs(op2)
    {% elif inst.unary_op.name == "CLZ" %}
        u_op2 = op2 & 0xFFFFFFFF
        res = 32 if u_op2 == 0 else 32 - u_op2.bit_length()
    {% elif inst.unary_op.name == "CTZ" %}
        u_op2 = op2 & 0xFFFFFFFF
        res = 32 if u_op2 == 0 else (u_op2 & -u_op2).bit_length() - 1
    {% elif inst.unary_op.name == "CPOP" %}
        res = bin(op2 & 0xFFFFFFFF).count("1")
    {% else %}
        res = op2
    {% endif %}
{% else %}
    res = op2
{% endif %}
        state.vregs.set_elem(inst.vd, i, res, 32)
{% endfor %}

DISPATCH_MAP = {
{% for inst in instructions %}
    "{{ inst.mnemonic }}": exec_{{ inst.mnemonic }},
{% endfor %}
}

def execute(state: PydrofoilState, inst: DecodedInstruction) -> bool:
    handler = DISPATCH_MAP.get(inst.mnemonic)
    if handler:
        handler(state, inst)
        return True
    return False
""",

"pydrofoil_emulator.py": r"""# Pydrofoil Vector ISA Emulator Core Engine
import struct
from typing import List, Optional
try:
    from .pydrofoil_state import PydrofoilState
    from .pydrofoil_decoder import decode, DecodedInstruction
    from .pydrofoil_instructions import execute
except (ImportError, ValueError):
    from pydrofoil_state import PydrofoilState
    from pydrofoil_decoder import decode, DecodedInstruction
    from pydrofoil_instructions import execute

class PydrofoilVectorEmulator:
    def __init__(self):
        self.state = PydrofoilState()

    def reset(self):
        self.state.reset()

    def step(self, instruction_word: int) -> bool:
        dec = decode(instruction_word)
        if not dec:
            return False
        ok = execute(self.state, dec)
        if ok:
            self.state.csr.pc += 4
        return ok

    def run_bytecode(self, bytecode_bytes: bytes) -> int:
        count = len(bytecode_bytes) // 4
        executed = 0
        for i in range(count):
            word = struct.unpack_from("<I", bytecode_bytes, i * 4)[0]
            if not self.step(word):
                break
            executed += 1
        return executed
""",

"pydrofoil_main.py": r"""#!/usr/bin/env python3
# Standalone Pydrofoil / Python Verification Harness and Bytecode Runner
import sys
import os
import struct
try:
    from .pydrofoil_state import PydrofoilState
    from .pydrofoil_decoder import decode
    from .pydrofoil_instructions import execute
    from .pydrofoil_emulator import PydrofoilVectorEmulator
except (ImportError, ValueError):
    from pydrofoil_state import PydrofoilState
    from pydrofoil_decoder import decode
    from pydrofoil_instructions import execute
    from pydrofoil_emulator import PydrofoilVectorEmulator

TEST_VECTORS = [
{% for inst in instructions %}
    (0x{{ "%08X" % inst.encode(3, 2, 1) }}, "{{ inst.mnemonic }}"),
{% endfor %}
]

def run_verification_suite():
    emu = PydrofoilVectorEmulator()
    print("=" * 60)
    print("Starting Pydrofoil JIT Vector ISA ({{ name }}) Verification")
    print(f"VLEN = {emu.state.vregs.regs[0].__len__() * 8} bits, Num VRegs = 32")
    print("=" * 60)

    passed = 0
    total = len(TEST_VECTORS)

    for idx, (word, mnemonic) in enumerate(TEST_VECTORS, start=1):
        emu.reset()
        # Setup test inputs
        emu.state.vregs.set_elem(1, 0, 10)
        emu.state.vregs.set_elem(1, 1, 20)
        emu.state.vregs.set_elem(1, 2, 30)
        emu.state.vregs.set_elem(1, 3, 40)

        emu.state.vregs.set_elem(2, 0, 2)
        emu.state.vregs.set_elem(2, 1, 4)
        emu.state.vregs.set_elem(2, 2, 6)
        emu.state.vregs.set_elem(2, 3, 8)

        emu.state.set_xreg(1, 5)

        ok = emu.step(word)
        if ok:
            res_elems = [emu.state.vregs.get_elem(3, e) for e in range(4)]
            print(f"[Test {idx}/{total}] Executing {mnemonic} (0x{word:08X})... SUCCESS -> v3: {res_elems}")
            passed += 1
        else:
            print(f"[Test {idx}/{total}] Executing {mnemonic} (0x{word:08X})... FAILED (Unknown Instruction)")

    print(f"\nResults: {passed}/{total} Pydrofoil tests passed.")
    return 0 if passed == total else 1


def run_bytecode_file(bin_path: str):
    if not os.path.exists(bin_path):
        print(f"Error: file not found '{bin_path}'")
        return 1

    with open(bin_path, "rb") as f:
        data = f.read()

    emu = PydrofoilVectorEmulator()
    # Setup initial state
    emu.state.vregs.set_elem(1, 0, 10)
    emu.state.vregs.set_elem(1, 1, 20)
    emu.state.vregs.set_elem(1, 2, 30)
    emu.state.vregs.set_elem(1, 3, 40)

    emu.state.vregs.set_elem(2, 0, 2)
    emu.state.vregs.set_elem(2, 1, 4)
    emu.state.vregs.set_elem(2, 2, 6)
    emu.state.vregs.set_elem(2, 3, 8)
    emu.state.set_xreg(1, 5)

    words_count = len(data) // 4
    print(f"Executing Bytecode Program ({words_count} instructions)...")
    for i in range(words_count):
        word = struct.unpack_from("<I", data, i * 4)[0]
        pc = emu.state.csr.pc
        dec = decode(word)
        mnem = dec.mnemonic if dec else "unknown"
        ok = emu.step(word)
        vd_val = [emu.state.vregs.get_elem(dec.vd, e) for e in range(4)] if dec else []
        print(f"  [{i+1}] PC=0x{pc:08x} Word=0x{word:08x} ({mnem})... {'OK' if ok else 'FAIL'} -> vd (v{dec.vd if dec else 0}): {vd_val}")

    print("\n[Final Vector Register File Dump]:")
    print(emu.state.vregs.dump())
    return 0


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--bin":
        sys.exit(run_bytecode_file(sys.argv[2]))
    else:
        sys.exit(run_verification_suite())


if __name__ == "__main__":
    main()
"""
}


class PydrofoilEmitterAdapter(PydrofoilCodeEmitterPort):
    """Adapter for generating Pydrofoil JIT / Python vector emulator projects."""

    def __init__(self):
        self.env = Environment(loader=DictLoader(PYDROFOIL_TEMPLATES), trim_blocks=True, lstrip_blocks=True)

    def emit_pydrofoil_project(self, spec: VectorIsaSpec, destination_dir: str) -> List[str]:
        os.makedirs(destination_dir, exist_ok=True)
        emitted_paths = []

        context = {
            "name": spec.name,
            "spec": spec,
            "config": spec.config,
            "instructions": spec.instructions,
        }

        for template_name in PYDROFOIL_TEMPLATES:
            tmpl = self.env.get_template(template_name)
            rendered = tmpl.render(context)
            out_file = os.path.join(destination_dir, template_name)
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(rendered)
            emitted_paths.append(out_file)

        # Also create __init__.py
        init_file = os.path.join(destination_dir, "__init__.py")
        with open(init_file, "w", encoding="utf-8") as f:
            f.write("# Pydrofoil Vector ISA Package\n")
        emitted_paths.append(init_file)

        return emitted_paths
