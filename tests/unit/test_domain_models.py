"""Unit tests for Domain Models and Value Objects."""

import pytest
from random_visa.domain.model.types import SEW, LMUL, InstructionFormat, BinaryOp
from random_visa.domain.model.vector_config import VectorConfig
from random_visa.domain.model.instruction import VectorInstruction
from random_visa.domain.model.isa_spec import VectorIsaSpec


def test_vector_config_validation():
    cfg = VectorConfig(vlen=128, elen=64, default_sew=SEW.E32, default_lmul=LMUL.M1)
    assert cfg.vlen_bytes == 16
    assert cfg.calculate_vlmax(SEW.E32, LMUL.M1) == 4
    assert cfg.calculate_vlmax(SEW.E8, LMUL.M1) == 16

    with pytest.raises(ValueError):
        VectorConfig(vlen=100)  # Not power of 2


def test_instruction_encoding_and_aggregate():
    inst = VectorInstruction(
        mnemonic="vadd_vv_custom",
        format=InstructionFormat.OP_VV,
        funct6=0b000000,
        funct3=0b000,
        opcode=0x57,
        binary_op=BinaryOp.ADD,
    )
    encoded = inst.encode(vd=1, vs2=2, vs1_or_rs1_or_imm=3, vm=1)
    assert (encoded & 0x7F) == 0x57  # opcode
    assert ((encoded >> 7) & 0x1F) == 1  # vd
    assert ((encoded >> 12) & 0x7) == 0  # funct3
    assert ((encoded >> 15) & 0x1F) == 3  # vs1
    assert ((encoded >> 20) & 0x1F) == 2  # vs2
    assert ((encoded >> 25) & 0x1) == 1   # vm
    assert ((encoded >> 26) & 0x3F) == 0  # funct6


def test_spec_collision_detection():
    spec = VectorIsaSpec(name="TestSpec")
    inst1 = VectorInstruction(
        mnemonic="vop1",
        format=InstructionFormat.OP_VV,
        funct6=10,
        funct3=0,
        binary_op=BinaryOp.ADD,
    )
    spec.add_instruction(inst1)

    # Adding with same encoding should raise ValueError
    inst_collide = VectorInstruction(
        mnemonic="vop2",
        format=InstructionFormat.OP_VV,
        funct6=10,
        funct3=0,
        binary_op=BinaryOp.SUB,
    )
    with pytest.raises(ValueError, match="collision"):
        spec.add_instruction(inst_collide)


def test_spec_decode():
    spec = VectorIsaSpec(name="TestDecodeSpec")
    inst = VectorInstruction(
        mnemonic="vmul_vv",
        format=InstructionFormat.OP_VV,
        funct6=15,
        funct3=0,
        binary_op=BinaryOp.MUL,
    )
    spec.add_instruction(inst)

    encoded = inst.encode(vd=5, vs2=6, vs1_or_rs1_or_imm=7, vm=1)
    decoded = spec.decode(encoded)
    assert decoded is not None
    assert decoded.mnemonic == "vmul_vv"
    assert decoded.funct6 == 15


def test_sail_synthesis_operands():
    inst_vx = VectorInstruction(
        mnemonic="vadd_vx_test",
        format=InstructionFormat.OP_VX,
        funct6=1,
        funct3=4,
        binary_op=BinaryOp.ADD,
    )
    sail_code = inst_vx.sail_function.to_sail()
    assert "rX(vs1_or_imm)" in sail_code

    inst_vi = VectorInstruction(
        mnemonic="vadd_vi_test",
        format=InstructionFormat.OP_VI,
        funct6=2,
        funct3=3,
        binary_op=BinaryOp.ADD,
    )
    sail_code_vi = inst_vi.sail_function.to_sail()
    assert "sign_extend(vs1_or_imm)" in sail_code_vi

