# Generated from /Volumes/External/Code/random_vISA/random_visa/adapters/inbound/parser/antlr/Sail.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SailParser import SailParser
else:
    from SailParser import SailParser

# This class defines a complete listener for a parse tree produced by SailParser.
class SailListener(ParseTreeListener):

    # Enter a parse tree produced by SailParser#spec.
    def enterSpec(self, ctx:SailParser.SpecContext):
        pass

    # Exit a parse tree produced by SailParser#spec.
    def exitSpec(self, ctx:SailParser.SpecContext):
        pass


    # Enter a parse tree produced by SailParser#topLevelItem.
    def enterTopLevelItem(self, ctx:SailParser.TopLevelItemContext):
        pass

    # Exit a parse tree produced by SailParser#topLevelItem.
    def exitTopLevelItem(self, ctx:SailParser.TopLevelItemContext):
        pass


    # Enter a parse tree produced by SailParser#defaultOrderDirective.
    def enterDefaultOrderDirective(self, ctx:SailParser.DefaultOrderDirectiveContext):
        pass

    # Exit a parse tree produced by SailParser#defaultOrderDirective.
    def exitDefaultOrderDirective(self, ctx:SailParser.DefaultOrderDirectiveContext):
        pass


    # Enter a parse tree produced by SailParser#includeDirective.
    def enterIncludeDirective(self, ctx:SailParser.IncludeDirectiveContext):
        pass

    # Exit a parse tree produced by SailParser#includeDirective.
    def exitIncludeDirective(self, ctx:SailParser.IncludeDirectiveContext):
        pass


    # Enter a parse tree produced by SailParser#includePath.
    def enterIncludePath(self, ctx:SailParser.IncludePathContext):
        pass

    # Exit a parse tree produced by SailParser#includePath.
    def exitIncludePath(self, ctx:SailParser.IncludePathContext):
        pass


    # Enter a parse tree produced by SailParser#letDecl.
    def enterLetDecl(self, ctx:SailParser.LetDeclContext):
        pass

    # Exit a parse tree produced by SailParser#letDecl.
    def exitLetDecl(self, ctx:SailParser.LetDeclContext):
        pass


    # Enter a parse tree produced by SailParser#typeDecl.
    def enterTypeDecl(self, ctx:SailParser.TypeDeclContext):
        pass

    # Exit a parse tree produced by SailParser#typeDecl.
    def exitTypeDecl(self, ctx:SailParser.TypeDeclContext):
        pass


    # Enter a parse tree produced by SailParser#registerDecl.
    def enterRegisterDecl(self, ctx:SailParser.RegisterDeclContext):
        pass

    # Exit a parse tree produced by SailParser#registerDecl.
    def exitRegisterDecl(self, ctx:SailParser.RegisterDeclContext):
        pass


    # Enter a parse tree produced by SailParser#valDecl.
    def enterValDecl(self, ctx:SailParser.ValDeclContext):
        pass

    # Exit a parse tree produced by SailParser#valDecl.
    def exitValDecl(self, ctx:SailParser.ValDeclContext):
        pass


    # Enter a parse tree produced by SailParser#functionDef.
    def enterFunctionDef(self, ctx:SailParser.FunctionDefContext):
        pass

    # Exit a parse tree produced by SailParser#functionDef.
    def exitFunctionDef(self, ctx:SailParser.FunctionDefContext):
        pass


    # Enter a parse tree produced by SailParser#paramList.
    def enterParamList(self, ctx:SailParser.ParamListContext):
        pass

    # Exit a parse tree produced by SailParser#paramList.
    def exitParamList(self, ctx:SailParser.ParamListContext):
        pass


    # Enter a parse tree produced by SailParser#param.
    def enterParam(self, ctx:SailParser.ParamContext):
        pass

    # Exit a parse tree produced by SailParser#param.
    def exitParam(self, ctx:SailParser.ParamContext):
        pass


    # Enter a parse tree produced by SailParser#BitsType.
    def enterBitsType(self, ctx:SailParser.BitsTypeContext):
        pass

    # Exit a parse tree produced by SailParser#BitsType.
    def exitBitsType(self, ctx:SailParser.BitsTypeContext):
        pass


    # Enter a parse tree produced by SailParser#IntType.
    def enterIntType(self, ctx:SailParser.IntTypeContext):
        pass

    # Exit a parse tree produced by SailParser#IntType.
    def exitIntType(self, ctx:SailParser.IntTypeContext):
        pass


    # Enter a parse tree produced by SailParser#NatType.
    def enterNatType(self, ctx:SailParser.NatTypeContext):
        pass

    # Exit a parse tree produced by SailParser#NatType.
    def exitNatType(self, ctx:SailParser.NatTypeContext):
        pass


    # Enter a parse tree produced by SailParser#BoolType.
    def enterBoolType(self, ctx:SailParser.BoolTypeContext):
        pass

    # Exit a parse tree produced by SailParser#BoolType.
    def exitBoolType(self, ctx:SailParser.BoolTypeContext):
        pass


    # Enter a parse tree produced by SailParser#UnitType.
    def enterUnitType(self, ctx:SailParser.UnitTypeContext):
        pass

    # Exit a parse tree produced by SailParser#UnitType.
    def exitUnitType(self, ctx:SailParser.UnitTypeContext):
        pass


    # Enter a parse tree produced by SailParser#RangeType.
    def enterRangeType(self, ctx:SailParser.RangeTypeContext):
        pass

    # Exit a parse tree produced by SailParser#RangeType.
    def exitRangeType(self, ctx:SailParser.RangeTypeContext):
        pass


    # Enter a parse tree produced by SailParser#VectorType.
    def enterVectorType(self, ctx:SailParser.VectorTypeContext):
        pass

    # Exit a parse tree produced by SailParser#VectorType.
    def exitVectorType(self, ctx:SailParser.VectorTypeContext):
        pass


    # Enter a parse tree produced by SailParser#CustomType.
    def enterCustomType(self, ctx:SailParser.CustomTypeContext):
        pass

    # Exit a parse tree produced by SailParser#CustomType.
    def exitCustomType(self, ctx:SailParser.CustomTypeContext):
        pass


    # Enter a parse tree produced by SailParser#LetStmt.
    def enterLetStmt(self, ctx:SailParser.LetStmtContext):
        pass

    # Exit a parse tree produced by SailParser#LetStmt.
    def exitLetStmt(self, ctx:SailParser.LetStmtContext):
        pass


    # Enter a parse tree produced by SailParser#AssignStmt.
    def enterAssignStmt(self, ctx:SailParser.AssignStmtContext):
        pass

    # Exit a parse tree produced by SailParser#AssignStmt.
    def exitAssignStmt(self, ctx:SailParser.AssignStmtContext):
        pass


    # Enter a parse tree produced by SailParser#ForeachStmt.
    def enterForeachStmt(self, ctx:SailParser.ForeachStmtContext):
        pass

    # Exit a parse tree produced by SailParser#ForeachStmt.
    def exitForeachStmt(self, ctx:SailParser.ForeachStmtContext):
        pass


    # Enter a parse tree produced by SailParser#IfStmt.
    def enterIfStmt(self, ctx:SailParser.IfStmtContext):
        pass

    # Exit a parse tree produced by SailParser#IfStmt.
    def exitIfStmt(self, ctx:SailParser.IfStmtContext):
        pass


    # Enter a parse tree produced by SailParser#CallStmt.
    def enterCallStmt(self, ctx:SailParser.CallStmtContext):
        pass

    # Exit a parse tree produced by SailParser#CallStmt.
    def exitCallStmt(self, ctx:SailParser.CallStmtContext):
        pass


    # Enter a parse tree produced by SailParser#ReturnStmt.
    def enterReturnStmt(self, ctx:SailParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by SailParser#ReturnStmt.
    def exitReturnStmt(self, ctx:SailParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by SailParser#callExpr.
    def enterCallExpr(self, ctx:SailParser.CallExprContext):
        pass

    # Exit a parse tree produced by SailParser#callExpr.
    def exitCallExpr(self, ctx:SailParser.CallExprContext):
        pass


    # Enter a parse tree produced by SailParser#BoolExpr.
    def enterBoolExpr(self, ctx:SailParser.BoolExprContext):
        pass

    # Exit a parse tree produced by SailParser#BoolExpr.
    def exitBoolExpr(self, ctx:SailParser.BoolExprContext):
        pass


    # Enter a parse tree produced by SailParser#CompareExpr.
    def enterCompareExpr(self, ctx:SailParser.CompareExprContext):
        pass

    # Exit a parse tree produced by SailParser#CompareExpr.
    def exitCompareExpr(self, ctx:SailParser.CompareExprContext):
        pass


    # Enter a parse tree produced by SailParser#CallExprRule.
    def enterCallExprRule(self, ctx:SailParser.CallExprRuleContext):
        pass

    # Exit a parse tree produced by SailParser#CallExprRule.
    def exitCallExprRule(self, ctx:SailParser.CallExprRuleContext):
        pass


    # Enter a parse tree produced by SailParser#HexExpr.
    def enterHexExpr(self, ctx:SailParser.HexExprContext):
        pass

    # Exit a parse tree produced by SailParser#HexExpr.
    def exitHexExpr(self, ctx:SailParser.HexExprContext):
        pass


    # Enter a parse tree produced by SailParser#BinaryExpr.
    def enterBinaryExpr(self, ctx:SailParser.BinaryExprContext):
        pass

    # Exit a parse tree produced by SailParser#BinaryExpr.
    def exitBinaryExpr(self, ctx:SailParser.BinaryExprContext):
        pass


    # Enter a parse tree produced by SailParser#VarExpr.
    def enterVarExpr(self, ctx:SailParser.VarExprContext):
        pass

    # Exit a parse tree produced by SailParser#VarExpr.
    def exitVarExpr(self, ctx:SailParser.VarExprContext):
        pass


    # Enter a parse tree produced by SailParser#BinExpr.
    def enterBinExpr(self, ctx:SailParser.BinExprContext):
        pass

    # Exit a parse tree produced by SailParser#BinExpr.
    def exitBinExpr(self, ctx:SailParser.BinExprContext):
        pass


    # Enter a parse tree produced by SailParser#IntExpr.
    def enterIntExpr(self, ctx:SailParser.IntExprContext):
        pass

    # Exit a parse tree produced by SailParser#IntExpr.
    def exitIntExpr(self, ctx:SailParser.IntExprContext):
        pass


    # Enter a parse tree produced by SailParser#ParenExpr.
    def enterParenExpr(self, ctx:SailParser.ParenExprContext):
        pass

    # Exit a parse tree produced by SailParser#ParenExpr.
    def exitParenExpr(self, ctx:SailParser.ParenExprContext):
        pass


    # Enter a parse tree produced by SailParser#UnaryExpr.
    def enterUnaryExpr(self, ctx:SailParser.UnaryExprContext):
        pass

    # Exit a parse tree produced by SailParser#UnaryExpr.
    def exitUnaryExpr(self, ctx:SailParser.UnaryExprContext):
        pass


    # Enter a parse tree produced by SailParser#TernaryExpr.
    def enterTernaryExpr(self, ctx:SailParser.TernaryExprContext):
        pass

    # Exit a parse tree produced by SailParser#TernaryExpr.
    def exitTernaryExpr(self, ctx:SailParser.TernaryExprContext):
        pass


    # Enter a parse tree produced by SailParser#commentItem.
    def enterCommentItem(self, ctx:SailParser.CommentItemContext):
        pass

    # Exit a parse tree produced by SailParser#commentItem.
    def exitCommentItem(self, ctx:SailParser.CommentItemContext):
        pass



del SailParser