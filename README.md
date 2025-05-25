# TinyPEG: A Complete PEG Parser Library with TinyCL Programming Language

TinyPEG is a comprehensive Parsing Expression Grammar (PEG) library implemented in Python, featuring a complete TinyCL (Tiny C-Like Language) programming language with parser, interpreter, and multi-target compiler.

## 🚀 Features

### Core PEG Parser Library
- **Complete PEG Implementation**: All standard PEG operators and expressions
- **Robust Reference Handling**: Proper forward references and circular dependencies
- **Extensible Architecture**: Easy to build new language parsers
- **Error Handling**: Comprehensive parsing error reporting

### TinyCL Programming Language - FULLY IMPLEMENTED
- **Complete Language**: Variables, functions, control flow, arrays, operators
- **Multi-target Compiler**: Generates executable Python and C code
- **Direct Interpreter**: Execute TinyCL code immediately
- **Production Quality**: Handles complex programs with proper scoping and precedence

## Installation

Clone the repository:

```bash
git clone https://github.com/Monotoba/tinypeg.git
cd tinypeg
```

## 🎯 Quick Start

### Running TinyCL Programs

```python
from src.tinycl.parser import TinyCLParser
from src.tinycl.interpreter import TinyCLInterpreter

# Create parser and interpreter
parser = TinyCLParser()
interpreter = TinyCLInterpreter()

# TinyCL program with all features
program = """
# Variables and arithmetic with proper precedence
var x = 10;
var y = 20;
var sum = x + y * 2;  # Result: 50 (20*2 + 10)

# Functions
func multiply(a, b) {
    return a * b;
}

# Arrays
var numbers = [1, 2, 3, 4, 5];
var result = multiply(sum, numbers[0]);

# Control flow
if (result > 40) {
    print("Large result: " + result);
} else {
    print("Small result: " + result);
}

# Loops
var i = 0;
while (i < 3) {
    print("Count: " + i);
    i = i + 1;
}
"""

# Parse and execute
ast = parser.parse(program)
interpreter.interpret(ast)
```

### Compiling TinyCL Code

```python
from src.tinycl.compiler import TinyCLCompiler

compiler = TinyCLCompiler()

# Generate Python code
python_code = compiler.compile(program, 'python')

# Generate C code
c_code = compiler.compile(program, 'c')
```

## 📋 TinyCL Language Features - Complete Implementation

| Feature | Status | Example |
|---------|--------|---------|
| **Variables** | ✅ Complete | `var x = 10;` |
| **Constants** | ✅ Complete | `const PI = 3.14;` |
| **Functions** | ✅ Complete | `func add(a, b) { return a + b; }` |
| **Arrays** | ✅ Complete | `var arr = [1, 2, 3]; print(arr[0]);` |
| **If-Else** | ✅ Complete | `if (x > 0) { ... } else { ... }` |
| **While Loops** | ✅ Complete | `while (i < 10) { i = i + 1; }` |
| **Arithmetic** | ✅ Complete | `+`, `-`, `*`, `/` with proper precedence |
| **Comparison** | ✅ Complete | `==`, `!=`, `<`, `>` |
| **Logical** | ✅ Complete | `&&`, `||`, `!` |
| **Data Types** | ✅ Complete | Numbers, strings, characters, booleans, arrays |
| **Comments** | ✅ Complete | `# This is a comment` |
| **Compilation** | ✅ Complete | Python and C code generation |

## 🎨 Example Programs

### Basic Calculator
```c
# Simple calculator with functions
func add(a, b) { return a + b; }
func multiply(a, b) { return a * b; }

var x = 10;
var y = 5;
var sum = add(x, y);
var product = multiply(x, y);

print("Sum: " + sum);        # Outputs: Sum: 15
print("Product: " + product); # Outputs: Product: 50
```

### Array Processing
```c
# Array operations and loops
var numbers = [10, 20, 30, 40, 50];
var total = 0;
var i = 0;

while (i < 5) {
    total = total + numbers[i];
    print("Adding: " + numbers[i]);
    i = i + 1;
}

print("Total: " + total);  # Outputs: Total: 150
```

### Complex Logic
```c
# Advanced control flow and expressions
var age = 25;
var hasLicense = true;
var canDrive = age >= 18 && hasLicense;

if (canDrive) {
    print("Can drive!");
} else {
    print("Cannot drive");
}

# Nested conditions
var score = 85;
if (score >= 90) {
    print("Grade: A");
} else {
    if (score >= 80) {
        print("Grade: B");
    } else {
        print("Grade: C");
    }
}
```

## 🚀 Getting Started

### Run the Examples

```bash
# Run comprehensive TinyCL test
python examples/tinycl_language/comprehensive_test.py

# Run individual TinyCL programs
python -c "
from src.tinycl.parser import TinyCLParser
from src.tinycl.interpreter import TinyCLInterpreter
parser = TinyCLParser()
interpreter = TinyCLInterpreter()
with open('examples/tinycl_language/basic/hello_world.tcl') as f:
    program = f.read()
ast = parser.parse(program)
interpreter.interpret(ast)
"

# Test PEG library usage
python examples/peg_usage/basic/simple_parser.py

# Test the compiler
python src/tinycl/compiler.py
```

### Expected Output
```
=== TinyCL Language Test ===
=== Variables ===
10
20
3
=== Arithmetic ===
50
25
100.0
=== Functions ===
30
200
30
=== Arrays ===
1
5
50
=== ALL TESTS COMPLETED SUCCESSFULLY! ===
```

## 📚 Documentation

### Complete References
- **[TinyCL Language Reference](TINYCL_COMPLETE_REFERENCE.md)** - Complete language documentation
- **[Grammar Specification](src/tinycl/docs/grammar.md)** - Formal grammar definition

### Complete E-Book: "Building Parsers with PEG"
**📚 Professional technical book with comprehensive coverage:**
- **[Complete PDF Ebook](docs/ebook/pdf/tinypeg_complete_ebook.pdf)** - Full book with covers (517 KB)
- **[HTML Version](docs/ebook/html/)** - Web-readable format
- **[Markdown Source](docs/ebook/markdown/)** - Source documentation

**📖 Chapters:**
- [Chapter 1](docs/ebook/markdown/chapter01_peg_basics.md): Understanding PEG Parsers
- [Chapter 2](docs/ebook/markdown/chapter02_library_overview.md): TinyPEG Library Overview
- [Chapter 3](docs/ebook/markdown/chapter03_building_parsers.md): Building Your First Parser
- [Chapter 4](docs/ebook/markdown/chapter04_examples.md): Example Parsers and Applications
- [Chapter 5](docs/ebook/markdown/chapter05_tiny_language.md): Creating TinyCL - A Complete Programming Language

**📋 Appendices:**
- [Appendix A](docs/ebook/markdown/appendix_a_peg_reference.md): TinyPEG Library Reference
- [Appendix B](docs/ebook/markdown/appendix_b_testing.md): Testing Framework
- [Appendix C](docs/ebook/markdown/appendix_c_tinycl_reference.md): TinyCL Language Reference

### Reference Documentation
- [Index](docs/index.md): Overview and quick start
- [Project Summary](docs/prj_summary.md): Project overview and goals
- [Project Status](docs/status.md): Current status and known issues
- [Changelog](docs/CHANGELOG.md): Recent changes and improvements

## 🏗️ Architecture

```
tinypeg/
├── src/
│   ├── peg/                 # Core PEG parser library
│   │   ├── core.py         # Base parser classes
│   │   ├── parsers.py      # Parser implementations
│   │   └── syntax_tree.py  # Grammar representation
│   └── tinycl/             # TinyCL language implementation
│       ├── ast.py          # Abstract Syntax Tree nodes
│       ├── parser.py       # TinyCL grammar and parser
│       ├── interpreter.py  # Direct execution engine
│       └── compiler.py     # Multi-target code generator
├── examples/               # ALL examples in one location
│   ├── peg_usage/          # Examples of using the PEG library
│   │   ├── basic/          # Basic PEG usage
│   │   ├── calculators/    # Calculator implementations
│   │   └── language_parsers/ # Language parser examples
│   └── tinycl_language/    # Programs written in TinyCL
│       ├── basic/          # Basic language features
│       ├── control_flow/   # Control structures
│       └── advanced/       # Advanced features
├── docs/                   # Comprehensive documentation
├── doc_tools/              # Documentation utilities
└── tests/                  # Test suite
```

## 🧪 Testing

```bash
# Test all components
python examples/tinycl_language/comprehensive_test.py  # Comprehensive language test
python src/tinycl/compiler.py      # Compiler test

# Test individual components
python -c "from src.tinycl.parser import TinyCLParser; print('Parser OK')"
python -c "from src.tinycl.interpreter import TinyCLInterpreter; print('Interpreter OK')"
```

## 🎯 Production Ready

This implementation is **production-quality** with:
- ✅ **Complete Feature Set**: All grammar features implemented and tested
- ✅ **Robust Error Handling**: Graceful parsing and runtime error management
- ✅ **Multi-target Compilation**: Python and C code generation
- ✅ **Comprehensive Testing**: All features thoroughly tested and verified
- ✅ **Clean Architecture**: Modular, extensible design
- ✅ **Complete Documentation**: Reference guides and examples

## 📄 License

MIT License - see LICENSE file for details.

---

**🎉 Ready to use!** This is a complete, working programming language implementation that demonstrates professional-level language design and implementation techniques using PEG parsing.

## 👤 Author

**Randall Morgan** - Experienced software engineer specializing in programming language implementation and compiler design.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 🙏 Acknowledgements

- Bryan Ford for formalizing Parsing Expression Grammars
- The Python community for their excellent documentation and tools

## 📄 Copyright

Copyright © 2024 Randall Morgan. All rights reserved.
