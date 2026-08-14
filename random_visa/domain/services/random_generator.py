"""Domain Service: Random Sail V-ISA Generator / Synthesizer."""

import random
from typing import Optional, List, Set, Tuple
from random_visa.domain.model.types import (
    SEW, LMUL, ElementKind, InstructionFormat, BinaryOp, UnaryOp
)
from random_visa.domain.model.vector_config import VectorConfig
from random_visa.domain.model.instruction import VectorInstruction
from random_visa.domain.model.isa_spec import VectorIsaSpec
from random_visa.domain.events.events import InstructionSynthesizedEvent, IsaSpecCompletedEvent


class RandomVisaGeneratorService:
    """Domain service for generating randomized, syntactically and semantically sound V-ISA specifications."""

    AVAILABLE_BINARY_OPS = [
        (BinaryOp.ADD, "add", [InstructionFormat.OP_VV, InstructionFormat.OP_VX, InstructionFormat.OP_VI]),
        (BinaryOp.SUB, "sub", [InstructionFormat.OP_VV, InstructionFormat.OP_VX]),
        (BinaryOp.MUL, "mul", [InstructionFormat.OP_VV, InstructionFormat.OP_VX]),
        (BinaryOp.AND, "and", [InstructionFormat.OP_VV, InstructionFormat.OP_VX, InstructionFormat.OP_VI]),
        (BinaryOp.OR, "or", [InstructionFormat.OP_VV, InstructionFormat.OP_VX, InstructionFormat.OP_VI]),
        (BinaryOp.XOR, "xor", [InstructionFormat.OP_VV, InstructionFormat.OP_VX, InstructionFormat.OP_VI]),
        (BinaryOp.SLL, "sll", [InstructionFormat.OP_VV, InstructionFormat.OP_VX, InstructionFormat.OP_VI]),
        (BinaryOp.SRL, "srl", [InstructionFormat.OP_VV, InstructionFormat.OP_VX, InstructionFormat.OP_VI]),
        (BinaryOp.SRA, "sra", [InstructionFormat.OP_VV, InstructionFormat.OP_VX, InstructionFormat.OP_VI]),
        (BinaryOp.MIN, "min", [InstructionFormat.OP_VV, InstructionFormat.OP_VX]),
        (BinaryOp.MAX, "max", [InstructionFormat.OP_VV, InstructionFormat.OP_VX]),
        (BinaryOp.SADD, "sadd", [InstructionFormat.OP_VV, InstructionFormat.OP_VX]),
        (BinaryOp.SSUB, "ssub", [InstructionFormat.OP_VV, InstructionFormat.OP_VX]),
    ]

    AVAILABLE_UNARY_OPS = [
        (UnaryOp.NEG, "neg", [InstructionFormat.OP_MVV]),
        (UnaryOp.NOT, "not", [InstructionFormat.OP_MVV]),
        (UnaryOp.ABS, "abs", [InstructionFormat.OP_MVV]),
        (UnaryOp.CLZ, "clz", [InstructionFormat.OP_MVV]),
        (UnaryOp.CTZ, "ctz", [InstructionFormat.OP_MVV]),
        (UnaryOp.CPOP, "cpop", [InstructionFormat.OP_MVV]),
    ]

    def __init__(self, seed: Optional[int] = None) -> None:
        self.rng = random.Random(seed)

    def generate_spec(
        self,
        name: str = "RVV_Custom_ISA",
        num_instructions: int = 16,
        config: Optional[VectorConfig] = None,
    ) -> Tuple[VectorIsaSpec, List[object]]:
        """Synthesize a complete randomized Vector ISA specification."""
        if config is None:
            config = VectorConfig(vlen=128, elen=64, default_sew=SEW.E32, default_lmul=LMUL.M1)

        spec = VectorIsaSpec(name=name, version="1.0-synth", config=config)
        events: List[object] = []
        allocated_encodings: Set[Tuple[int, int]] = set()  # (funct6, funct3)

        funct6_counter = 0

        # Generate a diverse suite of vector instructions
        for i in range(num_instructions):
            is_binary = self.rng.random() > 0.25

            if is_binary:
                bin_op, op_name, formats = self.rng.choice(self.AVAILABLE_BINARY_OPS)
                fmt = self.rng.choice(formats)
                funct3 = self._format_to_funct3(fmt)
                funct6 = self._alloc_funct6(allocated_encodings, funct3, funct6_counter)
                funct6_counter = (funct6 + 1) % 64

                suffix = self._format_to_suffix(fmt)
                mnemonic = f"v{op_name}_{suffix}_{i}"
                desc = f"Randomized vector {op_name} operation ({fmt.value})"

                inst = VectorInstruction(
                    mnemonic=mnemonic,
                    format=fmt,
                    funct6=funct6,
                    funct3=funct3,
                    opcode=0x57,
                    binary_op=bin_op,
                    element_kind=ElementKind.INT,
                    description=desc,
                )
            else:
                un_op, op_name, formats = self.rng.choice(self.AVAILABLE_UNARY_OPS)
                fmt = self.rng.choice(formats)
                funct3 = self._format_to_funct3(fmt)
                funct6 = self._alloc_funct6(allocated_encodings, funct3, funct6_counter)
                funct6_counter = (funct6 + 1) % 64

                suffix = self._format_to_suffix(fmt)
                mnemonic = f"v{op_name}_{suffix}_{i}"
                desc = f"Randomized unary vector {op_name} operation"

                inst = VectorInstruction(
                    mnemonic=mnemonic,
                    format=fmt,
                    funct6=funct6,
                    funct3=funct3,
                    opcode=0x57,
                    unary_op=un_op,
                    element_kind=ElementKind.INT,
                    description=desc,
                )

            spec.add_instruction(inst)
            allocated_encodings.add((inst.funct6, inst.funct3))
            events.append(
                InstructionSynthesizedEvent(
                    mnemonic=inst.mnemonic,
                    funct6=inst.funct6,
                    funct3=inst.funct3,
                    format_name=inst.format.value,
                )
            )

        events.append(
            IsaSpecCompletedEvent(
                spec_name=spec.name,
                instruction_count=len(spec.instructions),
                vlen=spec.config.vlen,
            )
        )
        return spec, events

    def _alloc_funct6(self, allocated: Set[Tuple[int, int]], funct3: int, start: int) -> int:
        for offset in range(64):
            candidate = (start + offset) % 64
            if (candidate, funct3) not in allocated:
                return candidate
        raise RuntimeError("Encoding space exhausted for funct3=" + str(funct3))

    def _format_to_funct3(self, fmt: InstructionFormat) -> int:
        if fmt == InstructionFormat.OP_VV:
            return 0b000  # OPIVV
        elif fmt == InstructionFormat.OP_VX:
            return 0b100  # OPIVX
        elif fmt == InstructionFormat.OP_VI:
            return 0b011  # OPIVI
        elif fmt == InstructionFormat.OP_MVV:
            return 0b010  # OPMVV
        elif fmt == InstructionFormat.OP_RED:
            return 0b001  # OPFVV / OPRED
        return 0b000

    def _format_to_suffix(self, fmt: InstructionFormat) -> str:
        if fmt == InstructionFormat.OP_VV:
            return "vv"
        elif fmt == InstructionFormat.OP_VX:
            return "vx"
        elif fmt == InstructionFormat.OP_VI:
            return "vi"
        elif fmt == InstructionFormat.OP_MVV:
            return "m"
        elif fmt == InstructionFormat.OP_RED:
            return "vs"
        return "v"
