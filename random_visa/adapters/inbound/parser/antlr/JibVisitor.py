# Generated from /Volumes/External/Code/random_vISA/random_visa/adapters/inbound/parser/antlr/Jib.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .JibParser import JibParser
else:
    from JibParser import JibParser

# This class defines a complete generic visitor for a parse tree produced by JibParser.

class JibVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by JibParser#spec.
    def visitSpec(self, ctx:JibParser.SpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#topLevelItem.
    def visitTopLevelItem(self, ctx:JibParser.TopLevelItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#pragmaDirective.
    def visitPragmaDirective(self, ctx:JibParser.PragmaDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#EnumTypeDef.
    def visitEnumTypeDef(self, ctx:JibParser.EnumTypeDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#StructTypeDef.
    def visitStructTypeDef(self, ctx:JibParser.StructTypeDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#UnionTypeDef.
    def visitUnionTypeDef(self, ctx:JibParser.UnionTypeDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#AliasTypeDef.
    def visitAliasTypeDef(self, ctx:JibParser.AliasTypeDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#enumFieldList.
    def visitEnumFieldList(self, ctx:JibParser.EnumFieldListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#structField.
    def visitStructField(self, ctx:JibParser.StructFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#unionField.
    def visitUnionField(self, ctx:JibParser.UnionFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#registerDecl.
    def visitRegisterDecl(self, ctx:JibParser.RegisterDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#globalDecl.
    def visitGlobalDecl(self, ctx:JibParser.GlobalDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#valDecl.
    def visitValDecl(self, ctx:JibParser.ValDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#functionDef.
    def visitFunctionDef(self, ctx:JibParser.FunctionDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#paramList.
    def visitParamList(self, ctx:JibParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#param.
    def visitParam(self, ctx:JibParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#UnitType.
    def visitUnitType(self, ctx:JibParser.UnitTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#BoolType.
    def visitBoolType(self, ctx:JibParser.BoolTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#BitType.
    def visitBitType(self, ctx:JibParser.BitTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#IntType.
    def visitIntType(self, ctx:JibParser.IntTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#LintType.
    def visitLintType(self, ctx:JibParser.LintTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#NatType.
    def visitNatType(self, ctx:JibParser.NatTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#StringType.
    def visitStringType(self, ctx:JibParser.StringTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#RealType.
    def visitRealType(self, ctx:JibParser.RealTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#SizedIntType.
    def visitSizedIntType(self, ctx:JibParser.SizedIntTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#SizedBvType.
    def visitSizedBvType(self, ctx:JibParser.SizedBvTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#SizedBitsType.
    def visitSizedBitsType(self, ctx:JibParser.SizedBitsTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#LargeBitsType.
    def visitLargeBitsType(self, ctx:JibParser.LargeBitsTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#VectorType.
    def visitVectorType(self, ctx:JibParser.VectorTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#FixedVectorType.
    def visitFixedVectorType(self, ctx:JibParser.FixedVectorTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#TupleType.
    def visitTupleType(self, ctx:JibParser.TupleTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#StructRefType.
    def visitStructRefType(self, ctx:JibParser.StructRefTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#EnumRefType.
    def visitEnumRefType(self, ctx:JibParser.EnumRefTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#UnionRefType.
    def visitUnionRefType(self, ctx:JibParser.UnionRefTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#CustomRefType.
    def visitCustomRefType(self, ctx:JibParser.CustomRefTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#LabelInst.
    def visitLabelInst(self, ctx:JibParser.LabelInstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#VarDeclInst.
    def visitVarDeclInst(self, ctx:JibParser.VarDeclInstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#AssignInstRule.
    def visitAssignInstRule(self, ctx:JibParser.AssignInstRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#CallInstRule.
    def visitCallInstRule(self, ctx:JibParser.CallInstRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#PrimInstRule.
    def visitPrimInstRule(self, ctx:JibParser.PrimInstRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#CopyInstRule.
    def visitCopyInstRule(self, ctx:JibParser.CopyInstRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#JumpInstRule.
    def visitJumpInstRule(self, ctx:JibParser.JumpInstRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#BranchInstRule.
    def visitBranchInstRule(self, ctx:JibParser.BranchInstRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#ReturnInstRule.
    def visitReturnInstRule(self, ctx:JibParser.ReturnInstRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#EndInstRule.
    def visitEndInstRule(self, ctx:JibParser.EndInstRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#ClearInstRule.
    def visitClearInstRule(self, ctx:JibParser.ClearInstRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#labelDecl.
    def visitLabelDecl(self, ctx:JibParser.LabelDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#varDecl.
    def visitVarDecl(self, ctx:JibParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#assignInst.
    def visitAssignInst(self, ctx:JibParser.AssignInstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#copyInst.
    def visitCopyInst(self, ctx:JibParser.CopyInstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#primInst.
    def visitPrimInst(self, ctx:JibParser.PrimInstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#callInst.
    def visitCallInst(self, ctx:JibParser.CallInstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#jumpInst.
    def visitJumpInst(self, ctx:JibParser.JumpInstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#IfBranchInst.
    def visitIfBranchInst(self, ctx:JibParser.IfBranchInstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#JumpIfInst.
    def visitJumpIfInst(self, ctx:JibParser.JumpIfInstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#returnInst.
    def visitReturnInst(self, ctx:JibParser.ReturnInstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#EndNormalInst.
    def visitEndNormalInst(self, ctx:JibParser.EndNormalInstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#FailInst.
    def visitFailInst(self, ctx:JibParser.FailInstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#clearInst.
    def visitClearInst(self, ctx:JibParser.ClearInstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#LiteralCval.
    def visitLiteralCval(self, ctx:JibParser.LiteralCvalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#FieldAccessCval.
    def visitFieldAccessCval(self, ctx:JibParser.FieldAccessCvalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#TupleAccessCval.
    def visitTupleAccessCval(self, ctx:JibParser.TupleAccessCvalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#TupleCval.
    def visitTupleCval(self, ctx:JibParser.TupleCvalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#CvalExpr.
    def visitCvalExpr(self, ctx:JibParser.CvalExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#UnaryExpr.
    def visitUnaryExpr(self, ctx:JibParser.UnaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#BinaryExpr.
    def visitBinaryExpr(self, ctx:JibParser.BinaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#CastExpr.
    def visitCastExpr(self, ctx:JibParser.CastExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#StructInitExpr.
    def visitStructInitExpr(self, ctx:JibParser.StructInitExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#VectorInitExpr.
    def visitVectorInitExpr(self, ctx:JibParser.VectorInitExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#fieldInit.
    def visitFieldInit(self, ctx:JibParser.FieldInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#IntLiteral.
    def visitIntLiteral(self, ctx:JibParser.IntLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#HexLiteral.
    def visitHexLiteral(self, ctx:JibParser.HexLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#BinLiteral.
    def visitBinLiteral(self, ctx:JibParser.BinLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#BoolLiteral.
    def visitBoolLiteral(self, ctx:JibParser.BoolLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#StringLiteral.
    def visitStringLiteral(self, ctx:JibParser.StringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JibParser#UnitLiteral.
    def visitUnitLiteral(self, ctx:JibParser.UnitLiteralContext):
        return self.visitChildren(ctx)



del JibParser