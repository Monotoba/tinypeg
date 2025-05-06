# src/peg/syntax_tree.py

class GrammarNode:
    """Represents a grammar rule in the syntax tree."""

    def __init__(self, name, rules=None):
        self.name = name
        self.rules = rules or []

    def accept(self, visitor):
        """Accept a visitor to walk the tree."""
        visitor.visit_GrammarNode(self)


class DebugVisitor:
    """Visitor for debugging the AST."""

    def __init__(self):
        pass

    def visit(self, node):
        print(f"Visiting node: {node}")

    def visit_GrammarNode(self, node):
        print(f"GrammarNode: {node.name}")
        for rule in node.rules:
            print(f"Rule: {rule}")


if __name__ == "__main__":
    # Main guard for testing syntax tree functionality.
    try:
        print("Testing syntax_tree.py functionality...")
        grammar_node = GrammarNode(name="TestGrammar", rules=["Statement", "Expression"])

        debug_visitor = DebugVisitor()
        grammar_node.accept(debug_visitor)
    except Exception as e:
        print(f"Error in syntax_tree.py main guard: {e}")
