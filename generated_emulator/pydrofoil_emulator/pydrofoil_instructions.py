# Pydrofoil / RPython JIT Instruction Semantics
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

def exec_vand_vv_0(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
        op1 = state.vregs.get_elem(inst.vs1, i, 32)

        res = 0
        res = op2 & op1
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vmax_vx_1(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
        op1 = state.get_xreg(inst.rs1)

        res = 0
        res = max(op2, op1)
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vdiv_vx_2(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
        op1 = state.get_xreg(inst.rs1)

        res = 0
        if op1 == 0:
            res = -1
        elif op2 == INT32_MIN and op1 == -1:
            res = INT32_MIN
        else:
            res = int(op2 / op1)
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vxor_vx_3(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
        op1 = state.get_xreg(inst.rs1)

        res = 0
        res = op2 ^ op1
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vdiv_vx_4(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
        op1 = state.get_xreg(inst.rs1)

        res = 0
        if op1 == 0:
            res = -1
        elif op2 == INT32_MIN and op1 == -1:
            res = INT32_MIN
        else:
            res = int(op2 / op1)
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vmax_vv_5(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
        op1 = state.vregs.get_elem(inst.vs1, i, 32)

        res = 0
        res = max(op2, op1)
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vdiv_vx_6(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
        op1 = state.get_xreg(inst.rs1)

        res = 0
        if op1 == 0:
            res = -1
        elif op2 == INT32_MIN and op1 == -1:
            res = INT32_MIN
        else:
            res = int(op2 / op1)
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vor_vx_7(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
        op1 = state.get_xreg(inst.rs1)

        res = 0
        res = op2 | op1
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vsrl_vx_8(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
        op1 = state.get_xreg(inst.rs1)

        res = 0
        u_op2 = op2 & 0xFFFFFFFF
        res = (u_op2 >> (op1 & 31)) & 0xFFFFFFFF
        if res & 0x80000000: res -= 0x100000000
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vclz_m_9(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)

        res = 0
        u_op2 = op2 & 0xFFFFFFFF
        res = 32 if u_op2 == 0 else 32 - u_op2.bit_length()
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vmin_vx_10(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
        op1 = state.get_xreg(inst.rs1)

        res = 0
        res = min(op2, op1)
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vmul_vv_11(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
        op1 = state.vregs.get_elem(inst.vs1, i, 32)

        res = 0
        res = (op2 * op1) & 0xFFFFFFFF
        if res & 0x80000000: res -= 0x100000000
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vsrl_vv_12(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
        op1 = state.vregs.get_elem(inst.vs1, i, 32)

        res = 0
        u_op2 = op2 & 0xFFFFFFFF
        res = (u_op2 >> (op1 & 31)) & 0xFFFFFFFF
        if res & 0x80000000: res -= 0x100000000
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vsadd_vx_13(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
        op1 = state.get_xreg(inst.rs1)

        res = 0
        res = clamp_i32(op2 + op1)
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vmul_vv_14(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
        op1 = state.vregs.get_elem(inst.vs1, i, 32)

        res = 0
        res = (op2 * op1) & 0xFFFFFFFF
        if res & 0x80000000: res -= 0x100000000
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vmax_vx_15(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
        op1 = state.get_xreg(inst.rs1)

        res = 0
        res = max(op2, op1)
        state.vregs.set_elem(inst.vd, i, res, 32)

DISPATCH_MAP = {
    "vand_vv_0": exec_vand_vv_0,
    "vmax_vx_1": exec_vmax_vx_1,
    "vdiv_vx_2": exec_vdiv_vx_2,
    "vxor_vx_3": exec_vxor_vx_3,
    "vdiv_vx_4": exec_vdiv_vx_4,
    "vmax_vv_5": exec_vmax_vv_5,
    "vdiv_vx_6": exec_vdiv_vx_6,
    "vor_vx_7": exec_vor_vx_7,
    "vsrl_vx_8": exec_vsrl_vx_8,
    "vclz_m_9": exec_vclz_m_9,
    "vmin_vx_10": exec_vmin_vx_10,
    "vmul_vv_11": exec_vmul_vv_11,
    "vsrl_vv_12": exec_vsrl_vv_12,
    "vsadd_vx_13": exec_vsadd_vx_13,
    "vmul_vv_14": exec_vmul_vv_14,
    "vmax_vx_15": exec_vmax_vx_15,
}

def execute(state: PydrofoilState, inst: DecodedInstruction) -> bool:
    handler = DISPATCH_MAP.get(inst.mnemonic)
    if handler:
        handler(state, inst)
        return True
    return False