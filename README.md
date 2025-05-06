# TinyPEG: A Parsing Expression Grammar Library

TinyPEG is a lightweight and easy-to-use Parsing Expression Grammar (PEG) library implemented in Python. It allows you to define grammars using Parsing Expression Grammar notation and use them to parse and analyze text.

## Features

- Simple and intuitive API
- Support for common PEG operators
- Extensible architecture
- Built-in AST construction
- Example parsers for various use cases
- Complete implementation of a tiny programming language (TinyCL)

## Installation

Clone the repository:

```bash
git clone https://github.com/Monotoba/tinypeg.git
cd tinypeg
```

## Usage

Here's a simple example of using TinyPEG to create a calculator parser:

```python
from src.peg import PEGParser, Rule, Reference, GrammarNode

class CalculatorParser(PEGParser):
    def __init__(self):
        super().__init__()
        
        # Define grammar for the calculator
        self.grammar = GrammarNode(
            name="Calculator",
            rules=[
                Rule("Expression", Reference("Term")),
                Rule("Term", Reference("Factor")),
                Rule("Factor", Reference("Number")),
                Rule("Number", Reference("[0-9]+")),
            ]
        )
    
    def parse(self, text: str):
        print(f"Parsing expression: {text}")
        result = super().parse(text)
        return result

# Use the parser
parser = CalculatorParser()
result = parser.parse("42")
print(result)
```

## Documentation

Comprehensive documentation is available in the `docs` directory:

- [Index](docs/index.md): Overview and quick start
- [Preface](docs/preface.md): Introduction to parsing and grammar concepts
- [Chapter 1](docs/chapter01_peg_basics.md): Understanding PEG Parsers
- [Chapter 2](docs/chapter02_library_overview.md): TinyPEG Library Overview
- [Chapter 3](docs/chapter03_building_parsers.md): Building Your First Parser
- [Chapter 4](docs/chapter04_examples.md): Example Parsers
- [Chapter 5](docs/chapter05_tiny_language.md): Creating a Tiny Programming Language
- [Appendix A](docs/appendix_a_peg_reference.md): PEG Grammar Reference
- [Appendix B](docs/appendix_b_testing.md): Testing Framework
- [Appendix C](docs/appendix_c_tinycl_reference.md): TinyCL Language Reference

## Examples

TinyPEG comes with several example parsers:

- [Calculator](src/examples/calc/calculator.py): Parse and evaluate arithmetic expressions
- [If Statement](src/examples/ifstmt/ifstmt.py): Parse if statements
- [While Loop](src/examples/while_loop/while.py): Parse while loops
- [EmLang](src/examples/emlang/emlang.py): Parse a simple language with variables and print statements
- [TinyCL](src/examples/tinycl/tinycl_parser.py): A complete tiny programming language

## Testing

Run the tests using Python's unittest framework:

```bash
python -m unittest discover tests
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

If you use this software in your project, please provide attribution by including the following text in your documentation or credits:

```
This project uses TinyPEG, created by Randy (https://github.com/Monotoba/tinypeg)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

- Bryan Ford for formalizing Parsing Expression Grammars
- The Python community for their excellent documentation and tools