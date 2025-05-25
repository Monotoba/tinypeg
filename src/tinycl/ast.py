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
        return f"VarDecl({self.name} = {self.value})"

class AssignmentNode(ASTNode):
    """AST node for an assignment statement."""
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return f"Assign({self.name} = {self.value})"

class IfNode(ASTNode):
    """AST node for an if statement."""
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def __str__(self):
        if self.else_block:
            return f"If({self.condition}, then: {self.then_block}, else: {self.else_block})"
        return f"If({self.condition}, then: {self.then_block})"

class WhileNode(ASTNode):
    """AST node for a while statement."""
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __str__(self):
        return f"While({self.condition}, body: {self.body})"

class PrintNode(ASTNode):
    """AST node for a print statement."""
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return f"Print({self.expression})"

class BlockNode(ASTNode):
    """AST node for a block of statements."""
    def __init__(self, statements):
        self.statements = statements

    def __str__(self):
        return f"Block({len(self.statements)} statements)"

class CommentNode(ASTNode):
    """AST node for a comment."""
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return f"Comment({self.text})"

class BinaryOpNode(ASTNode):
    """AST node for a binary operation."""
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        return f"BinaryOp({self.left} {self.operator} {self.right})"

class UnaryOpNode(ASTNode):
    """AST node for a unary operation."""
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __str__(self):
        return f"UnaryOp({self.operator}{self.operand})"

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

class BooleanNode(ASTNode):
    """AST node for a boolean."""
    def __init__(self, value):
        self.value = value == "true"

    def __str__(self):
        return f"Boolean({self.value})"

class IdentifierNode(ASTNode):
    """AST node for an identifier."""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Identifier({self.name})"

class FunctionDeclNode(ASTNode):
    """AST node for a function declaration."""
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters or []
        self.body = body

    def __str__(self):
        params_str = ", ".join(self.parameters)
        return f"FuncDecl({self.name}({params_str}), body: {self.body})"

class FunctionCallNode(ASTNode):
    """AST node for a function call statement."""
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments or []

    def __str__(self):
        args_str = ", ".join(str(arg) for arg in self.arguments)
        return f"FuncCall({self.name}({args_str}))"

class FunctionCallExprNode(ASTNode):
    """AST node for a function call expression."""
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments or []

    def __str__(self):
        args_str = ", ".join(str(arg) for arg in self.arguments)
        return f"FuncCallExpr({self.name}({args_str}))"

class ReturnNode(ASTNode):
    """AST node for a return statement."""
    def __init__(self, expression=None):
        self.expression = expression

    def __str__(self):
        expr_str = f" {self.expression}" if self.expression else ""
        return f"Return({expr_str})"

class ConstantDeclNode(ASTNode):
    """AST node for a constant declaration."""
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return f"ConstDecl({self.name} = {self.value})"

# Aliases for backward compatibility
IfStatementNode = IfNode
WhileStatementNode = WhileNode
PrintStatementNode = PrintNode
ReturnStatementNode = ReturnNode

class CharacterNode(ASTNode):
    """AST node for a character literal."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Char({self.value})"

class ArrayAccessNode(ASTNode):
    """AST node for array access."""
    def __init__(self, array, index):
        self.array = array
        self.index = index

    def __str__(self):
        return f"ArrayAccess({self.array}[{self.index}])"

class ArrayLiteralNode(ASTNode):
    """AST node for array literal."""
    def __init__(self, elements):
        self.elements = elements or []

    def __str__(self):
        return f"Array([{', '.join(str(e) for e in self.elements)}])"

