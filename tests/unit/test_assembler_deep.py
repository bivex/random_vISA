"""Deep unit tests for Vector Assembler Service and Bytecode binary formats."""

import pytest
from random_visa.domain.services.random_generator import RandomVisaGeneratorService
from random_visa.domain.services.assembler import VectorAssemblerService


@pytest.fixture
def sample_spec():
    from random_visa.domain.model.vector_config import VectorConfig
    gen_service = RandomVisaGeneratorService(seed=1234)
    spec, _ = gen_service.generate_spec(name="AsmTest_ISA", num_instructions=12, config=VectorConfig(vlen=128))
    return spec


def test_assemble_various_formats(sample_spec):
    assembler = VectorAssemblerService()
    
    # Find instructions of different formats
    inst_vv = next(inst for inst in sample_spec.instructions if inst.format.value == "OPIVV")
    inst_vx = next((inst for inst in sample_spec.instructions if inst.format.value == "OPIVX"), None)
    inst_vi = next((inst for inst in sample_spec.instructions if inst.format.value == "OPIVI"), None)

    lines = [f"{inst_vv.mnemonic} v4, v2, v1"]
    if inst_vx:
        lines.append(f"{inst_vx.mnemonic} v5, v2, x1")
    if inst_vi:
        lines.append(f"{inst_vi.mnemonic} v6, v2, 3")

    asm_text = "\n".join(lines)
    words = assembler.assemble_program(sample_spec, asm_text)
    assert len(words) == len(lines)

    for word in words:
        assert (word & 0x7F) == 0x57  # Standard RISC-V Vector opcode


def test_assemble_with_mask_modifier(sample_spec):
    assembler = VectorAssemblerService()
    inst = sample_spec.instructions[0]

    # Unmasked (default vm=1)
    word_unmasked = assembler.assemble_line(sample_spec, f"{inst.mnemonic} v4, v2, v1")
    vm_unmasked = (word_unmasked >> 25) & 0x1
    assert vm_unmasked == 1

    # Masked (vm=0 with v0.t)
    word_masked = assembler.assemble_line(sample_spec, f"{inst.mnemonic} v4, v2, v1, v0.t")
    vm_masked = (word_masked >> 25) & 0x1
    assert vm_masked == 0


def test_assemble_invalid_mnemonic(sample_spec):
    from random_visa.domain.services.assembler import AssemblySyntaxError
    assembler = VectorAssemblerService()
    with pytest.raises(AssemblySyntaxError, match="Unknown instruction"):
        assembler.assemble_line(sample_spec, "vnonexistent v1, v2, v3")


def test_assemble_invalid_register(sample_spec):
    from random_visa.domain.services.assembler import AssemblySyntaxError
    assembler = VectorAssemblerService()
    inst = sample_spec.instructions[0]
    with pytest.raises(AssemblySyntaxError, match="Invalid register"):
        assembler.assemble_line(sample_spec, f"{inst.mnemonic} v35, v2, v1")


def test_assemble_immediate_bounds(sample_spec):
    assembler = VectorAssemblerService()
    inst_vi = next((inst for inst in sample_spec.instructions if inst.format.value == "OPIVI"), None)
    if inst_vi:
        # Valid bounds: -16 to 15
        w1 = assembler.assemble_line(sample_spec, f"{inst_vi.mnemonic} v1, v2, 15")
        assert w1 is not None
        w2 = assembler.assemble_line(sample_spec, f"{inst_vi.mnemonic} v1, v2, -16")
        assert w2 is not None
