from src.peg import PEGParser, Rule, Reference, GrammarNode, Expression, ParserContext, ParseError

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
    
    def parse_assignment_statement(self, ctx):
        """Parse an assignment statement."""
        start_pos = ctx.pos
        
        # Parse identifier
        identifier = self.parse_identifier(ctx)
        if identifier is None:
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
        
        return AssignStatementNode(identifier, expression)
    
    def parse_if_statement(self, ctx):
        """Parse an if statement."""
        start_pos = ctx.pos
        
        # Expect "if"
        if ctx.pos + 2 > len(ctx.text) or ctx.text[ctx.pos:ctx.pos+2] != "if":
            return None
        ctx.pos += 2
        
        self.skip_whitespace(ctx)
        
        # Expect "("
        if ctx.eof() or ctx.peek() != '(':
            ctx.pos = start_pos
            return None
        ctx.consume()
        
        self.skip_whitespace(ctx)
        
        # Parse condition
        condition = self.parse_condition(ctx)
        if condition is None:
            ctx.pos = start_pos
            return None
        
        self.skip_whitespace(ctx)
        
        # Expect ")"
        if ctx.eof() or ctx.peek() != ')':
            ctx.pos = start_pos
            return None
        ctx.consume()
        
        self.skip_whitespace(ctx)
        
        # Parse then statement
        then_statement = self.parse_statement(ctx)
        if then_statement is None:
            ctx.pos = start_pos
            return None
        
        self.skip_whitespace(ctx)
        
        # Check for "else"
        else_statement = None
        if ctx.pos + 4 <= len(ctx.text) and ctx.text[ctx.pos:ctx.pos+4] == "else":
            ctx.pos += 4
            
            self.skip_whitespace(ctx)
            
            # Parse else statement
            else_statement = self.parse_statement(ctx)
            if else_statement is None:
                ctx.pos = start_pos
                return None
        
        return IfStatementNode(condition, then_statement, else_statement)
    
    def parse_while_statement(self, ctx):
        """Parse a while statement."""
        start_pos = ctx.pos
        
        # Expect "while"
        if ctx.pos + 5 > len(ctx.text) or ctx.text[ctx.pos:ctx.pos+5] != "while":
            return None
        ctx.pos += 5
        
        self.skip_whitespace(ctx)
        
        # Expect "("
        if ctx.eof() or ctx.peek() != '(':
            ctx.pos = start_pos
            return None
        ctx.consume()
        
        self.skip_whitespace(ctx)
        
        # Parse condition
        condition = self.parse_condition(ctx)
        if condition is None:
            ctx.pos = start_pos
            return None
        
        self.skip_whitespace(ctx)
        
        # Expect ")"
        if ctx.eof() or ctx.peek() != ')':
            ctx.pos = start_pos
            return None
        ctx.consume()
        
        self.skip_whitespace(ctx)
        
        # Parse body
        body = self.parse_statement(ctx)
        if body is None:
            ctx.pos = start_pos
            return None
        
        return WhileStatementNode(condition, body)
    
    def parse_print_statement(self, ctx):
        """Parse a print statement."""
        start_pos = ctx.pos
        
        # Expect "print"
        if ctx.pos + 5 > len(ctx.text) or ctx.text[ctx.pos:ctx.pos+5] != "print":
            return None
        ctx.pos += 5
        
        self.skip_whitespace(ctx)
        
        # Expect "("
        if ctx.eof() or ctx.peek() != '(':
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
        
        # Expect ")"
        if ctx.eof() or ctx.peek() != ')':
            ctx.pos = start_pos
            return None
        ctx.consume()
        
        self.skip_whitespace(ctx)
        
        # Expect ";"
        if ctx.eof() or ctx.peek() != ';':
            ctx.pos = start_pos
            return None
        ctx.consume()
        
        return PrintStatementNode(expression)
    
    def parse_block(self, ctx):
        """Parse a block."""
        start_pos = ctx.pos
        
        # Expect "{"
        if ctx.eof() or ctx.peek() != '{':
            return None
        ctx.consume()
        
        self.skip_whitespace(ctx)
        
        # Parse statements
        statements = []
        while not ctx.eof() and ctx.peek() != '}':
            statement = self.parse_statement(ctx)
            if statement is None:
                break
            statements.append(statement)
            self.skip_whitespace(ctx)
        
        # Expect "}"
        if ctx.eof() or ctx.peek() != '}':
            ctx.pos = start_pos
            return None
        ctx.consume()
        
        return BlockNode(statements)
    
    def parse_condition(self, ctx):
        """Parse a condition."""
        self.skip_whitespace(ctx)
        
        # Parse left expression
        left = self.parse_expression(ctx)
        if left is None:
            return None
        
        self.skip_whitespace(ctx)
        
        # Parse comparison operator
        op_pos = ctx.pos
        op = None
        if ctx.pos + 2 <= len(ctx.text):
            if ctx.text[ctx.pos:ctx.pos+2] == "==":
                op = "=="
                ctx.pos += 2
            elif ctx.text[ctx.pos:ctx.pos+2] == "!=":
                op = "!="
                ctx.pos += 2
            elif ctx.text[ctx.pos:ctx.pos+2] == "<=":
                op = "<="
                ctx.pos += 2
            elif ctx.text[ctx.pos:ctx.pos+2] == ">=":
                op = ">="
                ctx.pos += 2
        
        if op is None and not ctx.eof():
            if ctx.peek() == '<':
                op = "<"
                ctx.consume()
            elif ctx.peek() == '>':
                op = ">"
                ctx.consume()
        
        if op is None:
            ctx.pos = op_pos
            return None
        
        self.skip_whitespace(ctx)
        
        # Parse right expression
        right = self.parse_expression(ctx)
        if right is None:
            ctx.pos = op_pos
            return None
        
        return ConditionNode(left, op, right)
    
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

# Symbol table for the interpreter
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

# Interpreter for TinyCL
class TinyCLInterpreter:
    """Interpreter for TinyCL programs."""
    def __init__(self):
        self.symbol_table = SymbolTable()
    
    def interpret(self, program):
        """Interpret a TinyCL program."""
        if not isinstance(program, ProgramNode):
            raise TypeError("Expected a ProgramNode")
        
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
            value = self.symbol_table.lookup(expression.name)
            if value is None:
                raise NameError(f"Variable '{expression.name}' not defined")
            return value
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

# Example programs
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