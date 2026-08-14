# Generated from /Volumes/External/Code/random_vISA/random_visa/adapters/inbound/parser/antlr/Jib.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .JibParser import JibParser
else:
    from JibParser import JibParser

# This class defines a complete listener for a parse tree produced by JibParser.
class JibListener(ParseTreeListener):

    # Enter a parse tree produced by JibParser#spec.
    def enterSpec(self, ctx:JibParser.SpecContext):
        pass

    # Exit a parse tree produced by JibParser#spec.
    def exitSpec(self, ctx:JibParser.SpecContext):
        pass


    # Enter a parse tree produced by JibParser#topLevelItem.
    def enterTopLevelItem(self, ctx:JibParser.TopLevelItemContext):
        pass

    # Exit a parse tree produced by JibParser#topLevelItem.
    def exitTopLevelItem(self, ctx:JibParser.TopLevelItemContext):
        pass


    # Enter a parse tree produced by JibParser#pragmaDirective.
    def enterPragmaDirective(self, ctx:JibParser.PragmaDirectiveContext):
        pass

    # Exit a parse tree produced by JibParser#pragmaDirective.
    def exitPragmaDirective(self, ctx:JibParser.PragmaDirectiveContext):
        pass


    # Enter a parse tree produced by JibParser#EnumTypeDef.
    def enterEnumTypeDef(self, ctx:JibParser.EnumTypeDefContext):
        pass

    # Exit a parse tree produced by JibParser#EnumTypeDef.
    def exitEnumTypeDef(self, ctx:JibParser.EnumTypeDefContext):
        pass


    # Enter a parse tree produced by JibParser#StructTypeDef.
    def enterStructTypeDef(self, ctx:JibParser.StructTypeDefContext):
        pass

    # Exit a parse tree produced by JibParser#StructTypeDef.
    def exitStructTypeDef(self, ctx:JibParser.StructTypeDefContext):
        pass


    # Enter a parse tree produced by JibParser#UnionTypeDef.
    def enterUnionTypeDef(self, ctx:JibParser.UnionTypeDefContext):
        pass

    # Exit a parse tree produced by JibParser#UnionTypeDef.
    def exitUnionTypeDef(self, ctx:JibParser.UnionTypeDefContext):
        pass


    # Enter a parse tree produced by JibParser#AliasTypeDef.
    def enterAliasTypeDef(self, ctx:JibParser.AliasTypeDefContext):
        pass

    # Exit a parse tree produced by JibParser#AliasTypeDef.
    def exitAliasTypeDef(self, ctx:JibParser.AliasTypeDefContext):
        pass


    # Enter a parse tree produced by JibParser#enumFieldList.
    def enterEnumFieldList(self, ctx:JibParser.EnumFieldListContext):
        pass

    # Exit a parse tree produced by JibParser#enumFieldList.
    def exitEnumFieldList(self, ctx:JibParser.EnumFieldListContext):
        pass


    # Enter a parse tree produced by JibParser#structField.
    def enterStructField(self, ctx:JibParser.StructFieldContext):
        pass

    # Exit a parse tree produced by JibParser#structField.
    def exitStructField(self, ctx:JibParser.StructFieldContext):
        pass


    # Enter a parse tree produced by JibParser#unionField.
    def enterUnionField(self, ctx:JibParser.UnionFieldContext):
        pass

    # Exit a parse tree produced by JibParser#unionField.
    def exitUnionField(self, ctx:JibParser.UnionFieldContext):
        pass


    # Enter a parse tree produced by JibParser#registerDecl.
    def enterRegisterDecl(self, ctx:JibParser.RegisterDeclContext):
        pass

    # Exit a parse tree produced by JibParser#registerDecl.
    def exitRegisterDecl(self, ctx:JibParser.RegisterDeclContext):
        pass


    # Enter a parse tree produced by JibParser#globalDecl.
    def enterGlobalDecl(self, ctx:JibParser.GlobalDeclContext):
        pass

    # Exit a parse tree produced by JibParser#globalDecl.
    def exitGlobalDecl(self, ctx:JibParser.GlobalDeclContext):
        pass


    # Enter a parse tree produced by JibParser#valDecl.
    def enterValDecl(self, ctx:JibParser.ValDeclContext):
        pass

    # Exit a parse tree produced by JibParser#valDecl.
    def exitValDecl(self, ctx:JibParser.ValDeclContext):
        pass


    # Enter a parse tree produced by JibParser#functionDef.
    def enterFunctionDef(self, ctx:JibParser.FunctionDefContext):
        pass

    # Exit a parse tree produced by JibParser#functionDef.
    def exitFunctionDef(self, ctx:JibParser.FunctionDefContext):
        pass


    # Enter a parse tree produced by JibParser#paramList.
    def enterParamList(self, ctx:JibParser.ParamListContext):
        pass

    # Exit a parse tree produced by JibParser#paramList.
    def exitParamList(self, ctx:JibParser.ParamListContext):
        pass


    # Enter a parse tree produced by JibParser#param.
    def enterParam(self, ctx:JibParser.ParamContext):
        pass

    # Exit a parse tree produced by JibParser#param.
    def exitParam(self, ctx:JibParser.ParamContext):
        pass


    # Enter a parse tree produced by JibParser#UnitType.
    def enterUnitType(self, ctx:JibParser.UnitTypeContext):
        pass

    # Exit a parse tree produced by JibParser#UnitType.
    def exitUnitType(self, ctx:JibParser.UnitTypeContext):
        pass


    # Enter a parse tree produced by JibParser#BoolType.
    def enterBoolType(self, ctx:JibParser.BoolTypeContext):
        pass

    # Exit a parse tree produced by JibParser#BoolType.
    def exitBoolType(self, ctx:JibParser.BoolTypeContext):
        pass


    # Enter a parse tree produced by JibParser#BitType.
    def enterBitType(self, ctx:JibParser.BitTypeContext):
        pass

    # Exit a parse tree produced by JibParser#BitType.
    def exitBitType(self, ctx:JibParser.BitTypeContext):
        pass


    # Enter a parse tree produced by JibParser#IntType.
    def enterIntType(self, ctx:JibParser.IntTypeContext):
        pass

    # Exit a parse tree produced by JibParser#IntType.
    def exitIntType(self, ctx:JibParser.IntTypeContext):
        pass


    # Enter a parse tree produced by JibParser#LintType.
    def enterLintType(self, ctx:JibParser.LintTypeContext):
        pass

    # Exit a parse tree produced by JibParser#LintType.
    def exitLintType(self, ctx:JibParser.LintTypeContext):
        pass


    # Enter a parse tree produced by JibParser#NatType.
    def enterNatType(self, ctx:JibParser.NatTypeContext):
        pass

    # Exit a parse tree produced by JibParser#NatType.
    def exitNatType(self, ctx:JibParser.NatTypeContext):
        pass


    # Enter a parse tree produced by JibParser#StringType.
    def enterStringType(self, ctx:JibParser.StringTypeContext):
        pass

    # Exit a parse tree produced by JibParser#StringType.
    def exitStringType(self, ctx:JibParser.StringTypeContext):
        pass


    # Enter a parse tree produced by JibParser#RealType.
    def enterRealType(self, ctx:JibParser.RealTypeContext):
        pass

    # Exit a parse tree produced by JibParser#RealType.
    def exitRealType(self, ctx:JibParser.RealTypeContext):
        pass


    # Enter a parse tree produced by JibParser#SizedIntType.
    def enterSizedIntType(self, ctx:JibParser.SizedIntTypeContext):
        pass

    # Exit a parse tree produced by JibParser#SizedIntType.
    def exitSizedIntType(self, ctx:JibParser.SizedIntTypeContext):
        pass


    # Enter a parse tree produced by JibParser#SizedBvType.
    def enterSizedBvType(self, ctx:JibParser.SizedBvTypeContext):
        pass

    # Exit a parse tree produced by JibParser#SizedBvType.
    def exitSizedBvType(self, ctx:JibParser.SizedBvTypeContext):
        pass


    # Enter a parse tree produced by JibParser#SizedBitsType.
    def enterSizedBitsType(self, ctx:JibParser.SizedBitsTypeContext):
        pass

    # Exit a parse tree produced by JibParser#SizedBitsType.
    def exitSizedBitsType(self, ctx:JibParser.SizedBitsTypeContext):
        pass


    # Enter a parse tree produced by JibParser#LargeBitsType.
    def enterLargeBitsType(self, ctx:JibParser.LargeBitsTypeContext):
        pass

    # Exit a parse tree produced by JibParser#LargeBitsType.
    def exitLargeBitsType(self, ctx:JibParser.LargeBitsTypeContext):
        pass


    # Enter a parse tree produced by JibParser#VectorType.
    def enterVectorType(self, ctx:JibParser.VectorTypeContext):
        pass

    # Exit a parse tree produced by JibParser#VectorType.
    def exitVectorType(self, ctx:JibParser.VectorTypeContext):
        pass


    # Enter a parse tree produced by JibParser#FixedVectorType.
    def enterFixedVectorType(self, ctx:JibParser.FixedVectorTypeContext):
        pass

    # Exit a parse tree produced by JibParser#FixedVectorType.
    def exitFixedVectorType(self, ctx:JibParser.FixedVectorTypeContext):
        pass


    # Enter a parse tree produced by JibParser#TupleType.
    def enterTupleType(self, ctx:JibParser.TupleTypeContext):
        pass

    # Exit a parse tree produced by JibParser#TupleType.
    def exitTupleType(self, ctx:JibParser.TupleTypeContext):
        pass


    # Enter a parse tree produced by JibParser#StructRefType.
    def enterStructRefType(self, ctx:JibParser.StructRefTypeContext):
        pass

    # Exit a parse tree produced by JibParser#StructRefType.
    def exitStructRefType(self, ctx:JibParser.StructRefTypeContext):
        pass


    # Enter a parse tree produced by JibParser#EnumRefType.
    def enterEnumRefType(self, ctx:JibParser.EnumRefTypeContext):
        pass

    # Exit a parse tree produced by JibParser#EnumRefType.
    def exitEnumRefType(self, ctx:JibParser.EnumRefTypeContext):
        pass


    # Enter a parse tree produced by JibParser#UnionRefType.
    def enterUnionRefType(self, ctx:JibParser.UnionRefTypeContext):
        pass

    # Exit a parse tree produced by JibParser#UnionRefType.
    def exitUnionRefType(self, ctx:JibParser.UnionRefTypeContext):
        pass


    # Enter a parse tree produced by JibParser#CustomRefType.
    def enterCustomRefType(self, ctx:JibParser.CustomRefTypeContext):
        pass

    # Exit a parse tree produced by JibParser#CustomRefType.
    def exitCustomRefType(self, ctx:JibParser.CustomRefTypeContext):
        pass


    # Enter a parse tree produced by JibParser#LabelInst.
    def enterLabelInst(self, ctx:JibParser.LabelInstContext):
        pass

    # Exit a parse tree produced by JibParser#LabelInst.
    def exitLabelInst(self, ctx:JibParser.LabelInstContext):
        pass


    # Enter a parse tree produced by JibParser#VarDeclInst.
    def enterVarDeclInst(self, ctx:JibParser.VarDeclInstContext):
        pass

    # Exit a parse tree produced by JibParser#VarDeclInst.
    def exitVarDeclInst(self, ctx:JibParser.VarDeclInstContext):
        pass


    # Enter a parse tree produced by JibParser#AssignInstRule.
    def enterAssignInstRule(self, ctx:JibParser.AssignInstRuleContext):
        pass

    # Exit a parse tree produced by JibParser#AssignInstRule.
    def exitAssignInstRule(self, ctx:JibParser.AssignInstRuleContext):
        pass


    # Enter a parse tree produced by JibParser#CallInstRule.
    def enterCallInstRule(self, ctx:JibParser.CallInstRuleContext):
        pass

    # Exit a parse tree produced by JibParser#CallInstRule.
    def exitCallInstRule(self, ctx:JibParser.CallInstRuleContext):
        pass


    # Enter a parse tree produced by JibParser#PrimInstRule.
    def enterPrimInstRule(self, ctx:JibParser.PrimInstRuleContext):
        pass

    # Exit a parse tree produced by JibParser#PrimInstRule.
    def exitPrimInstRule(self, ctx:JibParser.PrimInstRuleContext):
        pass


    # Enter a parse tree produced by JibParser#CopyInstRule.
    def enterCopyInstRule(self, ctx:JibParser.CopyInstRuleContext):
        pass

    # Exit a parse tree produced by JibParser#CopyInstRule.
    def exitCopyInstRule(self, ctx:JibParser.CopyInstRuleContext):
        pass


    # Enter a parse tree produced by JibParser#JumpInstRule.
    def enterJumpInstRule(self, ctx:JibParser.JumpInstRuleContext):
        pass

    # Exit a parse tree produced by JibParser#JumpInstRule.
    def exitJumpInstRule(self, ctx:JibParser.JumpInstRuleContext):
        pass


    # Enter a parse tree produced by JibParser#BranchInstRule.
    def enterBranchInstRule(self, ctx:JibParser.BranchInstRuleContext):
        pass

    # Exit a parse tree produced by JibParser#BranchInstRule.
    def exitBranchInstRule(self, ctx:JibParser.BranchInstRuleContext):
        pass


    # Enter a parse tree produced by JibParser#ReturnInstRule.
    def enterReturnInstRule(self, ctx:JibParser.ReturnInstRuleContext):
        pass

    # Exit a parse tree produced by JibParser#ReturnInstRule.
    def exitReturnInstRule(self, ctx:JibParser.ReturnInstRuleContext):
        pass


    # Enter a parse tree produced by JibParser#EndInstRule.
    def enterEndInstRule(self, ctx:JibParser.EndInstRuleContext):
        pass

    # Exit a parse tree produced by JibParser#EndInstRule.
    def exitEndInstRule(self, ctx:JibParser.EndInstRuleContext):
        pass


    # Enter a parse tree produced by JibParser#ClearInstRule.
    def enterClearInstRule(self, ctx:JibParser.ClearInstRuleContext):
        pass

    # Exit a parse tree produced by JibParser#ClearInstRule.
    def exitClearInstRule(self, ctx:JibParser.ClearInstRuleContext):
        pass


    # Enter a parse tree produced by JibParser#labelDecl.
    def enterLabelDecl(self, ctx:JibParser.LabelDeclContext):
        pass

    # Exit a parse tree produced by JibParser#labelDecl.
    def exitLabelDecl(self, ctx:JibParser.LabelDeclContext):
        pass


    # Enter a parse tree produced by JibParser#varDecl.
    def enterVarDecl(self, ctx:JibParser.VarDeclContext):
        pass

    # Exit a parse tree produced by JibParser#varDecl.
    def exitVarDecl(self, ctx:JibParser.VarDeclContext):
        pass


    # Enter a parse tree produced by JibParser#assignInst.
    def enterAssignInst(self, ctx:JibParser.AssignInstContext):
        pass

    # Exit a parse tree produced by JibParser#assignInst.
    def exitAssignInst(self, ctx:JibParser.AssignInstContext):
        pass


    # Enter a parse tree produced by JibParser#copyInst.
    def enterCopyInst(self, ctx:JibParser.CopyInstContext):
        pass

    # Exit a parse tree produced by JibParser#copyInst.
    def exitCopyInst(self, ctx:JibParser.CopyInstContext):
        pass


    # Enter a parse tree produced by JibParser#primInst.
    def enterPrimInst(self, ctx:JibParser.PrimInstContext):
        pass

    # Exit a parse tree produced by JibParser#primInst.
    def exitPrimInst(self, ctx:JibParser.PrimInstContext):
        pass


    # Enter a parse tree produced by JibParser#callInst.
    def enterCallInst(self, ctx:JibParser.CallInstContext):
        pass

    # Exit a parse tree produced by JibParser#callInst.
    def exitCallInst(self, ctx:JibParser.CallInstContext):
        pass


    # Enter a parse tree produced by JibParser#jumpInst.
    def enterJumpInst(self, ctx:JibParser.JumpInstContext):
        pass

    # Exit a parse tree produced by JibParser#jumpInst.
    def exitJumpInst(self, ctx:JibParser.JumpInstContext):
        pass


    # Enter a parse tree produced by JibParser#IfBranchInst.
    def enterIfBranchInst(self, ctx:JibParser.IfBranchInstContext):
        pass

    # Exit a parse tree produced by JibParser#IfBranchInst.
    def exitIfBranchInst(self, ctx:JibParser.IfBranchInstContext):
        pass


    # Enter a parse tree produced by JibParser#JumpIfInst.
    def enterJumpIfInst(self, ctx:JibParser.JumpIfInstContext):
        pass

    # Exit a parse tree produced by JibParser#JumpIfInst.
    def exitJumpIfInst(self, ctx:JibParser.JumpIfInstContext):
        pass


    # Enter a parse tree produced by JibParser#returnInst.
    def enterReturnInst(self, ctx:JibParser.ReturnInstContext):
        pass

    # Exit a parse tree produced by JibParser#returnInst.
    def exitReturnInst(self, ctx:JibParser.ReturnInstContext):
        pass


    # Enter a parse tree produced by JibParser#EndNormalInst.
    def enterEndNormalInst(self, ctx:JibParser.EndNormalInstContext):
        pass

    # Exit a parse tree produced by JibParser#EndNormalInst.
    def exitEndNormalInst(self, ctx:JibParser.EndNormalInstContext):
        pass


    # Enter a parse tree produced by JibParser#FailInst.
    def enterFailInst(self, ctx:JibParser.FailInstContext):
        pass

    # Exit a parse tree produced by JibParser#FailInst.
    def exitFailInst(self, ctx:JibParser.FailInstContext):
        pass


    # Enter a parse tree produced by JibParser#clearInst.
    def enterClearInst(self, ctx:JibParser.ClearInstContext):
        pass

    # Exit a parse tree produced by JibParser#clearInst.
    def exitClearInst(self, ctx:JibParser.ClearInstContext):
        pass


    # Enter a parse tree produced by JibParser#LiteralCval.
    def enterLiteralCval(self, ctx:JibParser.LiteralCvalContext):
        pass

    # Exit a parse tree produced by JibParser#LiteralCval.
    def exitLiteralCval(self, ctx:JibParser.LiteralCvalContext):
        pass


    # Enter a parse tree produced by JibParser#FieldAccessCval.
    def enterFieldAccessCval(self, ctx:JibParser.FieldAccessCvalContext):
        pass

    # Exit a parse tree produced by JibParser#FieldAccessCval.
    def exitFieldAccessCval(self, ctx:JibParser.FieldAccessCvalContext):
        pass


    # Enter a parse tree produced by JibParser#TupleAccessCval.
    def enterTupleAccessCval(self, ctx:JibParser.TupleAccessCvalContext):
        pass

    # Exit a parse tree produced by JibParser#TupleAccessCval.
    def exitTupleAccessCval(self, ctx:JibParser.TupleAccessCvalContext):
        pass


    # Enter a parse tree produced by JibParser#TupleCval.
    def enterTupleCval(self, ctx:JibParser.TupleCvalContext):
        pass

    # Exit a parse tree produced by JibParser#TupleCval.
    def exitTupleCval(self, ctx:JibParser.TupleCvalContext):
        pass


    # Enter a parse tree produced by JibParser#CvalExpr.
    def enterCvalExpr(self, ctx:JibParser.CvalExprContext):
        pass

    # Exit a parse tree produced by JibParser#CvalExpr.
    def exitCvalExpr(self, ctx:JibParser.CvalExprContext):
        pass


    # Enter a parse tree produced by JibParser#UnaryExpr.
    def enterUnaryExpr(self, ctx:JibParser.UnaryExprContext):
        pass

    # Exit a parse tree produced by JibParser#UnaryExpr.
    def exitUnaryExpr(self, ctx:JibParser.UnaryExprContext):
        pass


    # Enter a parse tree produced by JibParser#BinaryExpr.
    def enterBinaryExpr(self, ctx:JibParser.BinaryExprContext):
        pass

    # Exit a parse tree produced by JibParser#BinaryExpr.
    def exitBinaryExpr(self, ctx:JibParser.BinaryExprContext):
        pass


    # Enter a parse tree produced by JibParser#CastExpr.
    def enterCastExpr(self, ctx:JibParser.CastExprContext):
        pass

    # Exit a parse tree produced by JibParser#CastExpr.
    def exitCastExpr(self, ctx:JibParser.CastExprContext):
        pass


    # Enter a parse tree produced by JibParser#StructInitExpr.
    def enterStructInitExpr(self, ctx:JibParser.StructInitExprContext):
        pass

    # Exit a parse tree produced by JibParser#StructInitExpr.
    def exitStructInitExpr(self, ctx:JibParser.StructInitExprContext):
        pass


    # Enter a parse tree produced by JibParser#VectorInitExpr.
    def enterVectorInitExpr(self, ctx:JibParser.VectorInitExprContext):
        pass

    # Exit a parse tree produced by JibParser#VectorInitExpr.
    def exitVectorInitExpr(self, ctx:JibParser.VectorInitExprContext):
        pass


    # Enter a parse tree produced by JibParser#fieldInit.
    def enterFieldInit(self, ctx:JibParser.FieldInitContext):
        pass

    # Exit a parse tree produced by JibParser#fieldInit.
    def exitFieldInit(self, ctx:JibParser.FieldInitContext):
        pass


    # Enter a parse tree produced by JibParser#IntLiteral.
    def enterIntLiteral(self, ctx:JibParser.IntLiteralContext):
        pass

    # Exit a parse tree produced by JibParser#IntLiteral.
    def exitIntLiteral(self, ctx:JibParser.IntLiteralContext):
        pass


    # Enter a parse tree produced by JibParser#HexLiteral.
    def enterHexLiteral(self, ctx:JibParser.HexLiteralContext):
        pass

    # Exit a parse tree produced by JibParser#HexLiteral.
    def exitHexLiteral(self, ctx:JibParser.HexLiteralContext):
        pass


    # Enter a parse tree produced by JibParser#BinLiteral.
    def enterBinLiteral(self, ctx:JibParser.BinLiteralContext):
        pass

    # Exit a parse tree produced by JibParser#BinLiteral.
    def exitBinLiteral(self, ctx:JibParser.BinLiteralContext):
        pass


    # Enter a parse tree produced by JibParser#BoolLiteral.
    def enterBoolLiteral(self, ctx:JibParser.BoolLiteralContext):
        pass

    # Exit a parse tree produced by JibParser#BoolLiteral.
    def exitBoolLiteral(self, ctx:JibParser.BoolLiteralContext):
        pass


    # Enter a parse tree produced by JibParser#StringLiteral.
    def enterStringLiteral(self, ctx:JibParser.StringLiteralContext):
        pass

    # Exit a parse tree produced by JibParser#StringLiteral.
    def exitStringLiteral(self, ctx:JibParser.StringLiteralContext):
        pass


    # Enter a parse tree produced by JibParser#UnitLiteral.
    def enterUnitLiteral(self, ctx:JibParser.UnitLiteralContext):
        pass

    # Exit a parse tree produced by JibParser#UnitLiteral.
    def exitUnitLiteral(self, ctx:JibParser.UnitLiteralContext):
        pass



del JibParser