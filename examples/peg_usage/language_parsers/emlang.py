# src/examples/tiny_language_parser.py

from src.peg.parsers import PEGParser, Rule
from src.peg.core import ParseError, Reference
from src.peg.syntax_tree import GrammarNode, DebugVisitor


class TinyLanguageParser(PEGParser):
    def __init__(self):
        super().__init__()

        # Define grammar for the minimal language
        self.grammar = GrammarNode(
            name="TinyLanguage",
            rules=[
                Rule("Program", Reference("Statement")),
                Rule("Statement", Reference("PrintStatement"), Reference("Assignment")),
                Rule("PrintStatement", Reference('"print"')),
                Rule("Assignment", Reference("Identifier"), Reference("="), Reference("Expression")),
                Rule("Expression", Reference("Number")),
                Rule("Number", Reference("[0-9]+")),
                Rule("Identifier", Reference("[a-zA-Z_][a-zA-Z0-9_]*"))
            ]
        )

    def parse(self, text: str):
        print(f"Parsing tiny language code: {text}")
        # Parse the input
        result = super().parse(text)
        return result


if __name__ == "__main__":
    try:
        code = "x = 10; print(x);"
        parser = TinyLanguageParser()
        syntax_tree = parser.parse(code)

        # Walk the syntax tree with a debug visitor
        debug_visitor = DebugVisitor()
        syntax_tree.accept(debug_visitor)
    except ParseError as e:
        print(f"Error while parsing tiny language code: {e}")
