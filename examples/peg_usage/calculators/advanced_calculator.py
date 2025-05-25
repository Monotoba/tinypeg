#!/usr/bin/env python3
"""
Advanced calculator example using the TinyPEG library.
Supports all four operations with proper precedence and parentheses.
"""

from calculator_base import AdvancedCalculator

def main():
    """Test the advanced calculator."""
    calculator = AdvancedCalculator()

    # Test expressions with precedence and parentheses
    expressions = [
        "3",
        "42",
        "3+5",
        "3 + 5",
        "10 - 4", 
        "3 * 5",
        "10 / 2",
        "3 + 5 * 2",        # Should be 13 with proper precedence
        "10 - 2 * 3",       # Should be 4 with proper precedence
        "3 * 5 + 2",        # Should be 17
        "10 / 2 - 3",       # Should be 2
        "(3 + 5) * 2",      # Should be 16
        "3 + (5 * 2)",      # Should be 13
        "3 * (5 + 2)",      # Should be 21
        "(3 + 5) * (2 + 1)" # Should be 24
    ]

    print("=== Advanced Calculator (Full Arithmetic with Precedence) ===")
    calculator.test_expressions(expressions)

if __name__ == "__main__":
    main()
