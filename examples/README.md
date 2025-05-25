# Examples Directory

This directory contains **ALL** examples organized into two clear categories:

## 📁 Unified Directory Structure

```
examples/
├── peg_usage/              # Examples of HOW TO USE the PEG library
│   ├── basic/              # Basic PEG usage
│   │   ├── simple_parser.py
│   │   ├── minimal_example.py
│   │   └── simple_parser_tinypeg.py
│   ├── calculators/        # Calculator implementations using PEG
│   │   ├── calculator_base.py      # Base classes for calculators
│   │   ├── simple_calculator.py    # Addition/subtraction only
│   │   ├── advanced_calculator.py  # Full arithmetic with precedence
│   │   └── number_parser.py        # Basic number parsing
│   └── language_parsers/   # Language parser implementations
│       ├── minimal_tinycl.py
│       ├── simple_tinycl.py
│       ├── emlang.py
│       ├── while.py
│       └── standalone_tinycl.py
│
├── tinycl_language/        # Programs WRITTEN IN TinyCL language
│   ├── basic/              # Basic language features
│   │   ├── hello_world.tcl
│   │   ├── variables.tcl
│   │   └── arithmetic.tcl
│   ├── control_flow/       # Control structures
│   │   ├── if_statements.tcl
│   │   ├── while_loops.tcl
│   │   └── functions.tcl
│   ├── advanced/           # Advanced features
│   │   ├── arrays.tcl
│   │   └── calculator.tcl
│   └── comprehensive_test.py  # Complete test suite
│
└── README.md               # This file
```

## 🚀 PEG Usage Examples (`peg_usage/`)

These examples show **how to use the TinyPEG library** to build parsers:

### Basic PEG Usage (`basic/`)
- **`simple_parser.py`** - Basic example of using PEG to parse numbers
- **`minimal_example.py`** - Minimal example showing core PEG library usage
- **`simple_parser_tinypeg.py`** - Alternative basic parser implementation

### Calculator Implementations (`calculators/`)
- **`calculator_base.py`** - Base classes with common functionality (reduces duplication)
- **`simple_calculator.py`** - Addition and subtraction only
- **`advanced_calculator.py`** - Full arithmetic with proper precedence and parentheses
- **`number_parser.py`** - Basic number parsing (simplest possible PEG example)

### Language Parser Implementations (`language_parsers/`)
- **`minimal_tinycl.py`** - Minimal TinyCL language implementation
- **`simple_tinycl.py`** - Simple TinyCL language implementation
- **`emlang.py`** - Example minimal language parser
- **`while.py`** - While loop parser example
- **`standalone_tinycl.py`** - Complete TinyCL without PEG library (for comparison)

## 📝 TinyCL Language Programs (`tinycl_language/`)

These are **programs written in the TinyCL language** (with `.tcl` extension):

### Basic Language Features (`basic/`)
- **`hello_world.tcl`** - Simple "Hello, World!" program
- **`variables.tcl`** - Variable and constant declarations
- **`arithmetic.tcl`** - Arithmetic operations and precedence

### Control Flow Structures (`control_flow/`)
- **`if_statements.tcl`** - Conditional logic and nested if statements
- **`while_loops.tcl`** - Loop examples and iteration
- **`functions.tcl`** - Function declaration, calls, and scope

### Advanced Features (`advanced/`)
- **`arrays.tcl`** - Array creation, access, and processing
- **`calculator.tcl`** - Complex calculator with multiple functions

### Complete Test Suite
- **`comprehensive_test.py`** - Python script that runs comprehensive TinyCL program testing all language features

## 🏃 Running the Examples

### PEG Usage Examples
```bash
# Basic PEG examples
python examples/peg_usage/basic/simple_parser.py
python examples/peg_usage/basic/minimal_example.py

# Calculator examples
python examples/peg_usage/calculators/simple_calculator.py
python examples/peg_usage/calculators/advanced_calculator.py
python examples/peg_usage/calculators/number_parser.py

# Language parser examples
python examples/peg_usage/language_parsers/minimal_tinycl.py
python examples/peg_usage/language_parsers/simple_tinycl.py
```

### TinyCL Language Programs
```bash
# Run TinyCL programs using the interpreter
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

# Or run the comprehensive test
python examples/tinycl_language/comprehensive_test.py
```

## 🎯 What Each Category Demonstrates

### PEG Usage Examples Show:
- How to define grammars using PEG notation
- How to create parsers with the TinyPEG library
- How to build language implementations
- Different approaches to parser construction

### TinyCL Programs Show:
- Complete TinyCL language syntax
- All language features in action
- Real programs that can be parsed and executed
- Progressive complexity from basic to advanced

This organization makes it immediately clear whether you're looking at:
- **Library usage examples** (how to use TinyPEG)
- **Language programs** (code written in TinyCL)
