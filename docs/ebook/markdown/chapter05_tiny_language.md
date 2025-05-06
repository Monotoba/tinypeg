# Chapter 5: Creating a Tiny Programming Language

In this chapter, we'll build a complete tiny programming language called TinyCL using our PEG parser library. TinyCL will be a simple but functional language with variables, control structures, and basic I/O.

## 5.1 Designing the TinyCL Language

Before we start implementing the parser, let's design the language itself.

### 5.1.1 Language Features

TinyCL will support the following features:

1. **Variables**: Declaration and assignment of integer and string variables
2. **Arithmetic Operations**: Addition, subtraction, multiplication, and division
3. **Control Structures**: If statements and while loops
4. **I/O Operations**: Print statements for output
5. **Comments**: Single-line comments

Here's an example of a TinyCL program:

```
# Calculate factorial
let n = 5;
let factorial = 1;

while (n > 0) {
    factorial = factorial * n;
    n = n - 1;
}

print("Factorial: " + factorial);
```

### 5.1.2 Grammar Specification

Now, let's define the grammar for TinyCL:

```
Program       ::= Statement*
Statement     ::= LetStatement | AssignStatement | IfStatement | WhileStatement | PrintStatement | Block | Comment
LetStatement  ::= "let" Identifier "=" Expression ";"
AssignStatement ::= Identifier "=" Expression ";"
IfStatement   ::= "if" "(" Condition ")" Statement ("else" Statement)?
WhileStatement ::= "while" "(" Condition ")" Statement
PrintStatement ::= "print" "(" Expression ")" ";"
Block         ::= "{" Statement* "}"
Comment       ::= "#" [^\n]*

Condition     ::= Expression ComparisonOp Expression
ComparisonOp  ::= "==" | "!=" | "<" | ">" | "<=" | ">="

Expression    ::= Term ("+" Term | "-" Term)*
Term          ::= Factor ("*" Factor | "/" Factor)*
Factor        ::= Number | String | Identifier | "(" Expression ")"
Number        ::= [0-9]+
String        ::= "\"" [^"]* "\""
Identifier    ::= [a-zA-Z_][a-zA-Z0-9_]*
```

This grammar defines the syntax of TinyCL programs. Now, let's implement the parser.

## 5.2 Implementing the Parser

We'll implement the TinyCL parser using our PEG parser library. First, let's create a new file for the parser:

```python
# src/examples/tinycl/tinycl_parser.py
from src.peg import PEGParser, Rule, Reference, GrammarNode, Expression, ParserContext, ParseError

class TinyCLParser(PEGParser):
    def __init__(self):
        super().__init__()
        
        # Define grammar for TinyCL
        self.grammar = GrammarNode(
            name="TinyCL",
            rules=[
                # Program structure
                Rule("Program", Reference("StatementList")),
                Rule("StatementList", Reference("Statement"), Reference("StatementList"), Reference("Statement")),
                
                # Statements
                Rule("Statement", Reference("LetStatement"), Reference("AssignStatement"), 
                     Reference("IfStatement"), Reference("WhileStatement"), 
                     Reference("PrintStatement"), Reference("Block"), Reference("Comment")),
                
                # Let statement
                Rule("LetStatement", Reference('"let"'), Reference("Identifier"), 
                     Reference('"="'), Reference("Expression"), Reference('";"')),
                
                # Assignment statement
                Rule("AssignStatement", Reference("Identifier"), Reference('"="'), 
                     Reference("Expression"), Reference('";"')),
                
                # If statement
                Rule("IfStatement", Reference('"if"'), Reference('"("'), Reference("Condition"), 
                     Reference('")"'), Reference("Statement"), 
                     Reference('"else"'), Reference("Statement")),
                
                # While statement
                Rule("WhileStatement", Reference('"while"'), Reference('"("'), Reference("Condition"), 
                     Reference('")"'), Reference("Statement")),
                
                # Print statement
                Rule("PrintStatement", Reference('"print"'), Reference('"("'), 
                     Reference("Expression"), Reference('")"'), Reference('";"')),
                
                # Block
                Rule("Block", Reference('"{"'), Reference("StatementList"), Reference('"}"')),
                
                # Comment
                Rule("Comment", Reference('"#"'), Reference('[^\\n]*')),
                
                # Condition
                Rule("Condition", Reference("Expression"), Reference("ComparisonOp"), Reference("Expression")),
                
                # Comparison operators
                Rule("ComparisonOp", Reference('"=="'), Reference('"!="'), 
                     Reference('"<"'), Reference('">"'), 
                     Reference('"<="'), Reference('">="')),
                
                # Expression
                Rule("Expression", Reference("Term"), Reference('"+"'), Reference("Term"), 
                     Reference('"-"'), Reference("Term")),
                
                # Term
                Rule("Term", Reference("Factor"), Reference('"*"'), Reference("Factor"), 
                     Reference('"/"'), Reference("Factor")),
                
                # Factor
                Rule("Factor", Reference("Number"), Reference("String"), 
                     Reference("Identifier"), Reference('"("'), 
                     Reference("Expression"), Reference('")"')),
                
                # Terminals
                Rule("Number", Reference('[0-9]+')),
                Rule("String", Reference('\\"[^\\"]*\\"')),
                Rule("Identifier", Reference('[a-zA-Z_][a-zA-Z0-9_]*')),
            ]
        )
    
    def parse(self, text: str):
        print(f"Parsing TinyCL program:\n{text}")
        # Create a ParserContext
        ctx = ParserContext(text)
        
        # Apply the grammar's start rule
        result = self.grammar.rules[0].parse(ctx)
        
        # Check if we consumed all input
        if ctx.eof():
            return result
        else:
            raise ParseError(f"Unexpected input at position {ctx.pos}")
```

This parser defines the grammar for TinyCL and implements the `parse` method to parse TinyCL programs. However, it doesn't yet build an AST or interpret the programs.

### 5.2.1 Lexical Elements

Let's enhance our parser to handle lexical elements like whitespace and comments properly:

```python
# Add to TinyCLParser class
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
```

### 5.2.2 Expressions

Now, let's implement the parsing of expressions:

```python
# Add to TinyCLParser class
def parse_expression(self, ctx):
    """Parse an expression."""
    self.skip_whitespace(ctx)
    
    # Parse a term
    left = self.parse_term(ctx)
    if left is None:
        return None
    
    # Parse any following +/- operations
    while not ctx.eof():
        self.skip_whitespace(ctx)
        
        # Try to parse an operator
        op_pos = ctx.pos
        if ctx.peek() == '+' or ctx.peek() == '-':
            op = ctx.consume()
            
            self.skip_whitespace(ctx)
            
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
    """Parse a term."""
    self.skip_whitespace(ctx)
    
    # Parse a factor
    left = self.parse_factor(ctx)
    if left is None:
        return None
    
    # Parse any following */÷ operations
    while not ctx.eof():
        self.skip_whitespace(ctx)
        
        # Try to parse an operator
        op_pos = ctx.pos
        if ctx.peek() == '*' or ctx.peek() == '/':
            op = ctx.consume()
            
            self.skip_whitespace(ctx)
            
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
    """Parse a factor."""
    self.skip_whitespace(ctx)
    
    if ctx.eof():
        return None
    
    # Try to parse a number
    if ctx.peek().isdigit():
        return self.parse_number(ctx)
    
    # Try to parse a string
    if ctx.peek() == '"':
        return self.parse_string(ctx)
    
    # Try to parse an identifier
    if ctx.peek().isalpha() or ctx.peek() == '_':
        return self.parse_identifier(ctx)
    
    # Try to parse a parenthesized expression
    if ctx.peek() == '(':
        ctx.consume()  # Consume '('
        
        self.skip_whitespace(ctx)
        
        # Parse the inner expression
        expr = self.parse_expression(ctx)
        if expr is None:
            return None
        
        self.skip_whitespace(ctx)
        
        # Expect a closing parenthesis
        if ctx.eof() or ctx.peek() != ')':
            return None
        ctx.consume()  # Consume ')'
        
        return expr
    
    return None

def parse_number(self, ctx):
    """Parse a number."""
    start = ctx.pos
    while not ctx.eof() and ctx.peek().isdigit():
        ctx.consume()
    
    if start == ctx.pos:
        return None
    
    return NumberNode(int(ctx.text[start:ctx.pos]))

def parse_string(self, ctx):
    """Parse a string."""
    if ctx.eof() or ctx.peek() != '"':
        return None
    
    ctx.consume()  # Consume opening quote
    
    start = ctx.pos
    while not ctx.eof() and ctx.peek() != '"':
        ctx.consume()
    
    if ctx.eof():
        return None  # Unterminated string
    
    value = ctx.text[start:ctx.pos]
    ctx.consume()  # Consume closing quote
    
    return StringNode(value)

def parse_identifier(self, ctx):
    """Parse an identifier."""
    if ctx.eof() or not (ctx.peek().isalpha() or ctx.peek() == '_'):
        return None
    
    start = ctx.pos
    ctx.consume()  # Consume first character
    
    while not ctx.eof() and (ctx.peek().isalnum() or ctx.peek() == '_'):
        ctx.consume()
    
    name = ctx.text[start:ctx.pos]
    return IdentifierNode(name)
```

### 5.2.3 Statements

Now, let's implement the parsing of statements:

```python
# Add to TinyCLParser class
def parse_statement(self, ctx):
    """Parse a statement."""
    self.skip_whitespace(ctx)
    
    if ctx.eof():
        return None
    
    # Try to parse a let statement
    if ctx.pos + 3 <= len(ctx.text) and ctx.text[ctx.pos:ctx.pos+3] == "let":
        return self.parse_let_statement(ctx)
    
    # Try to parse an if statement
    if ctx.pos + 2 <= len(ctx.text) and ctx.text[ctx.pos:ctx.pos+2] == "if":
        return self.parse_if_statement(ctx)
    
    # Try to parse a while statement
    if ctx.pos + 5 <= len(ctx.text) and ctx.text[ctx.pos:ctx.pos+5] == "while":
        return self.parse_while_statement(ctx)
    
    # Try to parse a print statement
    if ctx.pos + 5 <= len(ctx.text) and ctx.text[ctx.pos:ctx.pos+5] == "print":
        return self.parse_print_statement(ctx)
    
    # Try to parse a block
    if ctx.peek() == '{':
        return self.parse_block(ctx)
    
    # Try to parse an assignment statement
    return self.parse_assignment_statement(ctx)

def parse_let_statement(self, ctx):
    """Parse a let statement."""
    start_pos = ctx.pos
    
    # Expect "let"
    if ctx.pos + 3 > len(ctx.text) or ctx.text[ctx.pos:ctx.pos+3] != "let":
        return None
    ctx.pos += 3
    
    self.skip_whitespace(ctx)
    
    # Parse identifier
    identifier = self.parse_identifier(ctx)
    if identifier is None:
        ctx.pos = start_pos
        return None
    
    self.skip_whitespace(ctx)
    
    # Expect "="
    if ctx.eof() or ctx.peek() != '=':
        ctx.pos = start_pos
        return None
    ctx.consume()
    
    self.skip_whitespace(ctx)
    
    # Parse expression
    expression = self.parse_expression(ctx)
    if expression is None:
        ctx.pos = start_pos
        return None
    
    self.skip_whitespace(ctx)
    
    # Expect ";"
    if ctx.eof() or ctx.peek() != ';':
        ctx.pos = start_pos
        return None
    ctx.consume()
    
    return LetStatementNode(identifier, expression)

# Similar implementations for parse_assignment_statement, parse_if_statement,
# parse_while_statement, parse_print_statement, and parse_block
```

### 5.2.4 Program Structure

Finally, let's implement the parsing of the overall program structure:

```python
# Add to TinyCLParser class
def parse_program(self, ctx):
    """Parse a program."""
    statements = []
    
    while not ctx.eof():
        self.skip_whitespace(ctx)
        
        if ctx.eof():
            break
        
        statement = self.parse_statement(ctx)
        if statement is None:
            break
        
        statements.append(statement)
    
    return ProgramNode(statements)

def parse(self, text: str):
    """Parse a TinyCL program."""
    print(f"Parsing TinyCL program:\n{text}")
    
    # Create a ParserContext
    ctx = ParserContext(text)
    
    # Parse the program
    program = self.parse_program(ctx)
    
    # Skip any trailing whitespace
    self.skip_whitespace(ctx)
    
    # Check if we consumed all input
    if ctx.eof():
        return program
    else:
        raise ParseError(f"Unexpected input at position {ctx.pos}: '{ctx.text[ctx.pos:]}'")
```

## 5.3 Building the Abstract Syntax Tree

Now that we have the parsing functions, we need to define the AST node classes:

```python
# AST node classes
class ASTNode:
    """Base class for AST nodes."""
    pass

class ProgramNode(ASTNode):
    """AST node for a program."""
    def __init__(self, statements):
        self.statements = statements

class StatementNode(ASTNode):
    """Base class for statement nodes."""
    pass

class LetStatementNode(StatementNode):
    """AST node for a let statement."""
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

class AssignStatementNode(StatementNode):
    """AST node for an assignment statement."""
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

class IfStatementNode(StatementNode):
    """AST node for an if statement."""
    def __init__(self, condition, then_statement, else_statement=None):
        self.condition = condition
        self.then_statement = then_statement
        self.else_statement = else_statement

class WhileStatementNode(StatementNode):
    """AST node for a while statement."""
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class PrintStatementNode(StatementNode):
    """AST node for a print statement."""
    def __init__(self, expression):
        self.expression = expression

class BlockNode(StatementNode):
    """AST node for a block."""
    def __init__(self, statements):
        self.statements = statements

class ExpressionNode(ASTNode):
    """Base class for expression nodes."""
    pass

class BinaryOpNode(ExpressionNode):
    """AST node for a binary operation."""
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class NumberNode(ExpressionNode):
    """AST node for a number."""
    def __init__(self, value):
        self.value = value

class StringNode(ExpressionNode):
    """AST node for a string."""
    def __init__(self, value):
        self.value = value

class IdentifierNode(ExpressionNode):
    """AST node for an identifier."""
    def __init__(self, name):
        self.name = name

class ConditionNode(ASTNode):
    """AST node for a condition."""
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
```

### 5.3.1 AST Node Classes

These AST node classes represent the different elements of a TinyCL program. Each class corresponds to a specific grammar rule and contains the necessary information to represent that element in the AST.

### 5.3.2 Tree Construction

The parsing functions we implemented earlier construct the AST as they parse the input. Each parsing function returns an AST node representing the parsed element.

## 5.4 Semantic Analysis

After parsing the program and building the AST, we need to perform semantic analysis to check for errors and prepare for interpretation.

### 5.4.1 Symbol Table

The symbol table keeps track of variables and their types:

```python
class SymbolTable:
    """Symbol table for tracking variables."""
    def __init__(self):
        self.symbols = {}
    
    def define(self, name, value):
        """Define a variable."""
        self.symbols[name] = value
    
    def lookup(self, name):
        """Look up a variable."""
        return self.symbols.get(name)
    
    def update(self, name, value):
        """Update a variable's value."""
        if name not in self.symbols:
            raise NameError(f"Variable '{name}' not defined")
        self.symbols[name] = value
```

### 5.4.2 Type Checking

We can add type checking to ensure that operations are performed on compatible types:

```python
def check_types(node, symbol_table):
    """Check types in the AST."""
    if isinstance(node, ProgramNode):
        for statement in node.statements:
            check_types(statement, symbol_table)
    
    elif isinstance(node, LetStatementNode):
        # Check that the expression has a valid type
        expr_type = get_expression_type(node.expression, symbol_table)
        if expr_type is None:
            raise TypeError(f"Invalid expression in let statement")
        
        # Define the variable
        symbol_table.define(node.identifier.name, None)
    
    elif isinstance(node, AssignStatementNode):
        # Check that the variable is defined
        if symbol_table.lookup(node.identifier.name) is None:
            raise NameError(f"Variable '{node.identifier.name}' not defined")
        
        # Check that the expression has a valid type
        expr_type = get_expression_type(node.expression, symbol_table)
        if expr_type is None:
            raise TypeError(f"Invalid expression in assignment")
    
    # Similar implementations for other node types
    
    return True

def get_expression_type(node, symbol_table):
    """Get the type of an expression."""
    if isinstance(node, NumberNode):
        return "number"
    
    elif isinstance(node, StringNode):
        return "string"
    
    elif isinstance(node, IdentifierNode):
        # Check that the variable is defined
        if symbol_table.lookup(node.name) is None:
            raise NameError(f"Variable '{node.name}' not defined")
        
        # Return the type of the variable
        value = symbol_table.lookup(node.name)
        if isinstance(value, int):
            return "number"
        elif isinstance(value, str):
            return "string"
        else:
            return None
    
    elif isinstance(node, BinaryOpNode):
        # Get the types of the operands
        left_type = get_expression_type(node.left, symbol_table)
        right_type = get_expression_type(node.right, symbol_table)
        
        # Check that the operation is valid for the operand types
        if node.op in ['+', '-', '*', '/']:
            if left_type == "number" and right_type == "number":
                return "number"
            elif node.op == '+' and (left_type == "string" or right_type == "string"):
                return "string"  # String concatenation
            else:
                raise TypeError(f"Invalid operand types for operator '{node.op}'")
        else:
            raise TypeError(f"Unknown operator: {node.op}")
    
    # Similar implementations for other node types
    
    return None
```

## 5.5 Interpreter Implementation

Now, let's implement the interpreter that will execute TinyCL programs:

```python
class TinyCLInterpreter:
    """Interpreter for TinyCL programs."""
    def __init__(self):
        self.symbol_table = SymbolTable()
    
    def interpret(self, program):
        """Interpret a TinyCL program."""
        if not isinstance(program, ProgramNode):
            raise TypeError("Expected a ProgramNode")
        
        # Perform semantic analysis
        check_types(program, self.symbol_table)
        
        # Execute the program
        return self.execute_program(program)
    
    def execute_program(self, program):
        """Execute a program."""
        result = None
        for statement in program.statements:
            result = self.execute_statement(statement)
        return result
    
    def execute_statement(self, statement):
        """Execute a statement."""
        if isinstance(statement, LetStatementNode):
            return self.execute_let_statement(statement)
        elif isinstance(statement, AssignStatementNode):
            return self.execute_assign_statement(statement)
        elif isinstance(statement, IfStatementNode):
            return self.execute_if_statement(statement)
        elif isinstance(statement, WhileStatementNode):
            return self.execute_while_statement(statement)
        elif isinstance(statement, PrintStatementNode):
            return self.execute_print_statement(statement)
        elif isinstance(statement, BlockNode):
            return self.execute_block(statement)
        else:
            raise TypeError(f"Unknown statement type: {type(statement)}")
    
    def execute_let_statement(self, statement):
        """Execute a let statement."""
        value = self.evaluate_expression(statement.expression)
        self.symbol_table.define(statement.identifier.name, value)
        return None
    
    def execute_assign_statement(self, statement):
        """Execute an assignment statement."""
        value = self.evaluate_expression(statement.expression)
        self.symbol_table.update(statement.identifier.name, value)
        return None
    
    def execute_if_statement(self, statement):
        """Execute an if statement."""
        condition = self.evaluate_condition(statement.condition)
        if condition:
            return self.execute_statement(statement.then_statement)
        elif statement.else_statement is not None:
            return self.execute_statement(statement.else_statement)
        return None
    
    def execute_while_statement(self, statement):
        """Execute a while statement."""
        result = None
        while self.evaluate_condition(statement.condition):
            result = self.execute_statement(statement.body)
        return result
    
    def execute_print_statement(self, statement):
        """Execute a print statement."""
        value = self.evaluate_expression(statement.expression)
        print(value)
        return None
    
    def execute_block(self, block):
        """Execute a block."""
        result = None
        for statement in block.statements:
            result = self.execute_statement(statement)
        return result
    
    def evaluate_expression(self, expression):
        """Evaluate an expression."""
        if isinstance(expression, NumberNode):
            return expression.value
        elif isinstance(expression, StringNode):
            return expression.value
        elif isinstance(expression, IdentifierNode):
            return self.symbol_table.lookup(expression.name)
        elif isinstance(expression, BinaryOpNode):
            left = self.evaluate_expression(expression.left)
            right = self.evaluate_expression(expression.right)
            
            if expression.op == '+':
                return left + right
            elif expression.op == '-':
                return left - right
            elif expression.op == '*':
                return left * right
            elif expression.op == '/':
                return left / right
            else:
                raise ValueError(f"Unknown operator: {expression.op}")
        else:
            raise TypeError(f"Unknown expression type: {type(expression)}")
    
    def evaluate_condition(self, condition):
        """Evaluate a condition."""
        left = self.evaluate_expression(condition.left)
        right = self.evaluate_expression(condition.right)
        
        if condition.op == '==':
            return left == right
        elif condition.op == '!=':
            return left != right
        elif condition.op == '<':
            return left < right
        elif condition.op == '>':
            return left > right
        elif condition.op == '<=':
            return left <= right
        elif condition.op == '>=':
            return left >= right
        else:
            raise ValueError(f"Unknown comparison operator: {condition.op}")
```

### 5.5.1 Runtime Environment

The `SymbolTable` class provides the runtime environment for TinyCL programs. It keeps track of variables and their values.

### 5.5.2 Expression Evaluation

The `evaluate_expression` method evaluates expressions by recursively evaluating their components and applying the appropriate operations.

### 5.5.3 Statement Execution

The `execute_statement` method executes statements by dispatching to the appropriate method based on the statement type.

## 5.6 Example Programs and Testing

Let's create some example TinyCL programs to test our implementation:

```python
# Example 1: Factorial
factorial_program = """
# Calculate factorial
let n = 5;
let factorial = 1;

while (n > 0) {
    factorial = factorial * n;
    n = n - 1;
}

print("Factorial: " + factorial);
"""

# Example 2: Fibonacci
fibonacci_program = """
# Calculate Fibonacci numbers
let n = 10;
let a = 0;
let b = 1;
let i = 0;

print("Fibonacci sequence:");
print(a);
print(b);

while (i < n - 2) {
    let c = a + b;
    print(c);
    a = b;
    b = c;
    i = i + 1;
}
"""

# Test the TinyCL interpreter
if __name__ == "__main__":
    parser = TinyCLParser()
    interpreter = TinyCLInterpreter()
    
    print("Testing factorial program:")
    try:
        ast = parser.parse(factorial_program)
        interpreter.interpret(ast)
    except Exception as e:
        print(f"Error: {e}")
    
    print("\nTesting Fibonacci program:")
    try:
        ast = parser.parse(fibonacci_program)
        interpreter.interpret(ast)
    except Exception as e:
        print(f"Error: {e}")
```

## Summary

In this chapter, we've built a complete tiny programming language called TinyCL using our PEG parser library. We've:

1. Designed the language features and grammar
2. Implemented the parser to build an AST
3. Added semantic analysis for type checking
4. Created an interpreter to execute TinyCL programs
5. Tested the implementation with example programs

TinyCL demonstrates the power and flexibility of the TinyPEG library for building parsers and interpreters. While it's a simple language, it includes many of the fundamental concepts found in larger programming languages.

In the next chapter, we'll explore advanced topics and extensions to both the TinyPEG library and the TinyCL language.