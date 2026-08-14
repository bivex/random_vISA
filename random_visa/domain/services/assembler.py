"""Domain Service: Vector Assembler & Bytecode Compiler for synthesized V-ISAs."""

import re
import struct
from typing import List, Optional, Tuple
from random_visa.domain.model.types import InstructionFormat
from random_visa.domain.model.isa_spec import VectorIsaSpec
from random_visa.domain.model.instruction import VectorInstruction


class AssemblySyntaxError(Exception):
    """Raised when parsing vector assembly fails."""
    pass


class VectorAssemblerService:
    """Domain service for assembling human-readable vector assembly into 32-bit binary bytecode."""

    @staticmethod
    def parse_reg(reg_str: str) -> int:
        """Parse register identifier like 'v3', 'x1', '3' into integer index."""
        cleaned = reg_str.strip().lower()
        if cleaned.startswith(('v', 'x', 'f')):
            cleaned = cleaned[1:]
        try:
            val = int(cleaned)
            if not (0 <= val <= 31):
                raise ValueError()
            return val
        except Exception:
            raise AssemblySyntaxError(f"Invalid register operand: '{reg_str}' (must be v0-v31 or x0-x31)")

    @staticmethod
    def parse_imm(imm_str: str) -> int:
        """Parse 5-bit signed/unsigned immediate integer."""
        cleaned = imm_str.strip()
        try:
            return int(cleaned, 0) & 0x1F
        except Exception:
            raise AssemblySyntaxError(f"Invalid immediate operand: '{imm_str}'")

    def assemble_line(self, spec: VectorIsaSpec, line: str) -> Optional[int]:
        """Assemble a single line of assembly into a 32-bit instruction word."""
        # Strip comments (# or //)
        line = re.sub(r'(#|//).*$', '', line).strip()
        if not line:
            return None

        # Format: <mnemonic> <op1>, <op2>, <op3>, [vm]
        parts = re.split(r'[\s,]+', line)
        mnemonic = parts[0].strip().lower()

        inst = spec.get_by_mnemonic(mnemonic)
        if not inst:
            # Try case-insensitive matching
            for candidate in spec.instructions:
                if candidate.mnemonic.lower() == mnemonic:
                    inst = candidate
                    break
        if not inst:
            raise AssemblySyntaxError(f"Unknown instruction mnemonic '{mnemonic}' in ISA spec '{spec.name}'")

        operands = parts[1:]

        # Handle mask operand (vm=1 default unmasked, vm=0 masked by v0)
        vm = 1
        if operands and operands[-1] in ('v0.t', 'vm=0', 'masked'):
            vm = 0
            operands = operands[:-1]

        vd = 0
        vs2 = 0
        vs1_or_rs1_or_imm = 0

        if inst.format == InstructionFormat.OP_VV or inst.format == InstructionFormat.OP_RED or inst.format == InstructionFormat.OP_WIDENING:
            if len(operands) < 3:
                raise AssemblySyntaxError(f"Instruction {mnemonic} expects 3 operands: vd, vs2, vs1")
            vd = self.parse_reg(operands[0])
            vs2 = self.parse_reg(operands[1])
            vs1_or_rs1_or_imm = self.parse_reg(operands[2])

        elif inst.format == InstructionFormat.OP_VX:
            if len(operands) < 3:
                raise AssemblySyntaxError(f"Instruction {mnemonic} expects 3 operands: vd, vs2, rs1")
            vd = self.parse_reg(operands[0])
            vs2 = self.parse_reg(operands[1])
            vs1_or_rs1_or_imm = self.parse_reg(operands[2])

        elif inst.format == InstructionFormat.OP_VI:
            if len(operands) < 3:
                raise AssemblySyntaxError(f"Instruction {mnemonic} expects 3 operands: vd, vs2, simm5")
            vd = self.parse_reg(operands[0])
            vs2 = self.parse_reg(operands[1])
            vs1_or_rs1_or_imm = self.parse_imm(operands[2])

        elif inst.format == InstructionFormat.OP_MVV:
            if len(operands) == 2:
                vd = self.parse_reg(operands[0])
                vs2 = self.parse_reg(operands[1])
                vs1_or_rs1_or_imm = 0
            elif len(operands) >= 3:
                vd = self.parse_reg(operands[0])
                vs2 = self.parse_reg(operands[1])
                vs1_or_rs1_or_imm = self.parse_reg(operands[2])
            else:
                raise AssemblySyntaxError(f"Instruction {mnemonic} expects 2 operands: vd, vs2")

        return inst.encode(vd=vd, vs2=vs2, vs1_or_rs1_or_imm=vs1_or_rs1_or_imm, vm=vm)

    def assemble_program(self, spec: VectorIsaSpec, source_text: str) -> List[int]:
        """Assemble multi-line assembly source text into a list of 32-bit bytecode words."""
        bytecode: List[int] = []
        for line_no, raw_line in enumerate(source_text.splitlines(), start=1):
            try:
                word = self.assemble_line(spec, raw_line)
                if word is not None:
                    bytecode.append(word)
            except AssemblySyntaxError as e:
                raise AssemblySyntaxError(f"Line {line_no}: {str(e)}")
        return bytecode

    @staticmethod
    def write_binary_bytecode(words: List[int], filepath: str) -> str:
        """Write 32-bit bytecode words to a binary file (.vbc / .bin)."""
        with open(filepath, "wb") as f:
            for w in words:
                f.write(struct.pack("<I", w))
        return filepath

    @staticmethod
    def read_binary_bytecode(filepath: str) -> List[int]:
        """Read 32-bit bytecode words from a binary file."""
        words: List[int] = []
        with open(filepath, "rb") as f:
            data = f.read()
            count = len(data) // 4
            for i in range(count):
                words.append(struct.unpack_from("<I", data, i * 4)[0])
        return words
