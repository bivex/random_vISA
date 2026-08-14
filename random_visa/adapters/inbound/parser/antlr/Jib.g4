grammar Jib;

// =========================================================================
// Parser Rules for Sail Jib IR (Intermediate Representation)
// =========================================================================

spec
    : (topLevelItem)* EOF
    ;

topLevelItem
    : typeDef
    | registerDecl
    | globalDecl
    | valDecl
    | functionDef
    | pragmaDirective
    ;

pragmaDirective
    : PRAGMA_DIRECTIVE
    ;

// --- Type Definitions ---
typeDef
    : 'enum' ID '=' '{' enumFieldList? '}' (';')?                       # EnumTypeDef
    | 'struct' ID '=' '{' (structField (',' structField)*)? '}' (';')?  # StructTypeDef
    | 'union' ID '=' '{' (unionField (',' unionField)*)? '}' (';')?     # UnionTypeDef
    | 'type' ID '=' jibType (';')?                                      # AliasTypeDef
    ;

enumFieldList
    : ID (',' ID)*
    ;

structField
    : ID ':' jibType
    ;

unionField
    : ID ':' jibType
    ;

// --- Declarations ---
registerDecl
    : 'register' ID ':' jibType (';')?
    ;

globalDecl
    : 'global' ID ':' jibType ('=' expr)? (';')?
    ;

valDecl
    : 'val' ID ':' '(' (jibType (',' jibType)*)? ')' '->' jibType (';')?
    ;

// --- Functions ---
functionDef
    : 'fn' ID '(' paramList? ')' ('->' jibType)? '{' (instruction)* '}'
    ;

paramList
    : param (',' param)*
    ;

param
    : ID ':' jibType
    ;

// --- Types in Jib IR ---
jibType
    : 'unit'                                                    # UnitType
    | 'bool'                                                    # BoolType
    | 'bit'                                                     # BitType
    | 'int'                                                     # IntType
    | 'lint'                                                    # LintType
    | 'nat'                                                     # NatType
    | 'string'                                                  # StringType
    | 'real'                                                    # RealType
    | 'i' '(' size=INT_LITERAL ')'                              # SizedIntType
    | 'bv' '(' size=(INT_LITERAL | ID) ')'                      # SizedBvType
    | 'bits' '(' size=(INT_LITERAL | ID) ')'                    # SizedBitsType
    | 'lbits'                                                   # LargeBitsType
    | 'vector' '(' len=(INT_LITERAL | ID) ',' elemType=jibType ')' # VectorType
    | 'fvector' '(' len=(INT_LITERAL | ID) ',' elemType=jibType ')' # FixedVectorType
    | '(' (jibType (',' jibType)+)? ')'                         # TupleType
    | 'struct' ID                                               # StructRefType
    | 'enum' ID                                                 # EnumRefType
    | 'union' ID                                                # UnionRefType
    | ID                                                        # CustomRefType
    ;

// --- Jib Instructions (3-Address Code / Linear IR) ---
instruction
    : labelDecl                                                 # LabelInst
    | varDecl                                                   # VarDeclInst
    | assignInst                                                # AssignInstRule
    | callInst                                                  # CallInstRule
    | primInst                                                  # PrimInstRule
    | copyInst                                                  # CopyInstRule
    | jumpInst                                                  # JumpInstRule
    | branchInst                                                # BranchInstRule
    | returnInst                                                # ReturnInstRule
    | endInst                                                   # EndInstRule
    | clearInst                                                 # ClearInstRule
    ;

labelDecl
    : 'label' ID ':'
    | ID ':'
    ;

varDecl
    : ('var' | 'local') ID ':' jibType (';')?
    ;

assignInst
    : target=cval '=' expr ';'
    ;

copyInst
    : 'copy' target=cval '=' src=cval ';'
    ;

primInst
    : target=cval '=' op=ID '(' (cval (',' cval)*)? ')' ';'
    ;

callInst
    : (target=cval '=')? 'call' funcName=ID '(' (cval (',' cval)*)? ')' ';'
    ;

jumpInst
    : ('jump' | 'goto') targetLabel=ID ';'
    ;

branchInst
    : 'if' condition=cval ('then')? ('jump' | 'goto') thenLabel=ID ('else' ('jump' | 'goto') elseLabel=ID)? ';' # IfBranchInst
    | 'jump_if' condition=cval targetLabel=ID ';'                                                            # JumpIfInst
    ;

returnInst
    : 'return' (cval)? ';'
    ;

endInst
    : 'end' ';'                                                  # EndNormalInst
    | 'fail' (STRING_LITERAL)? ';'                               # FailInst
    ;

clearInst
    : 'clear' target=ID ';'
    ;

// --- Values & Expressions (CVal) ---
cval
    : literal                                                    # LiteralCval
    | ID ('.' ID)*                                               # FieldAccessCval
    | ID '[' INT_LITERAL ']'                                     # TupleAccessCval
    | '(' (cval (',' cval)*)? ')'                                # TupleCval
    ;

expr
    : cval                                                       # CvalExpr
    | op=('~' | '!' | '-') cval                                  # UnaryExpr
    | left=cval op=('+' | '-' | '*' | '/' | '%' | '&' | '|' | '^' | '<<' | '>>' | '==' | '!=' | '<' | '<=' | '>' | '>=') right=cval # BinaryExpr
    | '(' jibType ')' cval                                       # CastExpr
    | 'struct' ID '{' (fieldInit (',' fieldInit)*)? '}'          # StructInitExpr
    | 'vector' '[' (cval (',' cval)*)? ']'                       # VectorInitExpr
    ;

fieldInit
    : ID '=' cval
    ;

literal
    : INT_LITERAL (':' jibType)?                                 # IntLiteral
    | HEX_LITERAL (':' jibType)?                                 # HexLiteral
    | BIN_LITERAL (':' jibType)?                                 # BinLiteral
    | BOOL_LITERAL                                               # BoolLiteral
    | STRING_LITERAL                                             # StringLiteral
    | '()'                                                       # UnitLiteral
    ;

// =========================================================================
// Lexer Rules
// =========================================================================

PRAGMA_DIRECTIVE: '#' ~[\r\n]*;

BOOL_LITERAL: 'true' | 'false';

HEX_LITERAL: '0' [xX] [0-9a-fA-F]+;
BIN_LITERAL: '0' [bB] [0-1]+;
INT_LITERAL: [0-9]+;

STRING_LITERAL: '"' (~["\r\n\\] | '\\' .)* '"';

ID: [a-zA-Z_%] [a-zA-Z0-9_%#]*;

BLOCK_COMMENT: '/*' .*? '*/' -> channel(HIDDEN);
LINE_COMMENT: '//' ~[\r\n]* -> channel(HIDDEN);

WS: [ \t\r\n]+ -> channel(HIDDEN);
