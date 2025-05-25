#!/usr/bin/env python3
"""
A standalone implementation of the TinyCL language.
"""

import re
import sys

class ParseError(Exception):
    """Custom error for parsing issues."""
    pass

class ParserContext:
    """Context class to hold the parsing state."""
    
    def __init__(self, text):
        self.text = text
        self.pos = 0
    
    def eof(self):
        return self.pos >= len(self.text)
    
    def peek(self):
        return self.text[self.pos] if not self.eof() else None
    
    def consume(self):
        """Advance the position by one character."""
        char = self.peek()
        self.pos += 1
        return char
    
    def skip_whitespace(self):
        """Skip whitespace and comments."""
        while not self.eof():
            # Skip whitespace
            if self.peek().isspace():
                self.consume()
                continue
            
            # Skip comments
            if self.peek() == '#':
                while not self.eof() and self.peek() != '\n':
                    self.consume()
                continue
            
            # No more whitespace or comments to skip
            break

class ASTNode:
    """Base class for AST nodes."""
    pass

class ProgramNode(ASTNode):
    """AST node for a program."""
    def __init__(self, statements):
        self.statements = statements
    
    def __str__(self):
        return f"Program({len(self.statements)} statements)"

class VariableDeclNode(ASTNode):
    """AST node for a variable declaration."""
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def __str__(self):
        return f"VariableDecl({self.name}, {self.value})"

class PrintNode(ASTNode):
    """AST node for a print statement."""
    def __init__(self, expression):
        self.expression = expression
    
    def __str__(self):
        return f"Print({self.expression})"

class NumberNode(ASTNode):
    """AST node for a number."""
    def __init__(self, value):
        self.value = int(value)
    
    def __str__(self):
        return f"Number({self.value})"

class StringNode(ASTNode):
    """AST node for a string."""
    def __init__(self, value):
        self.value = value[1:-1]  # Remove the quotes
    
    def __str__(self):
        return f"String({self.value})"

class IdentifierNode(ASTNode):
    """AST node for an identifier."""
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return f"Identifier({self.name})"

class TinyCLParser:
    """A simple parser for the TinyCL language."""
    
    def parse(self, text):
        """Parse a TinyCL program."""
        ctx = ParserContext(text)
        statements = []
        
        while not ctx.eof():
            ctx.skip_whitespace()
            if ctx.eof():
                break
            
            # Try to parse a statement
            statement = self._parse_statement(ctx)
            if statement:
                statements.append(statement)
        
        return ProgramNode(statements)
    
    def _parse_statement(self, ctx):
        """Parse a statement."""
        ctx.skip_whitespace()
        
        # Try to parse a variable declaration
        if self._match_keyword(ctx, "var"):
            return self._parse_variable_decl(ctx)
        
        # Try to parse a print statement
        if self._match_keyword(ctx, "print"):
            return self._parse_print(ctx)
        
        # Unknown statement
        raise ParseError(f"Unknown statement at position {ctx.pos}: '{ctx.text[ctx.pos:ctx.pos+10]}...'")
    
    def _parse_variable_decl(self, ctx):
        """Parse a variable declaration."""
        ctx.skip_whitespace()
        
        # Parse the variable name
        name = self._parse_identifier(ctx)
        
        ctx.skip_whitespace()
        
        # Parse the equals sign
        if not self._match_literal(ctx, "="):
            raise ParseError(f"Expected '=' at position {ctx.pos}")
        
        ctx.skip_whitespace()
        
        # Parse the value
        value = self._parse_expression(ctx)
        
        ctx.skip_whitespace()
        
        # Parse the semicolon
        if not self._match_literal(ctx, ";"):
            raise ParseError(f"Expected ';' at position {ctx.pos}")
        
        return VariableDeclNode(name, value)
    
    def _parse_print(self, ctx):
        """Parse a print statement."""
        ctx.skip_whitespace()
        
        # Parse the opening parenthesis
        if not self._match_literal(ctx, "("):
            raise ParseError(f"Expected '(' at position {ctx.pos}")
        
        ctx.skip_whitespace()
        
        # Parse the expression
        expression = self._parse_expression(ctx)
        
        ctx.skip_whitespace()
        
        # Parse the closing parenthesis
        if not self._match_literal(ctx, ")"):
            raise ParseError(f"Expected ')' at position {ctx.pos}")
        
        ctx.skip_whitespace()
        
        # Parse the semicolon
        if not self._match_literal(ctx, ";"):
            raise ParseError(f"Expected ';' at position {ctx.pos}")
        
        return PrintNode(expression)
    
    def _parse_expression(self, ctx):
        """Parse an expression."""
        ctx.skip_whitespace()
        
        # Try to parse a number
        number_match = re.match(r"[0-9]+", ctx.text[ctx.pos:])
        if number_match:
            number = number_match.group(0)
            for _ in range(len(number)):
                ctx.consume()
            return NumberNode(number)
        
        # Try to parse a string
        if ctx.peek() == '"':
            return self._parse_string(ctx)
        
        # Try to parse an identifier
        identifier_match = re.match(r"[a-zA-Z_][a-zA-Z0-9_]*", ctx.text[ctx.pos:])
        if identifier_match:
            identifier = identifier_match.group(0)
            for _ in range(len(identifier)):
                ctx.consume()
            return IdentifierNode(identifier)
        
        # Unknown expression
        raise ParseError(f"Unknown expression at position {ctx.pos}: '{ctx.text[ctx.pos:ctx.pos+10]}...'")
    
    def _parse_string(self, ctx):
        """Parse a string."""
        # Parse the opening quote
        if not self._match_literal(ctx, '"'):
            raise ParseError(f"Expected '\"' at position {ctx.pos}")
        
        # Parse the string content
        content = ""
        while not ctx.eof() and ctx.peek() != '"':
            content += ctx.consume()
        
        # Parse the closing quote
        if not self._match_literal(ctx, '"'):
            raise ParseError(f"Expected '\"' at position {ctx.pos}")
        
        return StringNode(f'"{content}"')
    
    def _parse_identifier(self, ctx):
        """Parse an identifier."""
        identifier_match = re.match(r"[a-zA-Z_][a-zA-Z0-9_]*", ctx.text[ctx.pos:])
        if not identifier_match:
            raise ParseError(f"Expected identifier at position {ctx.pos}")
        
        identifier = identifier_match.group(0)
        for _ in range(len(identifier)):
            ctx.consume()
        
        return identifier
    
    def _match_keyword(self, ctx, keyword):
        """Match a keyword."""
        # Check if the text at the current position starts with the keyword
        if ctx.pos + len(keyword) <= len(ctx.text) and ctx.text[ctx.pos:ctx.pos+len(keyword)] == keyword:
            # Check that the keyword is followed by whitespace or a special character
            if ctx.pos + len(keyword) == len(ctx.text) or not ctx.text[ctx.pos+len(keyword)].isalnum():
                # Consume the keyword
                for _ in range(len(keyword)):
                    ctx.consume()
                return True
        
        return False
    
    def _match_literal(self, ctx, literal):
        """Match a literal string."""
        # Check if the text at the current position starts with the literal
        if ctx.pos + len(literal) <= len(ctx.text) and ctx.text[ctx.pos:ctx.pos+len(literal)] == literal:
            # Consume the literal
            for _ in range(len(literal)):
                ctx.consume()
            return True
        
        return False

class TinyCLInterpreter:
    """A simple interpreter for the TinyCL language."""
    
    def __init__(self):
        self.variables = {}
    
    def interpret(self, ast):
        """Interpret a TinyCL program."""
        if isinstance(ast, ProgramNode):
            for statement in ast.statements:
                self._interpret_statement(statement)
        else:
            raise ValueError(f"Expected ProgramNode, got {type(ast)}")
    
    def _interpret_statement(self, statement):
        """Interpret a statement."""
        if isinstance(statement, VariableDeclNode):
            self._interpret_variable_decl(statement)
        elif isinstance(statement, PrintNode):
            self._interpret_print(statement)
        else:
            raise ValueError(f"Unknown statement type: {type(statement)}")
    
    def _interpret_variable_decl(self, node):
        """Interpret a variable declaration."""
        value = self._evaluate_expression(node.value)
        self.variables[node.name] = value
    
    def _interpret_print(self, node):
        """Interpret a print statement."""
        value = self._evaluate_expression(node.expression)
        print(value)
    
    def _evaluate_expression(self, expression):
        """Evaluate an expression."""
        if isinstance(expression, NumberNode):
            return expression.value
        elif isinstance(expression, StringNode):
            return expression.value
        elif isinstance(expression, IdentifierNode):
            if expression.name not in self.variables:
                raise ValueError(f"Undefined variable: {expression.name}")
            return self.variables[expression.name]
        else:
            raise ValueError(f"Unknown expression type: {type(expression)}")

def main():
    """Test the TinyCL parser and interpreter."""
    # Example TinyCL program
    program = """
    # This is a comment
    var x = 42;
    var name = "Alice";
    print(x);
    print(name);
    """
    
    print("TinyCL Program:")
    print(program)
    
    try:
        # Parse the program
        parser = TinyCLParser()
        ast = parser.parse(program)
        print("\nParsed AST:")
        print(ast)
        
        # Interpret the program
        print("\nProgram Output:")
        interpreter = TinyCLInterpreter()
        interpreter.interpret(ast)
        
        return 0
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())