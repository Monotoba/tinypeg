# Chapter 4: Example Parsers

In this chapter, we'll explore the example parsers included with the TinyPEG library. These examples demonstrate different aspects of parser implementation and can serve as templates for your own parsers.

## 4.1 Calculator Parser

The calculator parser is a simple example that parses and evaluates arithmetic expressions. It supports basic operations like addition, subtraction, multiplication, and division.

### 4.1.1 Grammar Definition

The grammar for the calculator is defined as follows:

```
Expression ::= Term
Term       ::= Factor
Factor     ::= Number
Number     ::= [0-9]+
```

This is a simplified grammar that only handles numbers. In a more complete calculator, we would add support for operators and parentheses, as we did in the previous chapter.

### 4.1.2 Implementation

Let's look at the implementation of the calculator parser:

```python
# src/examples/calc/calculator.py
from src.peg.parsers import PEGParser, Rule
from src.peg.core import ParseError, Reference
from src.peg.syntax_tree import GrammarNode, DebugVisitor


class MathExpressionParser(PEGParser):
    def __init__(self):
        super().__init__()

        # Define grammar for the mathematical expression
        self.grammar = GrammarNode(
            name="Expression",
            rules=[
                Rule("Expression", Reference("Term")),
                Rule("Term", Reference("Factor")),
                Rule("Factor", Reference("Number")),
                Rule("Number", Reference("[0-9]+")),
            ]
        )

    def parse(self, text: str):
        print(f"Parsing expression: {text}")
        # Parse and return the expression's result
        result = super().parse(text)
        return result


if __name__ == "__main__":
    try:
        expression = "3 + 5 * (2 - 8)"
        parser = MathExpressionParser()
        syntax_tree = parser.parse(expression)

        # Visitor for debugging
        debug_visitor = DebugVisitor()
        syntax_tree.accept(debug_visitor)
    except ParseError as e:
        print(f"Error while parsing expression: {e}")
```

This implementation creates a parser with a simple grammar for mathematical expressions. The `parse` method takes a string input, parses it according to the grammar, and returns the result.

### 4.1.3 Testing and Usage

To test the calculator parser, we can run the script directly:

```bash
python -m src.examples.calc.calculator
```

This will parse the expression "3 + 5 * (2 - 8)" and print the resulting syntax tree.

To use the calculator parser in your own code, you can import and instantiate it:

```python
from src.examples.calc.calculator import MathExpressionParser

parser = MathExpressionParser()
result = parser.parse("42")
print(result)
```

## 4.2 If Statement Parser

The if statement parser demonstrates how to parse a simple if statement in a programming language.

### 4.2.1 Grammar Definition

The grammar for the if statement is defined as follows:

```
IfStatement ::= If
If          ::= "if"
Statement   ::= "print"
```

This is a very simplified grammar that only recognizes the basic structure of an if statement. In a real programming language parser, we would add support for conditions, blocks, and else clauses.

### 4.2.2 Implementation

Let's look at the implementation of the if statement parser:

```python
# src/examples/ifstmt/ifstmt.py
from src.peg.parsers import PEGParser, Rule
from src.peg.core import ParseError, Reference
from src.peg.syntax_tree import GrammarNode, DebugVisitor


class IfStatementParser(PEGParser):
    def __init__(self):
        super().__init__()

        # Define grammar for the if statement
        self.grammar = GrammarNode(
            name="IfStatement",
            rules=[
                Rule("IfStatement", Reference("If")),
                Rule("If", Reference('"if"')),
                Rule("Statement", Reference('"print"'))
            ]
        )

    def parse(self, text: str):
        print(f"Parsing if statement: {text}")
        # Parse the input
        result = super().parse(text)
        return result


if __name__ == "__main__":
    try:
        if_statement = "if (x > 5) { print(x); }"
        parser = IfStatementParser()
        syntax_tree = parser.parse(if_statement)

        # Walk the syntax tree with a debug visitor
        debug_visitor = DebugVisitor()
        syntax_tree.accept(debug_visitor)
    except ParseError as e:
        print(f"Error while parsing if statement: {e}")
```

This implementation creates a parser with a simple grammar for if statements. The `parse` method takes a string input, parses it according to the grammar, and returns the result.

### 4.2.3 Testing and Usage

To test the if statement parser, we can run the script directly:

```bash
python -m src.examples.ifstmt.ifstmt
```

This will parse the if statement "if (x > 5) { print(x); }" and print the resulting syntax tree.

To use the if statement parser in your own code, you can import and instantiate it:

```python
from src.examples.ifstmt.ifstmt import IfStatementParser

parser = IfStatementParser()
result = parser.parse("if (condition) { statement; }")
print(result)
```

## 4.3 While Loop Parser

The while loop parser demonstrates how to parse a simple while loop in a programming language.

### 4.3.1 Grammar Definition

The grammar for the while loop is defined as follows:

```
WhileLoop ::= While
While     ::= "while"
Statement ::= "print"
```

This is a very simplified grammar that only recognizes the basic structure of a while loop. In a real programming language parser, we would add support for conditions, blocks, and break/continue statements.

### 4.3.2 Implementation

Let's look at the implementation of the while loop parser:

```python
# src/examples/while_loop/while.py
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
```

This implementation creates a parser with a simple grammar for while loops. The `parse` method takes a string input, parses it according to the grammar, and returns the result.

### 4.3.3 Testing and Usage

To test the while loop parser, we can run the script directly:

```bash
python -m src.examples.while_loop.while
```

This will parse the while loop "while (x < 10) { print(x); }" and print the resulting syntax tree.

To use the while loop parser in your own code, you can import and instantiate it:

```python
from src.examples.while_loop.while import WhileLoopParser

parser = WhileLoopParser()
result = parser.parse("while (condition) { statement; }")
print(result)
```

## 4.4 Tiny Language Parser (EmLang)

The EmLang parser demonstrates how to parse a simple programming language with variables, assignments, and print statements.

### 4.4.1 Grammar Definition

The grammar for EmLang is defined as follows:

```
Program        ::= Statement
Statement      ::= PrintStatement | Assignment
PrintStatement ::= "print"
Assignment     ::= Identifier "=" Expression
Expression     ::= Number
Number         ::= [0-9]+
Identifier     ::= [a-zA-Z_][a-zA-Z0-9_]*
```

This grammar defines a simple language with two types of statements: print statements and assignments. Expressions are limited to numbers, and identifiers follow standard programming language conventions.

### 4.4.2 Implementation

Let's look at the implementation of the EmLang parser:

```python
# src/examples/emlang/emlang.py
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
```

This implementation creates a parser with a grammar for the EmLang language. The `parse` method takes a string input, parses it according to the grammar, and returns the result.

### 4.4.3 Testing and Usage

To test the EmLang parser, we can run the script directly:

```bash
python -m src.examples.emlang.emlang
```

This will parse the code "x = 10; print(x);" and print the resulting syntax tree.

To use the EmLang parser in your own code, you can import and instantiate it:

```python
from src.examples.emlang.emlang import TinyLanguageParser

parser = TinyLanguageParser()
result = parser.parse("x = 42; print(x);")
print(result)
```

## Enhancing the Examples

These examples are intentionally simplified to demonstrate the basic structure of parsers for different language constructs. In a real-world scenario, you would enhance them in several ways:

1. **Complete Grammar**: Add support for all language features, including operators, control structures, and more complex expressions.

2. **AST Construction**: Build a proper abstract syntax tree (AST) instead of just recognizing the syntax.

3. **Semantic Analysis**: Add checks for semantic correctness, such as type checking and variable declaration.

4. **Interpretation or Code Generation**: Add the ability to execute the parsed code or generate code in another language.

Let's see how we might enhance the EmLang parser to support a more complete language:

```python
# Enhanced EmLang parser
class EnhancedEmLangParser(PEGParser):
    def __init__(self):
        super().__init__()

        # Define grammar for the enhanced language
        self.grammar = GrammarNode(
            name="EnhancedEmLang",
            rules=[
                Rule("Program", Reference("StatementList")),
                Rule("StatementList", Reference("Statement"), Reference("StatementList"), Reference("Statement")),
                Rule("Statement", Reference("PrintStatement"), Reference("Assignment"), Reference("IfStatement"), Reference("WhileStatement")),
                Rule("PrintStatement", Reference('"print"'), Reference("("), Reference("Expression"), Reference(")")),
                Rule("Assignment", Reference("Identifier"), Reference("="), Reference("Expression")),
                Rule("IfStatement", Reference('"if"'), Reference("("), Reference("Condition"), Reference(")"), Reference("Block"), Reference('"else"'), Reference("Block")),
                Rule("WhileStatement", Reference('"while"'), Reference("("), Reference("Condition"), Reference(")"), Reference("Block")),
                Rule("Block", Reference("{"), Reference("StatementList"), Reference("}")),
                Rule("Condition", Reference("Expression"), Reference("ComparisonOp"), Reference("Expression")),
                Rule("ComparisonOp", Reference("=="), Reference("<"), Reference(">"), Reference("<="), Reference(">=")),
                Rule("Expression", Reference("Term"), Reference("+"), Reference("Expression"), Reference("-"), Reference("Expression"), Reference("Term")),
                Rule("Term", Reference("Factor"), Reference("*"), Reference("Term"), Reference("/"), Reference("Term"), Reference("Factor")),
                Rule("Factor", Reference("Number"), Reference("Identifier"), Reference("("), Reference("Expression"), Reference(")")),
                Rule("Number", Reference("[0-9]+")),
                Rule("Identifier", Reference("[a-zA-Z_][a-zA-Z0-9_]*"))
            ]
        )
```

This enhanced grammar supports a much richer language with if statements, while loops, blocks, conditions, and expressions with operators.

## Summary

In this chapter, we've explored the example parsers included with the TinyPEG library:

1. **Calculator Parser**: Parses and evaluates arithmetic expressions
2. **If Statement Parser**: Parses if statements in a programming language
3. **While Loop Parser**: Parses while loops in a programming language
4. **EmLang Parser**: Parses a simple programming language with variables and print statements

These examples demonstrate different aspects of parser implementation and can serve as templates for your own parsers. In the next chapter, we'll build a more complete programming language parser for TinyCL.