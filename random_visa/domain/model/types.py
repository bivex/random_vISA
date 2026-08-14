"""Domain Types and Enums for Vector ISA (V-ISA) Specification."""

from enum import Enum, auto


class SEW(int, Enum):
    """Standard Element Width in bits."""
    E8 = 8
    E16 = 16
    E32 = 32
    E64 = 64

    @property
    def byte_width(self) -> int:
        return self.value // 8

    @property
    def c_type(self) -> str:
        return f"int{self.value}_t"

    @property
    def c_utype(self) -> str:
        return f"uint{self.value}_t"


class LMUL(Enum):
    """Vector Register Multiplier."""
    MF8 = 0.125
    MF4 = 0.25
    MF2 = 0.5
    M1 = 1.0
    M2 = 2.0
    M4 = 4.0
    M8 = 8.0

    @property
    def multiplier_val(self) -> float:
        return self.value

    @property
    def num_registers(self) -> int:
        return max(1, int(self.value))


class ElementKind(Enum):
    """Semantic data type for vector operations."""
    INT = "int"
    UINT = "uint"
    FLOAT = "float"
    BITVECTOR = "bits"


class InstructionFormat(Enum):
    """Encoding and Operand Layout for Vector Instructions."""
    OP_VV = "OPIVV"  # vd, vs2, vs1, vm (vector-vector)
    OP_VX = "OPIVX"  # vd, vs2, rs1, vm (vector-scalar)
    OP_VI = "OPIVI"  # vd, vs2, imm, vm (vector-immediate)
    OP_RED = "OPRED" # vd, vs2, vs1, vm (vector-reduction)
    OP_MVV = "OPMVV" # vd, vs2, vs1, vm (vector-mask)
    OP_MEM_LOAD = "VLE"  # vd, (rs1), vm
    OP_MEM_STORE = "VSE" # vs3, (rs1), vm
    OP_WIDENING = "OPWVV" # vd_wide, vs2, vs1, vm


class BinaryOp(Enum):
    """Vector Binary Operator."""
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    REM = "%"
    AND = "&"
    OR = "|"
    XOR = "^"
    SLL = "<<"
    SRL = ">>"
    SRA = ">>_s"
    MIN = "min"
    MAX = "max"
    SADD = "+_sat"
    SSUB = "-_sat"


class UnaryOp(Enum):
    """Vector Unary Operator."""
    NEG = "-"
    NOT = "~"
    ABS = "abs"
    CLZ = "clz"
    CTZ = "ctz"
    CPOP = "cpop"


class TailPolicy(Enum):
    UNDISTURBED = "tu"
    AGNOSTIC = "ta"


class MaskPolicy(Enum):
    UNDISTURBED = "mu"
    AGNOSTIC = "ma"
