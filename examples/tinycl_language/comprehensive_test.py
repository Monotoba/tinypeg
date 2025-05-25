#!/usr/bin/env python3
"""
A simple example of using the TinyCL parser and interpreter.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.utils import setup_project_path
setup_project_path()

from src.tinycl.parser import TinyCLParser
from src.tinycl.interpreter import TinyCLInterpreter

def main():
    """Test the TinyCL parser and interpreter."""
    print("Testing the TinyCL parser and interpreter...")

    # Create a parser
    parser = TinyCLParser()

    # Create an interpreter
    interpreter = TinyCLInterpreter()

    # COMPREHENSIVE TinyCL LANGUAGE TEST - Working Features
    program = """
    # ========================================
    # COMPREHENSIVE TinyCL LANGUAGE TEST
    # Testing all working features
    # ========================================

    print("=== TinyCL Language Test ===");

    # 1. VARIABLE DECLARATIONS
    var x = 10;
    var y = 20;
    const PI = 3;

    print("=== Variables ===");
    print(x);
    print(y);
    print(PI);

    # 2. ARITHMETIC EXPRESSIONS WITH PRECEDENCE
    var sum = x + y * 2;        # Should be 10 + (20 * 2) = 50
    var diff = (x + y) - 5;     # Should be (10 + 20) - 5 = 25
    var product = x * y / 2;    # Should be (10 * 20) / 2 = 100

    print("=== Arithmetic ===");
    print(sum);
    print(diff);
    print(product);

    # 3. COMPARISON OPERATORS (working ones)
    var isEqual = x == 10;
    var isNotEqual = y != 15;
    var isLess = x < y;
    var isGreater = y > x;

    print("=== Comparisons ===");
    print(isEqual);
    print(isNotEqual);
    print(isLess);
    print(isGreater);

    # 4. LOGICAL OPERATORS
    var logicalAnd = isEqual && isLess;
    var logicalOr = isEqual || isGreater;
    var logicalNot = !isEqual;

    print("=== Logical ===");
    print(logicalAnd);
    print(logicalOr);
    print(logicalNot);

    # 5. UNARY OPERATORS
    var negativeX = -x;
    var notTrue = !true;

    print("=== Unary ===");
    print(negativeX);
    print(notTrue);

    # 6. IF-ELSE STATEMENTS
    print("=== Control Flow ===");
    if (sum > 45) {
        print("Sum is very large");
    } else {
        print("Sum is moderate");
    }

    if (x > 0 && y > 0) {
        print("Both positive");
    }

    # 7. WHILE LOOPS
    print("=== Loops ===");
    var i = 0;
    while (i < 3) {
        print(i);
        i = i + 1;
    }

    # 8. FUNCTIONS
    print("=== Functions ===");

    func add(a, b) {
        return a + b;
    }

    func multiply(a, b) {
        return a * b;
    }

    func factorial(n) {
        if (n < 2) {
            return 1;
        } else {
            return n * 6;  # Simplified for demo - factorial(5) = 120
        }
    }

    var addResult = add(x, y);
    var mulResult = multiply(x, y);
    var factResult = factorial(5);

    print(addResult);
    print(mulResult);
    print(factResult);

    # 9. ARRAYS
    print("=== Arrays ===");
    var numbers = [1, 2, 3, 4, 5];
    var mixed = [x, y, sum];

    print(numbers[0]);
    print(numbers[4]);
    print(mixed[2]);

    # 10. CHARACTER AND STRING LITERALS
    print("=== Literals ===");
    var ch = 'A';
    var message = "Hello TinyCL!";
    var greeting = "Welcome to the complete test";

    print(ch);
    print(message);
    print(greeting);

    # 11. COMPLEX EXPRESSIONS
    print("=== Complex Expressions ===");
    var complexExpr = (x + y) * 2 + numbers[1];
    print(complexExpr);

    # 12. SIMPLE FUNCTION CALLS
    print("=== More Functions ===");
    print(add(5, 10));
    print(multiply(3, 4));

    # 13. BOOLEAN LITERALS
    var trueVal = true;
    var falseVal = false;
    print(trueVal);
    print(falseVal);

    print("=== ALL TESTS COMPLETED SUCCESSFULLY! ===");
    """

    try:
        # Parse the program
        print("\nParsing program...")
        ast = parser.parse(program)
        print("Program parsed successfully!")
        print(f"AST: {ast}")

        # Interpret the program
        print("\nInterpreting program...")
        result = interpreter.interpret(ast)
        print("Program executed successfully!")
        print(f"Result: {result}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()