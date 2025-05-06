import unittest
from src.peg.syntax_tree import GrammarNode, DebugVisitor
from src.peg.parsers import Rule
from src.peg.core import Expression

class MockRule(Rule):
    def __init__(self, name):
        super().__init__(name, None)

class MockVisitor:
    def __init__(self):
        self.visited_grammars = []
        self.visited_rules = []
    
    def visit_grammar(self, grammar):
        self.visited_grammars.append(grammar)
    
    def visit_rule(self, rule):
        self.visited_rules.append(rule)

class TestGrammarNode(unittest.TestCase):
    def test_initialization(self):
        rules = [MockRule("Rule1"), MockRule("Rule2")]
        grammar = GrammarNode("TestGrammar", rules)
        self.assertEqual(grammar.name, "TestGrammar")
        self.assertEqual(grammar.rules, rules)
    
    def test_accept(self):
        rules = [MockRule("Rule1"), MockRule("Rule2")]
        grammar = GrammarNode("TestGrammar", rules)
        visitor = MockVisitor()
        grammar.accept(visitor)
        self.assertEqual(len(visitor.visited_grammars), 1)
        self.assertEqual(visitor.visited_grammars[0], grammar)
        self.assertEqual(len(visitor.visited_rules), 2)
        self.assertEqual(visitor.visited_rules[0], rules[0])
        self.assertEqual(visitor.visited_rules[1], rules[1])

class TestDebugVisitor(unittest.TestCase):
    def test_visit_grammar(self):
        # This is more of a functional test than a unit test
        # since it just prints to stdout
        visitor = DebugVisitor()
        grammar = GrammarNode("TestGrammar", [])
        visitor.visit_grammar(grammar)
        # No assertion, just make sure it doesn't raise an exception
    
    def test_visit_rule(self):
        visitor = DebugVisitor()
        rule = MockRule("TestRule")
        visitor.visit_rule(rule)
        # No assertion, just make sure it doesn't raise an exception

if __name__ == "__main__":
    unittest.main()