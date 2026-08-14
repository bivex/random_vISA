"""Vector ISA Specification Aggregate Root."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from random_visa.domain.model.vector_config import VectorConfig
from random_visa.domain.model.instruction import VectorInstruction


@dataclass
class VectorIsaSpec:
    """Aggregate Root representing a complete Vector ISA specification."""
    name: str
    version: str = "1.0-draft"
    config: VectorConfig = field(default_factory=VectorConfig)
    instructions: List[VectorInstruction] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)

    def add_instruction(self, instruction: VectorInstruction) -> None:
        # Check collision on (funct6, funct3, opcode)
        for existing in self.instructions:
            if (existing.funct6 == instruction.funct6 and 
                existing.funct3 == instruction.funct3 and 
                existing.opcode == instruction.opcode):
                raise ValueError(
                    f"Instruction encoding collision between {existing.mnemonic} "
                    f"and {instruction.mnemonic} (funct6={instruction.funct6}, funct3={instruction.funct3})"
                )
            if existing.mnemonic == instruction.mnemonic:
                raise ValueError(f"Duplicate mnemonic: {instruction.mnemonic}")
        self.instructions.append(instruction)

    def get_by_mnemonic(self, mnemonic: str) -> Optional[VectorInstruction]:
        for inst in self.instructions:
            if inst.mnemonic == mnemonic:
                return inst
        return None

    def decode(self, word: int) -> Optional[VectorInstruction]:
        """Decode a 32-bit instruction word."""
        opcode = word & 0x7F
        funct3 = (word >> 12) & 0x7
        funct6 = (word >> 26) & 0x3F
        for inst in self.instructions:
            if inst.opcode == opcode and inst.funct3 == funct3 and inst.funct6 == funct6:
                return inst
        return None

    def to_sail_specification(self) -> str:
        """Render the complete formal Sail specification file."""
        lines = [
            f"/* ========================================================================= */",
            f"/* Sail Formal Specification for {self.name} (V-ISA)                         */",
            f"/* Version: {self.version}                                                   */",
            f"/* Generated via Hexagonal DDD random_vISA Synthesizer                       */",
            f"/* ========================================================================= */",
            "",
            "default Order dec",
            "$include <prelude.sail>",
            "",
            f"let VLEN : int = {self.config.vlen}",
            f"let ELEN : int = {self.config.elen}",
            f"let NUM_VREGS : int = {self.config.num_vregs}",
            "",
            "type vreg_idx = range(0, 31)",
            "type vreg_t = bits(VLEN)",
            "",
            "register v0  : vreg_t",
            "register v1  : vreg_t",
            "register v2  : vreg_t",
            "register v3  : vreg_t",
            "register vl  : bits(64)",
            "register vtype : bits(64)",
            "",
            "val get_velem : (vreg_t, int, int) -> bits(32)",
            "val set_velem : (vreg_t, int, int, bits(32)) -> unit",
            "val get_vmask_bit : (vreg_t, int) -> bits(1)",
            "",
        ]

        for inst in self.instructions:
            lines.append(f"/* Instruction: {inst.mnemonic} ({inst.format.value}) */")
            if inst.description:
                lines.append(f"/* {inst.description} */")
            if inst.sail_function:
                lines.append(inst.sail_function.to_sail())
            lines.append("")

        return "\n".join(lines)
