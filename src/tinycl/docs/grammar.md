# TinyCL Language Grammar

```ebnf

Program       ::= Statements

Statements    ::= Statement*

Statement     ::= FunctionDecl
               | VariableDecl
               | ConstantDecl
               | "if" "(" Expression ")" Block ( "else" Block )?
               | "while" "(" Expression ")" Block
               | "print" "(" Expression ")" ";"
               | "return" Expression ";"
               | Id "=" Expression ";"
               | Id "(" Arguments? ")" ";"
               | Block

FunctionDecl  ::= "func" Id "(" Parameters? ")" Block
VariableDecl  ::= "var" Id "=" Expression ";"
ConstantDecl  ::= "const" Id "=" Expression ";" | VariableDecl

Parameters    ::= Id ( "," Id )*
Arguments     ::= Expression ( "," Expression )*

Block         ::= "{" Statements? "}"

Expression    ::= Equality
Equality      ::= Comparison ( ( "==" | "!=" ) Comparison )*
Comparison    ::= Term ( ( "<" | ">" | "<=" | ">=" ) Term )*
Term          ::= Factor ( ( "+" | "-" ) Factor )*
Factor        ::= Unary ( ( "*" | "/" ) Unary )*
Unary         ::= ( "!" | "-" ) Unary | Postfix

Postfix       ::= Primary ( "[" Expression "]" )*

Primary       ::= "(" Expression ")"
               | Id "(" Arguments? ")"
               | Id
               | Number
               | String
               | Character
               | "true"
               | "false"

String        ::= '"' StringChar* '"'
StringChar    ::= [#x20-#x21] | [#x23-#x5B] | [#x5D-#x7E] | "\\" EscapeChar
EscapeChar    ::= '"' | "'" | "\\" | "n" | "r" | "t" | "0" | "b" | "f" | "v" | "l"

Character     ::= "'" CharChar "'"
CharChar      ::= [#x20-#x26] | [#x28-#x5B] | [#x5D-#x7E] | "\\" EscapeChar

Id            ::= Letter ( Letter | Digit | "_" )*
Number        ::= Digit+
Letter        ::= [a-zA-Z]
Digit         ::= [0-9]

```
