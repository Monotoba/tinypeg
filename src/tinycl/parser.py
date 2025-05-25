#!/usr/bin/env python3
"""
TinyCL parser implementation using the TinyPEG library.
"""

import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.peg import (
    PEGParser, Rule, Reference, GrammarNode, ParseError,
    Sequence, Choice, ZeroOrMore, OneOrMore, Optional, Literal, Regex
)

# Import AST node classes
from src.tinycl.ast import *

class TinyCLParser(PEGParser):
    """Parser for the TinyCL language."""

    def __init__(self):
        super().__init__()

        # Define grammar for TinyCL
        self.grammar = GrammarNode(
            name="TinyCL",
            rules=[
                # Program structure
                Rule("Program", ZeroOrMore(Reference("Statement"))),

                # Statements
                Rule("Statement", Choice(
                    Reference("FunctionDecl"),
                    Reference("VariableDecl"),
                    Reference("ConstantDecl"),
                    Reference("IfStatement"),
                    Reference("WhileStatement"),
                    Reference("PrintStatement"),
                    Reference("ReturnStatement"),
                    Reference("AssignmentStatement"),
                    Reference("FunctionCallStatement"),
                    Reference("Block")
                )),

                # Function declaration
                Rule("FunctionDecl", Sequence(
                    Literal("func"),
                    Reference("Identifier"),
                    Literal("("),
                    Optional(Reference("Parameters")),
                    Literal(")"),
                    Reference("Block")
                )),

                # Parameters
                Rule("Parameters", Sequence(
                    Reference("Identifier"),
                    ZeroOrMore(Sequence(
                        Literal(","),
                        Reference("Identifier")
                    ))
                )),

                # Variable declaration
                Rule("VariableDecl", Sequence(
                    Literal("var"),
                    Reference("Identifier"),
                    Literal("="),
                    Reference("Expression"),
                    Literal(";")
                )),

                # Constant declaration
                Rule("ConstantDecl", Sequence(
                    Literal("const"),
                    Reference("Identifier"),
                    Literal("="),
                    Reference("Expression"),
                    Literal(";")
                )),

                # If statement
                Rule("IfStatement", Sequence(
                    Literal("if"),
                    Literal("("),
                    Reference("Expression"),
                    Literal(")"),
                    Reference("Block"),
                    Optional(Sequence(
                        Literal("else"),
                        Reference("Block")
                    ))
                )),

                # While statement
                Rule("WhileStatement", Sequence(
                    Literal("while"),
                    Literal("("),
                    Reference("Expression"),
                    Literal(")"),
                    Reference("Block")
                )),

                # Print statement
                Rule("PrintStatement", Sequence(
                    Literal("print"),
                    Literal("("),
                    Reference("Expression"),
                    Literal(")"),
                    Literal(";")
                )),

                # Return statement
                Rule("ReturnStatement", Sequence(
                    Literal("return"),
                    Optional(Reference("Expression")),
                    Literal(";")
                )),

                # Assignment statement
                Rule("AssignmentStatement", Sequence(
                    Reference("Identifier"),
                    Literal("="),
                    Reference("Expression"),
                    Literal(";")
                )),

                # Function call statement
                Rule("FunctionCallStatement", Sequence(
                    Reference("Identifier"),
                    Literal("("),
                    Optional(Reference("Arguments")),
                    Literal(")"),
                    Literal(";")
                )),

                # Arguments
                Rule("Arguments", Sequence(
                    Reference("Expression"),
                    ZeroOrMore(Sequence(
                        Literal(","),
                        Reference("Expression")
                    ))
                )),

                # Block
                Rule("Block", Sequence(
                    Literal("{"),
                    ZeroOrMore(Reference("Statement")),
                    Literal("}")
                )),

                # Expression
                Rule("Expression", Reference("LogicalOr")),

                # Logical OR
                Rule("LogicalOr", Sequence(
                    Reference("LogicalAnd"),
                    ZeroOrMore(Sequence(
                        Literal("||"),
                        Reference("LogicalAnd")
                    ))
                )),

                # Logical AND
                Rule("LogicalAnd", Sequence(
                    Reference("Equality"),
                    ZeroOrMore(Sequence(
                        Literal("&&"),
                        Reference("Equality")
                    ))
                )),

                # Equality
                Rule("Equality", Sequence(
                    Reference("Comparison"),
                    ZeroOrMore(Sequence(
                        Choice(
                            Literal("!="),
                            Literal("==")
                        ),
                        Reference("Comparison")
                    ))
                )),

                # Comparison
                Rule("Comparison", Sequence(
                    Reference("Term"),
                    ZeroOrMore(Sequence(
                        Choice(
                            Literal("<="),
                            Literal(">="),
                            Literal("<"),
                            Literal(">")
                        ),
                        Reference("Term")
                    ))
                )),

                # Term
                Rule("Term", Sequence(
                    Reference("Factor"),
                    ZeroOrMore(Sequence(
                        Choice(
                            Literal("+"),
                            Literal("-")
                        ),
                        Reference("Factor")
                    ))
                )),

                # Factor
                Rule("Factor", Sequence(
                    Reference("Unary"),
                    ZeroOrMore(Sequence(
                        Choice(
                            Literal("*"),
                            Literal("/")
                        ),
                        Reference("Unary")
                    ))
                )),

                # Unary
                Rule("Unary", Choice(
                    Sequence(
                        Choice(
                            Literal("!"),
                            Literal("-")
                        ),
                        Reference("Unary")
                    ),
                    Reference("Postfix")
                )),

                # Postfix
                Rule("Postfix", Sequence(
                    Reference("Primary"),
                    ZeroOrMore(Sequence(
                        Literal("["),
                        Reference("Expression"),
                        Literal("]")
                    ))
                )),

                # Primary
                Rule("Primary", Choice(
                    Sequence(
                        Literal("("),
                        Reference("Expression"),
                        Literal(")")
                    ),
                    Sequence(
                        Reference("Identifier"),
                        Literal("("),
                        Optional(Reference("Arguments")),
                        Literal(")")
                    ),
                    Sequence(
                        Literal("["),
                        Optional(Reference("Arguments")),
                        Literal("]")
                    ),
                    Reference("Identifier"),
                    Reference("Number"),
                    Reference("String"),
                    Reference("Character"),
                    Literal("true"),
                    Literal("false")
                )),

                # Terminals
                Rule("Number", Regex("[0-9]+")),
                Rule("String", Regex("\"[^\"]*\"")),
                Rule("Character", Regex("'[^']'")),
                Rule("Identifier", Regex("[a-zA-Z_][a-zA-Z0-9_]*"))
            ]
        )

    def skip_whitespace(self, ctx):
        """Skip whitespace and comments."""
        while not ctx.eof():
            # Skip whitespace
            if ctx.peek().isspace():
                ctx.consume()
                continue

            # Skip comments
            if ctx.peek() == '#':
                while not ctx.eof() and ctx.peek() != '\n':
                    ctx.consume()
                continue

            # No more whitespace or comments to skip
            break

    def _parse_expression(self, expr, ctx):
        """Override to handle whitespace between tokens."""
        # Skip whitespace before parsing
        self.skip_whitespace(ctx)

        # Parse the expression
        result = super()._parse_expression(expr, ctx)

        # Skip whitespace after parsing
        self.skip_whitespace(ctx)

        return result

    def parse(self, text):
        """Parse a TinyCL program."""
        result = super().parse(text)
        return self._build_ast(result)

    def _build_ast(self, parse_result):
        """Build an AST from the parse result."""
        if parse_result is None:
            return None

        # Build a program node
        return ProgramNode(self._build_statements(parse_result))

    def _build_statements(self, statements):
        """Build statement nodes from parse results."""
        if not statements:
            return []

        # Handle nested list structure from PEG parser
        if isinstance(statements, list) and len(statements) == 1 and isinstance(statements[0], list):
            statements = statements[0]

        result = []
        for statement in statements:
            node = self._build_statement(statement)
            if node:
                result.append(node)

        return result

    def _build_statement(self, statement):
        """Build a statement node from a parse result."""
        if not statement:
            return None

        # Debug output (commented out)
        # print(f"DEBUG: Building statement from: {statement} (type: {type(statement)})")

        # Determine the type of statement
        if isinstance(statement, list) and len(statement) > 0:
            first = statement[0]

            # Function declaration
            if first == "func":
                name = statement[1]
                # Extract parameters between parentheses
                parameters = []
                if len(statement) > 3 and statement[3] != ")":
                    parameters = self._build_parameters(statement[3])
                body = statement[-1]
                # print(f"DEBUG: Function {name} with parameters {parameters}")
                return FunctionDeclNode(name, parameters, self._build_block(body))

            # Variable declaration
            elif first == "var":
                name = statement[1]
                expression = statement[3]
                return VariableDeclNode(name, self._build_expression(expression))

            # Constant declaration
            elif first == "const":
                name = statement[1]
                expression = statement[3]
                return ConstantDeclNode(name, self._build_expression(expression))

            # If statement
            elif first == "if":
                condition = statement[2]
                then_block = statement[4]
                else_block = None

                # Check for else clause
                if len(statement) > 5 and statement[5] is not None:
                    else_part = statement[5]
                    if isinstance(else_part, list) and len(else_part) > 1 and else_part[0] == "else":
                        else_block = else_part[1]

                built_then_block = self._build_block(then_block)

                return IfStatementNode(
                    self._build_expression(condition),
                    built_then_block,
                    self._build_block(else_block) if else_block else None
                )

            # While statement
            elif first == "while":
                condition = statement[2]
                body = statement[4]
                return WhileStatementNode(
                    self._build_expression(condition),
                    self._build_block(body)
                )

            # Print statement
            elif first == "print":
                expression = statement[2]
                return PrintStatementNode(self._build_expression(expression))

            # Return statement
            elif first == "return":
                expression = statement[1] if len(statement) > 2 and statement[1] != ";" else None
                return ReturnStatementNode(self._build_expression(expression) if expression else None)

            # Block
            elif first == "{":
                return self._build_block(statement)

            # Assignment or function call
            elif isinstance(first, str) and (first.isalpha() or first == "_"):
                if len(statement) > 1 and statement[1] == "=":
                    # Assignment
                    name = first
                    expression = statement[2]
                    return AssignmentNode(name, self._build_expression(expression))
                elif len(statement) > 1 and statement[1] == "(":
                    # Function call
                    name = first
                    arguments = statement[2] if len(statement) > 2 and statement[2] != ")" else []
                    return FunctionCallNode(name, self._build_arguments(arguments))

        return None

    def _build_block(self, block):
        """Build a block node from a parse result."""
        if not block:
            return BlockNode([])

        # Handle different block formats
        if isinstance(block, list):
            # If it starts with "{", extract statements between braces
            if len(block) >= 3 and block[0] == "{" and block[-1] == "}":
                statements = block[1:-1]
                return BlockNode(self._build_statements(statements))
            # If it's just a list of statements
            else:
                return BlockNode(self._build_statements(block))

        # Single statement
        statement_node = self._build_statement(block)
        return BlockNode([statement_node] if statement_node else [])

    def _build_expression(self, expression):
        """Build an expression node from a parse result."""
        if not expression:
            return None

        # Flatten deeply nested lists from PEG parser
        expression = self._flatten_expression(expression)

        # Debug output
        # print(f"DEBUG: Building expression from flattened: {expression}")

        result = self._build_logical_or(expression)
        # if result is None:
        #     print(f"WARNING: Failed to build expression from: {expression}")
        return result

    def _build_logical_or(self, expr):
        """Build logical OR expression (||)."""
        if not isinstance(expr, list):
            return self._build_logical_and(expr)

        # Handle single-element lists (unwrap them)
        if len(expr) == 1:
            return self._build_logical_or(expr[0])

        if not expr:  # Empty list
            return None

        # Look for logical OR operators
        for i in range(len(expr)):
            if expr[i] == "||":
                left_part = expr[:i]
                right_part = expr[i+1:]
                if left_part and right_part:
                    left = self._build_logical_and(left_part)
                    right = self._build_logical_or(right_part)
                    if left and right:
                        return BinaryOpNode(left, expr[i], right)

        return self._build_logical_and(expr)

    def _build_logical_and(self, expr):
        """Build logical AND expression (&&)."""
        if not isinstance(expr, list):
            return self._build_equality(expr)

        # Handle single-element lists (unwrap them)
        if len(expr) == 1:
            return self._build_logical_and(expr[0])

        if not expr:  # Empty list
            return None

        # Look for logical AND operators
        for i in range(len(expr)):
            if expr[i] == "&&":
                left_part = expr[:i]
                right_part = expr[i+1:]
                if left_part and right_part:
                    left = self._build_equality(left_part)
                    right = self._build_logical_and(right_part)
                    if left and right:
                        return BinaryOpNode(left, expr[i], right)

        return self._build_equality(expr)

    def _build_equality(self, expr):
        """Build equality expression (== !=)."""
        if not isinstance(expr, list):
            return self._build_comparison(expr)

        # Handle single-element lists (unwrap them)
        if len(expr) == 1:
            return self._build_equality(expr[0])

        if not expr:  # Empty list
            return None

        # Look for equality operators (check longer operators first)
        for i in range(len(expr)):
            if expr[i] in ["!=", "=="]:
                left_part = expr[:i]
                right_part = expr[i+1:]
                if left_part and right_part:
                    left = self._build_comparison(left_part)
                    right = self._build_equality(right_part)
                    if left and right:
                        return BinaryOpNode(left, expr[i], right)

        return self._build_comparison(expr)

    def _build_comparison(self, expr):
        """Build comparison expression (< > <= >=)."""
        if not isinstance(expr, list):
            return self._build_term(expr)

        # Handle single-element lists (unwrap them)
        if len(expr) == 1:
            return self._build_comparison(expr[0])

        if not expr:  # Empty list
            return None

        # Look for comparison operators (check longer operators first)
        for i in range(len(expr)):
            if expr[i] in ["<=", ">=", "<", ">", "!=", "=="]:
                left_part = expr[:i]
                right_part = expr[i+1:]
                if left_part and right_part:
                    left = self._build_term(left_part)
                    right = self._build_comparison(right_part)
                    if left and right:
                        return BinaryOpNode(left, expr[i], right)

        return self._build_term(expr)

    def _build_term(self, expr):
        """Build term expression (+ -)."""
        if not isinstance(expr, list):
            return self._build_factor(expr)

        # Handle single-element lists (unwrap them)
        if len(expr) == 1:
            return self._build_term(expr[0])

        if not expr:  # Empty list
            return None

        # Look for term operators
        for i in range(len(expr)):
            if expr[i] in ["+", "-"]:
                left_part = expr[:i]
                right_part = expr[i+1:]
                if left_part and right_part:  # Make sure both parts exist
                    left = self._build_factor(left_part)
                    right = self._build_term(right_part)
                    if left and right:  # Make sure both are valid
                        return BinaryOpNode(left, expr[i], right)

        return self._build_factor(expr)

    def _build_factor(self, expr):
        """Build factor expression (* /)."""
        if not isinstance(expr, list):
            return self._build_unary(expr)

        # Handle single-element lists (unwrap them)
        if len(expr) == 1:
            return self._build_factor(expr[0])

        if not expr:  # Empty list
            return None

        # Look for factor operators
        for i in range(len(expr)):
            if expr[i] in ["*", "/"]:
                left_part = expr[:i]
                right_part = expr[i+1:]
                if left_part and right_part:
                    left = self._build_unary(left_part)
                    right = self._build_factor(right_part)
                    if left and right:
                        return BinaryOpNode(left, expr[i], right)

        return self._build_unary(expr)

    def _build_unary(self, expr):
        """Build unary expression (! -)."""
        if not isinstance(expr, list):
            return self._build_postfix(expr)

        # Handle single-element lists (unwrap them)
        if len(expr) == 1:
            return self._build_unary(expr[0])

        # Check for unary operators
        if len(expr) >= 2 and expr[0] in ["!", "-"]:
            operand = self._build_unary(expr[1:])
            return UnaryOpNode(expr[0], operand)

        return self._build_postfix(expr)

    def _build_postfix(self, expr):
        """Build postfix expression (array access)."""
        if not isinstance(expr, list):
            return self._build_primary(expr)

        # Handle single-element lists (unwrap them)
        if len(expr) == 1:
            return self._build_postfix(expr[0])

        # Look for array access [index]
        for i in range(len(expr)):
            if expr[i] == "[" and i + 2 < len(expr) and expr[i + 2] == "]":
                base = self._build_primary(expr[:i])
                index = self._build_expression(expr[i + 1])
                # Create array access node
                return ArrayAccessNode(base, index)

        return self._build_primary(expr)

    def _build_primary(self, expr):
        """Build primary expression (literals, identifiers, function calls, parentheses)."""
        if not isinstance(expr, list):
            # Handle literals and identifiers
            if isinstance(expr, str):
                if expr.isdigit():
                    return NumberNode(expr)
                elif expr.startswith('"') and expr.endswith('"'):
                    return StringNode(expr)
                elif expr.startswith("'") and expr.endswith("'"):
                    return CharacterNode(expr[1:-1])
                elif expr == "true":
                    return BooleanNode("true")
                elif expr == "false":
                    return BooleanNode("false")
                elif expr.isalpha() or expr.startswith("_"):
                    return IdentifierNode(expr)
            return None

        # Handle single-element lists (unwrap them)
        if len(expr) == 1:
            return self._build_primary(expr[0])

        # Handle parenthesized expressions
        if len(expr) >= 3 and expr[0] == "(" and expr[-1] == ")":
            return self._build_expression(expr[1:-1])

        # Handle function calls
        if len(expr) >= 3 and expr[1] == "(" and expr[-1] == ")":
            name = expr[0]
            arguments = expr[2:-1] if len(expr) > 3 else []
            # Check if FunctionCallExprNode exists, otherwise use FunctionCallNode
            try:
                return FunctionCallExprNode(name, self._build_arguments(arguments))
            except NameError:
                return FunctionCallNode(name, self._build_arguments(arguments))

        # Handle array literals
        if len(expr) >= 2 and expr[0] == "[" and expr[-1] == "]":
            elements = expr[1:-1] if len(expr) > 2 else []
            return ArrayLiteralNode(self._build_arguments(elements))

        # If we can't parse it, try the first element
        return self._build_primary(expr[0]) if expr else None

    def _flatten_expression(self, expr):
        """Flatten deeply nested expression lists from PEG parser."""
        if not isinstance(expr, list):
            return expr

        # If it's a single-element list, unwrap it
        if len(expr) == 1:
            return self._flatten_expression(expr[0])

        # If it's a list with multiple elements, flatten each element
        result = []
        for item in expr:
            if isinstance(item, list):
                flattened = self._flatten_expression(item)
                if isinstance(flattened, list):
                    result.extend(flattened)
                else:
                    result.append(flattened)
            else:
                result.append(item)

        return result

    def _build_arguments(self, arguments):
        """Build argument nodes from parse results."""
        if not arguments:
            return []

        result = []
        for arg in arguments:
            if arg != ",":
                node = self._build_expression(arg)
                if node:
                    result.append(node)

        return result

    def _build_parameters(self, parameters):
        """Build parameter list from parse results."""
        if not parameters:
            return []

        # Flatten the parameters structure
        flattened = self._flatten_expression(parameters)

        result = []
        if isinstance(flattened, list):
            for param in flattened:
                if param != "," and isinstance(param, str) and param.strip():
                    result.append(param)
        elif isinstance(flattened, str) and flattened.strip():
            result.append(flattened)
        return result

# Removed duplicate interpreter - use the one in interpreter.py