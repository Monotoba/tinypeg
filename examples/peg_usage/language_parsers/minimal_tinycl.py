#!/usr/bin/env python3
"""
A minimal TinyCL implementation using the TinyPEG library.
"""

import sys
import os

# Add the project root to the Python path (go up 3 levels from examples/peg_usage/language_parsers/)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.peg.core import GrammarNode, Rule, ParseError, ParserContext
from src.peg.parsers import PEGParser, Literal, Regex, Sequence, Choice, ZeroOrMore, Optional

def main():
    """Test a minimal TinyCL parser."""
    # Create a simple grammar for variable declarations
    grammar = GrammarNode(
        name="MinimalTinyCL",
        rules=[
            # Variable declaration
            Rule("VariableDecl", Sequence(
                Literal("var"),
                Regex("[a-zA-Z_][a-zA-Z0-9_]*"),  # Identifier
                Literal("="),
                Regex("[0-9]+"),  # Number
                Literal(";")
            ))
        ]
    )

    # Create a parser with the grammar
    parser = PEGParser()
    parser.grammar = grammar

    # Example TinyCL program
    program = "var x = 42;"

    print("TinyCL Program:")
    print(program)

    try:
        # Parse the program
        print("\nParsing program...")
        result = parser.parse(program)
        print("Program parsed successfully!")
        print(f"Result: {result}")

        # Extract the variable name and value
        var_name = result[1]
        var_value = result[3]

        print(f"\nVariable declaration:")
        print(f"Name: {var_name}")
        print(f"Value: {var_value}")

        return 0
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())