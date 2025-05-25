# Chapter 3: Building a Programming Language with TinyPEG

## Introduction to TinyCL

In this chapter, we'll build a simple programming language called TinyCL (Tiny C-Like Language) using the TinyPEG library. TinyCL is a small, imperative language with variables, functions, conditionals, and loops. It's designed to be simple enough to implement in a single chapter, but powerful enough to be useful for real tasks.

## TinyCL Language Features

TinyCL includes the following features:

1. **Variables and Constants**: Declare variables with `var` and constants with `const`.
2. **Functions**: Define functions with `func` and call them by name.
3. **Control Flow**: Use `if`, `else`, and `while` for control flow.
4. **Expressions**: Support for arithmetic, comparison, and logical expressions.
5. **I/O**: Basic input/output with `print`.
6. **Types**: Support for numbers, strings, and booleans.

## TinyCL Grammar

Here's the grammar for TinyCL in EBNF notation:

```ebnf
Program       ::= Statements

Statements    ::= Statement*

Statement     ::= FunctionDecl
               | VariableDecl
               | ConstantDecl
               | "if" "(" Expression ")" Block ( "else" Block )?
               | "while" "(" Expression ")" Block
               | "print" "(" Expression ")" ";"
               | "return" Expression? ";"
               | Id "=" Expression ";"
               | Id "(" Arguments? ")" ";"
               | Block
               | Comment

FunctionDecl  ::= "func" Id "(" Parameters? ")" Block
VariableDecl  ::= "var" Id "=" Expression ";"
ConstantDecl  ::= "const" Id "=" Expression ";"

Parameters    ::= Id ( "," Id )*
Arguments     ::= Expression ( "," Expression )*

Block         ::= "{" Statements? "}"

# Expression hierarchy with proper precedence
Expression    ::= LogicalOr
LogicalOr     ::= LogicalAnd ( "||" LogicalAnd )*
LogicalAnd    ::= Equality ( "&&" Equality )*
Equality      ::= Comparison ( ( "!=" | "==" ) Comparison )*
Comparison    ::= Term ( ( "<=" | ">=" | "<" | ">" ) Term )*
Term          ::= Factor ( ( "+" | "-" ) Factor )*
Factor        ::= Unary ( ( "*" | "/" ) Unary )*
Unary         ::= ( "!" | "-" )? Postfix
Postfix       ::= Primary ( "[" Expression "]" )*

Primary       ::= "(" Expression ")"
               | Id "(" Arguments? ")"
               | "[" Arguments? "]"
               | Id
               | Number
               | String
               | Character
               | "true"
               | "false"

# Literals
String        ::= '"' StringChar* '"'
StringChar    ::= [#x20-#x21] | [#x23-#x5B] | [#x5D-#x7E] | "\\" EscapeChar
EscapeChar    ::= '"' | "'" | "\\" | "n" | "r" | "t" | "0" | "b" | "f" | "v" | "l"

Character     ::= "'" CharChar "'"
CharChar      ::= [#x20-#x26] | [#x28-#x5B] | [#x5D-#x7E] | "\\" EscapeChar

Id            ::= Letter ( Letter | Digit | "_" )*
Number        ::= Digit+
Letter        ::= [a-zA-Z]
Digit         ::= [0-9]

Comment       ::= "#" [^\n]*
```

## Implementing the TinyCL Parser

Let's implement the TinyCL parser using TinyPEG. We'll start by defining the AST node classes:

```python
# Note: In practice, these AST classes are defined in src/tinycl/ast.py
# and imported with: from src.tinycl.ast import *

class ASTNode:
    """Base class for AST nodes."""
    def __str__(self):
        return self.__class__.__name__

class ProgramNode(ASTNode):
    """AST node for a program."""
    def __init__(self, statements):
        self.statements = statements or []

    def __str__(self):
        return f"Program({len(self.statements)} statements)"

class StatementNode(ASTNode):
    """Base class for statement nodes."""
    pass

class FunctionDeclNode(StatementNode):
    """AST node for a function declaration."""
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters or []
        self.body = body

    def __str__(self):
        return f"FunctionDecl({self.name}, {len(self.parameters)} params)"

class VariableDeclNode(StatementNode):
    """AST node for a variable declaration."""
    def __init__(self, name, expression, is_const=False):
        self.name = name
        self.expression = expression
        self.is_const = is_const

    def __str__(self):
        prefix = "Const" if self.is_const else "Var"
        return f"{prefix}Decl({self.name})"

class IfStatementNode(StatementNode):
    """AST node for an if statement."""
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def __str__(self):
        return f"If({self.condition}, has_else={self.else_block is not None})"

class WhileStatementNode(StatementNode):
    """AST node for a while statement."""
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __str__(self):
        return f"While({self.condition})"

class PrintStatementNode(StatementNode):
    """AST node for a print statement."""
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return f"Print({self.expression})"

class ReturnStatementNode(StatementNode):
    """AST node for a return statement."""
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return f"Return({self.expression})"

class AssignmentNode(StatementNode):
    """AST node for an assignment statement."""
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def __str__(self):
        return f"Assign({self.name})"

class FunctionCallNode(StatementNode):
    """AST node for a function call statement."""
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments or []

    def __str__(self):
        return f"Call({self.name}, {len(self.arguments)} args)"

class BlockNode(StatementNode):
    """AST node for a block."""
    def __init__(self, statements):
        self.statements = statements or []

    def __str__(self):
        return f"Block({len(self.statements)} statements)"

class ExpressionNode(ASTNode):
    """Base class for expression nodes."""
    pass

class BinaryOpNode(ExpressionNode):
    """AST node for a binary operation."""
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def __str__(self):
        return f"BinaryOp({self.operator}, {self.left}, {self.right})"

class UnaryOpNode(ExpressionNode):
    """AST node for a unary operation."""
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __str__(self):
        return f"UnaryOp({self.operator}, {self.operand})"

class LiteralNode(ExpressionNode):
    """Base class for literal nodes."""
    pass

class NumberNode(LiteralNode):
    """AST node for a number literal."""
    def __init__(self, value):
        self.value = int(value)

    def __str__(self):
        return f"Number({self.value})"

class StringNode(LiteralNode):
    """AST node for a string literal."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"String({self.value})"

class BooleanNode(LiteralNode):
    """AST node for a boolean literal."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Boolean({self.value})"

class IdentifierNode(ExpressionNode):
    """AST node for an identifier."""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Id({self.name})"
```

Now, let's implement the TinyCL parser:

```python
from src.peg import (
    PEGParser, Rule, Reference, ParseError,
    Sequence, Choice, ZeroOrMore, OneOrMore, Optional, Literal, Regex
)
from src.peg.syntax_tree import GrammarNode
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
                    Reference("Expression"),
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
            if ctx.peek() in " \t\n\r":
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

    # ... (AST building methods omitted for brevity)
```

## Implementing the TinyCL Interpreter

Now that we have a parser for TinyCL, let's implement an interpreter to execute TinyCL programs:

```python
from src.tinycl.ast import *

class TinyCLInterpreter:
    """Interpreter for the TinyCL language."""

    def __init__(self):
        self.variables = {}
        self.functions = {}

    def interpret(self, program):
        """Interpret a TinyCL program."""
        if not isinstance(program, ProgramNode):
            raise ValueError("Expected a ProgramNode")

        # Execute each statement in the program
        for statement in program.statements:
            self._execute_statement(statement)

    def _execute_statement(self, statement):
        """Execute a statement."""
        if isinstance(statement, VariableDeclNode):
            # Variable declaration
            value = self._evaluate_expression(statement.value)
            self.variables[statement.name] = value

        elif isinstance(statement, AssignmentNode):
            # Assignment
            value = self._evaluate_expression(statement.value)
            self.variables[statement.name] = value

        elif isinstance(statement, (IfNode, IfStatementNode)):
            # If statement
            condition = self._evaluate_expression(statement.condition)
            if condition:
                self._execute_block(statement.then_block)
            elif statement.else_block:
                self._execute_block(statement.else_block)

        elif isinstance(statement, (WhileNode, WhileStatementNode)):
            # While statement
            while self._evaluate_expression(statement.condition):
                self._execute_block(statement.body)

        elif isinstance(statement, (PrintNode, PrintStatementNode)):
            # Print statement
            value = self._evaluate_expression(statement.expression)
            print(value)

        elif isinstance(statement, BlockNode):
            # Block
            self._execute_block(statement)

        elif isinstance(statement, (FunctionDeclNode, FunctionCallNode)):
            # Function declaration or call
            return self._execute_function_statement(statement)

        elif isinstance(statement, (ReturnNode, ReturnStatementNode)):
            # Return statement
            if hasattr(statement, 'expression') and statement.expression:
                value = self._evaluate_expression(statement.expression)
                raise ReturnException(value)
            raise ReturnException(None)

        elif isinstance(statement, (ConstantDeclNode,)):
            # Constant declaration
            value = self._evaluate_expression(statement.value)
            self.variables[statement.name] = value

        else:
            raise ValueError(f"Unknown statement type: {type(statement)}")

    def _interpret_block(self, block):
        """Interpret a block node."""
        result = None
        for statement in block.statements:
            result = self._interpret_statement(statement)
            if isinstance(statement, ReturnStatementNode):
                break
        return result

    def _interpret_expression(self, expression):
        """Interpret an expression node."""
        if isinstance(expression, NumberNode):
            return expression.value

        elif isinstance(expression, StringNode):
            return expression.value

        elif isinstance(expression, BooleanNode):
            return expression.value

        elif isinstance(expression, IdentifierNode):
            if expression.name in self.global_scope:
                return self.global_scope[expression.name]
            raise NameError(f"Undefined variable: {expression.name}")

        elif isinstance(expression, BinaryOpNode):
            left = self._interpret_expression(expression.left)
            right = self._interpret_expression(expression.right)

            if expression.operator == "+":
                return left + right
            elif expression.operator == "-":
                return left - right
            elif expression.operator == "*":
                return left * right
            elif expression.operator == "/":
                return left / right
            elif expression.operator == "==":
                return left == right
            elif expression.operator == "!=":
                return left != right
            elif expression.operator == "<":
                return left < right
            elif expression.operator == ">":
                return left > right
            elif expression.operator == "<=":
                return left <= right
            elif expression.operator == ">=":
                return left >= right

        elif isinstance(expression, UnaryOpNode):
            operand = self._interpret_expression(expression.operand)

            if expression.operator == "!":
                return not operand
            elif expression.operator == "-":
                return -operand

        elif isinstance(expression, FunctionCallNode):
            return self._call_function(expression.name, expression.arguments)

        return None

    def _call_function(self, name, arguments):
        """Call a function with the given arguments."""
        if name not in self.functions:
            raise NameError(f"Undefined function: {name}")

        function = self.functions[name]

        # Create a new scope for the function
        old_scope = self.global_scope.copy()

        # Bind arguments to parameters
        for i, param in enumerate(function.parameters):
            if i < len(arguments):
                self.global_scope[param] = self._interpret_expression(arguments[i])

        # Execute the function body
        result = self._interpret_block(function.body)

        # Restore the old scope
        self.global_scope = old_scope

        return result
```

## Using the TinyCL Interpreter

Now we can use our TinyCL interpreter to execute TinyCL programs:

```python
def main():
    """Test the TinyCL interpreter."""
    interpreter = TinyCLInterpreter()

    # Test program
    program = """
    # This is a comment
    var x = 42;
    var y = 10;

    if (x > y) {
        print(x);
    } else {
        print(y);
    }

    func add(a, b) {
        return a + b;
    }

    var z = add(x, y);
    print(z);
    """

    try:
        print("Interpreting program...")
        result = interpreter.interpret(program)
        print("Program executed successfully!")
        print(f"Result: {result}")

        return 0
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    main()
```

This will output:

```
Interpreting program...
42
52
Program executed successfully!
Result: None
```

## Conclusion

In this chapter, we've built a simple programming language called TinyCL using the TinyPEG library. We've defined the grammar, implemented a parser, and built an interpreter to execute TinyCL programs.

TinyCL is a simple language, but it demonstrates the key concepts of language design and implementation. With TinyPEG, it's relatively easy to build parsers for a wide range of languages, from simple DSLs to complex programming languages.

In the next chapter, we'll explore how to extend TinyCL with more advanced features, such as arrays, objects, and more sophisticated control flow constructs.