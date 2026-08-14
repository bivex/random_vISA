"""Vector Instruction Aggregate and Encoding definitions."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from random_visa.domain.model.types import (
    InstructionFormat, BinaryOp, UnaryOp, ElementKind, SEW
)
from random_visa.domain.model.sail_ast import (
    SailFunctionDef, SailBitsType, SailVectorLoopStmt, SailIfStmt,
    SailLetStmt, SailVectorElemExpr, SailSetVectorElemStmt, SailVarExpr,
    SailMaskCheckExpr, SailBinaryExpr, SailUnaryExpr, SailLiteralInt, SailUnitType
)


@dataclass
class VectorInstruction:
    """Vector Instruction Aggregate Root."""
    mnemonic: str
    format: InstructionFormat
    funct6: int
    funct3: int
    opcode: int = 0x57  # Standard RISC-V Vector Opcode
    binary_op: Optional[BinaryOp] = None
    unary_op: Optional[UnaryOp] = None
    element_kind: ElementKind = ElementKind.INT
    is_widening: bool = False
    is_reduction: bool = False
    description: str = ""
    sail_function: Optional[SailFunctionDef] = None

    def __post_init__(self) -> None:
        if self.sail_function is None:
            self.sail_function = self._synthesize_sail_function()

    @property
    def full_name(self) -> str:
        return f"{self.mnemonic.upper()}"

    def encode(self, vd: int, vs2: int, vs1_or_rs1_or_imm: int, vm: int = 1) -> int:
        """Encode 32-bit RISC-V V-ISA instruction word."""
        # 31:26 funct6 | 25 vm | 24:20 vs2 | 19:15 vs1/rs1/imm | 14:12 funct3 | 11:7 vd | 6:0 opcode
        f6 = (self.funct6 & 0x3F) << 26
        m = (vm & 0x1) << 25
        v2 = (vs2 & 0x1F) << 20
        v1 = (vs1_or_rs1_or_imm & 0x1F) << 15
        f3 = (self.funct3 & 0x7) << 12
        d = (vd & 0x1F) << 7
        op = (self.opcode & 0x7F)
        return f6 | m | v2 | v1 | f3 | d | op

    def _synthesize_sail_function(self) -> SailFunctionDef:
        """Synthesize canonical Sail formal execution specification for this instruction."""
        fn_name = f"execute_{self.mnemonic}"
        params = [
            ("vd_idx", SailBitsType(5)),
            ("vs2_idx", SailBitsType(5)),
            ("vs1_or_imm", SailBitsType(5)),
            ("vm", SailBitsType(1)),
        ]
        
        loop_var = "i"
        loop_body = []

        # Mask check: if vm == 1 or mask[i] == 1
        mask_cond = SailMaskCheckExpr("v0", SailVarExpr(loop_var), SailVarExpr("vm"))
        
        # Read vs2[i]
        elem_vs2 = SailVectorElemExpr("vs2", SailVarExpr(loop_var), 32)
        loop_body.append(SailLetStmt("op2", elem_vs2))

        # Operand 1 source based on format
        if self.format == InstructionFormat.OP_VV:
            elem_vs1 = SailVectorElemExpr("vs1", SailVarExpr(loop_var), 32)
            loop_body.append(SailLetStmt("op1", elem_vs1))
            rhs_expr = SailVarExpr("op1")
        elif self.format == InstructionFormat.OP_VX:
            loop_body.append(SailLetStmt("op1", SailVarExpr("rs1_val")))
            rhs_expr = SailVarExpr("op1")
        elif self.format == InstructionFormat.OP_VI:
            loop_body.append(SailLetStmt("op1", SailVarExpr("simm5")))
            rhs_expr = SailVarExpr("op1")
        else:
            elem_vs1 = SailVectorElemExpr("vs1", SailVarExpr(loop_var), 32)
            loop_body.append(SailLetStmt("op1", elem_vs1))
            rhs_expr = SailVarExpr("op1")

        # Compute result element
        if self.binary_op:
            compute_expr = SailBinaryExpr(
                left=SailVarExpr("op2"),
                op=self.binary_op,
                right=rhs_expr,
                kind=self.element_kind
            )
        elif self.unary_op:
            compute_expr = SailUnaryExpr(
                op=self.unary_op,
                operand=SailVarExpr("op2")
            )
        else:
            compute_expr = SailVarExpr("op2")

        loop_body.append(SailLetStmt("res_elem", compute_expr))
        loop_body.append(SailSetVectorElemStmt("vd", SailVarExpr(loop_var), SailVarExpr("res_elem"), 32))

        masked_if = SailIfStmt(
            condition=mask_cond,
            then_branch=loop_body
        )

        vector_loop = SailVectorLoopStmt(
            loop_var=loop_var,
            bound_expr=SailVarExpr("vl"),
            body=[masked_if]
        )

        return SailFunctionDef(
            name=fn_name,
            params=params,
            return_type=SailUnitType(),
            body=[vector_loop]
        )
