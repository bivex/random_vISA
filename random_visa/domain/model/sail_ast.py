"""Sail AST Domain Model for formal ISA specification.

Sail is an imperative specification language designed to express the semantics
of instruction sets. This AST models the subset required for Vector ISAs.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Union
from random_visa.domain.model.types import BinaryOp, UnaryOp, ElementKind


# --- Sail Types ---

class SailType(ABC):
    """Base class for Sail Type definitions."""
    @abstractmethod
    def to_sail(self) -> str:
        pass


@dataclass(frozen=True)
class SailBitsType(SailType):
    width: int

    def to_sail(self) -> str:
        return f"bits({self.width})"


@dataclass(frozen=True)
class SailIntType(SailType):
    signed: bool = True

    def to_sail(self) -> str:
        return "int" if self.signed else "nat"


@dataclass(frozen=True)
class SailBoolType(SailType):
    def to_sail(self) -> str:
        return "bool"


@dataclass(frozen=True)
class SailUnitType(SailType):
    def to_sail(self) -> str:
        return "unit"


@dataclass(frozen=True)
class SailVectorType(SailType):
    element_type: SailType
    length: int

    def to_sail(self) -> str:
        return f"vector({self.length}, {self.element_type.to_sail()})"


# --- Sail Expressions ---

class SailExpr(ABC):
    """Base class for Sail expressions."""
    @abstractmethod
    def to_sail(self) -> str:
        pass


@dataclass(frozen=True)
class SailLiteralInt(SailExpr):
    value: int
    bits: Optional[int] = None

    def to_sail(self) -> str:
        if self.bits is not None:
            # Hex/binary bitvector literal in Sail
            return f"{hex(self.value)} : bits({self.bits})"
        return str(self.value)


@dataclass(frozen=True)
class SailLiteralBool(SailExpr):
    value: bool

    def to_sail(self) -> str:
        return "true" if self.value else "false"


@dataclass(frozen=True)
class SailVarExpr(SailExpr):
    name: str

    def to_sail(self) -> str:
        return self.name


@dataclass(frozen=True)
class SailBinaryExpr(SailExpr):
    left: SailExpr
    op: BinaryOp
    right: SailExpr
    kind: ElementKind = ElementKind.INT

    def to_sail(self) -> str:
        op_map = {
            BinaryOp.ADD: "+",
            BinaryOp.SUB: "-",
            BinaryOp.MUL: "*",
            BinaryOp.DIV: "/",
            BinaryOp.REM: "%",
            BinaryOp.AND: "&",
            BinaryOp.OR: "|",
            BinaryOp.XOR: "^",
            BinaryOp.SLL: "<<",
            BinaryOp.SRL: ">>",
            BinaryOp.SRA: ">>_s",
            BinaryOp.MIN: "min",
            BinaryOp.MAX: "max",
            BinaryOp.SADD: "+_sat",
            BinaryOp.SSUB: "-_sat",
        }
        symbol = op_map.get(self.op, "+")
        if self.op in (BinaryOp.MIN, BinaryOp.MAX):
            return f"{symbol}({self.left.to_sail()}, {self.right.to_sail()})"
        return f"({self.left.to_sail()} {symbol} {self.right.to_sail()})"


@dataclass(frozen=True)
class SailUnaryExpr(SailExpr):
    op: UnaryOp
    operand: SailExpr

    def to_sail(self) -> str:
        if self.op == UnaryOp.NEG:
            return f"(-{self.operand.to_sail()})"
        elif self.op == UnaryOp.NOT:
            return f"(~{self.operand.to_sail()})"
        else:
            return f"{self.op.value}({self.operand.to_sail()})"


@dataclass(frozen=True)
class SailVectorElemExpr(SailExpr):
    """Access element `index` of vector register `reg_name` with bit width `sew`."""
    reg_name: str
    index_expr: SailExpr
    sew: int

    def to_sail(self) -> str:
        return f"get_velem({self.reg_name}, {self.index_expr.to_sail()}, {self.sew})"


@dataclass(frozen=True)
class SailMaskCheckExpr(SailExpr):
    """Check if mask bit for index `i` is enabled (or vm=1 unmasked)."""
    mask_reg: str
    index_expr: SailExpr
    vm_is_unmasked: SailExpr

    def to_sail(self) -> str:
        return f"({self.vm_is_unmasked.to_sail()} == 1 | get_vmask_bit({self.mask_reg}, {self.index_expr.to_sail()}) == 1)"


@dataclass(frozen=True)
class SailCallExpr(SailExpr):
    """Function invocation expression in Sail."""
    func_name: str
    args: List[SailExpr] = field(default_factory=list)

    def to_sail(self) -> str:
        args_str = ", ".join(arg.to_sail() for arg in self.args)
        return f"{self.func_name}({args_str})"


# --- Sail Statements ---

class SailStmt(ABC):
    """Base class for Sail statements."""
    @abstractmethod
    def to_sail(self, indent: int = 0) -> str:
        pass


@dataclass
class SailLetStmt(SailStmt):
    var_name: str
    expr: SailExpr
    var_type: Optional[SailType] = None

    def to_sail(self, indent: int = 0) -> str:
        pad = " " * indent
        type_annot = f" : {self.var_type.to_sail()}" if self.var_type else ""
        return f"{pad}let {self.var_name}{type_annot} = {self.expr.to_sail()};"


@dataclass
class SailAssignStmt(SailStmt):
    target: str
    expr: SailExpr

    def to_sail(self, indent: int = 0) -> str:
        pad = " " * indent
        return f"{pad}{self.target} = {self.expr.to_sail()};"


@dataclass
class SailSetVectorElemStmt(SailStmt):
    reg_name: str
    index_expr: SailExpr
    value_expr: SailExpr
    sew: int

    def to_sail(self, indent: int = 0) -> str:
        pad = " " * indent
        return f"{pad}set_velem({self.reg_name}, {self.index_expr.to_sail()}, {self.sew}, {self.value_expr.to_sail()});"


@dataclass
class SailIfStmt(SailStmt):
    condition: SailExpr
    then_branch: List[SailStmt]
    else_branch: List[SailStmt] = field(default_factory=list)

    def to_sail(self, indent: int = 0) -> str:
        pad = " " * indent
        lines = [f"{pad}if {self.condition.to_sail()} then {{"]
        for stmt in self.then_branch:
            lines.append(stmt.to_sail(indent + 2))
        if self.else_branch:
            lines.append(f"{pad}}} else {{")
            for stmt in self.else_branch:
                lines.append(stmt.to_sail(indent + 2))
        lines.append(f"{pad}}}")
        return "\n".join(lines)


@dataclass
class SailVectorLoopStmt(SailStmt):
    """Iterate over active elements 0 <= i < vl."""
    loop_var: str
    bound_expr: SailExpr
    body: List[SailStmt]

    def to_sail(self, indent: int = 0) -> str:
        pad = " " * indent
        lines = [f"{pad}foreach ({self.loop_var} from 0 to ({self.bound_expr.to_sail()} - 1)) {{"]
        for stmt in self.body:
            lines.append(stmt.to_sail(indent + 2))
        lines.append(f"{pad}}};")
        return "\n".join(lines)


@dataclass
class SailFunctionDef:
    name: str
    params: List[tuple[str, SailType]]
    return_type: SailType
    body: List[SailStmt]

    def to_sail(self, indent: int = 0) -> str:
        pad = " " * indent
        params_str = ", ".join(f"{name}: {t.to_sail()}" for name, t in self.params)
        lines = [
            f"{pad}val {self.name} : ({', '.join(t.to_sail() for _, t in self.params)}) -> {self.return_type.to_sail()}",
            f"{pad}function {self.name}({params_str}) = {{",
        ]
        for stmt in self.body:
            lines.append(stmt.to_sail(indent + 2))
        lines.append(f"{pad}}}")
        return "\n".join(lines)
