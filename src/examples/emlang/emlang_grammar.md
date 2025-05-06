```ebnf
Program ::= Statement+
Statement ::= "print" "(" Expression ")"
            | Identifier "=" Expression
Expression ::= Number | Identifier
Number     ::= [0-9]+
Identifier ::= [a-zA-Z_][a-zA-Z0-9_]*

```
