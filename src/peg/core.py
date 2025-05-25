#!/usr/bin/env python3
"""
Core module for the TinyPEG library.
"""

import re

class ParseError(Exception):
    """Custom error for parsing issues."""
    pass

class ParserContext:
    """Context class to hold the parsing state."""

    def __init__(self, text):
        self.text = text
        self.pos = 0

    def eof(self):
        """Check if we've reached the end of the input."""
        return self.pos >= len(self.text)

    def peek(self):
        """Return the current character without advancing."""
        return self.text[self.pos] if not self.eof() else None

    def consume(self):
        """Advance the position by one character."""
        char = self.peek()
        self.pos += 1
        return char

    def skip_whitespace(self):
        """Skip whitespace characters."""
        while not self.eof() and self.peek().isspace():
            self.consume()


class Expression:
    """Base class for expressions."""
    def parse(self, ctx):
        raise NotImplementedError("Subclasses should implement this method.")

class Reference(Expression):
    """Reference to a rule by name."""

    def __init__(self, name):
        self.name = name

    def parse(self, ctx):
        """Parse method - should be handled by the grammar system."""
        raise NotImplementedError("Reference parsing is handled by the grammar system")

    def __str__(self):
        return f"Reference('{self.name}')"

class Rule(Expression):
    """A grammar rule with a name and expression."""

    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def parse(self, ctx):
        """Parse this rule using its expression."""
        return self.expr.parse(ctx)

    def __str__(self):
        return f"Rule('{self.name}', {self.expr})"

class GrammarNode:
    """The root node of a grammar."""

    def __init__(self, name, rules):
        """Initialize with a name and a list of rules."""
        self.name = name
        self.rules = rules

    def __str__(self):
        """Return a string representation of the grammar."""
        return f"Grammar({self.name}, {len(self.rules)} rules)"

if __name__ == "__main__":
    # Main guard for testing core functionality.
    try:
        print("Testing core.py functionality...")
        ctx = ParserContext("test input")
        print(f"Initial position: {ctx.pos}, EOF: {ctx.eof()}")
        ctx.consume()
        print(f"Position after consume: {ctx.pos}, Peek: {ctx.peek()}")
    except Exception as e:
        print(f"Error: {e}")
        print(f"Error in core.py main guard: {e}")
