grammar CPP14;

// =========================================================================
// Official ISO C++14 ANTLR4 Grammar
// Standard implementation based on antlr/grammars-v4/cpp
// =========================================================================

translationUnit
    : declarationseq? EOF
    ;

primaryExpression
    : literal
    | 'this'
    | '(' expression ')'
    | idExpression
    | lambdaExpression
    ;

idExpression
    : unqualifiedId
    | qualifiedId
    ;

unqualifiedId
    : ID
    | operatorFunctionId
    | conversionFunctionId
    | literalOperatorId
    | '~' className
    | templateId
    ;

qualifiedId
    : nestedNameSpecifier 'template'? unqualifiedId
    ;

nestedNameSpecifier
    : (theTypeName | namespaceName)? '::' (nestedNameSpecifier)?
    ;

lambdaExpression
    : lambdaIntroducer lambdaDeclarator? compoundStatement
    ;

lambdaIntroducer
    : '[' lambdaCapture? ']'
    ;

lambdaCapture
    : captureDefault
    | captureList
    | captureDefault ',' captureList
    ;

captureDefault
    : '&'
    | '='
    ;

captureList
    : capture (',' capture)*
    ;

capture
    : simpleCapture
    | initCapture
    ;

simpleCapture
    : '&'? ID
    | 'this'
    ;

initCapture
    : '&'? ID initializer
    ;

lambdaDeclarator
    : '(' parameterDeclarationClause? ')' 'mutable'? exceptionSpecification? attributeSpecifierSeq? trailingReturnType?
    ;

postfixExpression
    : primaryExpression
    | postfixExpression '[' (expression | bracedInitList) ']'
    | postfixExpression '(' expressionList? ')'
    | (simpleTypeNameSpecifier | typeNameSpecifier) '(' expressionList? ')'
    | (simpleTypeNameSpecifier | typeNameSpecifier) bracedInitList
    | postfixExpression '.' 'template'? idExpression
    | postfixExpression '->' 'template'? idExpression
    | postfixExpression '++'
    | postfixExpression '--'
    | ('dynamic_cast' | 'static_cast' | 'reinterpret_cast' | 'const_cast') '<' theTypeId '>' '(' expression ')'
    | 'typeid' '(' (expression | theTypeId) ')'
    ;

expressionList
    : initializerList
    ;

unaryExpression
    : postfixExpression
    | '++' unaryExpression
    | '--' unaryExpression
    | unaryOperator castExpression
    | 'sizeof' (unaryExpression | '(' theTypeId ')')
    | 'sizeof' '...' '(' ID ')'
    | 'alignof' '(' theTypeId ')'
    | noExceptExpression
    | newExpression
    | deleteExpression
    ;

unaryOperator
    : '*' | '&' | '+' | '-' | '!' | '~'
    ;

newExpression
    : '::'? 'new' newPlacement? (newTypeId | '(' theTypeId ')') newInitializer?
    ;

newPlacement
    : '(' expressionList ')'
    ;

newTypeId
    : typeSpecifierSeq newDeclarator?
    ;

newDeclarator
    : pointerOperator newDeclarator?
    | noPointerNewDeclarator
    ;

noPointerNewDeclarator
    : '[' expression ']' attributeSpecifierSeq?
    | noPointerNewDeclarator '[' constantExpression ']' attributeSpecifierSeq?
    ;

newInitializer
    : '(' expressionList? ')'
    | bracedInitList
    ;

deleteExpression
    : '::'? 'delete' ('[' ']')? castExpression
    ;

noExceptExpression
    : 'noexcept' '(' expression ')'
    ;

castExpression
    : unaryExpression
    | '(' theTypeId ')' castExpression
    ;

pmExpression
    : castExpression (('.*' | '->*') castExpression)*
    ;

multiplicativeExpression
    : pmExpression (('*' | '/' | '%') pmExpression)*
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
    : logicalOrExpression ('?' expression ':' assignmentExpression)?
    ;

assignmentExpression
    : conditionalExpression (assignmentOperator initializerClause)?
    | throwExpression
    ;

assignmentOperator
    : '=' | '*=' | '/=' | '%=' | '+=' | '-=' | '>>=' | '<<=' | '&=' | '^=' | '|='
    ;

expression
    : assignmentExpression (',' assignmentExpression)*
    ;

constantExpression
    : conditionalExpression
    ;

// --- Statements ---
statement
    : labeledStatement
    | declarationStatement
    | attributeSpecifierSeq? (
        expressionStatement
        | compoundStatement
        | selectionStatement
        | iterationStatement
        | jumpStatement
        | tryBlock
    )
    ;

labeledStatement
    : attributeSpecifierSeq? (
        ID ':' statement
        | 'case' constantExpression ':' statement
        | 'default' ':' statement
    )
    ;

expressionStatement
    : expression? ';'
    ;

compoundStatement
    : '{' statementSeq? '}'
    ;

statementSeq
    : statement+
    ;

selectionStatement
    : 'if' '(' condition ')' statement ('else' statement)?
    | 'switch' '(' condition ')' statement
    ;

condition
    : expression
    | attributeSpecifierSeq? declSpecifierSeq declarator ('=' initializerClause | bracedInitList)
    ;

iterationStatement
    : 'while' '(' condition ')' statement
    | 'do' statement 'while' '(' expression ')' ';'
    | 'for' '(' initStatement condition? ';' expression? ')' statement
    | 'for' '(' forRangeDeclaration ':' forRangeInitializer ')' statement
    ;

forRangeDeclaration
    : attributeSpecifierSeq? declSpecifierSeq declarator
    ;

forRangeInitializer
    : expression
    | bracedInitList
    ;

initStatement
    : simpleDeclaration
    | expressionStatement
    ;

jumpStatement
    : 'break' ';'
    | 'continue' ';'
    | 'return' (expression | bracedInitList)? ';'
    | 'goto' ID ';'
    ;

declarationStatement
    : blockDeclaration
    ;

throwExpression
    : 'throw' assignmentExpression?
    ;

tryBlock
    : 'try' compoundStatement handlerSeq
    ;

handlerSeq
    : handler+
    ;

handler
    : 'catch' '(' exceptionDeclaration ')' compoundStatement
    ;

exceptionDeclaration
    : attributeSpecifierSeq? typeSpecifierSeq (declarator | abstractDeclarator)?
    | '...'
    ;

// --- Declarations ---
declarationseq
    : declaration+
    ;

declaration
    : functionDefinition
    | blockDeclaration
    | templateDeclaration
    | explicitInstantiation
    | explicitSpecialization
    | linkageSpecification
    | namespaceDefinition
    | emptyDeclaration
    | attributeDeclaration
    ;

blockDeclaration
    : simpleDeclaration
    | asmDefinition
    | namespaceAliasDefinition
    | usingDeclaration
    | usingDirective
    | staticAssertDeclaration
    | aliasDeclaration
    | opaqueEnumDeclaration
    ;

simpleDeclaration
    : declSpecifierSeq? initDeclaratorList? ';'
    | attributeSpecifierSeq declSpecifierSeq? initDeclaratorList ';'
    ;

emptyDeclaration
    : ';'
    ;

attributeDeclaration
    : attributeSpecifierSeq ';'
    ;

declSpecifier
    : storageClassSpecifier
    | typeSpecifier
    | functionSpecifier
    | 'friend'
    | 'typedef'
    | 'constexpr'
    ;

declSpecifierSeq
    : declSpecifier+ attributeSpecifierSeq?
    ;

storageClassSpecifier
    : 'register'
    | 'static'
    | 'thread_local'
    | 'extern'
    | 'mutable'
    | 'auto'
    ;

functionSpecifier
    : 'inline'
    | 'virtual'
    | 'explicit'
    ;

typedefName
    : ID
    ;

theTypeName
    : className
    | enumName
    | typedefName
    | simpleTemplateId
    ;

typeSpecifier
    : trailingTypeSpecifier
    | classSpecifier
    | enumSpecifier
    ;

trailingTypeSpecifier
    : simpleTypeSpecifier
    | elaboratedTypeSpecifier
    | typeNameSpecifier
    | cvQualifier
    ;

typeSpecifierSeq
    : typeSpecifier+ attributeSpecifierSeq?
    ;

trailingTypeSpecifierSeq
    : trailingTypeSpecifier+ attributeSpecifierSeq?
    ;

simpleTypeSpecifier
    : nestedNameSpecifier? theTypeName
    | nestedNameSpecifier 'template' simpleTemplateId
    | 'char'
    | 'char16_t'
    | 'char32_t'
    | 'wchar_t'
    | 'bool'
    | 'short'
    | 'int'
    | 'long'
    | 'signed'
    | 'unsigned'
    | 'float'
    | 'double'
    | 'void'
    | 'auto'
    | decltypeSpecifier
    ;

theTypeId
    : typeSpecifierSeq abstractDeclarator?
    ;

decltypeSpecifier
    : 'decltype' '(' (expression | 'auto') ')'
    ;

typeNameSpecifier
    : 'typename' nestedNameSpecifier (ID | 'template'? simpleTemplateId)
    ;

simpleTypeNameSpecifier
    : theTypeName
    | simpleTypeSpecifier
    ;

elaboratedTypeSpecifier
    : classKey (attributeSpecifierSeq? nestedNameSpecifier? ID | simpleTemplateId | nestedNameSpecifier 'template'? simpleTemplateId)
    | 'enum' nestedNameSpecifier? ID
    ;

enumName
    : ID
    ;

enumSpecifier
    : enumHead '{' (enumeratorList ','?)? '}'
    ;

enumHead
    : enumKey attributeSpecifierSeq? (nestedNameSpecifier? ID)? enumBase?
    ;

opaqueEnumDeclaration
    : enumKey attributeSpecifierSeq? ID enumBase? ';'
    ;

enumKey
    : 'enum' ('class' | 'struct')?
    ;

enumBase
    : ':' typeSpecifierSeq
    ;

enumeratorList
    : enumeratorDefinition (',' enumeratorDefinition)*
    ;

enumeratorDefinition
    : enumerator ('=' constantExpression)?
    ;

enumerator
    : ID
    ;

namespaceName
    : originalNamespaceName
    | namespaceAlias
    ;

originalNamespaceName
    : ID
    ;

namespaceDefinition
    : 'inline'? 'namespace' (ID | originalNamespaceName)? '{' namespaceBody '}'
    ;

namespaceBody
    : declarationseq?
    ;

namespaceAlias
    : ID
    ;

namespaceAliasDefinition
    : 'namespace' ID '=' qualifiedNamespaceSpecifier ';'
    ;

qualifiedNamespaceSpecifier
    : nestedNameSpecifier? namespaceName
    ;

usingDeclaration
    : 'using' 'typename'? nestedNameSpecifier unqualifiedId ';'
    ;

usingDirective
    : attributeSpecifierSeq? 'using' 'namespace' nestedNameSpecifier? namespaceName ';'
    ;

asmDefinition
    : attributeSpecifierSeq? 'asm' '(' STRING_LITERAL ')' ';'
    ;

linkageSpecification
    : 'extern' STRING_LITERAL ('{' declarationseq? '}' | declaration)
    ;

attributeSpecifierSeq
    : attributeSpecifier+
    ;

attributeSpecifier
    : '[' '[' attributeList ']' ']'
    | alignmentSpecifier
    ;

alignmentSpecifier
    : 'alignas' '(' (theTypeId | constantExpression) ')'
    | '_Alignas' '(' (theTypeId | constantExpression) ')'
    ;

attributeList
    : (attribute (',' attribute)*)?
    ;

attribute
    : (attributeNamespace '::')? ID ('(' expressionList? ')')?
    ;

attributeNamespace
    : ID
    ;

// --- Declarators ---
initDeclaratorList
    : initDeclarator (',' initDeclarator)*
    ;

initDeclarator
    : declarator initializer?
    ;

declarator
    : pointerOperator* noPointerDeclarator
    ;

noPointerDeclarator
    : noPointerDeclarator '[' constantExpression? ']' attributeSpecifierSeq?
    | noPointerDeclarator parametersAndQualifiers trailingReturnType?
    | '(' declarator ')'
    | declaratorid attributeSpecifierSeq?
    ;

parametersAndQualifiers
    : '(' parameterDeclarationClause? ')' cvqualifierSeq? refqualifier? exceptionSpecification? attributeSpecifierSeq?
    ;

exceptionSpecification
    : dynamicExceptionSpecification
    | noexceptSpecification
    ;

dynamicExceptionSpecification
    : 'throw' '(' theTypeIdList? ')'
    ;

theTypeIdList
    : theTypeId (',' theTypeId)*
    ;

noexceptSpecification
    : 'noexcept' ('(' constantExpression ')')?
    ;

trailingReturnType
    : '->' trailingTypeSpecifierSeq abstractDeclarator?
    ;

pointerOperator
    : ('*' | '&' | '&&') attributeSpecifierSeq? cvqualifierSeq?
    | nestedNameSpecifier '*' attributeSpecifierSeq? cvqualifierSeq?
    ;

cvqualifierSeq
    : cvQualifier+
    ;

cvQualifier
    : 'const'
    | 'volatile'
    ;

refqualifier
    : '&'
    | '&&'
    ;

declaratorid
    : '...'? idExpression
    ;

abstractDeclarator
    : pointerOperator* noPointerAbstractDeclarator? parametersAndQualifiers trailingReturnType?
    | pointerOperator+
    ;

noPointerAbstractDeclarator
    : '(' abstractDeclarator ')' ('[' constantExpression? ']' attributeSpecifierSeq? | '(' parametersAndQualifiers ')')*
    | ('[' constantExpression? ']' attributeSpecifierSeq? | '(' parametersAndQualifiers ')')+
    ;

parameterDeclarationClause
    : parameterDeclarationList (','? '...')?
    ;

parameterDeclarationList
    : parameterDeclaration (',' parameterDeclaration)*
    ;

parameterDeclaration
    : attributeSpecifierSeq? declSpecifierSeq (declarator | abstractDeclarator?) ('=' initializerClause)?
    ;

// --- Function Definition ---
functionDefinition
    : attributeSpecifierSeq? declSpecifierSeq? declarator virtSpecifierSeq? functionBody
    ;

functionBody
    : ctorInitializer? compoundStatement
    | functionTryBlock
    | '=' ('default' | 'delete') ';'
    ;

functionTryBlock
    : 'try' ctorInitializer? compoundStatement handlerSeq
    ;

virtSpecifierSeq
    : virtSpecifier+
    ;

virtSpecifier
    : 'override'
    | 'final'
    ;

// --- Classes ---
classSpecifier
    : classHead '{' memberSpecification? '}'
    ;

classHead
    : classKey attributeSpecifierSeq? (classHeadName classVirtSpecifierSeq?)? baseClause?
    ;

classHeadName
    : nestedNameSpecifier? className
    ;

classVirtSpecifierSeq
    : classVirtSpecifier+
    ;

classVirtSpecifier
    : 'final'
    ;

classKey
    : 'class'
    | 'struct'
    | 'union'
    ;

className
    : ID
    | simpleTemplateId
    ;

memberSpecification
    : (memberDeclaration | accessSpecifier ':')+
    ;

memberDeclaration
    : functionDefinition
    | attributeSpecifierSeq? declSpecifierSeq? memberDeclaratorList? ';'
    | usingDeclaration
    | staticAssertDeclaration
    | templateDeclaration
    | aliasDeclaration
    | emptyDeclaration
    ;

memberDeclaratorList
    : memberDeclarator (',' memberDeclarator)*
    ;

memberDeclarator
    : declarator (virtSpecifierSeq? pureSpecifier? | braceOrEqualInitializer?)
    | ID? attributeSpecifierSeq? ':' constantExpression
    ;

pureSpecifier
    : '=' (INT_LITERAL | '0')
    ;

accessSpecifier
    : 'private'
    | 'protected'
    | 'public'
    ;

baseClause
    : ':' baseSpecifierList
    ;

baseSpecifierList
    : baseSpecifier (',' baseSpecifier)*
    ;

baseSpecifier
    : attributeSpecifierSeq? ('virtual' accessSpecifier? | accessSpecifier 'virtual'?)? baseTypeSpecifier
    ;

baseTypeSpecifier
    : classOrDeclType
    ;

classOrDeclType
    : nestedNameSpecifier? className
    | decltypeSpecifier
    ;

ctorInitializer
    : ':' memInitializerList
    ;

memInitializerList
    : memInitializer (',' memInitializer)*
    ;

memInitializer
    : memInitializerId ('(' expressionList? ')' | bracedInitList)
    ;

memInitializerId
    : classOrDeclType
    | ID
    ;

// --- Templates ---
templateDeclaration
    : 'template' '<' templateParameterList '>' declaration
    ;

templateParameterList
    : templateParameter (',' templateParameter)*
    ;

templateParameter
    : typeParameter
    | parameterDeclaration
    ;

typeParameter
    : ('class' | 'typename') ('...'? ID ('=' theTypeId)?)?
    | ('class' | 'typename') ('=' theTypeId)
    | 'template' '<' templateParameterList '>' ('class' | 'typename') ('...'? ID ('=' idExpression)?)?
    | 'template' '<' templateParameterList '>' ('class' | 'typename') ('=' idExpression)
    ;

simpleTemplateId
    : templateName '<' templateArgumentList? '>'
    ;

templateId
    : simpleTemplateId
    | (operatorFunctionId | literalOperatorId) '<' templateArgumentList? '>'
    ;

templateName
    : ID
    ;

templateArgumentList
    : templateArgument (',' templateArgument)*
    ;

templateArgument
    : theTypeId
    | constantExpression
    | idExpression
    ;

explicitInstantiation
    : 'extern'? 'template' declaration
    ;

explicitSpecialization
    : 'template' '<' '>' declaration
    ;

aliasDeclaration
    : 'using' ID attributeSpecifierSeq? '=' theTypeId ';'
    ;

staticAssertDeclaration
    : 'static_assert' '(' constantExpression ',' STRING_LITERAL ')' ';'
    ;

operatorFunctionId
    : 'operator' theOperator
    ;

literalOperatorId
    : 'operator' STRING_LITERAL ID
    ;

conversionFunctionId
    : 'operator' conversionTypeId
    ;

conversionTypeId
    : typeSpecifierSeq conversionDeclarator?
    ;

conversionDeclarator
    : pointerOperator*
    ;

theOperator
    : 'new' | 'delete' | 'new' '[' ']' | 'delete' '[' ']' | '+' | '-' | '*' | '/' | '%' | '^' | '&' | '|' | '~'
    | '!' | '=' | '<' | '>' | '+=' | '-=' | '*=' | '/=' | '%=' | '^=' | '&=' | '|=' | '<<'
    | '>>' | '>>=' | '<<=' | '==' | '!=' | '<=' | '>=' | '&&' | '||' | '++' | '--' | ','
    | '->*' | '->' | '(' ')' | '[' ']'
    ;

initializer
    : braceOrEqualInitializer
    | '(' expressionList ')'
    ;

braceOrEqualInitializer
    : '=' initializerClause
    | bracedInitList
    ;

initializerClause
    : assignmentExpression
    | bracedInitList
    ;

initializerList
    : initializerClause (',' initializerClause)*
    ;

bracedInitList
    : '{' (initializerList ','?)? '}'
    ;

literal
    : INT_LITERAL
    | '0'
    | HEX_LITERAL
    | BIN_LITERAL
    | FLOAT_LITERAL
    | CHAR_LITERAL
    | STRING_LITERAL
    | BOOL_LITERAL
    | 'nullptr'
    ;

// =========================================================================
// Lexer Rules for C++14
// =========================================================================

PREPROCESSOR_DIRECTIVE: '#' ~[\r\n]* -> channel(HIDDEN);

BOOL_LITERAL: 'true' | 'false';

HEX_LITERAL: '0' [xX] [0-9a-fA-F]+ [uUlLzZ]*;
BIN_LITERAL: '0' [bB] [0-1]+ [uUlLzZ]*;
FLOAT_LITERAL: [0-9]+ '.' [0-9]* ([eE] [+-]? [0-9]+)? [fFlL]?
             | '.' [0-9]+ ([eE] [+-]? [0-9]+)? [fFlL]?
             | [0-9]+ [eE] [+-]? [0-9]+ [fFlL]?;
INT_LITERAL: [0-9]+ [uUlLzZ]*;

CHAR_LITERAL: '\'' (~['\r\n\\] | '\\' .) '\'';
STRING_LITERAL: '"' (~["\r\n\\] | '\\' .)* '"';

ID: [a-zA-Z_] [a-zA-Z0-9_]*;

BLOCK_COMMENT: '/*' .*? '*/' -> channel(HIDDEN);
LINE_COMMENT: '//' ~[\r\n]* -> channel(HIDDEN);

WS: [ \t\r\n]+ -> channel(HIDDEN);
