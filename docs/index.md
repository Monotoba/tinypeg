# TinyPEG: A Parsing Expression Grammar Library

Welcome to the documentation for TinyPEG, a lightweight and easy-to-use Parsing Expression Grammar (PEG) library implemented in Python.

## What is TinyPEG?

TinyPEG is a parser library that allows you to define grammars using Parsing Expression Grammar notation and use them to parse and analyze text. It's designed to be:

- **Simple**: Easy to understand and use
- **Flexible**: Adaptable to various parsing needs
- **Educational**: A great tool for learning about parsers and language design

## Getting Started

We've created a comprehensive e-book to help you learn about PEG parsers and how to build your own programming language:

**📚 Complete E-book: "Building Parsers with PEG"**
- **[Complete PDF](ebook/pdf/tinypeg_complete_ebook.pdf)** - Full book with covers (517 KB)
- **[HTML Version](ebook/html/)** - Web-readable format

**📖 Individual Chapters:**
- [Chapter 1](ebook/markdown/chapter01_peg_basics.md): Understanding PEG Parsers
- [Chapter 2](ebook/markdown/chapter02_library_overview.md): TinyPEG Library Overview
- [Chapter 3](ebook/markdown/chapter03_building_parsers.md): Building Your First Parser
- [Chapter 4](ebook/markdown/chapter04_examples.md): Example Parsers and Applications
- [Chapter 5](ebook/markdown/chapter05_tiny_language.md): Creating TinyCL - A Complete Programming Language

## TinyCL Language

TinyCL is a small programming language implemented using the TinyPEG library. It includes:

- Variables and constants
- Functions with parameters
- Control flow (if/else, while)
- Expressions with operator precedence
- Basic I/O with print statements

For more details, see the [TinyCL Complete Reference](../TINYCL_COMPLETE_REFERENCE.md).

## Quick Example

```python
from src.peg import PEGParser, Rule, Reference, GrammarNode

# Create a simple arithmetic expression parser
class ArithmeticParser(PEGParser):
    def __init__(self):
        super().__init__()

        # Define grammar for arithmetic expressions
        self.grammar = GrammarNode(
            name="Arithmetic",
            rules=[
                Rule("Expression", Reference("Term")),
                Rule("Term", Reference("Factor")),
                Rule("Factor", Reference("Number")),
                Rule("Number", Reference("[0-9]+")),
            ]
        )

# Use the parser
parser = ArithmeticParser()
result = parser.parse("42")
```

## License

This project is open source and available under the MIT License.

## 👤 Author

**Randall Morgan** - Experienced software engineer specializing in programming language implementation and compiler design.

## 📄 Copyright

Copyright © 2024 Randall Morgan. All rights reserved.
