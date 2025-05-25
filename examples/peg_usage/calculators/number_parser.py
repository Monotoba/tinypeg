#!/usr/bin/env python3
"""
Basic number parser example using the TinyPEG library.
Shows the simplest possible PEG parser.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from src.utils import setup_project_path
setup_project_path()

from src.peg import PEGParser, Rule, Regex, ParseError
from src.peg.syntax_tree import GrammarNode

class NumberParser(PEGParser):
    """Simple parser that only recognizes numbers."""

    def __init__(self):
        super().__init__()
        
        # Define grammar for just numbers
        self.grammar = GrammarNode(
            name="Number",
            rules=[
                Rule("Number", Regex("[0-9]+"))
            ]
        )

    def parse_number(self, text: str):
        """Parse a number and return its integer value."""
        result = self.parse(text)
        return int(result)

def main():
    """Test the number parser."""
    parser = NumberParser()

    # Test numbers
    test_numbers = [
        "42",
        "123",
        "0",
        "999"
    ]

    print("=== Number Parser (Numbers Only) ===")
    for num_str in test_numbers:
        try:
            print(f"\nInput: {num_str}")
            result = parser.parse(num_str)
            print(f"Parsed: {result}")
            
            value = parser.parse_number(num_str)
            print(f"Value: {value}")
        except ParseError as e:
            print(f"Parse Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    # Test invalid inputs
    print("\n=== Testing Invalid Inputs ===")
    invalid_inputs = ["abc", "12abc", "", "3.14"]
    for invalid in invalid_inputs:
        try:
            print(f"\nInput: '{invalid}'")
            result = parser.parse(invalid)
            print(f"Unexpected success: {result}")
        except ParseError as e:
            print(f"Expected Parse Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
