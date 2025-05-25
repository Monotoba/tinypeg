# src/peg/syntax_tree.py

class GrammarNode:
    """Represents a grammar rule in the syntax tree."""

    def __init__(self, name, rules=None):
        self.name = name
        self.rules = rules or []

    def accept(self, visitor):
        """Accept a visitor to walk the tree."""
        # Try the new method name first, then fall back to the old one
        if hasattr(visitor, 'visit_GrammarNode'):
            visitor.visit_GrammarNode(self)
        elif hasattr(visitor, 'visit_grammar'):
            visitor.visit_grammar(self)
        else:
            raise AttributeError(f"Visitor {visitor} has neither visit_GrammarNode nor visit_grammar method")
        
        # Visit each rule
        for rule in self.rules:
            if hasattr(visitor, 'visit_rule'):
                visitor.visit_rule(rule)
    
    def get_rule(self, name):
        """Get a rule by name."""
        for rule in self.rules:
            if rule.name == name:
                return rule
        return None


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
    
    # Alias methods for backward compatibility
    def visit_grammar(self, node):
        """Alias for visit_GrammarNode for backward compatibility."""
        return self.visit_GrammarNode(node)
    
    def visit_rule(self, rule):
        """Visit a rule node."""
        print(f"Rule: {rule.name}")
        print(f"  Expression: {rule.expr}")


if __name__ == "__main__":
    # Main guard for testing syntax tree functionality.
    try:
        print("Testing syntax_tree.py functionality...")
        grammar_node = GrammarNode(name="TestGrammar", rules=["Statement", "Expression"])

        debug_visitor = DebugVisitor()
        grammar_node.accept(debug_visitor)
    except Exception as e:
        print(f"Error in syntax_tree.py main guard: {e}")
