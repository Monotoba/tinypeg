#!/usr/bin/env python3
"""
Parsers module for the TinyPEG library.
"""

import re
from .core import Expression, Reference, Rule, GrammarNode, ParserContext, ParseError

def _parse_expression_or_reference(expr, ctx):
    """Utility function to parse either an Expression or Reference."""
    if isinstance(expr, Reference):
        parser = ctx._parser if hasattr(ctx, '_parser') else None
        if parser:
            return parser._parse_reference(expr, ctx)
        else:
            raise ParseError(f"Cannot parse reference '{expr}' without a parser")
    elif isinstance(expr, Expression):
        return expr.parse(ctx)
    else:
        raise TypeError(f"Unknown expression type: {type(expr)}")

class Literal(Expression):
    """Match a literal string."""

    def __init__(self, text):
        """Initialize with a literal string to match."""
        self.text = text

    def parse(self, ctx):
        """Parse by matching the literal string."""
        start_pos = ctx.pos

        # Check if the input starts with the literal
        if ctx.eof():
            raise ParseError(f"Expected '{self.text}', but reached end of input")

        for char in self.text:
            if ctx.eof() or ctx.peek() != char:
                ctx.pos = start_pos
                raise ParseError(f"Expected '{self.text}', got '{ctx.text[start_pos:start_pos+len(self.text)]}'")
            ctx.consume()

        # Skip trailing whitespace
        ctx.skip_whitespace()

        return self.text

    def __str__(self):
        return f"Literal('{self.text}')"

class Regex(Expression):
    """Match a regular expression pattern."""

    def __init__(self, pattern):
        """Initialize with a regex pattern to match."""
        self.pattern = pattern
        self.regex = re.compile(f"^{pattern}")

    def parse(self, ctx):
        """Parse by matching the regex pattern."""
        start_pos = ctx.pos

        # Skip trailing whitespace
        ctx.skip_whitespace()

        if ctx.eof():
            raise ParseError(f"Expected pattern '{self.pattern}', but reached end of input")

        # Try to match at the current position
        match = self.regex.match(ctx.text[ctx.pos:])
        if not match:
            raise ParseError(f"Expected pattern '{self.pattern}', got '{ctx.text[ctx.pos:ctx.pos+10]}...'")

        # Get the matched string
        matched = match.group(0)

        # Advance the position
        for _ in range(len(matched)):
            ctx.consume()

        return matched

    def __str__(self):
        return f"Regex('{self.pattern}')"

class Sequence(Expression):
    """Match a sequence of expressions."""

    def __init__(self, *exprs):
        """Initialize with a sequence of expressions."""
        self.exprs = exprs

    def parse(self, ctx):
        """Parse by matching each expression in sequence."""
        results = []
        start_pos = ctx.pos

        try:
            for expr in self.exprs:
                # Skip whitespace between sequence elements
                ctx.skip_whitespace()

                # Parse the expression
                result = _parse_expression_or_reference(expr, ctx)

                results.append(result)

            return results
        except ParseError as e:
            ctx.pos = start_pos
            raise ParseError(f"Sequence failed: {e}")

    def __str__(self):
        return f"Sequence({len(self.exprs)} expressions)"

class Choice(Expression):
    """Match one of several expressions."""

    def __init__(self, *exprs):
        """Initialize with a choice of expressions."""
        self.exprs = exprs

    def parse(self, ctx):
        """Parse by trying each expression in order."""
        start_pos = ctx.pos
        errors = []

        for expr in self.exprs:
            try:
                ctx.pos = start_pos
                return _parse_expression_or_reference(expr, ctx)
            except ParseError as e:
                errors.append(str(e))

        ctx.pos = start_pos
        raise ParseError(f"None of the choices matched: {', '.join(errors)}")

    def __str__(self):
        return f"Choice({len(self.exprs)} expressions)"

class ZeroOrMore(Expression):
    """Match an expression zero or more times."""

    def __init__(self, expr):
        """Initialize with an expression to match zero or more times."""
        self.expr = expr

    def parse(self, ctx):
        """Parse by matching the expression as many times as possible."""
        results = []

        while True:
            start_pos = ctx.pos
            try:
                result = _parse_expression_or_reference(self.expr, ctx)
                results.append(result)

                # Check for infinite loop
                if ctx.pos == start_pos:
                    break
            except ParseError:
                # No more matches
                break

        return results

    def __str__(self):
        return f"ZeroOrMore({self.expr})"

class OneOrMore(Expression):
    """Match an expression one or more times."""

    def __init__(self, expr):
        """Initialize with an expression to match one or more times."""
        self.expr = expr

    def parse(self, ctx):
        """Parse by matching the expression at least once."""
        results = []
        start_pos = ctx.pos

        try:
            # Must match at least once
            result = _parse_expression_or_reference(self.expr, ctx)
            results.append(result)

            # Then match zero or more times
            while True:
                start_pos = ctx.pos
                try:
                    result = _parse_expression_or_reference(self.expr, ctx)
                    results.append(result)

                    # Check for infinite loop
                    if ctx.pos == start_pos:
                        break
                except ParseError:
                    # No more matches
                    break

            return results
        except ParseError as e:
            ctx.pos = start_pos
            raise ParseError(f"OneOrMore failed: {e}")

    def __str__(self):
        return f"OneOrMore({self.expr})"

class Optional(Expression):
    """Match an expression zero or one time."""

    def __init__(self, expr):
        """Initialize with an expression to match optionally."""
        self.expr = expr

    def parse(self, ctx):
        """Parse by trying to match the expression, but succeeding even if it fails."""
        start_pos = ctx.pos

        try:
            return _parse_expression_or_reference(self.expr, ctx)
        except ParseError:
            # Expression didn't match, but that's OK for optional
            ctx.pos = start_pos
            return None

    def __str__(self):
        return f"Optional({self.expr})"

class AndPredicate(Expression):
    """Positive lookahead assertion."""

    def __init__(self, expr):
        """Initialize with an expression to check."""
        self.expr = expr

    def parse(self, ctx):
        """Parse by checking if the expression matches without consuming input."""
        start_pos = ctx.pos

        try:
            # Try to match the expression
            result = self.expr.parse(ctx)

            # Reset position (don't consume input)
            ctx.pos = start_pos

            # Return an empty string
            return ""
        except ParseError as e:
            # Expression didn't match
            ctx.pos = start_pos
            raise ParseError(f"Positive lookahead failed: {e}")

    def __str__(self):
        return f"AndPredicate({self.expr})"

class NotPredicate(Expression):
    """Negative lookahead assertion."""

    def __init__(self, expr):
        """Initialize with an expression to check."""
        self.expr = expr

    def parse(self, ctx):
        """Parse by checking if the expression doesn't match without consuming input."""
        start_pos = ctx.pos

        try:
            # Try to match the expression
            self.expr.parse(ctx)

            # If we get here, the expression matched, which is a failure for NotPredicate
            ctx.pos = start_pos
            raise ParseError("Negative lookahead failed: expression matched")
        except ParseError:
            # Expression didn't match, which is what we want
            ctx.pos = start_pos
            return ""

    def __str__(self):
        return f"NotPredicate({self.expr})"

class PEGParser:
    """Parser for PEG grammars."""

    def __init__(self):
        """Initialize the parser."""
        self.grammar = None
        self.rule_cache = {}

    def parse(self, text):
        """Parse the input text using the grammar."""
        if not self.grammar:
            raise ValueError("No grammar defined")

        ctx = ParserContext(text)
        # Store a reference to the parser in the context
        ctx._parser = self
        self.rule_cache = {}

        # Skip initial whitespace
        ctx.skip_whitespace()

        # Get the start rule (first rule in the grammar)
        if not self.grammar.rules:
            raise ValueError("Grammar has no rules")

        start_rule = self.grammar.rules[0]

        # Parse the input using the start rule
        result = self._parse_rule(start_rule, ctx)

        # Skip final whitespace
        ctx.skip_whitespace()

        # Check if we've consumed all input
        if not ctx.eof():
            raise ParseError(f"Unexpected input at position {ctx.pos}: '{ctx.text[ctx.pos:]}'")

        return result

    def _parse_rule(self, rule, ctx):
        """Parse a rule at the current position."""
        # Check if we've already parsed this rule at this position (memoization)
        cache_key = (rule.name, ctx.pos)
        if cache_key in self.rule_cache:
            result, new_pos = self.rule_cache[cache_key]
            ctx.pos = new_pos
            return result

        # Save the current position for backtracking
        start_pos = ctx.pos

        try:
            # Skip whitespace before parsing the rule
            ctx.skip_whitespace()

            # Parse the rule's expression
            result = self._parse_expression(rule.expr, ctx)

            # Cache the result
            self.rule_cache[cache_key] = (result, ctx.pos)

            return result
        except ParseError as e:
            # Backtrack on failure
            ctx.pos = start_pos
            raise ParseError(f"Rule '{rule.name}' failed: {e}")

    def _parse_expression(self, expr, ctx):
        """Parse an expression at the current position."""
        # Skip whitespace before parsing the expression
        ctx.skip_whitespace()

        if isinstance(expr, Reference):
            return self._parse_reference(expr, ctx)
        elif isinstance(expr, Expression):
            return expr.parse(ctx)
        elif isinstance(expr, list):
            # Handle lists of expressions (e.g., from Sequence)
            results = []
            for e in expr:
                results.append(self._parse_expression(e, ctx))
            return results
        else:
            raise TypeError(f"Unknown expression type: {type(expr)}")

    def _parse_reference(self, ref, ctx):
        """Parse a reference to another rule."""
        # Find the referenced rule
        for rule in self.grammar.rules:
            if rule.name == ref.name:
                return self._parse_rule(rule, ctx)

        raise ParseError(f"Undefined rule: {ref.name}")

    def __str__(self):
        return f"PEGParser({self.grammar})"
