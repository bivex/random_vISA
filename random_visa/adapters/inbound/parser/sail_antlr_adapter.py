"""Inbound Adapter: ANTLR4-based Sail Specification Parser to Domain Model."""

import re
from typing import Optional, List, Dict, Any
from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker
from antlr4.error.ErrorListener import ErrorListener

from random_visa.domain.model.types import (
    SEW, LMUL, ElementKind, InstructionFormat, BinaryOp, UnaryOp
)
from random_visa.domain.model.vector_config import VectorConfig
from random_visa.domain.model.sail_ast import (
    SailType, SailBitsType, SailIntType, SailBoolType, SailUnitType,
    SailExpr, SailLiteralInt, SailLiteralBool, SailVarExpr, SailBinaryExpr,
    SailUnaryExpr, SailVectorElemExpr, SailMaskCheckExpr, SailCallExpr,
    SailStmt, SailLetStmt, SailAssignStmt, SailSetVectorElemStmt, SailIfStmt,
    SailVectorLoopStmt, SailFunctionDef
)
from random_visa.domain.model.instruction import VectorInstruction
from random_visa.domain.model.isa_spec import VectorIsaSpec
from random_visa.domain.ports.inbound.ports import SailParserPort

from random_visa.adapters.inbound.parser.antlr.SailLexer import SailLexer
from random_visa.adapters.inbound.parser.antlr.SailParser import SailParser
from random_visa.adapters.inbound.parser.antlr.SailVisitor import SailVisitor


class SailSyntaxException(Exception):
    """Raised when parsing Sail specification fails."""
    pass


class StrictErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SailSyntaxException(f"Sail Parse Error at line {line}:{column} - {msg}")


class SailToDomainVisitor(SailVisitor):
    """Walks the ANTLR4 Sail Parse Tree and constructs Domain VectorIsaSpec."""

    def __init__(self, spec_name: str = "Parsed_Sail_ISA") -> None:
        super().__init__()
        self.spec_name = spec_name
        self.vlen = 128
        self.elen = 64
        self.num_vregs = 32
        self.instructions: List[VectorInstruction] = []
        self.funct6_allocator = 0

    def visitLetDecl(self, ctx: SailParser.LetDeclContext):
        var_name = ctx.ID().getText()
        expr_val = ctx.expr().getText()
        if var_name == "VLEN" and expr_val.isdigit():
            self.vlen = int(expr_val)
        elif var_name == "ELEN" and expr_val.isdigit():
            self.elen = int(expr_val)
        elif var_name == "NUM_VREGS" and expr_val.isdigit():
            self.num_vregs = int(expr_val)
        return self.visitChildren(ctx)

    def visitFunctionDef(self, ctx: SailParser.FunctionDefContext):
        fn_name = ctx.ID().getText()
        
        # Mnemonic inference
        mnemonic = fn_name
        if mnemonic.startswith("execute_"):
            mnemonic = mnemonic[len("execute_"):]

        # Visit and convert parameter list
        params: List[tuple[str, SailType]] = []
        if ctx.paramList():
            for p_ctx in ctx.paramList().param():
                p_name = p_ctx.ID().getText()
                p_type = self.visit(p_ctx.typeRef())
                params.append((p_name, p_type or SailBitsType(5)))

        # Visit body statements
        body_stmts: List[SailStmt] = []
        for s_ctx in ctx.stmt():
            stmt_obj = self.visit(s_ctx)
            if stmt_obj:
                body_stmts.append(stmt_obj)

        # Inspect semantic operations from body
        bin_op, un_op, fmt = self._analyze_instruction_semantics(mnemonic, body_stmts)

        # Allocate unique funct6/funct3 encoding
        funct3 = 0b000
        if fmt == InstructionFormat.OP_VX:
            funct3 = 0b100
        elif fmt == InstructionFormat.OP_VI:
            funct3 = 0b011
        elif fmt == InstructionFormat.OP_MVV:
            funct3 = 0b010

        funct6 = self.funct6_allocator % 64
        self.funct6_allocator += 1

        fn_def = SailFunctionDef(
            name=fn_name,
            params=params,
            return_type=SailUnitType(),
            body=body_stmts,
        )

        inst = VectorInstruction(
            mnemonic=mnemonic,
            format=fmt,
            funct6=funct6,
            funct3=funct3,
            opcode=0x57,
            binary_op=bin_op,
            unary_op=un_op,
            element_kind=ElementKind.INT,
            description=f"Parsed from Sail function {fn_name}",
            sail_function=fn_def,
        )
        self.instructions.append(inst)
        return None

    def _analyze_instruction_semantics(self, mnemonic: str, stmts: List[SailStmt]):
        """Infer BinaryOp, UnaryOp and Format from mnemonic and AST."""
        fmt = InstructionFormat.OP_VV
        if "_vx" in mnemonic:
            fmt = InstructionFormat.OP_VX
        elif "_vi" in mnemonic:
            fmt = InstructionFormat.OP_VI
        elif "_m" in mnemonic:
            fmt = InstructionFormat.OP_MVV

        bin_op = None
        un_op = None

        # Infer from mnemonic keywords
        op_map = {
            "add": BinaryOp.ADD,
            "sub": BinaryOp.SUB,
            "mul": BinaryOp.MUL,
            "div": BinaryOp.DIV,
            "rem": BinaryOp.REM,
            "and": BinaryOp.AND,
            "or": BinaryOp.OR,
            "xor": BinaryOp.XOR,
            "sll": BinaryOp.SLL,
            "srl": BinaryOp.SRL,
            "sra": BinaryOp.SRA,
            "min": BinaryOp.MIN,
            "max": BinaryOp.MAX,
            "sadd": BinaryOp.SADD,
            "ssub": BinaryOp.SSUB,
        }
        for name, op in op_map.items():
            if f"v{name}" in mnemonic or f"_{name}_" in mnemonic:
                bin_op = op
                break

        unary_map = {
            "neg": UnaryOp.NEG,
            "not": UnaryOp.NOT,
            "abs": UnaryOp.ABS,
            "clz": UnaryOp.CLZ,
            "ctz": UnaryOp.CTZ,
            "cpop": UnaryOp.CPOP,
        }
        for name, op in unary_map.items():
            if f"v{name}" in mnemonic or f"_{name}_" in mnemonic:
                un_op = op
                break

        if bin_op is None and un_op is None:
            bin_op = BinaryOp.ADD  # default fallback

        return bin_op, un_op, fmt

    # --- Type visitor ---
    def visitBitsType(self, ctx: SailParser.BitsTypeContext):
        if ctx.INT_LITERAL():
            width = int(ctx.INT_LITERAL().getText())
        else:
            width = self.vlen
        return SailBitsType(width=width)

    def visitIntType(self, ctx: SailParser.IntTypeContext):
        return SailIntType(signed=True)

    def visitNatType(self, ctx: SailParser.NatTypeContext):
        return SailIntType(signed=False)

    def visitBoolType(self, ctx: SailParser.BoolTypeContext):
        return SailBoolType()

    def visitUnitType(self, ctx: SailParser.UnitTypeContext):
        return SailUnitType()

    def visitCustomType(self, ctx: SailParser.CustomTypeContext):
        return SailVarExpr(ctx.ID().getText())

    # --- Statement visitor ---
    def visitLetStmt(self, ctx: SailParser.LetStmtContext):
        var_name = ctx.ID().getText()
        expr_obj = self.visit(ctx.expr())
        type_obj = self.visit(ctx.typeRef()) if ctx.typeRef() else None
        return SailLetStmt(var_name=var_name, expr=expr_obj, var_type=type_obj)

    def visitAssignStmt(self, ctx: SailParser.AssignStmtContext):
        target = ctx.target.text
        expr_obj = self.visit(ctx.expr())
        return SailAssignStmt(target=target, expr=expr_obj)

    def visitForeachStmt(self, ctx: SailParser.ForeachStmtContext):
        loop_var = ctx.ID().getText()
        end_expr = self.visit(ctx.endExpr)
        body: List[SailStmt] = []
        for s_ctx in ctx.stmt():
            s = self.visit(s_ctx)
            if s:
                body.append(s)
        return SailVectorLoopStmt(loop_var=loop_var, bound_expr=end_expr, body=body)

    def visitIfStmt(self, ctx: SailParser.IfStmtContext):
        cond = self.visit(ctx.cond)
        then_stmts = [self.visit(s) for s in ctx.thenStmts if s]
        else_stmts = [self.visit(s) for s in ctx.elseStmts if s] if ctx.elseStmts else []
        return SailIfStmt(condition=cond, then_branch=then_stmts, else_branch=else_stmts)

    def visitCallStmt(self, ctx: SailParser.CallStmtContext):
        expr = self.visit(ctx.funcCallStmt)
        if isinstance(expr, SailCallExpr) and expr.func_name == "set_velem" and len(expr.args) >= 4:
            reg_name = expr.args[0].to_sail()
            index_expr = expr.args[1]
            val_expr = expr.args[3]
            return SailSetVectorElemStmt(reg_name=reg_name, index_expr=index_expr, value_expr=val_expr, sew=32)
        return SailAssignStmt(target="_", expr=expr)

    # --- Expression visitor ---
    def visitParenExpr(self, ctx: SailParser.ParenExprContext):
        return self.visit(ctx.expr())

    def visitUnaryExpr(self, ctx: SailParser.UnaryExprContext):
        op_text = ctx.op.text
        operand = self.visit(ctx.operand)
        op_enum = UnaryOp.NEG if op_text == '-' else UnaryOp.NOT
        return SailUnaryExpr(op=op_enum, operand=operand)

    def visitBinaryExpr(self, ctx: SailParser.BinaryExprContext):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        op_text = ctx.op.text
        
        op_map = {
            "+": BinaryOp.ADD,
            "-": BinaryOp.SUB,
            "*": BinaryOp.MUL,
            "/": BinaryOp.DIV,
            "%": BinaryOp.REM,
            "&": BinaryOp.AND,
            "|": BinaryOp.OR,
            "^": BinaryOp.XOR,
            "<<": BinaryOp.SLL,
            ">>": BinaryOp.SRL,
            ">>_s": BinaryOp.SRA,
            "+_sat": BinaryOp.SADD,
            "-_sat": BinaryOp.SSUB,
        }
        bin_op = op_map.get(op_text, BinaryOp.ADD)
        return SailBinaryExpr(left=left, op=bin_op, right=right)

    def visitCallExpr(self, ctx: SailParser.CallExprContext):
        func_name = ctx.ID().getText()
        args = [self.visit(e) for e in ctx.expr()] if ctx.expr() else []

        if func_name == "get_velem" and len(args) >= 2:
            reg_name = args[0].to_sail()
            idx = args[1]
            return SailVectorElemExpr(reg_name=reg_name, index_expr=idx, sew=32)
        elif func_name in ("min", "max") and len(args) == 2:
            op_enum = BinaryOp.MIN if func_name == "min" else BinaryOp.MAX
            return SailBinaryExpr(left=args[0], op=op_enum, right=args[1])
        elif func_name in ("clz", "ctz", "cpop") and len(args) == 1:
            un_enum = UnaryOp.CLZ if func_name == "clz" else (UnaryOp.CTZ if func_name == "ctz" else UnaryOp.CPOP)
            return SailUnaryExpr(op=un_enum, operand=args[0])

        return SailCallExpr(func_name=func_name, args=args)

    def visitCallExprRule(self, ctx: SailParser.CallExprRuleContext):
        return self.visit(ctx.callExpr())

    def visitHexExpr(self, ctx: SailParser.HexExprContext):
        val = int(ctx.HEX_LITERAL().getText(), 16)
        return SailLiteralInt(value=val)

    def visitIntExpr(self, ctx: SailParser.IntExprContext):
        val = int(ctx.INT_LITERAL().getText())
        return SailLiteralInt(value=val)

    def visitBoolExpr(self, ctx: SailParser.BoolExprContext):
        val = (ctx.BOOL_LITERAL().getText() == "true")
        return SailLiteralBool(value=val)

    def visitVarExpr(self, ctx: SailParser.VarExprContext):
        return SailVarExpr(name=ctx.ID().getText())


class AntlrSailParserAdapter(SailParserPort):
    """Adapter for parsing Sail formal specification files using ANTLR4."""

    def parse_sail_source(self, source_text: str, spec_name: str = "Parsed_Sail_ISA") -> VectorIsaSpec:
        input_stream = InputStream(source_text)
        lexer = SailLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(StrictErrorListener())

        token_stream = CommonTokenStream(lexer)
        parser = SailParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(StrictErrorListener())

        tree = parser.spec()

        visitor = SailToDomainVisitor(spec_name=spec_name)
        visitor.visit(tree)

        config = VectorConfig(
            vlen=visitor.vlen,
            elen=visitor.elen,
            num_vregs=visitor.num_vregs,
            default_sew=SEW.E32,
            default_lmul=LMUL.M1,
        )

        spec = VectorIsaSpec(
            name=spec_name,
            version="1.0-parsed",
            config=config,
        )

        for inst in visitor.instructions:
            spec.add_instruction(inst)

        return spec

    def parse_sail_file(self, file_path: str, spec_name: Optional[str] = None) -> VectorIsaSpec:
        name = spec_name or "Parsed_Sail_ISA"
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return self.parse_sail_source(content, spec_name=name)
