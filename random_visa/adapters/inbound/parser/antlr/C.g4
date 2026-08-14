grammar C;

// =========================================================================
// Official ISO C11 / C99 ANTLR4 Grammar
// =========================================================================

compilationUnit
    : translationUnit? EOF
    ;

translationUnit
    : externalDeclaration+
    ;

externalDeclaration
    : functionDefinition
    | declaration
    | ';'
    ;

functionDefinition
    : declarationSpecifiers? declarator declarationList? compoundStatement
    ;

declarationList
    : declaration+
    ;

declaration
    : declarationSpecifiers initDeclaratorList? ';'
    | staticAssertDeclaration
    ;

declarationSpecifiers
    : declarationSpecifier+
    ;

declarationSpecifier
    : storageClassSpecifier
    | typeSpecifier
    | typeQualifier
    | functionSpecifier
    | alignmentSpecifier
    ;

initDeclaratorList
    : initDeclarator (',' initDeclarator)*
    ;

initDeclarator
    : declarator ('=' initializer)?
    ;

storageClassSpecifier
    : 'typedef'
    | 'extern'
    | 'static'
    | '_Thread_local'
    | 'auto'
    | 'register'
    ;

typeSpecifier
    : 'void'
    | 'char'
    | 'short'
    | 'int'
    | 'long'
    | 'float'
    | 'double'
    | 'signed'
    | 'unsigned'
    | '_Bool'
    | '_Complex'
    | '__m128'
    | '__m256'
    | '__m512'
    | atomicTypeSpecifier
    | structOrUnionSpecifier
    | enumSpecifier
    | typedefName
    ;

structOrUnionSpecifier
    : structOrUnion (ID)? '{' structDeclarationList '}'
    | structOrUnion ID
    ;

structOrUnion
    : 'struct'
    | 'union'
    ;

structDeclarationList
    : structDeclaration+
    ;

structDeclaration
    : specifierQualifierList (structDeclaratorList)? ';'
    | staticAssertDeclaration
    ;

specifierQualifierList
    : (typeSpecifier | typeQualifier)+
    ;

structDeclaratorList
    : structDeclarator (',' structDeclarator)*
    ;

structDeclarator
    : declarator
    | declarator? ':' constantExpression
    ;

enumSpecifier
    : 'enum' (ID)? '{' enumeratorList ','? '}'
    | 'enum' ID
    ;

enumeratorList
    : enumerator (',' enumerator)*
    ;

enumerator
    : enumerationConstant ('=' constantExpression)?
    ;

enumerationConstant
    : ID
    ;

atomicTypeSpecifier
    : '_Atomic' '(' typeName ')'
    ;

typeQualifier
    : 'const'
    | 'restrict'
    | 'volatile'
    | '_Atomic'
    ;

functionSpecifier
    : 'inline'
    | '_Noreturn'
    | '__inline__'
    | '__attribute__' '(' '(' argumentExpressionList? ')' ')'
    ;

alignmentSpecifier
    : '_Alignas' '(' (typeName | constantExpression) ')'
    ;

declarator
    : pointer? directDeclarator
    ;

directDeclarator
    : ID
    | '(' declarator ')'
    | directDeclarator '[' typeQualifierList? assignmentExpression? ']'
    | directDeclarator '(' parameterTypeList ')'
    | directDeclarator '(' identifierList? ')'
    ;

pointer
    : ('*' typeQualifierList?)+
    ;

typeQualifierList
    : typeQualifier+
    ;

parameterTypeList
    : parameterList (',' '...')?
    ;

parameterList
    : parameterDeclaration (',' parameterDeclaration)*
    ;

parameterDeclaration
    : declarationSpecifiers declarator
    | declarationSpecifiers abstractDeclarator?
    ;

identifierList
    : ID (',' ID)*
    ;

typeName
    : specifierQualifierList abstractDeclarator?
    ;

abstractDeclarator
    : pointer
    | pointer? directAbstractDeclarator
    ;

directAbstractDeclarator
    : '(' abstractDeclarator ')'
    | '[' typeQualifierList? assignmentExpression? ']'
    | directAbstractDeclarator '[' typeQualifierList? assignmentExpression? ']'
    | '(' parameterTypeList? ')'
    | directAbstractDeclarator '(' parameterTypeList? ')'
    ;

typedefName
    : ID
    ;

initializer
    : assignmentExpression
    | '{' initializerList ','? '}'
    ;

initializerList
    : (designation? initializer) (',' (designation? initializer))*
    ;

designation
    : designatorList '='
    ;

designatorList
    : designator+
    ;

designator
    : '[' constantExpression ']'
    | '.' ID
    ;

staticAssertDeclaration
    : '_Static_assert' '(' constantExpression ',' STRING_LITERAL ')' ';'
    ;

// --- Statements ---
statement
    : labeledStatement
    | compoundStatement
    | expressionStatement
    | selectionStatement
    | iterationStatement
    | jumpStatement
    ;

labeledStatement
    : ID ':' statement
    | 'case' constantExpression ':' statement
    | 'default' ':' statement
    ;

compoundStatement
    : '{' blockItemList? '}'
    ;

blockItemList
    : blockItem+
    ;

blockItem
    : declaration
    | statement
    ;

expressionStatement
    : expression? ';'
    ;

selectionStatement
    : 'if' '(' expression ')' statement ('else' statement)?
    | 'switch' '(' expression ')' statement
    ;

iterationStatement
    : 'while' '(' expression ')' statement
    | 'do' statement 'while' '(' expression ')' ';'
    | 'for' '(' (declaration | expressionStatement) expressionStatement expression? ')' statement
    ;

jumpStatement
    : 'goto' ID ';'
    | 'continue' ';'
    | 'break' ';'
    | 'return' expression? ';'
    ;

// --- Expressions ---
primaryExpression
    : ID
    | constant
    | STRING_LITERAL
    | '(' expression ')'
    | '(' compoundStatement ')'
    ;

constant
    : INT_LITERAL
    | HEX_LITERAL
    | BIN_LITERAL
    | FLOAT_LITERAL
    | CHAR_LITERAL
    ;

postfixExpression
    : primaryExpression
    | postfixExpression '[' expression ']'
    | postfixExpression '(' argumentExpressionList? ')'
    | postfixExpression '.' ID
    | postfixExpression '->' ID
    | postfixExpression '++'
    | postfixExpression '--'
    | '(' typeName ')' '{' initializerList ','? '}'
    ;

argumentExpressionList
    : assignmentExpression (',' assignmentExpression)*
    ;

unaryExpression
    : postfixExpression
    | '++' unaryExpression
    | '--' unaryExpression
    | unaryOperator castExpression
    | 'sizeof' unaryExpression
    | 'sizeof' '(' typeName ')'
    | '_Alignof' '(' typeName ')'
    ;

unaryOperator
    : '&' | '*' | '+' | '-' | '~' | '!'
    ;

castExpression
    : '(' typeName ')' castExpression
    | unaryExpression
    ;

multiplicativeExpression
    : castExpression (('*' | '/' | '%') castExpression)*
    ;

additiveExpression
    : multiplicativeExpression (('+' | '-') multiplicativeExpression)*
    ;

shiftExpression
    : additiveExpression (('<<' | '>>') additiveExpression)*
    ;

relationalExpression
    : shiftExpression (('<' | '>' | '<=' | '>=') shiftExpression)*
    ;

equalityExpression
    : relationalExpression (('==' | '!=') relationalExpression)*
    ;

andExpression
    : equalityExpression ('&' equalityExpression)*
    ;

exclusiveOrExpression
    : andExpression ('^' andExpression)*
    ;

inclusiveOrExpression
    : exclusiveOrExpression ('|' exclusiveOrExpression)*
    ;

logicalAndExpression
    : inclusiveOrExpression ('&&' inclusiveOrExpression)*
    ;

logicalOrExpression
    : logicalAndExpression ('||' logicalAndExpression)*
    ;

conditionalExpression
    : logicalOrExpression ('?' expression ':' conditionalExpression)?
    ;

assignmentExpression
    : conditionalExpression
    | unaryExpression assignmentOperator assignmentExpression
    ;

assignmentOperator
    : '=' | '*=' | '/=' | '%=' | '+=' | '-=' | '<<=' | '>>=' | '&=' | '^=' | '|='
    ;

expression
    : assignmentExpression (',' assignmentExpression)*
    ;

constantExpression
    : conditionalExpression
    ;

// =========================================================================
// Lexer Rules for C
// =========================================================================

PREPROCESSOR_DIRECTIVE: '#' ~[\r\n]* -> channel(HIDDEN);

HEX_LITERAL: '0' [xX] [0-9a-fA-F]+ [uUlL]*;
BIN_LITERAL: '0' [bB] [0-1]+ [uUlL]*;
FLOAT_LITERAL: [0-9]+ '.' [0-9]* ([eE] [+-]? [0-9]+)? [fFlL]?
             | '.' [0-9]+ ([eE] [+-]? [0-9]+)? [fFlL]?
             | [0-9]+ [eE] [+-]? [0-9]+ [fFlL]?;
INT_LITERAL: [0-9]+ [uUlL]*;

CHAR_LITERAL: '\'' (~['\r\n\\] | '\\' .) '\'';
STRING_LITERAL: '"' (~["\r\n\\] | '\\' .)* '"';

ID: [a-zA-Z_] [a-zA-Z0-9_]*;

BLOCK_COMMENT: '/*' .*? '*/' -> channel(HIDDEN);
LINE_COMMENT: '//' ~[\r\n]* -> channel(HIDDEN);

WS: [ \t\r\n]+ -> channel(HIDDEN);
