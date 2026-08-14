grammar Sail;

// ==========================================
// Parser Rules
// ==========================================

spec
    : (topLevelItem)* EOF
    ;

topLevelItem
    : defaultOrderDirective
    | includeDirective
    | letDecl
    | typeDecl
    | registerDecl
    | valDecl
    | functionDef
    | commentItem
    ;

defaultOrderDirective
    : 'default' 'Order' ('dec' | 'inc')
    ;

includeDirective
    : '$include' (STRING_LITERAL | '<' includePath '>')
    ;

includePath
    : ID (('.' | '/' | '-') ID)* ('.' ID)?
    ;

letDecl
    : 'let' ID (':' typeRef)? '=' expr (';')?
    ;

typeDecl
    : 'type' ID '=' typeRef
    ;

registerDecl
    : 'register' ID ':' typeRef
    ;

valDecl
    : 'val' ID ':' '(' (typeRef (',' typeRef)*)? ')' '->' typeRef
    ;

functionDef
    : 'function' ID '(' (paramList)? ')' ('->' typeRef)? '=' '{' (stmt)* '}'
    ;

paramList
    : param (',' param)*
    ;

param
    : ID ':' typeRef
    ;

typeRef
    : 'bits' '(' (INT_LITERAL | ID) ')'              # BitsType
    | 'int'                                         # IntType
    | 'nat'                                         # NatType
    | 'bool'                                        # BoolType
    | 'unit'                                        # UnitType
    | 'range' '(' (INT_LITERAL | ID) ',' (INT_LITERAL | ID) ')'   # RangeType
    | 'vector' '(' (INT_LITERAL | ID) ',' typeRef ')'      # VectorType
    | ID                                            # CustomType
    ;

stmt
    : 'let' ID (':' typeRef)? '=' expr ';'                                     # LetStmt
    | target=ID '=' expr ';'                                                   # AssignStmt
    | 'foreach' '(' ID 'from' startExpr=expr 'to' endExpr=expr ')' '{' (stmt)* '}' (';')? # ForeachStmt
    | 'if' cond=expr 'then' '{' (thenStmts+=stmt)* '}' ('else' '{' (elseStmts+=stmt)* '}')? # IfStmt
    | funcCallStmt=callExpr ';'                                                # CallStmt
    | 'return' (expr)? ';'                                                     # ReturnStmt
    ;

callExpr
    : ID '(' (expr (',' expr)*)? ')'
    ;

expr
    : '(' expr ')'                                                 # ParenExpr
    | op=('~' | '!' | '-') operand=expr                            # UnaryExpr
    | left=expr op=('+' | '-' | '*' | '/' | '%' | '&' | '|' | '^' | '<<' | '>>' | '>>_s' | '+_sat' | '-_sat') right=expr # BinaryExpr
    | left=expr op=('==' | '!=' | '<' | '<=' | '>' | '>=') right=expr # CompareExpr
    | 'if' cond=expr 'then' thenExpr=expr 'else' elseExpr=expr      # TernaryExpr
    | callExpr                                                     # CallExprRule
    | HEX_LITERAL (':' typeRef)?                                   # HexExpr
    | BIN_LITERAL (':' typeRef)?                                   # BinExpr
    | INT_LITERAL (':' typeRef)?                                   # IntExpr
    | BOOL_LITERAL                                                 # BoolExpr
    | ID                                                           # VarExpr
    ;

commentItem
    : BLOCK_COMMENT
    | LINE_COMMENT
    ;

// ==========================================
// Lexer Rules
// ==========================================

BOOL_LITERAL: 'true' | 'false';

HEX_LITERAL: '0' [xX] [0-9a-fA-F]+;
BIN_LITERAL: '0' [bB] [0-1]+;
INT_LITERAL: [0-9]+;

STRING_LITERAL: '"' (~["\r\n\\] | '\\' .)* '"';

ID: [a-zA-Z_] [a-zA-Z0-9_]*;

BLOCK_COMMENT: '/*' .*? '*/' -> channel(HIDDEN);
LINE_COMMENT: '//' ~[\r\n]* -> channel(HIDDEN);

WS: [ \t\r\n]+ -> channel(HIDDEN);
