# Pydrofoil / Jib IR 32-bit Vector Instruction Decoder
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
    (0, 2): "vclz_m_0",
    (1, 3): "vor_vi_1",
    (2, 4): "vxor_vx_2",
    (3, 4): "vmin_vx_3",
    (4, 4): "vsadd_vx_4",
    (5, 4): "vsra_vx_5",
    (6, 4): "vrem_vx_6",
    (7, 2): "vabs_m_7",
    (8, 2): "vclz_m_8",
    (9, 4): "vsrl_vx_9",
    (10, 2): "vcpop_m_10",
    (11, 2): "vcpop_m_11",
    (12, 0): "vrem_vv_12",
    (13, 4): "vxor_vx_13",
    (14, 4): "vmax_vx_14",
    (15, 0): "vrem_vv_15",
    (16, 4): "vxor_vx_16",
    (17, 0): "vdiv_vv_17",
    (18, 2): "vabs_m_18",
    (19, 0): "vxor_vv_19",
    (20, 2): "vclz_m_20",
    (21, 2): "vnot_m_21",
    (22, 0): "vmin_vv_22",
    (23, 2): "vcpop_m_23",
    (24, 4): "vor_vx_24",
    (25, 0): "vmul_vv_25",
    (26, 2): "vcpop_m_26",
    (27, 4): "vdiv_vx_27",
    (28, 2): "vclz_m_28",
    (29, 4): "vsrl_vx_29",
    (30, 0): "vsadd_vv_30",
    (31, 4): "vadd_vx_31",
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