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

def exec_vclz_m_0(state: PydrofoilState, inst: DecodedInstruction):
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
def exec_vor_vi_1(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
        op1 = inst.imm

        res = 0
        res = op2 | op1
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vxor_vx_2(state: PydrofoilState, inst: DecodedInstruction):
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
def exec_vmin_vx_3(state: PydrofoilState, inst: DecodedInstruction):
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
def exec_vsadd_vx_4(state: PydrofoilState, inst: DecodedInstruction):
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
def exec_vsra_vx_5(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
        op1 = state.get_xreg(inst.rs1)

        res = 0
        res = op2 >> (op1 & 31)
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vrem_vx_6(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
        op1 = state.get_xreg(inst.rs1)

        res = 0
        if op1 == 0:
            res = op2
        elif op2 == INT32_MIN and op1 == -1:
            res = 0
        else:
            res = op2 - int(op2 / op1) * op1
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vabs_m_7(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)

        res = 0
        res = INT32_MIN if op2 == INT32_MIN else abs(op2)
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vclz_m_8(state: PydrofoilState, inst: DecodedInstruction):
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
def exec_vsrl_vx_9(state: PydrofoilState, inst: DecodedInstruction):
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
def exec_vcpop_m_10(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)

        res = 0
        res = bin(op2 & 0xFFFFFFFF).count("1")
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vcpop_m_11(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)

        res = 0
        res = bin(op2 & 0xFFFFFFFF).count("1")
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vrem_vv_12(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
        op1 = state.vregs.get_elem(inst.vs1, i, 32)

        res = 0
        if op1 == 0:
            res = op2
        elif op2 == INT32_MIN and op1 == -1:
            res = 0
        else:
            res = op2 - int(op2 / op1) * op1
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vxor_vx_13(state: PydrofoilState, inst: DecodedInstruction):
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
def exec_vmax_vx_14(state: PydrofoilState, inst: DecodedInstruction):
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
def exec_vrem_vv_15(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
        op1 = state.vregs.get_elem(inst.vs1, i, 32)

        res = 0
        if op1 == 0:
            res = op2
        elif op2 == INT32_MIN and op1 == -1:
            res = 0
        else:
            res = op2 - int(op2 / op1) * op1
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vxor_vx_16(state: PydrofoilState, inst: DecodedInstruction):
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
def exec_vdiv_vv_17(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
        op1 = state.vregs.get_elem(inst.vs1, i, 32)

        res = 0
        if op1 == 0:
            res = -1
        elif op2 == INT32_MIN and op1 == -1:
            res = INT32_MIN
        else:
            res = int(op2 / op1)
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vabs_m_18(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)

        res = 0
        res = INT32_MIN if op2 == INT32_MIN else abs(op2)
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vxor_vv_19(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
        op1 = state.vregs.get_elem(inst.vs1, i, 32)

        res = 0
        res = op2 ^ op1
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vclz_m_20(state: PydrofoilState, inst: DecodedInstruction):
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
def exec_vnot_m_21(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)

        res = 0
        res = ~op2
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vmin_vv_22(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
        op1 = state.vregs.get_elem(inst.vs1, i, 32)

        res = 0
        res = min(op2, op1)
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vcpop_m_23(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)

        res = 0
        res = bin(op2 & 0xFFFFFFFF).count("1")
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vor_vx_24(state: PydrofoilState, inst: DecodedInstruction):
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
def exec_vmul_vv_25(state: PydrofoilState, inst: DecodedInstruction):
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
def exec_vcpop_m_26(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)

        res = 0
        res = bin(op2 & 0xFFFFFFFF).count("1")
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vdiv_vx_27(state: PydrofoilState, inst: DecodedInstruction):
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
def exec_vclz_m_28(state: PydrofoilState, inst: DecodedInstruction):
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
def exec_vsrl_vx_29(state: PydrofoilState, inst: DecodedInstruction):
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
def exec_vsadd_vv_30(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
        op1 = state.vregs.get_elem(inst.vs1, i, 32)

        res = 0
        res = clamp_i32(op2 + op1)
        state.vregs.set_elem(inst.vd, i, res, 32)
def exec_vadd_vx_31(state: PydrofoilState, inst: DecodedInstruction):
    vl = state.csr.vl
    unmasked = (inst.vm == 1)

    for i in range(vl):
        if not unmasked and not state.vregs.is_mask_set(0, i):
            continue

        op2 = state.vregs.get_elem(inst.vs2, i, 32)
        op1 = state.get_xreg(inst.rs1)

        res = 0
        res = (op2 + op1) & 0xFFFFFFFF
        if res & 0x80000000: res -= 0x100000000
        state.vregs.set_elem(inst.vd, i, res, 32)

DISPATCH_MAP = {
    "vclz_m_0": exec_vclz_m_0,
    "vor_vi_1": exec_vor_vi_1,
    "vxor_vx_2": exec_vxor_vx_2,
    "vmin_vx_3": exec_vmin_vx_3,
    "vsadd_vx_4": exec_vsadd_vx_4,
    "vsra_vx_5": exec_vsra_vx_5,
    "vrem_vx_6": exec_vrem_vx_6,
    "vabs_m_7": exec_vabs_m_7,
    "vclz_m_8": exec_vclz_m_8,
    "vsrl_vx_9": exec_vsrl_vx_9,
    "vcpop_m_10": exec_vcpop_m_10,
    "vcpop_m_11": exec_vcpop_m_11,
    "vrem_vv_12": exec_vrem_vv_12,
    "vxor_vx_13": exec_vxor_vx_13,
    "vmax_vx_14": exec_vmax_vx_14,
    "vrem_vv_15": exec_vrem_vv_15,
    "vxor_vx_16": exec_vxor_vx_16,
    "vdiv_vv_17": exec_vdiv_vv_17,
    "vabs_m_18": exec_vabs_m_18,
    "vxor_vv_19": exec_vxor_vv_19,
    "vclz_m_20": exec_vclz_m_20,
    "vnot_m_21": exec_vnot_m_21,
    "vmin_vv_22": exec_vmin_vv_22,
    "vcpop_m_23": exec_vcpop_m_23,
    "vor_vx_24": exec_vor_vx_24,
    "vmul_vv_25": exec_vmul_vv_25,
    "vcpop_m_26": exec_vcpop_m_26,
    "vdiv_vx_27": exec_vdiv_vx_27,
    "vclz_m_28": exec_vclz_m_28,
    "vsrl_vx_29": exec_vsrl_vx_29,
    "vsadd_vv_30": exec_vsadd_vv_30,
    "vadd_vx_31": exec_vadd_vx_31,
}

def execute(state: PydrofoilState, inst: DecodedInstruction) -> bool:
    handler = DISPATCH_MAP.get(inst.mnemonic)
    if handler:
        handler(state, inst)
        return True
    return False