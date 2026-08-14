"""Unit tests for Vector Assembler and Bytecode Generation."""

import tempfile
import os
from random_visa.domain.model.types import InstructionFormat, BinaryOp
from random_visa.domain.model.instruction import VectorInstruction
from random_visa.domain.model.isa_spec import VectorIsaSpec
from random_visa.domain.services.assembler import VectorAssemblerService


def test_assemble_and_read_bytecode():
    spec = VectorIsaSpec(name="AsmTestSpec")
    inst1 = VectorInstruction(
        mnemonic="vadd_vv_0",
        format=InstructionFormat.OP_VV,
        funct6=0,
        funct3=0,
        binary_op=BinaryOp.ADD,
    )
    inst2 = VectorInstruction(
        mnemonic="vadd_vx_1",
        format=InstructionFormat.OP_VX,
        funct6=1,
        funct3=4,
        binary_op=BinaryOp.ADD,
    )
    spec.add_instruction(inst1)
    spec.add_instruction(inst2)

    asm_src = """
    # Vector code
    vadd_vv_0 v3, v2, v1
    vadd_vx_1 v4, v3, x1
    """

    assembler = VectorAssemblerService()
    words = assembler.assemble_program(spec, asm_src)
    assert len(words) == 2

    # Verify bitfields of word 0: vd=3, vs2=2, vs1=1
    w0 = words[0]
    assert (w0 & 0x7F) == 0x57
    assert ((w0 >> 7) & 0x1F) == 3
    assert ((w0 >> 20) & 0x1F) == 2
    assert ((w0 >> 15) & 0x1F) == 1

    # Test binary file read/write
    with tempfile.NamedTemporaryFile(suffix=".vbc", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        assembler.write_binary_bytecode(words, tmp_path)
        read_words = assembler.read_binary_bytecode(tmp_path)
        assert read_words == words
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
