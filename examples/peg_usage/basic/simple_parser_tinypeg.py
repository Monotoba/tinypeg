#!/usr/bin/env python3
"""
A simple parser implementation using the TinyPEG library.
"""

import sys
import os
import re

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import directly from the modules
from src.peg.core import GrammarNode, Rule, ParseError, ParserContext
from src.peg.parsers import PEGParser, Literal, Regex

def main():
    """Test the TinyPEG parser implementation."""
    print("Testing the TinyPEG parser...")
    
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
        
        # Create a parser context
        ctx = ParserContext("42")
        ctx._parser = parser
        print("Created parser context")
        
        # Parse the Number rule directly
        rule = grammar.rules[0]
        expr = rule.expr
        print(f"Rule: {rule.name}, Expression type: {type(expr).__name__}")
        
        # Try to parse the expression
        print("Parsing expression directly...")
        result = expr.parse(ctx)
        print(f"Expression result: {result}")
        print(f"Final position: {ctx.pos}")
        
        # Now try the full parser
        print("\nParsing using the full parser...")
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
