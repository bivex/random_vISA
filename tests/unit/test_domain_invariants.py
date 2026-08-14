"""Unit tests for domain models, invariants, and edge cases."""

import pytest
from random_visa.domain.model.types import (
    SEW,
    LMUL,
    InstructionFormat,
    BinaryOp,
    UnaryOp,
)
from random_visa.domain.model.instruction import VectorInstruction
from random_visa.domain.model.vector_config import VectorConfig
from random_visa.domain.model.isa_spec import VectorIsaSpec


def test_sew_values_and_properties():
    assert SEW.E8.value == 8
    assert SEW.E8.byte_width == 1
    assert SEW.E8.c_type == "int8_t"

    assert SEW.E16.value == 16
    assert SEW.E16.byte_width == 2
    assert SEW.E16.c_type == "int16_t"

    assert SEW.E32.value == 32
    assert SEW.E32.byte_width == 4
    assert SEW.E32.c_type == "int32_t"

    assert SEW.E64.value == 64
    assert SEW.E64.byte_width == 8
    assert SEW.E64.c_type == "int64_t"


def test_all_binary_and_unary_ops_present():
    assert len(BinaryOp) == 15
    assert len(UnaryOp) == 6

    expected_binary = {
        "ADD", "SUB", "MUL", "DIV", "REM",
        "AND", "OR", "XOR", "SLL", "SRL",
        "SRA", "MIN", "MAX", "SADD", "SSUB"
    }
    assert {op.name for op in BinaryOp} == expected_binary

    expected_unary = {"NEG", "NOT", "ABS", "CLZ", "CTZ", "CPOP"}
    assert {op.name for op in UnaryOp} == expected_unary


def test_vector_config_validation():
    cfg = VectorConfig(vlen=256, elen=64, num_vregs=32, default_sew=SEW.E32)
    assert cfg.vlen_bytes == 32
    assert cfg.calculate_vlmax(SEW.E32, LMUL.M1) == 8

    # Invalid VLEN < 64
    with pytest.raises(ValueError):
        VectorConfig(vlen=32)

    # Invalid VLEN not power of 2
    with pytest.raises(ValueError):
        VectorConfig(vlen=100)


def test_vector_instruction_encoding_and_invariants():
    inst = VectorInstruction(
        mnemonic="vadd_vv_0",
        format=InstructionFormat.OP_VV,
        funct6=0b000001,
        funct3=0b000,
        opcode=0x57,
        binary_op=BinaryOp.ADD,
        description="Vector Add",
    )
    word = inst.encode(vd=3, vs2=2, vs1_or_rs1_or_imm=1, vm=1)
    assert (word & 0x7F) == 0x57
    assert ((word >> 7) & 0x1F) == 3
    assert ((word >> 12) & 0x7) == 0
    assert ((word >> 15) & 0x1F) == 1
    assert ((word >> 20) & 0x1F) == 2
    assert ((word >> 25) & 0x1) == 1
    assert ((word >> 26) & 0x3F) == 1


def test_vector_isa_spec_collision_and_lookup():
    cfg = VectorConfig(vlen=128)
    spec = VectorIsaSpec(name="TestSpec", config=cfg)

    inst1 = VectorInstruction(
        mnemonic="vcustom_0",
        format=InstructionFormat.OP_VV,
        funct6=1,
        funct3=0,
        opcode=0x57,
        binary_op=BinaryOp.ADD,
        description="Custom Add",
    )
    spec.add_instruction(inst1)
    assert len(spec.instructions) == 1
    assert spec.get_by_mnemonic("vcustom_0") == inst1
    assert spec.get_by_mnemonic("non_existent") is None

    # Duplicate mnemonic collision
    inst_dup_mnemonic = VectorInstruction(
        mnemonic="vcustom_0",
        format=InstructionFormat.OP_VV,
        funct6=2,
        funct3=0,
        opcode=0x57,
        binary_op=BinaryOp.SUB,
    )
    with pytest.raises(ValueError, match="Duplicate mnemonic"):
        spec.add_instruction(inst_dup_mnemonic)

    # Duplicate encoding collision
    inst_dup_encoding = VectorInstruction(
        mnemonic="vcustom_1",
        format=InstructionFormat.OP_VV,
        funct6=1,
        funct3=0,
        opcode=0x57,
        binary_op=BinaryOp.SUB,
    )
    with pytest.raises(ValueError, match="Instruction encoding collision"):
        spec.add_instruction(inst_dup_encoding)
