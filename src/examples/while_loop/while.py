# src/examples/while_loop_parser.py

from src.peg.parsers import PEGParser, Rule
from src.peg.core import ParseError, Reference
from src.peg.syntax_tree import GrammarNode, DebugVisitor


class WhileLoopParser(PEGParser):
    def __init__(self):
        super().__init__()

        # Define grammar for the while loop
        self.grammar = GrammarNode(
            name="WhileLoop",
            rules=[
                Rule("WhileLoop", Reference("While")),
                Rule("While", Reference('"while"')),
                Rule("Statement", Reference('"print"'))
            ]
        )

    def parse(self, text: str):
        print(f"Parsing while loop: {text}")
        # Parse the input
        result = super().parse(text)
        return result


if __name__ == "__main__":
    try:
        while_loop = "while (x < 10) { print(x); }"
        parser = WhileLoopParser()
        syntax_tree = parser.parse(while_loop)

        # Walk the syntax tree with a debug visitor
        debug_visitor = DebugVisitor()
        syntax_tree.accept(debug_visitor)
    except ParseError as e:
        print(f"Error while parsing while loop: {e}")
