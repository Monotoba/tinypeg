# Appendix C: TinyCL Language Reference

This appendix provides a comprehensive reference for the TinyCL language, including its syntax, semantics, standard library, and example programs.

## C.1 Syntax Reference

### C.1.1 Program Structure

A TinyCL program consists of a sequence of statements:

```
Program ::= Statement*
```

### C.1.2 Statements

TinyCL supports the following types of statements:

```
Statement ::= LetStatement | AssignStatement | IfStatement | WhileStatement | PrintStatement | Block | Comment
```

#### Let Statement

A let statement declares a new variable and initializes it with a value:

```
LetStatement ::= "let" Identifier "=" Expression ";"
```

Example:
```
let x = 42;
```

#### Assignment Statement

An assignment statement assigns a new value to an existing variable:

```
AssignStatement ::= Identifier "=" Expression ";"
```

Example:
```
x = 42;
```

#### If Statement

An if statement conditionally executes code based on a condition:

```
IfStatement ::= "if" "(" Condition ")" Statement ("else" Statement)?
```

Example:
```
if (x > 0) {
    print("Positive");
} else {
    print("Non-positive");
}
```

#### While Statement

A while statement repeatedly executes code as long as a condition is true:

```
WhileStatement ::= "while" "(" Condition ")" Statement
```

Example:
```
while (x > 0) {
    print(x);
    x = x - 1;
}
```

#### Print Statement

A print statement outputs a value:

```
PrintStatement ::= "print" "(" Expression ")" ";"
```

Example:
```
print("Hello, world!");
```

#### Block

A block groups multiple statements together:

```
Block ::= "{" Statement* "}"
```

Example:
```
{
    let x = 1;
    let y = 2;
    print(x + y);
}
```

#### Comment

A comment is a line of text that is ignored by the parser:

```
Comment ::= "#" [^\n]*
```

Example:
```
# This is a comment
```

### C.1.3 Conditions

A condition compares two expressions:

```
Condition ::= Expression ComparisonOp Expression
ComparisonOp ::= "==" | "!=" | "<" | ">" | "<=" | ">="
```

Example:
```
x == 42
y != 0
z < 10
```

### C.1.4 Expressions

Expressions can be combined using arithmetic operators:

```
Expression ::= Term ("+" Term | "-" Term)*
Term ::= Factor ("*" Factor | "/" Factor)*
Factor ::= Number | String | Identifier | "(" Expression ")"
```

Example:
```
2 + 3 * 4
(2 + 3) * 4
"Hello, " + name
```

### C.1.5 Literals

TinyCL supports numeric and string literals:

```
Number ::= [0-9]+
String ::= "\"" [^"]* "\""
```

Example:
```
42
"Hello, world!"
```

### C.1.6 Identifiers

Identifiers are used for variable names:

```
Identifier ::= [a-zA-Z_][a-zA-Z0-9_]*
```

Example:
```
x
counter
first_name
```

## C.2 Standard Library

TinyCL has a minimal standard library with the following built-in functionality:

### C.2.1 Input/Output

- `print(expression)`: Print the value of an expression.

Example:
```
print("Hello, world!");
print(42);
print("The answer is " + 42);
```

### C.2.2 Arithmetic Operations

TinyCL supports the following arithmetic operations:

- Addition: `a + b`
- Subtraction: `a - b`
- Multiplication: `a * b`
- Division: `a / b`

Example:
```
let x = 2 + 3;  # x = 5
let y = x * 4;  # y = 20
let z = y / 2;  # z = 10
let w = z - 1;  # w = 9
```

### C.2.3 String Operations

TinyCL supports string concatenation using the `+` operator:

Example:
```
let name = "Alice";
let greeting = "Hello, " + name + "!";  # greeting = "Hello, Alice!"
```

### C.2.4 Comparison Operations

TinyCL supports the following comparison operations:

- Equal to: `a == b`
- Not equal to: `a != b`
- Less than: `a < b`
- Greater than: `a > b`
- Less than or equal to: `a <= b`
- Greater than or equal to: `a >= b`

Example:
```
if (x == 42) {
    print("x is 42");
}

if (y != 0) {
    print("y is not 0");
}

if (z < 10) {
    print("z is less than 10");
}
```

## C.3 Example Programs

Here are some example TinyCL programs to demonstrate the language's features:

### C.3.1 Hello, World!

```
# Hello, World! program
print("Hello, World!");
```

### C.3.2 Factorial

```
# Calculate factorial
let n = 5;
let factorial = 1;

while (n > 0) {
    factorial = factorial * n;
    n = n - 1;
}

print("Factorial: " + factorial);
```

### C.3.3 Fibonacci Sequence

```
# Calculate Fibonacci numbers
let n = 10;
let a = 0;
let b = 1;
let i = 0;

print("Fibonacci sequence:");
print(a);
print(b);

while (i < n - 2) {
    let c = a + b;
    print(c);
    a = b;
    b = c;
    i = i + 1;
}
```

### C.3.4 FizzBuzz

```
# FizzBuzz program
let i = 1;

while (i <= 100) {
    if (i % 15 == 0) {
        print("FizzBuzz");
    } else {
        if (i % 3 == 0) {
            print("Fizz");
        } else {
            if (i % 5 == 0) {
                print("Buzz");
            } else {
                print(i);
            }
        }
    }
    i = i + 1;
}
```

### C.3.5 Prime Numbers

```
# Print prime numbers up to n
let n = 100;
let i = 2;

while (i <= n) {
    let is_prime = 1;
    let j = 2;
    
    while (j < i) {
        if (i % j == 0) {
            is_prime = 0;
        }
        j = j + 1;
    }
    
    if (is_prime == 1) {
        print(i);
    }
    
    i = i + 1;
}
```

## C.4 Language Limitations

TinyCL is intentionally simple and has several limitations:

1. **Limited Data Types**: TinyCL only supports integers and strings.
2. **No Functions**: TinyCL does not support user-defined functions.
3. **No Arrays or Data Structures**: TinyCL does not support arrays or other data structures.
4. **Limited I/O**: TinyCL only supports output via the `print` statement and has no input capabilities.
5. **No Exception Handling**: TinyCL does not have try-catch blocks or other exception handling mechanisms.
6. **Limited Standard Library**: TinyCL has a minimal standard library.

Despite these limitations, TinyCL is a complete programming language that can express a wide range of algorithms and computations.

## C.5 Future Extensions

Here are some possible extensions to TinyCL that could be implemented:

1. **Functions**: Add support for user-defined functions.
2. **More Data Types**: Add support for floating-point numbers, booleans, and null.
3. **Arrays and Data Structures**: Add support for arrays, lists, and dictionaries.
4. **Input**: Add support for reading input from the user.
5. **Exception Handling**: Add try-catch blocks for handling errors.
6. **Modules**: Add support for importing code from other files.
7. **Standard Library**: Expand the standard library with more functions.

These extensions would make TinyCL more powerful and useful for real-world programming tasks.

## Summary

TinyCL is a simple but complete programming language with variables, control structures, and basic I/O. Its syntax is inspired by popular programming languages like JavaScript and Python, making it easy to learn and use.

This appendix has provided a comprehensive reference for TinyCL, including its syntax, semantics, standard library, and example programs. With this information, you should be able to write and understand TinyCL programs.