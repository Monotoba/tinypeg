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

        elif isinstance(statement, CommentNode):
            # Comment - do nothing
            pass

        else:
            raise ValueError(f"Unknown statement type: {type(statement)}")

    def _execute_block(self, block):
        """Execute a block of statements."""
        for statement in block.statements:
            self._execute_statement(statement)

    def _evaluate_expression(self, expression):
        """Evaluate an expression."""
        if isinstance(expression, NumberNode):
            return expression.value

        elif isinstance(expression, StringNode):
            return expression.value

        elif isinstance(expression, BooleanNode):
            return expression.value

        elif isinstance(expression, IdentifierNode):
            if expression.name not in self.variables:
                raise ValueError(f"Undefined variable: {expression.name}")
            return self.variables[expression.name]

        elif isinstance(expression, BinaryOpNode):
            left = self._evaluate_expression(expression.left)
            right = self._evaluate_expression(expression.right)

            if expression.operator == "+":
                # Handle string concatenation and numeric addition
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                else:
                    return left + right
            elif expression.operator == "-":
                return left - right
            elif expression.operator == "*":
                return left * right
            elif expression.operator == "/":
                return left / right
            elif expression.operator == "%":
                return left % right
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
            elif expression.operator == "&&":
                return left and right
            elif expression.operator == "||":
                return left or right
            else:
                raise ValueError(f"Unknown operator: {expression.operator}")

        elif isinstance(expression, UnaryOpNode):
            operand = self._evaluate_expression(expression.operand)

            if expression.operator == "-":
                return -operand
            elif expression.operator == "!":
                return not operand
            else:
                raise ValueError(f"Unknown operator: {expression.operator}")

        elif isinstance(expression, (FunctionCallExprNode,)):
            # Function call expression
            return self._call_function(expression.name, expression.arguments)

        elif isinstance(expression, FunctionCallNode):
            # Function call statement as expression
            return self._call_function(expression.name, expression.arguments)

        elif isinstance(expression, ArrayAccessNode):
            # Array access
            array = self._evaluate_expression(expression.array)
            index = self._evaluate_expression(expression.index)
            if isinstance(array, (list, tuple, str)):
                return array[index]
            else:
                raise ValueError(f"Cannot index non-array type: {type(array)}")

        elif isinstance(expression, CharacterNode):
            return expression.value

        elif isinstance(expression, ArrayLiteralNode):
            # Array literal
            return [self._evaluate_expression(elem) for elem in expression.elements]

        else:
            raise ValueError(f"Unknown expression type: {type(expression)}")

    def _execute_function_statement(self, statement):
        """Execute function declaration or call statement."""
        if isinstance(statement, FunctionDeclNode):
            # Store function definition
            self.functions[statement.name] = statement
            return None
        elif isinstance(statement, FunctionCallNode):
            # Execute function call
            return self._call_function(statement.name, statement.arguments)

    def _call_function(self, name, arguments):
        """Call a function with given arguments."""
        if name not in self.functions:
            raise ValueError(f"Undefined function: {name}")

        function = self.functions[name]

        # Evaluate arguments
        arg_values = [self._evaluate_expression(arg) for arg in arguments]

        # Create new scope for function
        old_variables = self.variables.copy()

        # Bind parameters to arguments
        for i, param in enumerate(function.parameters):
            if i < len(arg_values):
                self.variables[param] = arg_values[i]

        # Debug: print current variables
        # print(f"DEBUG: Function {name} parameters: {function.parameters}")
        # print(f"DEBUG: Function {name} arguments: {arg_values}")
        # print(f"DEBUG: Function {name} variables: {self.variables}")

        # Execute function body
        result = None
        try:
            self._execute_block(function.body)
        except ReturnException as e:
            result = e.value
        finally:
            # Restore old scope
            self.variables = old_variables

        return result

class ReturnException(Exception):
    """Exception used to handle return statements."""
    def __init__(self, value):
        self.value = value