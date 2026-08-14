# Generated from /Volumes/External/Code/random_vISA/random_visa/adapters/inbound/parser/antlr/Sail.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SailParser import SailParser
else:
    from SailParser import SailParser

# This class defines a complete generic visitor for a parse tree produced by SailParser.

class SailVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SailParser#spec.
    def visitSpec(self, ctx:SailParser.SpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#topLevelItem.
    def visitTopLevelItem(self, ctx:SailParser.TopLevelItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#defaultOrderDirective.
    def visitDefaultOrderDirective(self, ctx:SailParser.DefaultOrderDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#includeDirective.
    def visitIncludeDirective(self, ctx:SailParser.IncludeDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#includePath.
    def visitIncludePath(self, ctx:SailParser.IncludePathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#letDecl.
    def visitLetDecl(self, ctx:SailParser.LetDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#typeDecl.
    def visitTypeDecl(self, ctx:SailParser.TypeDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#registerDecl.
    def visitRegisterDecl(self, ctx:SailParser.RegisterDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#valDecl.
    def visitValDecl(self, ctx:SailParser.ValDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#functionDef.
    def visitFunctionDef(self, ctx:SailParser.FunctionDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#paramList.
    def visitParamList(self, ctx:SailParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#param.
    def visitParam(self, ctx:SailParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#BitsType.
    def visitBitsType(self, ctx:SailParser.BitsTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#IntType.
    def visitIntType(self, ctx:SailParser.IntTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#NatType.
    def visitNatType(self, ctx:SailParser.NatTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#BoolType.
    def visitBoolType(self, ctx:SailParser.BoolTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#UnitType.
    def visitUnitType(self, ctx:SailParser.UnitTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#RangeType.
    def visitRangeType(self, ctx:SailParser.RangeTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#VectorType.
    def visitVectorType(self, ctx:SailParser.VectorTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#CustomType.
    def visitCustomType(self, ctx:SailParser.CustomTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#LetStmt.
    def visitLetStmt(self, ctx:SailParser.LetStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#AssignStmt.
    def visitAssignStmt(self, ctx:SailParser.AssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#ForeachStmt.
    def visitForeachStmt(self, ctx:SailParser.ForeachStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#IfStmt.
    def visitIfStmt(self, ctx:SailParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#CallStmt.
    def visitCallStmt(self, ctx:SailParser.CallStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#ReturnStmt.
    def visitReturnStmt(self, ctx:SailParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#callExpr.
    def visitCallExpr(self, ctx:SailParser.CallExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#BoolExpr.
    def visitBoolExpr(self, ctx:SailParser.BoolExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#CompareExpr.
    def visitCompareExpr(self, ctx:SailParser.CompareExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#CallExprRule.
    def visitCallExprRule(self, ctx:SailParser.CallExprRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#HexExpr.
    def visitHexExpr(self, ctx:SailParser.HexExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#BinaryExpr.
    def visitBinaryExpr(self, ctx:SailParser.BinaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#VarExpr.
    def visitVarExpr(self, ctx:SailParser.VarExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#BinExpr.
    def visitBinExpr(self, ctx:SailParser.BinExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#IntExpr.
    def visitIntExpr(self, ctx:SailParser.IntExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#ParenExpr.
    def visitParenExpr(self, ctx:SailParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#UnaryExpr.
    def visitUnaryExpr(self, ctx:SailParser.UnaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#TernaryExpr.
    def visitTernaryExpr(self, ctx:SailParser.TernaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SailParser#commentItem.
    def visitCommentItem(self, ctx:SailParser.CommentItemContext):
        return self.visitChildren(ctx)



del SailParser