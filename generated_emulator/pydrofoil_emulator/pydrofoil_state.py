# Pydrofoil / RPython Architectural Vector State Representation
from typing import List

VLEN = 256
VLEN_BYTES = VLEN // 8
NUM_VREGS = 32
NUM_XREGS = 32

class CSRState:
    def __init__(self):
        self.vl = 8
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