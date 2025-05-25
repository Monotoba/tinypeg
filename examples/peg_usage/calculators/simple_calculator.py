#!/usr/bin/env python3
"""
Simple calculator example using the TinyPEG library.
Supports only addition and subtraction.
"""

from calculator_base import SimpleCalculator

def main():
    """Test the simple calculator."""
    calculator = SimpleCalculator()

    # Test expressions for simple arithmetic
    expressions = [
        "3",
        "42", 
        "3+5",
        "3 + 5",
        "10 - 4",
        "3 + 5 - 2",
        "100 + 200 - 50"
    ]

    print("=== Simple Calculator (Addition/Subtraction Only) ===")
    calculator.test_expressions(expressions)

if __name__ == "__main__":
    main()
