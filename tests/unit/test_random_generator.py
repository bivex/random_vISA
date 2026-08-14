"""Unit tests for Random V-ISA Synthesizer Domain Service."""

from random_visa.domain.services.random_generator import RandomVisaGeneratorService
from random_visa.domain.model.vector_config import VectorConfig


def test_random_spec_generation_deterministic():
    gen1 = RandomVisaGeneratorService(seed=42)
    spec1, events1 = gen1.generate_spec(name="SpecA", num_instructions=10)

    gen2 = RandomVisaGeneratorService(seed=42)
    spec2, events2 = gen2.generate_spec(name="SpecA", num_instructions=10)

    assert len(spec1.instructions) == 10
    assert len(spec2.instructions) == 10
    assert [i.mnemonic for i in spec1.instructions] == [i.mnemonic for i in spec2.instructions]
    assert [i.funct6 for i in spec1.instructions] == [i.funct6 for i in spec2.instructions]


def test_unique_encodings_guarantee():
    gen = RandomVisaGeneratorService(seed=999)
    spec, _ = gen.generate_spec(name="LargeSpec", num_instructions=24)
    assert len(spec.instructions) == 24

    encodings = {(i.funct6, i.funct3, i.opcode) for i in spec.instructions}
    assert len(encodings) == 24  # No collision allowed
