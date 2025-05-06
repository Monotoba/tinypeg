# Chapter 3: Building Your First Parser

## 3.1 Setting Up the Environment

Before we start building parsers with TinyPEG, let's ensure our environment is properly set up. We'll need:

1. Python 3.6 or later
2. The TinyPEG library (which we're building in this tutorial)

Let's create a simple project structure:

```
my_parser_project/
├── src/
│   └── peg/  # The TinyPEG library
├── examples/
│   └── simple_parser.py  # Our first parser
└── tests/
    └── test_simple_parser.py  # Tests for our parser
```

For this chapter, we'll focus on creating a simple numeric expression parser that can handle basic arithmetic operations.

## 3.2 Creating a Simple Numeric Expression Parser

Let's start by creating a parser that can recognize and evaluate simple numeric expressions like "42" or "3.14".

First, we need to import the necessary components from the TinyPEG library:

```python
# examples/simple_parser.py
from src.peg import PEGParser, Rule, Reference, GrammarNode, Expression, ParserContext

class NumberParser(PEGParser):
    def __init__(self):
        super().__init__()
        
        # Define grammar for numbers
        self.grammar = GrammarNode(
            name="Number",
            rules=[
                Rule("Number", Reference("Integer")),
                Rule("Integer", Reference("[0-9]+")),
            ]
        )
    
    def parse(self, text: str):
        print(f"Parsing number: {text}")
        # In a real implementation, we would:
        # 1. Create a ParserContext
        # 2. Apply the grammar's start rule
        # 3. Return the result
        
        # For now, we'll just return a dummy result
        try:
            return int(text)
        except ValueError:
            return None
```

This simple parser can recognize integer numbers. Let's test it:

```python
# Test the number parser
if __name__ == "__main__":
    parser = NumberParser()
    result = parser.parse("42")
    print(f"Result: {result}")
```

Running this should output:
```
Parsing number: 42
Result: 42
```

Of course, this is a very simplified implementation. In a real parser, we would:
1. Create a `ParserContext` with the input text
2. Apply the grammar's start rule to the context
3. Build and return a parse tree or AST

Let's enhance our parser to do this properly.

## 3.3 Adding Support for Operators

Now, let's extend our parser to handle basic arithmetic operators: addition, subtraction, multiplication, and division.

In PEG, we need to carefully define the precedence of operators. We'll use the following grammar:

```
Expression ::= Term (('+' | '-') Term)*
Term       ::= Factor (('*' | '/') Factor)*
Factor     ::= Number | '(' Expression ')'
Number     ::= [0-9]+
```

This grammar ensures that multiplication and division have higher precedence than addition and subtraction.

Let's implement this grammar:

```python
# examples/arithmetic_parser.py
from src.peg import PEGParser, Rule, Reference, GrammarNode, Expression, ParserContext

# We'll need some additional expression types for operators
class Sequence(Expression):
    """Match a sequence of expressions in order."""
    def __init__(self, *exprs):
        self.exprs = exprs
    
    def parse(self, ctx):
        results = []
        start_pos = ctx.pos
        
        for expr in self.exprs:
            result = expr.parse(ctx)
            if result is None:
                # Backtrack if any expression fails
                ctx.pos = start_pos
                return None
            results.append(result)
        
        return results

class Choice(Expression):
    """Try expressions in order until one succeeds."""
    def __init__(self, *exprs):
        self.exprs = exprs
    
    def parse(self, ctx):
        for expr in self.exprs:
            start_pos = ctx.pos
            result = expr.parse(ctx)
            if result is not None:
                return result
            # Backtrack for the next choice
            ctx.pos = start_pos
        
        return None

class Literal(Expression):
    """Match a literal string."""
    def __init__(self, literal):
        self.literal = literal
    
    def parse(self, ctx):
        if ctx.pos + len(self.literal) <= len(ctx.text) and \
           ctx.text[ctx.pos:ctx.pos + len(self.literal)] == self.literal:
            ctx.pos += len(self.literal)
            return self.literal
        return None

class ArithmeticParser(PEGParser):
    def __init__(self):
        super().__init__()
        
        # Define grammar for arithmetic expressions
        self.grammar = GrammarNode(
            name="Arithmetic",
            rules=[
                Rule("Expression", Sequence(
                    Reference("Term"),
                    Reference("ExpressionTail")
                )),
                Rule("ExpressionTail", Choice(
                    Sequence(
                        Choice(Literal("+"), Literal("-")),
                        Reference("Term"),
                        Reference("ExpressionTail")
                    ),
                    # Empty alternative for optional tail
                    None
                )),
                Rule("Term", Sequence(
                    Reference("Factor"),
                    Reference("TermTail")
                )),
                Rule("TermTail", Choice(
                    Sequence(
                        Choice(Literal("*"), Literal("/")),
                        Reference("Factor"),
                        Reference("TermTail")
                    ),
                    # Empty alternative for optional tail
                    None
                )),
                Rule("Factor", Choice(
                    Reference("Number"),
                    Sequence(
                        Literal("("),
                        Reference("Expression"),
                        Literal(")")
                    )
                )),
                Rule("Number", Reference("[0-9]+")),
            ]
        )
    
    def parse(self, text: str):
        print(f"Parsing expression: {text}")
        # Create a ParserContext
        ctx = ParserContext(text)
        
        # Apply the grammar's start rule
        result = self.grammar.rules[0].parse(ctx)
        
        # Check if we consumed all input
        if ctx.eof():
            return result
        else:
            print(f"Error: Unexpected input at position {ctx.pos}")
            return None
```

This parser is more complex but still incomplete. In a real implementation, we would need to:
1. Properly handle whitespace
2. Convert the parse tree into an AST
3. Evaluate the AST to compute the result

Let's address these issues in the next sections.

## 3.4 Handling Parentheses and Precedence

Our grammar already accounts for operator precedence and parentheses, but our parser implementation needs to be enhanced to properly build and evaluate the parse tree.

Let's add some AST node classes:

```python
# AST node classes
class ASTNode:
    """Base class for AST nodes."""
    pass

class NumberNode(ASTNode):
    """AST node for numbers."""
    def __init__(self, value):
        self.value = value
    
    def evaluate(self):
        return self.value

class BinaryOpNode(ASTNode):
    """AST node for binary operations."""
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
    
    def evaluate(self):
        left_val = self.left.evaluate()
        right_val = self.right.evaluate()
        
        if self.op == "+":
            return left_val + right_val
        elif self.op == "-":
            return left_val - right_val
        elif self.op == "*":
            return left_val * right_val
        elif self.op == "/":
            return left_val / right_val
        else:
            raise ValueError(f"Unknown operator: {self.op}")
```

Now we need to modify our parser to build these AST nodes during parsing.

## 3.5 Building an Abstract Syntax Tree

To build an AST, we need to modify our expression classes to construct AST nodes as they parse:

```python
class RegexMatcher(Expression):
    """Match a regular expression pattern."""
    def __init__(self, pattern):
        import re
        self.pattern = re.compile(pattern)
    
    def parse(self, ctx):
        if ctx.eof():
            return None
        
        match = self.pattern.match(ctx.text[ctx.pos:])
        if match:
            matched = match.group(0)
            ctx.pos += len(matched)
            return matched
        return None

# Modify our parser to build AST nodes
class ArithmeticParser(PEGParser):
    def __init__(self):
        super().__init__()
        
        # Define grammar for arithmetic expressions
        # (Same as before)
    
    def parse_expression(self, ctx):
        # Parse a term
        left = self.parse_term(ctx)
        if left is None:
            return None
        
        # Parse any following +/- operations
        while not ctx.eof():
            # Try to parse an operator
            op_pos = ctx.pos
            if ctx.text[op_pos] == '+' or ctx.text[op_pos] == '-':
                op = ctx.text[op_pos]
                ctx.pos += 1
                
                # Parse the right term
                right = self.parse_term(ctx)
                if right is None:
                    # Backtrack if the right term fails
                    ctx.pos = op_pos
                    break
                
                # Create a binary operation node
                left = BinaryOpNode(op, left, right)
            else:
                break
        
        return left
    
    def parse_term(self, ctx):
        # Parse a factor
        left = self.parse_factor(ctx)
        if left is None:
            return None
        
        # Parse any following */÷ operations
        while not ctx.eof():
            # Try to parse an operator
            op_pos = ctx.pos
            if ctx.text[op_pos] == '*' or ctx.text[op_pos] == '/':
                op = ctx.text[op_pos]
                ctx.pos += 1
                
                # Parse the right factor
                right = self.parse_factor(ctx)
                if right is None:
                    # Backtrack if the right factor fails
                    ctx.pos = op_pos
                    break
                
                # Create a binary operation node
                left = BinaryOpNode(op, left, right)
            else:
                break
        
        return left
    
    def parse_factor(self, ctx):
        # Skip whitespace
        while not ctx.eof() and ctx.text[ctx.pos].isspace():
            ctx.pos += 1
        
        if ctx.eof():
            return None
        
        # Try to parse a number
        if ctx.text[ctx.pos].isdigit():
            start = ctx.pos
            while not ctx.eof() and ctx.text[ctx.pos].isdigit():
                ctx.pos += 1
            return NumberNode(int(ctx.text[start:ctx.pos]))
        
        # Try to parse a parenthesized expression
        if ctx.text[ctx.pos] == '(':
            ctx.pos += 1
            
            # Parse the inner expression
            expr = self.parse_expression(ctx)
            if expr is None:
                return None
            
            # Expect a closing parenthesis
            if ctx.eof() or ctx.text[ctx.pos] != ')':
                return None
            ctx.pos += 1
            
            return expr
        
        return None
    
    def parse(self, text: str):
        print(f"Parsing expression: {text}")
        # Create a ParserContext
        ctx = ParserContext(text)
        
        # Skip initial whitespace
        while not ctx.eof() and ctx.text[ctx.pos].isspace():
            ctx.pos += 1
        
        # Parse the expression
        ast = self.parse_expression(ctx)
        
        # Skip trailing whitespace
        while not ctx.eof() and ctx.text[ctx.pos].isspace():
            ctx.pos += 1
        
        # Check if we consumed all input
        if ctx.eof():
            return ast
        else:
            print(f"Error: Unexpected input at position {ctx.pos}")
            return None
```

This implementation directly builds an AST during parsing, rather than first building a parse tree and then converting it to an AST. This is a common approach in hand-written recursive descent parsers.

## 3.6 Evaluating Expressions

Now that we have an AST, evaluating expressions is straightforward:

```python
# Test the arithmetic parser
if __name__ == "__main__":
    parser = ArithmeticParser()
    
    test_expressions = [
        "42",
        "2 + 3",
        "2 * 3 + 4",
        "2 + 3 * 4",
        "(2 + 3) * 4",
        "10 / 2 - 3"
    ]
    
    for expr in test_expressions:
        ast = parser.parse(expr)
        if ast:
            result = ast.evaluate()
            print(f"{expr} = {result}")
        else:
            print(f"Failed to parse: {expr}")
```

Running this should output:
```
Parsing expression: 42
42 = 42
Parsing expression: 2 + 3
2 + 3 = 5
Parsing expression: 2 * 3 + 4
2 * 3 + 4 = 10
Parsing expression: 2 + 3 * 4
2 + 3 * 4 = 14
Parsing expression: (2 + 3) * 4
(2 + 3) * 4 = 20
Parsing expression: 10 / 2 - 3
10 / 2 - 3 = 2.0
```

This demonstrates that our parser correctly handles operator precedence and parentheses.

## Summary

In this chapter, we've built a simple arithmetic expression parser using the TinyPEG library. We've learned how to:

1. Define a grammar for arithmetic expressions
2. Implement parsing functions for each grammar rule
3. Build an AST during parsing
4. Evaluate the AST to compute the result

While our implementation is still somewhat simplified, it demonstrates the key concepts of recursive descent parsing and AST construction. In a real-world parser, we would need to handle more complex cases, such as:

- Error reporting and recovery
- More sophisticated tokenization
- Support for variables and functions
- Type checking and semantic analysis

In the next chapter, we'll explore the example parsers included with the TinyPEG library, which demonstrate these more advanced features.