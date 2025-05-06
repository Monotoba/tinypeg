# src/examples/expression_parser.py
from src.peg.parsers import PEGParser, Rule
from src.peg.core import ParseError, Reference
from src.peg.syntax_tree import GrammarNode, DebugVisitor


class MathExpressionParser(PEGParser):
    def __init__(self):
        super().__init__()

        # Define grammar for the mathematical expression
        self.grammar = GrammarNode(
            name="Expression",
            rules=[
                Rule("Expression", Reference("Term")),
                Rule("Term", Reference("Factor")),
                Rule("Factor", Reference("Number")),
                Rule("Number", Reference("[0-9]+")),
            ]
        )

    def parse(self, text: str):
        print(f"Parsing expression: {text}")
        # Parse and return the expression's result
        result = super().parse(text)
        return result


if __name__ == "__main__":
    try:
        expression = "3 + 5 * (2 - 8)"
        parser = MathExpressionParser()
        syntax_tree = parser.parse(expression)

        # Visitor for debugging
        debug_visitor = DebugVisitor()
        syntax_tree.accept(debug_visitor)
    except ParseError as e:
        print(f"Error while parsing expression: {e}")
