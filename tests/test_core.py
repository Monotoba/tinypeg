import unittest
from src.peg.core import Expression, Reference, ParserContext, ParseError

class TestParserContext(unittest.TestCase):
    def test_initialization(self):
        ctx = ParserContext("test")
        self.assertEqual(ctx.text, "test")
        self.assertEqual(ctx.pos, 0)
    
    def test_eof(self):
        ctx = ParserContext("")
        self.assertTrue(ctx.eof())
        
        ctx = ParserContext("a")
        self.assertFalse(ctx.eof())
        ctx.pos = 1
        self.assertTrue(ctx.eof())
    
    def test_peek(self):
        ctx = ParserContext("abc")
        self.assertEqual(ctx.peek(), "a")
        ctx.pos = 1
        self.assertEqual(ctx.peek(), "b")
        ctx.pos = 3  # Beyond the end
        self.assertIsNone(ctx.peek())
    
    def test_consume(self):
        ctx = ParserContext("abc")
        self.assertEqual(ctx.consume(), "a")
        self.assertEqual(ctx.pos, 1)
        self.assertEqual(ctx.consume(), "b")
        self.assertEqual(ctx.pos, 2)
        self.assertEqual(ctx.consume(), "c")
        self.assertEqual(ctx.pos, 3)
        self.assertIsNone(ctx.consume())  # Beyond the end
        self.assertEqual(ctx.pos, 4)

class TestExpression(unittest.TestCase):
    def test_parse_not_implemented(self):
        expr = Expression()
        ctx = ParserContext("test")
        with self.assertRaises(NotImplementedError):
            expr.parse(ctx)

class TestReference(unittest.TestCase):
    def test_initialization(self):
        ref = Reference("TestRule")
        self.assertEqual(ref.name, "TestRule")
    
    def test_parse_not_implemented(self):
        ref = Reference("TestRule")
        ctx = ParserContext("test")
        with self.assertRaises(NotImplementedError):
            ref.parse(ctx)

class TestParseError(unittest.TestCase):
    def test_error_message(self):
        error = ParseError("Test error message")
        self.assertEqual(str(error), "Test error message")

if __name__ == "__main__":
    unittest.main()