"""Inbound Adapter: ISO C11/C99 ANTLR4 Parser and AST Visitor."""

from typing import List, Dict, Any, Optional
from antlr4 import InputStream, CommonTokenStream
from random_visa.adapters.inbound.parser.antlr.CLexer import CLexer
from random_visa.adapters.inbound.parser.antlr.CParser import CParser
from random_visa.adapters.inbound.parser.antlr.CVisitor import CVisitor


class CCodeInspectorVisitor(CVisitor):
    """Visitor that inspects C parse trees and extracts structural declarations."""

    def __init__(self):
        super().__init__()
        self.functions: List[str] = []
        self.structs: List[str] = []
        self.typedefs: List[str] = []

    def visitFunctionDefinition(self, ctx: CParser.FunctionDefinitionContext):
        # Extract function name from declarator
        if ctx.declarator():
            func_name = ctx.declarator().getText()
            # Clean up pointer/parentheses
            func_name = func_name.split('(')[0].replace('*', '').strip()
            self.functions.append(func_name)
        return self.visitChildren(ctx)

    def visitStructOrUnionSpecifier(self, ctx: CParser.StructOrUnionSpecifierContext):
        if ctx.ID():
            struct_name = ctx.ID().getText()
            self.structs.append(struct_name)
        return self.visitChildren(ctx)

    def visitDeclaration(self, ctx: CParser.DeclarationContext):
        decl_text = ctx.getText()
        if decl_text.startswith("typedef"):
            self.typedefs.append(decl_text)
        return self.visitChildren(ctx)


class AntlrCParserAdapter:
    """Inbound adapter for parsing C source code with ANTLR4."""

    @staticmethod
    def parse_c_source(c_code: str) -> Dict[str, Any]:
        """Parse C source code and return extracted metadata."""
        input_stream = InputStream(c_code)
        lexer = CLexer(input_stream)
        tokens = CommonTokenStream(lexer)
        parser = CParser(tokens)

        tree = parser.compilationUnit()
        visitor = CCodeInspectorVisitor()
        visitor.visit(tree)

        return {
            "syntax_errors": parser.getNumberOfSyntaxErrors(),
            "functions": visitor.functions,
            "structs": visitor.structs,
            "typedefs": visitor.typedefs,
            "tree": tree,
        }

    @staticmethod
    def parse_c_file(filepath: str) -> Dict[str, Any]:
        """Parse a .c or .h file from disk."""
        with open(filepath, "r", encoding="utf-8") as f:
            return AntlrCParserAdapter.parse_c_source(f.read())
