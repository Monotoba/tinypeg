# src/examples/if_statement_parser.py

from src.peg.parsers import PEGParser, Rule
from src.peg.core import ParseError, Reference
from src.peg.syntax_tree import GrammarNode, DebugVisitor


class IfStatementParser(PEGParser):
    def __init__(self):
        super().__init__()

        # Define grammar for the if statement
        self.grammar = GrammarNode(
            name="IfStatement",
            rules=[
                Rule("IfStatement", Reference("If")),
                Rule("If", Reference('"if"')),
                Rule("Statement", Reference('"print"'))
            ]
        )

    def parse(self, text: str):
        print(f"Parsing if statement: {text}")
        # Parse the input
        result = super().parse(text)
        return result


if __name__ == "__main__":
    try:
        if_statement = "if (x > 5) { print(x); }"
        parser = IfStatementParser()
        syntax_tree = parser.parse(if_statement)

        # Walk the syntax tree with a debug visitor
        debug_visitor = DebugVisitor()
        syntax_tree.accept(debug_visitor)
    except ParseError as e:
        print(f"Error while parsing if statement: {e}")
