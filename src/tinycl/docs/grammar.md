# TinyCL Language Grammar - Complete Implementation

This grammar specification matches the current implementation in the TinyCL parser, interpreter, and compiler.

## Overview

TinyCL is a complete programming language with:
- Variables, constants, and functions with proper scoping
- Arrays with indexing and dynamic creation
- Complete control flow (if-else, while loops)
- All data types (numbers, strings, characters, booleans, arrays)
- Full operator support with proper precedence
- Multi-target compilation (Python and C)

## Complete Grammar (EBNF)

```ebnf

Program       ::= Statements

Statements    ::= Statement*

Statement     ::= FunctionDecl
               | VariableDecl
               | ConstantDecl
               | "if" "(" Expression ")" Block ( "else" Block )?
               | "while" "(" Expression ")" Block
               | "print" "(" Expression ")" ";"
               | "return" Expression? ";"
               | Id "=" Expression ";"
               | Id "(" Arguments? ")" ";"
               | Block
               | Comment

FunctionDecl  ::= "func" Id "(" Parameters? ")" Block
VariableDecl  ::= "var" Id "=" Expression ";"
ConstantDecl  ::= "const" Id "=" Expression ";"

Parameters    ::= Id ( "," Id )*
Arguments     ::= Expression ( "," Expression )*

Block         ::= "{" Statements? "}"

# Expression hierarchy with proper precedence
Expression    ::= LogicalOr
LogicalOr     ::= LogicalAnd ( "||" LogicalAnd )*
LogicalAnd    ::= Equality ( "&&" Equality )*
Equality      ::= Comparison ( ( "!=" | "==" ) Comparison )*
Comparison    ::= Term ( ( "<=" | ">=" | "<" | ">" ) Term )*
Term          ::= Factor ( ( "+" | "-" ) Factor )*
Factor        ::= Unary ( ( "*" | "/" ) Unary )*
Unary         ::= ( "!" | "-" )? Postfix
Postfix       ::= Primary ( "[" Expression "]" )*

Primary       ::= "(" Expression ")"
               | Id "(" Arguments? ")"
               | "[" Arguments? "]"
               | Id
               | Number
               | String
               | Character
               | "true"
               | "false"

# Literals
String        ::= '"' StringChar* '"'
StringChar    ::= [#x20-#x21] | [#x23-#x5B] | [#x5D-#x7E] | "\\" EscapeChar
EscapeChar    ::= '"' | "'" | "\\" | "n" | "r" | "t" | "0" | "b" | "f" | "v" | "l"

Character     ::= "'" CharChar "'"
CharChar      ::= [#x20-#x26] | [#x28-#x5B] | [#x5D-#x7E] | "\\" EscapeChar

Id            ::= Letter ( Letter | Digit | "_" )*
Number        ::= Digit+
Letter        ::= [a-zA-Z]
Digit         ::= [0-9]

Comment       ::= "#" [^\n]*

```

## Operator Precedence (Implemented)

From highest to lowest precedence:

1. **Primary expressions**: literals, identifiers, function calls, parentheses `()`
2. **Postfix operators**: array access `[]`
3. **Unary operators**: logical NOT `!`, unary minus `-`
4. **Multiplicative**: multiplication `*`, division `/`
5. **Additive**: addition `+`, subtraction `-`
6. **Comparison**: less than `<`, greater than `>`, less/greater equal `<=`, `>=`
7. **Equality**: equal `==`, not equal `!=`
8. **Logical AND**: `&&`
9. **Logical OR**: `||`

## Implementation Status

### ✅ Fully Implemented Features

- **All data types**: Numbers, strings, characters, booleans, arrays
- **All operators**: Arithmetic, comparison, logical, unary with correct precedence
- **Variables and constants**: Proper declaration and scoping
- **Functions**: Declaration, calls, parameters, returns, local scope
- **Control flow**: If-else statements, while loops, nested blocks
- **Arrays**: Creation `[1, 2, 3]`, indexing `arr[0]`, mixed-type support
- **Comments**: Full comment support `# comment`
- **Expression evaluation**: Complex nested expressions
- **Multi-target compilation**: Python and C code generation

### Example Programs

#### Complete Feature Demo
```c
# Variables and constants
var x = 10;
const PI = 3;

# Arrays
var numbers = [1, 2, 3, 4, 5];
var mixed = [x, "hello", true];

# Functions
func add(a, b) {
    return a + b;
}

# Complex expressions with precedence
var result = x + numbers[0] * 2;  # 10 + (1 * 2) = 12

# Control flow
if (result > 10 && x < 20) {
    print("Valid result: " + result);
}

# Loops with arrays
var i = 0;
while (i < 5) {
    print("Number: " + numbers[i]);
    i = i + 1;
}
```

This grammar is fully implemented and tested in the current TinyCL parser, interpreter, and compiler.
