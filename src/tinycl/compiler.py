#!/usr/bin/env python3
"""
TinyCL compiler implementation.
Compiles TinyCL programs to different target languages.
"""

import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.tinycl.parser import TinyCLParser
from src.tinycl.ast import *

class CodeGenerator:
    """Base class for code generators."""

    def __init__(self):
        self.indent_level = 0
        self.output = []

    def indent(self):
        """Increase indentation level."""
        self.indent_level += 1

    def dedent(self):
        """Decrease indentation level."""
        self.indent_level = max(0, self.indent_level - 1)

    def emit(self, code):
        """Emit a line of code with proper indentation."""
        indent_str = "    " * self.indent_level
        self.output.append(indent_str + code)

    def emit_raw(self, code):
        """Emit a line of code without indentation."""
        self.output.append(code)

    def get_code(self):
        """Get the generated code as a string."""
        return "\n".join(self.output)

    def generate(self, ast):
        """Generate code from an AST."""
        raise NotImplementedError("Subclasses must implement generate method")

class PythonCodeGenerator(CodeGenerator):
    """Code generator for Python target."""

    def __init__(self):
        super().__init__()
        self.variables = set()
        self.functions = set()

    def generate(self, ast):
        """Generate Python code from TinyCL AST."""
        self.output = []
        self.indent_level = 0

        # Add header
        self.emit_raw("#!/usr/bin/env python3")
        self.emit_raw('"""Generated Python code from TinyCL."""')
        self.emit_raw("")

        # Generate the program
        self._generate_program(ast)

        return self.get_code()

    def _generate_program(self, program):
        """Generate code for a program node."""
        if not isinstance(program, ProgramNode):
            raise TypeError("Expected ProgramNode")

        # Generate main function wrapper
        self.emit("def main():")
        self.indent()

        # Initialize variables dictionary for runtime
        self.emit("# Variable storage")
        self.emit("_vars = {}")
        self.emit("")

        # Generate statements
        for statement in program.statements:
            self._generate_statement(statement)

        self.emit("")
        self.emit("return 0")
        self.dedent()
        self.emit("")
        self.emit('if __name__ == "__main__":')
        self.indent()
        self.emit("import sys")
        self.emit("sys.exit(main())")
        self.dedent()

    def _generate_statement(self, stmt):
        """Generate code for a statement."""
        if isinstance(stmt, VariableDeclNode):
            self._generate_var_decl(stmt)
        elif isinstance(stmt, AssignmentNode):
            self._generate_assignment(stmt)
        elif isinstance(stmt, (IfNode, IfStatementNode)):
            self._generate_if(stmt)
        elif isinstance(stmt, (WhileNode, WhileStatementNode)):
            self._generate_while(stmt)
        elif isinstance(stmt, (PrintNode, PrintStatementNode)):
            self._generate_print(stmt)
        elif isinstance(stmt, (ReturnNode, ReturnStatementNode)):
            self._generate_return(stmt)
        elif isinstance(stmt, ConstantDeclNode):
            self._generate_const_decl(stmt)
        elif isinstance(stmt, BlockNode):
            self._generate_block(stmt)
        elif isinstance(stmt, FunctionDeclNode):
            self._generate_function_decl(stmt)
        elif isinstance(stmt, FunctionCallNode):
            self._generate_function_call_stmt(stmt)
        elif isinstance(stmt, CommentNode):
            self._generate_comment(stmt)
        else:
            self.emit(f"# Unknown statement: {type(stmt)}")

    def _generate_var_decl(self, stmt):
        """Generate code for variable declaration."""
        expr_code = self._generate_expression(stmt.value)
        self.emit(f"_vars['{stmt.name}'] = {expr_code}")
        self.variables.add(stmt.name)

    def _generate_assignment(self, stmt):
        """Generate code for assignment."""
        expr_code = self._generate_expression(stmt.value)
        self.emit(f"_vars['{stmt.name}'] = {expr_code}")

    def _generate_if(self, stmt):
        """Generate code for if statement."""
        condition_code = self._generate_expression(stmt.condition)
        self.emit(f"if {condition_code}:")
        self.indent()
        self._generate_statement(stmt.then_block)
        self.dedent()

        if stmt.else_block:
            self.emit("else:")
            self.indent()
            self._generate_statement(stmt.else_block)
            self.dedent()

    def _generate_while(self, stmt):
        """Generate code for while statement."""
        condition_code = self._generate_expression(stmt.condition)
        self.emit(f"while {condition_code}:")
        self.indent()
        self._generate_statement(stmt.body)
        self.dedent()

    def _generate_print(self, stmt):
        """Generate code for print statement."""
        expr_code = self._generate_expression(stmt.expression)
        self.emit(f"print({expr_code})")

    def _generate_return(self, stmt):
        """Generate code for return statement."""
        if stmt.expression:
            expr_code = self._generate_expression(stmt.expression)
            self.emit(f"return {expr_code}")
        else:
            self.emit("return")

    def _generate_block(self, stmt):
        """Generate code for block statement."""
        for statement in stmt.statements:
            self._generate_statement(statement)

    def _generate_function_decl(self, stmt):
        """Generate code for function declaration."""
        # For now, we'll generate functions as nested functions
        params_str = ", ".join(stmt.parameters)
        self.emit(f"def {stmt.name}({params_str}):")
        self.indent()
        self._generate_statement(stmt.body)
        self.dedent()
        self.emit("")
        self.functions.add(stmt.name)

    def _generate_function_call_stmt(self, stmt):
        """Generate code for function call statement."""
        args_code = ", ".join(self._generate_expression(arg) for arg in stmt.arguments)
        self.emit(f"{stmt.name}({args_code})")

    def _generate_comment(self, stmt):
        """Generate code for comment."""
        self.emit(f"# {stmt.text}")

    def _generate_const_decl(self, stmt):
        """Generate code for constant declaration."""
        expr_code = self._generate_expression(stmt.value)
        self.emit(f"_vars['{stmt.name}'] = {expr_code}")
        self.variables.add(stmt.name)

    def _generate_expression(self, expr):
        """Generate code for an expression."""
        if isinstance(expr, NumberNode):
            return str(expr.value)
        elif isinstance(expr, StringNode):
            return f'"{expr.value}"'
        elif isinstance(expr, BooleanNode):
            return str(expr.value)
        elif isinstance(expr, IdentifierNode):
            return f"_vars['{expr.name}']"
        elif isinstance(expr, BinaryOpNode):
            left_code = self._generate_expression(expr.left)
            right_code = self._generate_expression(expr.right)
            # Handle logical operators
            if expr.operator == "&&":
                return f"({left_code} and {right_code})"
            elif expr.operator == "||":
                return f"({left_code} or {right_code})"
            else:
                return f"({left_code} {expr.operator} {right_code})"
        elif isinstance(expr, UnaryOpNode):
            operand_code = self._generate_expression(expr.operand)
            return f"({expr.operator}{operand_code})"
        elif isinstance(expr, FunctionCallExprNode):
            args_code = ", ".join(self._generate_expression(arg) for arg in expr.arguments)
            return f"{expr.name}({args_code})"
        elif isinstance(expr, CharacterNode):
            return f"'{expr.value}'"
        elif isinstance(expr, ArrayAccessNode):
            array_code = self._generate_expression(expr.array)
            index_code = self._generate_expression(expr.index)
            return f"{array_code}[{index_code}]"
        elif isinstance(expr, ArrayLiteralNode):
            elements_code = ", ".join(self._generate_expression(elem) for elem in expr.elements)
            return f"[{elements_code}]"
        else:
            return f"# Unknown expression: {type(expr)}"

class CCodeGenerator(CodeGenerator):
    """Code generator for C target."""

    def __init__(self):
        super().__init__()
        self.variables = set()
        self.functions = set()

    def generate(self, ast):
        """Generate C code from TinyCL AST."""
        self.output = []
        self.indent_level = 0

        # Add header
        self.emit_raw("/* Generated C code from TinyCL */")
        self.emit_raw("#include <stdio.h>")
        self.emit_raw("#include <stdlib.h>")
        self.emit_raw("")

        # Generate the program
        self._generate_program(ast)

        return self.get_code()

    def _generate_program(self, program):
        """Generate code for a program node."""
        if not isinstance(program, ProgramNode):
            raise TypeError("Expected ProgramNode")

        # Generate main function
        self.emit("int main() {")
        self.indent()

        # Generate statements
        for statement in program.statements:
            self._generate_statement(statement)

        self.emit("")
        self.emit("return 0;")
        self.dedent()
        self.emit("}")

    def _generate_statement(self, stmt):
        """Generate code for a statement."""
        if isinstance(stmt, VariableDeclNode):
            self._generate_var_decl(stmt)
        elif isinstance(stmt, (PrintNode, PrintStatementNode)):
            self._generate_print(stmt)
        elif isinstance(stmt, (IfNode, IfStatementNode)):
            self._generate_if(stmt)
        elif isinstance(stmt, ConstantDeclNode):
            self._generate_const_decl(stmt)
        elif isinstance(stmt, FunctionDeclNode):
            self._generate_function_decl(stmt)
        elif isinstance(stmt, (ReturnNode, ReturnStatementNode)):
            self._generate_return(stmt)
        elif isinstance(stmt, CommentNode):
            self._generate_comment(stmt)
        else:
            self.emit(f"/* Unknown statement: {type(stmt)} */")

    def _generate_var_decl(self, stmt):
        """Generate code for variable declaration."""
        # For simplicity, assume all variables are integers
        expr_code = self._generate_expression(stmt.value)
        self.emit(f"int {stmt.name} = {expr_code};")
        self.variables.add(stmt.name)

    def _generate_print(self, stmt):
        """Generate code for print statement."""
        expr_code = self._generate_expression(stmt.expression)
        if isinstance(stmt.expression, StringNode):
            self.emit(f'printf("%s\\n", {expr_code});')
        else:
            self.emit(f'printf("%d\\n", {expr_code});')

    def _generate_comment(self, stmt):
        """Generate code for comment."""
        self.emit(f"/* {stmt.text} */")

    def _generate_if(self, stmt):
        """Generate code for if statement."""
        condition_code = self._generate_expression(stmt.condition)
        self.emit(f"if ({condition_code}) {{")
        self.indent()
        self._generate_block(stmt.then_block)
        self.dedent()
        self.emit("}")

        if stmt.else_block:
            self.emit("else {")
            self.indent()
            self._generate_block(stmt.else_block)
            self.dedent()
            self.emit("}")

    def _generate_block(self, block):
        """Generate code for a block."""
        if hasattr(block, 'statements'):
            for statement in block.statements:
                self._generate_statement(statement)
        else:
            self._generate_statement(block)

    def _generate_expression(self, expr):
        """Generate code for an expression."""
        if isinstance(expr, NumberNode):
            return str(int(expr.value))
        elif isinstance(expr, StringNode):
            return f'"{expr.value}"'
        elif isinstance(expr, IdentifierNode):
            return expr.name
        elif isinstance(expr, BinaryOpNode):
            left_code = self._generate_expression(expr.left)
            right_code = self._generate_expression(expr.right)
            # Handle logical operators
            if expr.operator == "&&":
                return f"({left_code} && {right_code})"
            elif expr.operator == "||":
                return f"({left_code} || {right_code})"
            else:
                return f"({left_code} {expr.operator} {right_code})"
        elif isinstance(expr, FunctionCallExprNode):
            args_code = ", ".join(self._generate_expression(arg) for arg in expr.arguments)
            return f"{expr.name}({args_code})"
        elif isinstance(expr, ArrayLiteralNode):
            # For C, we'll use a simple array initialization (limited support)
            elements_code = ", ".join(self._generate_expression(elem) for elem in expr.elements)
            return f"{{{elements_code}}}"
        elif isinstance(expr, ArrayAccessNode):
            array_code = self._generate_expression(expr.array)
            index_code = self._generate_expression(expr.index)
            return f"{array_code}[{index_code}]"
        else:
            return f"/* Unknown expression: {type(expr)} */"

    def _generate_const_decl(self, stmt):
        """Generate code for constant declaration."""
        expr_code = self._generate_expression(stmt.value)
        self.emit(f"const int {stmt.name} = {expr_code};")
        self.variables.add(stmt.name)

    def _generate_function_decl(self, stmt):
        """Generate code for function declaration."""
        params_str = ", ".join(f"int {param}" for param in stmt.parameters)
        self.emit(f"int {stmt.name}({params_str}) {{")
        self.indent()
        self._generate_block(stmt.body)
        self.dedent()
        self.emit("}")
        self.emit("")
        self.functions.add(stmt.name)

    def _generate_return(self, stmt):
        """Generate code for return statement."""
        if hasattr(stmt, 'expression') and stmt.expression:
            expr_code = self._generate_expression(stmt.expression)
            self.emit(f"return {expr_code};")
        else:
            self.emit("return 0;")

class TinyCLCompiler:
    """Main compiler class for TinyCL."""

    def __init__(self):
        self.parser = TinyCLParser()
        self.generators = {
            'python': PythonCodeGenerator,
            'c': CCodeGenerator,
        }

    def compile(self, source_code, target='python'):
        """Compile TinyCL source code to target language."""
        # Parse the source code
        ast = self.parser.parse(source_code)

        # Get the appropriate code generator
        if target not in self.generators:
            raise ValueError(f"Unsupported target: {target}")

        generator = self.generators[target]()

        # Generate code
        return generator.generate(ast)

    def compile_file(self, input_file, output_file, target='python'):
        """Compile a TinyCL file to target language."""
        with open(input_file, 'r') as f:
            source_code = f.read()

        compiled_code = self.compile(source_code, target)

        with open(output_file, 'w') as f:
            f.write(compiled_code)

        return compiled_code

def main():
    """Test the compiler."""
    compiler = TinyCLCompiler()

    # Test program with comprehensive features
    program = """
    # Comprehensive TinyCL program
    var x = 10;
    var y = 20;
    const PI = 3;

    # Arithmetic with precedence
    var sum = x + y * 2;
    print(sum);

    # Arrays
    var numbers = [1, 2, 3];
    print(numbers[0]);

    # Functions
    func add(a, b) {
        return a + b;
    }

    var result = add(x, y);
    print(result);

    # Control flow
    if (sum > 45) {
        print("Sum is large");
    } else {
        print("Sum is small");
    }

    # Logical operators
    var test = x > 5 && y < 30;
    print(test);
    """

    try:
        print("Compiling to Python...")
        python_code = compiler.compile(program, 'python')
        print("Python code:")
        print(python_code)

        print("\nCompiling to C...")
        c_code = compiler.compile(program, 'c')
        print("C code:")
        print(c_code)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
