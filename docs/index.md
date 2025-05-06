# TinyPEG: A Parsing Expression Grammar Library

Welcome to the documentation for TinyPEG, a lightweight and easy-to-use Parsing Expression Grammar (PEG) library implemented in Python.

## What is TinyPEG?

TinyPEG is a parser library that allows you to define grammars using Parsing Expression Grammar notation and use them to parse and analyze text. It's designed to be:

- **Simple**: Easy to understand and use
- **Flexible**: Adaptable to various parsing needs
- **Educational**: A great tool for learning about parsers and language design

## Getting Started

- [Preface](preface.md): Introduction to parsing and grammar concepts
- [Contents](contents.md): Full table of contents
- [Chapter 1](chapter01_peg_basics.md): Understanding PEG Parsers
- [Chapter 2](chapter02_library_overview.md): TinyPEG Library Overview
- [Chapter 3](chapter03_building_parsers.md): Building Your First Parser
- [Chapter 4](chapter04_examples.md): Example Parsers
- [Chapter 5](chapter05_tiny_language.md): Creating a Tiny Programming Language

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

This project is open source and available under the [MIT License](../LICENSE).

If you use this software in your project, please provide attribution by including the following text in your documentation or credits:

```
This project uses TinyPEG, created by Randy (https://github.com/Monotoba/tinypeg)
```
