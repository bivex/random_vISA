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
    (0, 0): "vand_vv_0",
    (1, 4): "vmax_vx_1",
    (2, 4): "vdiv_vx_2",
    (3, 4): "vxor_vx_3",
    (4, 4): "vdiv_vx_4",
    (5, 0): "vmax_vv_5",
    (6, 4): "vdiv_vx_6",
    (7, 4): "vor_vx_7",
    (8, 4): "vsrl_vx_8",
    (9, 2): "vclz_m_9",
    (10, 4): "vmin_vx_10",
    (11, 0): "vmul_vv_11",
    (12, 0): "vsrl_vv_12",
    (13, 4): "vsadd_vx_13",
    (14, 0): "vmul_vv_14",
    (15, 4): "vmax_vx_15",
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