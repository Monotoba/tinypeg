#!/usr/bin/env python3
"""
A simplified TinyCL implementation using the TinyPEG library.
"""

import sys
import os

# Add the project root to the Python path (go up 3 levels from examples/peg_usage/language_parsers/)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.peg.core import GrammarNode, Rule, ParserContext
from src.peg.parsers import PEGParser, Literal, Regex, Sequence, Choice, ZeroOrMore, Optional

def main():
    """Test a simplified TinyCL parser."""
    # Create a simple grammar for variable declarations
    grammar = GrammarNode(
        name="SimpleTinyCL",
        rules=[
            # Program
            Rule("Program", ZeroOrMore(
                Choice(
                    # Variable declaration
                    Sequence(
                        Literal("var"),
                        Regex("[a-zA-Z_][a-zA-Z0-9_]*"),  # Identifier
                        Literal("="),
                        Choice(
                            Regex("[0-9]+"),  # Number
                            Sequence(
                                Literal("\""),
                                Regex("[^\"]*"),  # String content
                                Literal("\"")
                            )
                        ),
                        Literal(";")
                    ),
                    # Print statement
                    Sequence(
                        Literal("print"),
                        Literal("("),
                        Regex("[a-zA-Z_][a-zA-Z0-9_]*"),  # Identifier
                        Literal(")"),
                        Literal(";")
                    ),
                    # Comment
                    Sequence(
                        Literal("#"),
                        Regex(".*")  # Comment content
                    )
                )
            ))
        ]
    )

    # Create a parser with the grammar
    parser = PEGParser()
    parser.grammar = grammar

    # Example TinyCL program
    program = """
    # This is a comment
    var x = 42;
    var name = "Alice";
    print(x);
    print(name);
    """

    print("TinyCL Program:")
    print(program)

    try:
        # Parse the program
        print("\nParsing program...")
        print(f"Grammar: {grammar}")
        print(f"Rules: {[rule.name for rule in grammar.rules]}")
        print(f"First rule: {grammar.rules[0].name}")

        # Create a parser context for debugging
        ctx = ParserContext(program)
        ctx._parser = parser

        # Try to parse the first rule directly
        print("Parsing first rule directly...")
        try:
            rule = grammar.rules[0]
            result = parser._parse_rule(rule, ctx)
            print(f"Direct parse result: {result}")
        except Exception as e:
            print(f"Error parsing first rule: {e}")

        # Now try the full parser
        print("Parsing with full parser...")
        result = parser.parse(program)
        print("Program parsed successfully!")

        # Print the parse result
        print("\nParse Result:")
        for item in result:
            if isinstance(item, list):
                if item[0] == "var":
                    var_name = item[1]
                    var_value = item[3]
                    if isinstance(var_value, list):
                        # String value
                        var_value = var_value[1]
                    print(f"Variable: {var_name} = {var_value}")
                elif item[0] == "print":
                    var_name = item[2]
                    print(f"Print: {var_name}")
                elif item[0] == "#":
                    comment = item[1].strip()
                    print(f"Comment: {comment}")

        return 0
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
