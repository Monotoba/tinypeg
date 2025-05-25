# Chapter 2: Building a PEG Parser with TinyPEG

## Introduction to TinyPEG

TinyPEG is a lightweight, easy-to-use library for building Parsing Expression Grammar (PEG) parsers in Python. It provides a simple API for defining grammars and parsing input text, making it an ideal choice for building parsers for domain-specific languages, configuration files, or even full-fledged programming languages.

In this chapter, we'll explore how to use TinyPEG to build a simple parser for arithmetic expressions.

## Setting Up TinyPEG

First, let's make sure we have TinyPEG installed. You can install it from the project repository:

```bash
git clone https://github.com/Monotoba/tinypeg.git
cd tinypeg
pip install -e .
```

## Basic Components of TinyPEG

TinyPEG provides several key components for building parsers:

1. **PEGParser**: The base class for all parsers.
2. **Rule**: Defines a named rule in the grammar.
3. **Reference**: References another rule by name.
4. **GrammarNode**: Represents the root of the grammar.
5. **Expression**: The base class for all parsing expressions.
6. **Sequence**: Matches a sequence of expressions.
7. **Choice**: Matches one of several alternatives.
8. **ZeroOrMore**: Matches an expression zero or more times.
9. **OneOrMore**: Matches an expression one or more times.
10. **Optional**: Matches an expression zero or one time.
11. **Literal**: Matches a literal string.
12. **Regex**: Matches a regular expression.

## Building a Simple Calculator Parser

Let's build a simple parser for arithmetic expressions. We'll start by defining the grammar:

```python
from src.peg import (
    PEGParser, Rule, Reference, ParseError,
    Sequence, Choice, ZeroOrMore, Literal, Regex
)
from src.peg.syntax_tree import GrammarNode

class CalculatorParser(PEGParser):
    """Advanced calculator with full arithmetic operations and precedence."""

    def __init__(self):
        super().__init__()

        # Define grammar with proper precedence
        self.grammar = GrammarNode(
            name="Expression",
            rules=[
                # Expression = Term (('+' | '-') Term)*
                Rule("Expression", Sequence(
                    Reference("Term"),
                    ZeroOrMore(
                        Sequence(
                            Choice(Literal("+"), Literal("-")),
                            Reference("Term")
                        )
                    )
                )),

                # Term = Factor (('*' | '/') Factor)*
                Rule("Term", Sequence(
                    Reference("Factor"),
                    ZeroOrMore(
                        Sequence(
                            Choice(Literal("*"), Literal("/")),
                            Reference("Factor")
                        )
                    )
                )),

                # Factor = Number | '(' Expression ')'
                Rule("Factor", Choice(
                    Reference("Number"),
                    Sequence(
                        Literal("("),
                        Reference("Expression"),
                        Literal(")")
                    )
                )),

                # Number = [0-9]+
                Rule("Number", Regex("[0-9]+"))
            ]
        )

    def skip_whitespace(self, ctx):
        """Skip whitespace in the input."""
        while not ctx.eof() and ctx.peek() in " \t\n\r":
            ctx.consume()

    def _parse_expression(self, expr, ctx):
        """Override to handle whitespace between tokens."""
        # Skip whitespace before parsing
        self.skip_whitespace(ctx)

        # Parse the expression
        result = super()._parse_expression(expr, ctx)

        # Skip whitespace after parsing
        self.skip_whitespace(ctx)

        return result
```

This parser defines a grammar for arithmetic expressions with proper operator precedence. It can parse expressions like `1 + 2 * 3` and `(1 + 2) * 3`.

## Building an AST

The parser above will produce a parse tree, but it's often more useful to have an abstract syntax tree (AST) that represents the structure of the expression in a more abstract way. Let's define some AST node classes:

```python
class ASTNode:
    """Base class for AST nodes."""
    pass

class BinaryOpNode(ASTNode):
    """AST node for a binary operation."""
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.op} {self.right})"

class NumberNode(ASTNode):
    """AST node for a number."""
    def __init__(self, value):
        self.value = int(value)

    def __str__(self):
        return str(self.value)
```

Now, let's add a method to our parser to build an AST from the parse tree:

```python
def parse(self, text: str):
    """Parse an arithmetic expression."""
    print(f"Parsing expression: {text}")
    return super().parse(text)

def evaluate(self, text: str):
    """Parse and evaluate an arithmetic expression."""
    ast = self.parse(text)
    return self._evaluate_node(ast)

def _evaluate_node(self, node):
    """Evaluate an AST node with proper precedence."""
    if isinstance(node, str):
        if node.isdigit():
            return int(node)
        elif node in "+-*/()":
            return node
        else:
            return node
    elif isinstance(node, list):
        if len(node) == 1:
            return self._evaluate_node(node[0])
        elif len(node) == 3 and node[0] == "(" and node[2] == ")":
            # Parenthesized expression
            return self._evaluate_node(node[1])
        else:
            # Handle operations with proper precedence
            return self._evaluate_expression_list(node)
    else:
        return node

def _evaluate_expression_list(self, nodes):
    """Evaluate a list of nodes representing an expression."""
    # Convert to a flat list
    flat = []
    for node in nodes:
        if isinstance(node, list):
            flat.extend(self._flatten_node(node))
        else:
            flat.append(self._evaluate_node(node))

    # Handle multiplication and division first (higher precedence)
    i = 1
    while i < len(flat):
        if flat[i] == '*':
            result = flat[i-1] * flat[i+1]
            flat = flat[:i-1] + [result] + flat[i+2:]
        elif flat[i] == '/':
            result = flat[i-1] / flat[i+1]
            flat = flat[:i-1] + [result] + flat[i+2:]
        else:
            i += 2

    # Handle addition and subtraction (lower precedence)
    i = 1
    while i < len(flat):
        if flat[i] == '+':
            result = flat[i-1] + flat[i+1]
            flat = flat[:i-1] + [result] + flat[i+2:]
        elif flat[i] == '-':
            result = flat[i-1] - flat[i+1]
            flat = flat[:i-1] + [result] + flat[i+2:]
        else:
            i += 2

    return flat[0] if flat else 0

def _flatten_node(self, node):
    """Flatten a nested node structure."""
    if isinstance(node, list):
        result = []
        for item in node:
            if isinstance(item, list):
                result.extend(self._flatten_node(item))
            else:
                result.append(self._evaluate_node(item))
        return result
    else:
        return [self._evaluate_node(node)]
```

## Using the Calculator Parser

Now we can use our calculator parser to parse and evaluate arithmetic expressions:

```python
def main():
    """Test the calculator parser."""
    parser = CalculatorParser()

    # Test expressions with precedence and parentheses
    expressions = [
        "3",
        "42",
        "3+5",
        "3 + 5",
        "10 - 4",
        "3 * 5",
        "10 / 2",
        "3 + 5 * 2",        # Should be 13 with proper precedence
        "10 - 2 * 3",       # Should be 4 with proper precedence
        "3 * 5 + 2",        # Should be 17
        "10 / 2 - 3",       # Should be 2
        "(3 + 5) * 2",      # Should be 16
        "3 + (5 * 2)",      # Should be 13
        "3 * (5 + 2)",      # Should be 21
        "(3 + 5) * (2 + 1)" # Should be 24
    ]

    print("=== Advanced Calculator (Full Arithmetic with Precedence) ===")
    for expr in expressions:
        try:
            print(f"\nExpression: {expr}")
            result = parser.parse(expr)
            print(f"Parsed: {result}")

            value = parser.evaluate(expr)
            print(f"Value: {value}")
        except ParseError as e:
            print(f"Parse Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

This will output something like:

```
=== Advanced Calculator (Full Arithmetic with Precedence) ===

Expression: 3
Parsing expression: 3
Parsed: 3
Value: 3

Expression: 3 + 5
Parsing expression: 3 + 5
Parsed: [3, [['+', 5]]]
Value: 8

Expression: 3 * 5
Parsing expression: 3 * 5
Parsed: [[3, [['*', 5]]], []]
Value: 15

Expression: 3 + 5 * 2
Parsing expression: 3 + 5 * 2
Parsed: [3, [['+', [5, [['*', 2]]]]]]
Value: 13

Expression: (3 + 5) * 2
Parsing expression: (3 + 5) * 2
Parsed: [['(', [3, [['+', 5]]], ')'], [['*', 2]]]
Value: 16
```

## Conclusion

In this chapter, we've seen how to use TinyPEG to build a simple parser for arithmetic expressions. We've defined a grammar, built an AST, and evaluated the AST to compute the result of the expression.

TinyPEG makes it easy to build parsers for a wide range of languages, from simple arithmetic expressions to complex programming languages. In the next chapter, we'll explore how to build a more complex parser for a simple programming language called TinyCL.