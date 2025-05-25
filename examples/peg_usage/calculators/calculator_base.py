#!/usr/bin/env python3
"""
Base calculator classes for PEG usage examples.
This module provides common functionality to reduce code duplication.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from src.utils import setup_project_path
setup_project_path()

from src.peg import (
    PEGParser, Rule, Reference, ParseError,
    Sequence, Choice, ZeroOrMore, OneOrMore, Optional, Literal, Regex
)
from src.peg.syntax_tree import GrammarNode

class BaseCalculator(PEGParser):
    """Base calculator class with common functionality."""

    def __init__(self):
        super().__init__()
        self.grammar = None  # To be defined by subclasses

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

    def parse(self, text: str):
        """Parse an arithmetic expression."""
        print(f"Parsing expression: {text}")
        return super().parse(text)

    def evaluate(self, text: str):
        """Parse and evaluate an arithmetic expression."""
        ast = self.parse(text)
        return self._evaluate_node(ast)

    def _evaluate_node(self, node):
        """Evaluate an AST node. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement _evaluate_node")

    def test_expressions(self, expressions):
        """Test a list of expressions."""
        for expr in expressions:
            try:
                print(f"\nExpression: {expr}")
                result = self.parse(expr)
                print(f"Parsed: {result}")

                value = self.evaluate(expr)
                print(f"Value: {value}")
            except ParseError as e:
                print(f"Parse Error: {e}")
            except Exception as e:
                print(f"Error: {e}")

class SimpleCalculator(BaseCalculator):
    """Simple calculator for addition and subtraction only."""

    def __init__(self):
        super().__init__()

        # Define grammar for basic arithmetic
        self.grammar = GrammarNode(
            name="Expression",
            rules=[
                # Expression = Number ('+' Number | '-' Number)*
                Rule("Expression", Sequence(
                    Reference("Number"),
                    ZeroOrMore(
                        Sequence(
                            Choice(Literal("+"), Literal("-")),
                            Reference("Number")
                        )
                    )
                )),
                # Number = [0-9]+
                Rule("Number", Regex("[0-9]+"))
            ]
        )

    def _evaluate_node(self, node):
        """Evaluate an AST node for simple arithmetic."""
        if isinstance(node, str) and node.isdigit():
            return int(node)
        elif isinstance(node, list):
            if len(node) == 2:
                # [number, operations_list]
                result = self._evaluate_node(node[0])
                operations = node[1]
                for op_pair in operations:
                    if isinstance(op_pair, list) and len(op_pair) == 2:
                        operator, operand = op_pair
                        operand_value = self._evaluate_node(operand)
                        if operator == '+':
                            result += operand_value
                        elif operator == '-':
                            result -= operand_value
                return result
            elif len(node) == 1:
                return self._evaluate_node(node[0])
            else:
                # Fallback for other structures
                result = self._evaluate_node(node[0])
                i = 1
                while i < len(node):
                    if node[i] == '+':
                        result += self._evaluate_node(node[i+1])
                    elif node[i] == '-':
                        result -= self._evaluate_node(node[i+1])
                    i += 2
                return result
        else:
            return int(str(node))

class AdvancedCalculator(BaseCalculator):
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
