#!/usr/bin/env python3
"""
A minimal example using the TinyPEG library.
"""

import sys
import os

# Add the project root to the Python path (go up 3 levels from examples/peg_usage/basic/)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the necessary modules
from src.peg.core import GrammarNode, Rule, ParserContext
from src.peg.parsers import PEGParser, Regex

def main():
    """Test a minimal example."""
    print("Testing a minimal example...")

    # Create a simple grammar for numbers
    grammar = GrammarNode(
        name="Simple",
        rules=[
            Rule("Number", Regex("[0-9]+"))
        ]
    )

    print(f"Created grammar: {grammar}")

    # Create a parser with the grammar
    parser = PEGParser()
    parser.grammar = grammar

    print(f"Created parser: {parser}")

    # Parse a number
    try:
        print("\nParsing '42'...")
        result = parser.parse("42")
        print(f"Parser result: {result}")

        print("\nTest passed!")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())