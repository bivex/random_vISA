"""Unit tests for Sail specification writer and ANTLR4 parser round-trip."""

import tempfile
import os
from random_visa.domain.services.random_generator import RandomVisaGeneratorService
from random_visa.adapters.outbound.sail.sail_file_adapter import SailFileAdapter
from random_visa.adapters.inbound.parser.sail_antlr_adapter import AntlrSailParserAdapter


def test_sail_generation_and_parsing_roundtrip(tmp_path):
    from random_visa.domain.model.vector_config import VectorConfig
    gen_service = RandomVisaGeneratorService(seed=4242)
    spec, _ = gen_service.generate_spec(name="RoundTrip_ISA", num_instructions=16, config=VectorConfig(vlen=256))

    assert len(spec.instructions) == 16
    assert spec.config.vlen == 256

    sail_file = str(tmp_path / "roundtrip.sail")
    writer = SailFileAdapter()
    writer.write_spec(spec, sail_file)
    assert os.path.exists(sail_file)

    # Parse back using ANTLR4 Sail parser
    parser = AntlrSailParserAdapter()
    parsed_spec = parser.parse_sail_file(sail_file, spec_name="RoundTrip_ISA")

    assert parsed_spec.name == "RoundTrip_ISA"
    assert parsed_spec.config.vlen == 256
    assert len(parsed_spec.instructions) == 16

    # Verify instruction matching
    for orig_inst, parsed_inst in zip(spec.instructions, parsed_spec.instructions):
        assert orig_inst.mnemonic == parsed_inst.mnemonic
        assert orig_inst.format.value == parsed_inst.format.value
        assert orig_inst.funct6 == parsed_inst.funct6
        assert orig_inst.funct3 == parsed_inst.funct3
        if orig_inst.binary_op:
            assert orig_inst.binary_op.name == parsed_inst.binary_op.name
        if orig_inst.unary_op:
            assert orig_inst.unary_op.name == parsed_inst.unary_op.name
