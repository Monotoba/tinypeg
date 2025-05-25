import unittest
from src.peg.parsers import PEGParser, Rule, Literal, Sequence
from src.peg.core import Expression, ParserContext
from src.peg.syntax_tree import GrammarNode

class MockExpression(Expression):
    def __init__(self, result=True):
        self.result = result
        self.called = False
    
    def parse(self, ctx):
        self.called = True
        return self.result
        
    def __repr__(self):
        return f"MockExpression(result={self.result}, called={self.called})"

class TestRule(unittest.TestCase):
    def test_initialization(self):
        expr = MockExpression()
        rule = Rule("TestRule", expr)
        self.assertEqual(rule.name, "TestRule")
        self.assertEqual(rule.expr, expr)
    
    def test_parse(self):
        expr = MockExpression(True)
        rule = Rule("TestRule", expr)
        ctx = ParserContext("test")
        result = rule.parse(ctx)
        self.assertTrue(expr.called)
        self.assertTrue(result)
    
    def test_parse_with_multiple_expressions(self):
        expr1 = MockExpression(True)
        expr2 = MockExpression(True)
        # Create a sequence of expressions
        seq = Sequence(expr1, expr2)
        rule = Rule("TestRule", seq)
        ctx = ParserContext("test")
        result = rule.parse(ctx)
        self.assertTrue(expr1.called)
        self.assertTrue(expr2.called)
        self.assertIsNotNone(result)

class TestPEGParser(unittest.TestCase):
    def test_initialization(self):
        parser = PEGParser()
        # Basic initialization test
        self.assertIsInstance(parser, PEGParser)
    
    def test_parse(self):
        parser = PEGParser()
        # Set up a simple grammar for testing
        parser.grammar = GrammarNode(
            name="TestGrammar",
            rules=[
                Rule("Start", Literal("test"))
            ]
        )
        result = parser.parse("test")
        # Check that it returns something
        self.assertIsNotNone(result)

if __name__ == "__main__":
    unittest.main()