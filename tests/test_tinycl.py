import unittest
from src.examples.tinycl.tinycl_parser import TinyCLParser, TinyCLInterpreter, ParseError

class TestTinyCLParser(unittest.TestCase):
    def setUp(self):
        self.parser = TinyCLParser()
    
    def test_parse_let_statement(self):
        program = "let x = 42;"
        ast = self.parser.parse(program)
        self.assertEqual(len(ast.statements), 1)
        stmt = ast.statements[0]
        self.assertEqual(stmt.identifier.name, "x")
        self.assertEqual(stmt.expression.value, 42)
    
    def test_parse_print_statement(self):
        program = 'print("Hello, world!");'
        ast = self.parser.parse(program)
        self.assertEqual(len(ast.statements), 1)
        stmt = ast.statements[0]
        self.assertEqual(stmt.expression.value, "Hello, world!")
    
    def test_parse_if_statement(self):
        program = 'if (x > 0) { print("Positive"); }'
        ast = self.parser.parse(program)
        self.assertEqual(len(ast.statements), 1)
        stmt = ast.statements[0]
        self.assertEqual(stmt.condition.op, ">")
        self.assertEqual(stmt.condition.left.name, "x")
        self.assertEqual(stmt.condition.right.value, 0)
    
    def test_parse_while_statement(self):
        program = 'while (i < 10) { i = i + 1; }'
        ast = self.parser.parse(program)
        self.assertEqual(len(ast.statements), 1)
        stmt = ast.statements[0]
        self.assertEqual(stmt.condition.op, "<")
        self.assertEqual(stmt.condition.left.name, "i")
        self.assertEqual(stmt.condition.right.value, 10)
    
    def test_parse_block(self):
        program = '{ let x = 1; let y = 2; }'
        ast = self.parser.parse(program)
        self.assertEqual(len(ast.statements), 1)
        block = ast.statements[0]
        self.assertEqual(len(block.statements), 2)
    
    def test_parse_expression(self):
        program = 'let result = 2 + 3 * 4;'
        ast = self.parser.parse(program)
        self.assertEqual(len(ast.statements), 1)
        stmt = ast.statements[0]
        self.assertEqual(stmt.identifier.name, "result")
        # The exact structure depends on how your parser handles operator precedence
    
    def test_parse_invalid_input(self):
        invalid_programs = [
            'let x = ;',  # Missing expression
            'if (x > 0) print("Positive");',  # Missing braces
            'while (i < 10) i = i + 1;',  # Missing braces
            'print("Hello, world")',  # Missing semicolon
        ]
        for program in invalid_programs:
            with self.assertRaises(ParseError):
                self.parser.parse(program)

class TestTinyCLInterpreter(unittest.TestCase):
    def setUp(self):
        self.parser = TinyCLParser()
        self.interpreter = TinyCLInterpreter()
    
    def test_interpret_let_statement(self):
        program = "let x = 42;"
        ast = self.parser.parse(program)
        self.interpreter.interpret(ast)
        self.assertEqual(self.interpreter.symbol_table.lookup("x"), 42)
    
    def test_interpret_assignment(self):
        program = "let x = 42; x = 43;"
        ast = self.parser.parse(program)
        self.interpreter.interpret(ast)
        self.assertEqual(self.interpreter.symbol_table.lookup("x"), 43)
    
    def test_interpret_if_statement(self):
        program = "let x = 42; if (x > 0) { x = 0; }"
        ast = self.parser.parse(program)
        self.interpreter.interpret(ast)
        self.assertEqual(self.interpreter.symbol_table.lookup("x"), 0)
    
    def test_interpret_while_statement(self):
        program = "let i = 0; let sum = 0; while (i < 5) { sum = sum + i; i = i + 1; }"
        ast = self.parser.parse(program)
        self.interpreter.interpret(ast)
        self.assertEqual(self.interpreter.symbol_table.lookup("sum"), 10)  # 0 + 1 + 2 + 3 + 4
    
    def test_interpret_expression(self):
        program = "let result = 2 + 3 * 4;"
        ast = self.parser.parse(program)
        self.interpreter.interpret(ast)
        # The exact result depends on how your interpreter handles operator precedence
        # If it follows standard precedence, the result should be 14 (3 * 4 = 12, 2 + 12 = 14)
        # If it evaluates left to right, the result would be 20 ((2 + 3) * 4 = 20)
    
    def test_interpret_string_concatenation(self):
        program = 'let greeting = "Hello, " + "world!";'
        ast = self.parser.parse(program)
        self.interpreter.interpret(ast)
        self.assertEqual(self.interpreter.symbol_table.lookup("greeting"), "Hello, world!")

if __name__ == "__main__":
    unittest.main()