"""Inbound Adapter: ISO C++14 ANTLR4 Parser and AST Inspector."""

from typing import List, Dict, Any, Optional
from antlr4 import InputStream, CommonTokenStream
from random_visa.adapters.inbound.parser.antlr.CPP14Lexer import CPP14Lexer
from random_visa.adapters.inbound.parser.antlr.CPP14Parser import CPP14Parser
from random_visa.adapters.inbound.parser.antlr.CPP14Visitor import CPP14Visitor


class CppCodeInspectorVisitor(CPP14Visitor):
    """Visitor that inspects C++ parse trees and extracts structural declarations."""

    def __init__(self):
        super().__init__()
        self.classes: List[str] = []
        self.functions: List[str] = []
        self.namespaces: List[str] = []
        self.templates: List[str] = []

    def visitClassSpecifier(self, ctx: CPP14Parser.ClassSpecifierContext):
        if ctx.classHead() and ctx.classHead().classHeadName():
            class_name = ctx.classHead().classHeadName().getText()
            self.classes.append(class_name)
        return self.visitChildren(ctx)

    def visitFunctionDefinition(self, ctx: CPP14Parser.FunctionDefinitionContext):
        if ctx.declarator():
            func_name = ctx.declarator().getText()
            func_name = func_name.split('(')[0].replace('*', '').replace('&', '').strip()
            self.functions.append(func_name)
        return self.visitChildren(ctx)

    def visitNamespaceDefinition(self, ctx: CPP14Parser.NamespaceDefinitionContext):
        if ctx.ID():
            ns_name = ctx.ID().getText()
            self.namespaces.append(ns_name)
        return self.visitChildren(ctx)

    def visitTemplateDeclaration(self, ctx: CPP14Parser.TemplateDeclarationContext):
        self.templates.append(ctx.getText())
        return self.visitChildren(ctx)


class AntlrCppParserAdapter:
    """Inbound adapter for parsing C++ source code with the official ISO C++ ANTLR4 grammar."""

    @staticmethod
    def parse_cpp_source(cpp_code: str) -> Dict[str, Any]:
        """Parse C++ source string and return extracted architectural elements."""
        input_stream = InputStream(cpp_code)
        lexer = CPP14Lexer(input_stream)
        tokens = CommonTokenStream(lexer)
        parser = CPP14Parser(tokens)

        tree = parser.translationUnit()
        visitor = CppCodeInspectorVisitor()
        visitor.visit(tree)

        return {
            "syntax_errors": parser.getNumberOfSyntaxErrors(),
            "classes": visitor.classes,
            "functions": visitor.functions,
            "namespaces": visitor.namespaces,
            "templates_count": len(visitor.templates),
            "tree": tree,
        }

    @staticmethod
    def parse_cpp_file(filepath: str) -> Dict[str, Any]:
        """Parse a .cpp or .hpp file from disk."""
        with open(filepath, "r", encoding="utf-8") as f:
            return AntlrCppParserAdapter.parse_cpp_source(f.read())
