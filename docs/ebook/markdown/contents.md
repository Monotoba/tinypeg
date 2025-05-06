# Table of Contents

## [Preface](preface.md)
- The Art and Science of Parsing
- Why Parsing Expression Grammars?
- About This Documentation

## [Chapter 1: Understanding PEG Parsers](chapter01_peg_basics.md)
- 1.1 Introduction to Parsing Expression Grammars
- 1.2 PEG vs. Context-Free Grammars
- 1.3 PEG Operators and Notation
- 1.4 Recursive Descent Parsing
- 1.5 Packrat Parsing and Memoization

## [Chapter 2: TinyPEG Library Overview](chapter02_library_overview.md)
- 2.1 Architecture and Design Philosophy
- 2.2 Core Components
  - 2.2.1 Expression Class
  - 2.2.2 Reference Class
  - 2.2.3 ParserContext Class
  - 2.2.4 ParseError Class
- 2.3 Parser Components
  - 2.3.1 PEGParser Class
  - 2.3.2 Rule Class
- 2.4 Syntax Tree Components
  - 2.4.1 GrammarNode Class
  - 2.4.2 DebugVisitor Class
- 2.5 Testing the Library

## [Chapter 3: Building Your First Parser](chapter03_building_parsers.md)
- 3.1 Setting Up the Environment
- 3.2 Creating a Simple Numeric Expression Parser
- 3.3 Adding Support for Operators
- 3.4 Handling Parentheses and Precedence
- 3.5 Building an Abstract Syntax Tree
- 3.6 Evaluating Expressions

## [Chapter 4: Example Parsers](chapter04_examples.md)
- 4.1 Calculator Parser
  - 4.1.1 Grammar Definition
  - 4.1.2 Implementation
  - 4.1.3 Testing and Usage
- 4.2 If Statement Parser
  - 4.2.1 Grammar Definition
  - 4.2.2 Implementation
  - 4.2.3 Testing and Usage
- 4.3 While Loop Parser
  - 4.3.1 Grammar Definition
  - 4.3.2 Implementation
  - 4.3.3 Testing and Usage
- 4.4 Tiny Language Parser (EmLang)
  - 4.4.1 Grammar Definition
  - 4.4.2 Implementation
  - 4.4.3 Testing and Usage

## [Chapter 5: Creating a Tiny Programming Language](chapter05_tiny_language.md)
- 5.1 Designing the TinyCL Language
  - 5.1.1 Language Features
  - 5.1.2 Grammar Specification
- 5.2 Implementing the Parser
  - 5.2.1 Lexical Elements
  - 5.2.2 Expressions
  - 5.2.3 Statements
  - 5.2.4 Program Structure
- 5.3 Building the Abstract Syntax Tree
  - 5.3.1 AST Node Classes
  - 5.3.2 Tree Construction
- 5.4 Semantic Analysis
  - 5.4.1 Symbol Table
  - 5.4.2 Type Checking
- 5.5 Interpreter Implementation
  - 5.5.1 Runtime Environment
  - 5.5.2 Expression Evaluation
  - 5.5.3 Statement Execution
- 5.6 Example Programs and Testing

## [Appendix A: PEG Grammar Reference](appendix_a_peg_reference.md)
- A.1 PEG Syntax and Semantics
- A.2 Common PEG Patterns
- A.3 Comparison with Regular Expressions

## [Appendix B: Testing Framework](appendix_b_testing.md)
- B.1 Unit Testing Parsers
- B.2 Test Case Design
- B.3 Debugging Techniques

## [Appendix C: TinyCL Language Reference](appendix_c_tinycl_reference.md)
- C.1 Syntax Reference
- C.2 Standard Library
- C.3 Example Programs