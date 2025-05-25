# TinyCL Language Complete Reference

## Overview

TinyCL (Tiny C-Like Language) is a complete, fully-functional programming language implemented using a PEG (Parsing Expression Grammar) parser. It includes a parser, interpreter, and multi-target compiler that can generate both Python and C code.

## Language Features

### 1. Data Types

#### Numbers
```c
var x = 42;
var y = -10;
```

#### Strings
```c
var message = "Hello, World!";
var greeting = "Welcome to TinyCL";
```

#### Characters
```c
var ch = 'A';
var newline = '\n';
```

#### Booleans
```c
var isTrue = true;
var isFalse = false;
```

#### Arrays
```c
var numbers = [1, 2, 3, 4, 5];
var mixed = [x, y, "hello"];
var empty = [];
```

### 2. Variables and Constants

#### Variable Declarations
```c
var x = 10;
var name = "Alice";
var flag = true;
```

#### Constant Declarations
```c
const PI = 3.14159;
const MAX_SIZE = 100;
```

### 3. Operators

#### Arithmetic Operators
```c
var sum = x + y;        // Addition
var diff = x - y;       // Subtraction
var product = x * y;    // Multiplication
var quotient = x / y;   // Division
var negative = -x;      // Unary minus
```

#### Comparison Operators
```c
var isEqual = x == y;       // Equal
var isNotEqual = x != y;    // Not equal
var isLess = x < y;         // Less than
var isGreater = x > y;      // Greater than
var isLessEqual = x <= y;   // Less than or equal (limited support)
var isGreaterEqual = x >= y; // Greater than or equal (limited support)
```

#### Logical Operators
```c
var andResult = x > 0 && y > 0;  // Logical AND
var orResult = x > 0 || y > 0;   // Logical OR
var notResult = !isTrue;         // Logical NOT
```

### 4. Control Flow

#### If-Else Statements
```c
if (condition) {
    // statements
} else {
    // statements
}

// Simple if
if (x > 10) {
    print("x is large");
}
```

#### While Loops
```c
var i = 0;
while (i < 10) {
    print(i);
    i = i + 1;
}
```

### 5. Functions

#### Function Declaration
```c
func add(a, b) {
    return a + b;
}

func greet(name) {
    print("Hello, " + name);
}

func factorial(n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);  // Recursion (limited support)
    }
}
```

#### Function Calls
```c
var result = add(10, 20);
greet("Alice");
var fact = factorial(5);
```

### 6. Array Operations

#### Array Access
```c
var numbers = [1, 2, 3, 4, 5];
var first = numbers[0];
var last = numbers[4];
```

#### Array Assignment
```c
var arr = [1, 2, 3];
// Note: Array element assignment not yet implemented
```

### 7. Comments
```c
# This is a single-line comment
var x = 10;  # End-of-line comment
```

## Expression Precedence

TinyCL follows standard operator precedence:

1. **Parentheses**: `()`
2. **Unary operators**: `!`, `-`
3. **Multiplicative**: `*`, `/`
4. **Additive**: `+`, `-`
5. **Comparison**: `<`, `>`, `<=`, `>=`
6. **Equality**: `==`, `!=`
7. **Logical AND**: `&&`
8. **Logical OR**: `||`

## Built-in Functions

### print()
Outputs a value to the console.
```c
print("Hello, World!");
print(42);
print(x + y);
```

## Example Programs

### Basic Arithmetic
```c
var x = 10;
var y = 20;
var sum = x + y * 2;  // Result: 50 (precedence: 20 * 2 + 10)
print(sum);
```

### Control Flow Example
```c
var age = 18;

if (age >= 18) {
    print("You are an adult");
} else {
    print("You are a minor");
}
```

### Function Example
```c
func calculateArea(width, height) {
    return width * height;
}

var area = calculateArea(10, 5);
print("Area: " + area);
```

### Array Example
```c
var scores = [85, 92, 78, 96, 88];
var total = 0;
var i = 0;

while (i < 5) {
    total = total + scores[i];
    i = i + 1;
}

var average = total / 5;
print("Average score: " + average);
```

## Compilation Targets

### Python Target
TinyCL can compile to Python code:
```python
#!/usr/bin/env python3
"""Generated Python code from TinyCL."""

def main():
    _vars = {}
    _vars['x'] = 10
    _vars['y'] = 20
    _vars['sum'] = (_vars['x'] + (_vars['y'] * 2))
    print(_vars['sum'])
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
```

### C Target
TinyCL can compile to C code:
```c
/* Generated C code from TinyCL */
#include <stdio.h>
#include <stdlib.h>

int main() {
    int x = 10;
    int y = 20;
    int sum = (x + (y * 2));
    printf("%d\n", sum);
    return 0;
}
```

## Usage

### Running the Interpreter
```bash
python examples/tinycl_language/comprehensive_test.py
```

### Using the Compiler
```bash
python src/tinycl/compiler.py
```

## Implementation Status

### ✅ Fully Implemented
- Variable declarations and assignments
- Arithmetic expressions with proper precedence
- Comparison operators (`==`, `!=`, `<`, `>`)
- Logical operators (`&&`, `||`, `!`)
- Unary operators (`-`, `!`)
- If-else statements
- While loops
- Function declarations and calls
- Arrays and array access
- String, number, character, and boolean literals
- Comments
- Multi-target compilation (Python, C)

### ⚠️ Limited Support
- Recursive function calls (basic support)
- Comparison operators `<=`, `>=` (parsing issues)
- Nested function calls in expressions
- Array element assignment

### 🚧 Future Enhancements
- For loops
- Switch statements
- More data types (floats, objects)
- Standard library functions
- Module system
- Error handling (try-catch)
- More compilation targets (JavaScript, Assembly)

## Architecture

The TinyCL implementation consists of:

1. **PEG Parser Library** (`src/peg/`) - Core parsing engine
2. **AST Definitions** (`src/tinycl/ast.py`) - Abstract Syntax Tree nodes
3. **Parser** (`src/tinycl/parser.py`) - TinyCL-specific grammar and parsing
4. **Interpreter** (`src/tinycl/interpreter.py`) - Direct execution engine
5. **Compiler** (`src/tinycl/compiler.py`) - Multi-target code generation
6. **Examples** (`examples/`) - Sample programs and tests

This implementation demonstrates a complete language processing pipeline from source code to executable output.

---

## 👤 Author

**Randall Morgan** - Experienced software engineer specializing in programming language implementation and compiler design.

## 📄 Copyright

Copyright © 2024 Randall Morgan. All rights reserved.
