# Chapter 4: Advanced Topics in Parser Development

## Introduction

In the previous chapters, we've built a simple PEG parser library and used it to implement a small programming language called TinyCL. In this chapter, we'll explore some advanced topics in parser development that can help you build more powerful and efficient parsers.

## Error Handling and Recovery

One of the most important aspects of a good parser is how it handles errors. When a syntax error is encountered, the parser should:

1. Detect the error and report it with a clear, helpful message.
2. Recover from the error and continue parsing if possible.
3. Avoid cascading errors (where a single error causes many error messages).

Let's enhance our TinyPEG library with better error handling:

```python
class ParseError(Exception):
    """Exception raised when a parsing error occurs."""
    
    def __init__(self, message, position, line, column, context=None):
        self.message = message
        self.position = position
        self.line = line
        self.column = column
        self.context = context
        
        # Format the error message
        error_msg = f"Parse error at line {line}, column {column}: {message}"
        if context:
            error_msg += f"\n{context}"
        
        super().__init__(error_msg)

class ParserContext:
    """Context for parsing, with error handling."""
    
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.error_pos = -1
        self.error_msg = None
        self.error_stack = []
    
    def eof(self):
        """Check if we've reached the end of the input."""
        return self.pos >= len(self.text)
    
    def peek(self):
        """Look at the current character without consuming it."""
        if self.eof():
            return None
        return self.text[self.pos]
    
    def consume(self):
        """Consume the current character and return it."""
        if self.eof():
            return None
        c = self.text[self.pos]
        self.pos += 1
        return c
    
    def expect(self, expected):
        """Expect a specific character or string."""
        if isinstance(expected, str):
            # Check if the expected string matches
            if self.pos + len(expected) <= len(self.text) and self.text[self.pos:self.pos+len(expected)] == expected:
                self.pos += len(expected)
                return expected
        else:
            # Check if the current character matches
            if not self.eof() and self.peek() == expected:
                return self.consume()
        
        # Record the error
        self.record_error(f"Expected {expected}, got {self.peek() if not self.eof() else 'EOF'}")
        return None
    
    def record_error(self, message):
        """Record an error at the current position."""
        if self.pos > self.error_pos:
            self.error_pos = self.pos
            self.error_msg = message
    
    def push_error_context(self, context):
        """Push an error context onto the stack."""
        self.error_stack.append(context)
    
    def pop_error_context(self):
        """Pop an error context from the stack."""
        if self.error_stack:
            return self.error_stack.pop()
        return None
    
    def get_error(self):
        """Get the current error, if any."""
        if self.error_msg:
            # Calculate line and column
            line = 1
            line_start = 0
            for i in range(self.error_pos):
                if self.text[i] == '\n':
                    line += 1
                    line_start = i + 1
            column = self.error_pos - line_start + 1
            
            # Get context
            context = None
            if self.error_stack:
                context = ", ".join(self.error_stack)
            
            return ParseError(self.error_msg, self.error_pos, line, column, context)
        return None
```

Now, let's update our `PEGParser` class to use this enhanced error handling:

```python
class PEGParser:
    """Base class for PEG parsers."""
    
    def __init__(self):
        self.grammar = None
    
    def parse(self, text):
        """Parse the input text according to the grammar."""
        if not self.grammar:
            raise ValueError("Grammar not defined")
        
        ctx = ParserContext(text)
        result = self._parse_expression(self.grammar, ctx)
        
        # Check for errors
        error = ctx.get_error()
        if error:
            raise error
        
        # Check if we consumed all input
        if not ctx.eof():
            line = 1
            line_start = 0
            for i in range(ctx.pos):
                if text[i] == '\n':
                    line += 1
                    line_start = i + 1
            column = ctx.pos - line_start + 1
            
            raise ParseError(f"Unexpected input at position {ctx.pos}: '{text[ctx.pos:]}'", ctx.pos, line, column)
        
        return result
    
    def _parse_expression(self, expr, ctx):
        """Parse an expression."""
        # Push error context
        ctx.push_error_context(f"Parsing {expr}")
        
        try:
            # Dispatch to the appropriate parsing method
            if isinstance(expr, Literal):
                return self._parse_literal(expr, ctx)
            elif isinstance(expr, Regex):
                return self._parse_regex(expr, ctx)
            elif isinstance(expr, Sequence):
                return self._parse_sequence(expr, ctx)
            elif isinstance(expr, Choice):
                return self._parse_choice(expr, ctx)
            elif isinstance(expr, ZeroOrMore):
                return self._parse_zero_or_more(expr, ctx)
            elif isinstance(expr, OneOrMore):
                return self._parse_one_or_more(expr, ctx)
            elif isinstance(expr, Optional):
                return self._parse_optional(expr, ctx)
            elif isinstance(expr, Reference):
                return self._parse_reference(expr, ctx)
            elif isinstance(expr, GrammarNode):
                return self._parse_grammar_node(expr, ctx)
            elif isinstance(expr, Rule):
                return self._parse_rule(expr, ctx)
            else:
                raise ValueError(f"Unknown expression type: {type(expr)}")
        finally:
            # Pop error context
            ctx.pop_error_context()
    
    # ... (other parsing methods omitted for brevity)
```

With these enhancements, our parser will provide more helpful error messages when it encounters syntax errors.

## Optimizing Parser Performance

PEG parsers can be inefficient due to backtracking. One way to optimize parser performance is to use a technique called "packrat parsing," which memoizes the results of parsing expressions to avoid redundant work.

Let's add memoization to our `PEGParser` class:

```python
class PEGParser:
    """Base class for PEG parsers with memoization."""
    
    def __init__(self):
        self.grammar = None
        self.memo = {}
    
    def parse(self, text):
        """Parse the input text according to the grammar."""
        if not self.grammar:
            raise ValueError("Grammar not defined")
        
        # Clear the memoization cache
        self.memo = {}
        
        ctx = ParserContext(text)
        result = self._parse_expression(self.grammar, ctx)
        
        # ... (error handling code omitted for brevity)
        
        return result
    
    def _parse_expression(self, expr, ctx):
        """Parse an expression with memoization."""
        # Check if we've already parsed this expression at this position
        memo_key = (id(expr), ctx.pos)
        if memo_key in self.memo:
            # Restore the position and return the memoized result
            result, new_pos = self.memo[memo_key]
            ctx.pos = new_pos
            return result
        
        # Save the current position
        start_pos = ctx.pos
        
        # Parse the expression
        result = self._parse_expression_impl(expr, ctx)
        
        # Memoize the result
        self.memo[memo_key] = (result, ctx.pos)
        
        return result
    
    def _parse_expression_impl(self, expr, ctx):
        """Actual implementation of expression parsing."""
        # ... (dispatch to the appropriate parsing method)
```

With memoization, our parser will avoid redundant work and be much more efficient, especially for complex grammars.

## Left Recursion

PEGs cannot directly express left-recursive rules, which can make some grammars more complex. For example, consider the following grammar for expressions:

```
expr = expr '+' term | expr '-' term | term
term = term '*' factor | term '/' factor | factor
factor = '(' expr ')' | number
```

This grammar is left-recursive because the `expr` rule refers to itself at the beginning of its definition. PEGs cannot handle this directly, but we can transform the grammar to eliminate left recursion:

```
expr = term expr_tail
expr_tail = '+' term expr_tail | '-' term expr_tail | ε
term = factor term_tail
term_tail = '*' factor term_tail | '/' factor term_tail | ε
factor = '(' expr ')' | number
```

This transformed grammar is equivalent to the original but doesn't use left recursion.

Alternatively, we can extend our PEG parser to handle left recursion directly using a technique called "packrat parsing with left recursion." This is more complex but allows for more natural grammar definitions.

## Semantic Actions

So far, our parser has focused on syntax analysis (parsing the structure of the input). But in a real compiler or interpreter, we also need semantic analysis (understanding the meaning of the input).

We can add semantic actions to our parser to build an AST or perform other semantic analyses during parsing:

```python
class Rule:
    """A named rule in a grammar, with a semantic action."""
    
    def __init__(self, name, expression, action=None):
        self.name = name
        self.expression = expression
        self.action = action
    
    def apply_action(self, result):
        """Apply the semantic action to the parse result."""
        if self.action:
            return self.action(result)
        return result
```

Now, we can define rules with semantic actions:

```python
# Define a rule for numbers with a semantic action
Rule("Number", Regex("[0-9]+"), lambda result: int(result))

# Define a rule for addition with a semantic action
Rule("Addition", Sequence(
    Reference("Term"),
    Literal("+"),
    Reference("Term")
), lambda result: result[0] + result[2])
```

With semantic actions, our parser can build an AST or evaluate expressions directly during parsing.

## Conclusion

In this chapter, we've explored some advanced topics in parser development:

1. **Error Handling and Recovery**: We've enhanced our parser with better error handling to provide more helpful error messages.
2. **Optimizing Parser Performance**: We've added memoization to our parser to avoid redundant work and improve performance.
3. **Left Recursion**: We've discussed how to handle left recursion in PEG parsers.
4. **Semantic Actions**: We've added semantic actions to our parser to build an AST or perform other semantic analyses during parsing.

These techniques can help you build more powerful, efficient, and user-friendly parsers for a wide range of languages and applications.

In the next chapter, we'll explore how to use our parser to build a more sophisticated programming language with advanced features like type checking, closures, and more.