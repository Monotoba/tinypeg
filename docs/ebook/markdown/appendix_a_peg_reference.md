# Appendix A: PEG Grammar Reference

## A.1 PEG Syntax and Semantics

Parsing Expression Grammars (PEGs) have a specific syntax and semantics that differ from other grammar formalisms like Context-Free Grammars (CFGs). This appendix provides a comprehensive reference for PEG syntax and semantics.

### A.1.1 Basic Syntax

A PEG consists of a set of rules, each with a name and a parsing expression:

```
RuleName ← ParsingExpression
```

In many implementations, including our TinyPEG library, the arrow (`←`) is replaced with an equals sign (`=`) or another symbol.

### A.1.2 Parsing Expressions

PEGs support the following types of parsing expressions:

| Expression | Description | Example |
|------------|-------------|---------|
| `"literal"` | Match a literal string | `"while"` |
| `[a-z]` | Match a character class | `[0-9]` |
| `e1 e2` | Match e1 followed by e2 | `"if" Condition` |
| `e1 / e2` | Try to match e1; if it fails, try e2 | `IfStmt / WhileStmt` |
| `e*` | Match e zero or more times | `Statement*` |
| `e+` | Match e one or more times | `Digit+` |
| `e?` | Match e or nothing | `"else" Block?` |
| `&e` | Succeed if e matches but don't consume input | `&[a-z]` |
| `!e` | Succeed if e doesn't match and don't consume input | `![0-9]` |
| `(e)` | Group expressions | `("+" / "-") Term` |
| `NonTerminal` | Match the rule with this name | `Expression` |
| `.` | Match any character | `.` |

### A.1.3 Semantics

The key semantic difference between PEGs and CFGs is that PEGs are unambiguous due to the ordered choice operator (`/`). When multiple alternatives could match, a PEG parser will always choose the first matching alternative.

For example, in the expression `A / B`, the parser will first try to match `A`. Only if `A` fails will it try to match `B`. This is in contrast to CFGs, where both `A` and `B` would be considered equally valid alternatives.

Another important aspect of PEG semantics is that they use unlimited lookahead. This means that a PEG parser can look ahead in the input as far as necessary to determine whether a rule matches.

## A.2 Common PEG Patterns

Here are some common patterns used in PEGs:

### A.2.1 Whitespace Handling

```
# Skip whitespace between tokens
Spacing ← [ \t\n\r]*

# A token followed by optional whitespace
keyword ← "keyword" Spacing
```

### A.2.2 Identifiers

```
# Match an identifier (letters, digits, underscore)
Identifier ← [a-zA-Z_][a-zA-Z0-9_]* Spacing
```

### A.2.3 Numbers

```
# Match an integer
Integer ← [0-9]+ Spacing

# Match a floating-point number
Float ← [0-9]+ "." [0-9]+ Spacing
```

### A.2.4 Strings

```
# Match a double-quoted string
String ← "\"" (!("\"") .)* "\"" Spacing
```

### A.2.5 Comments

```
# Match a single-line comment
Comment ← "#" (!"\n" .)* "\n"

# Match a multi-line comment
MultiLineComment ← "/*" (!"*/" .)* "*/"
```

### A.2.6 Expressions with Precedence

```
# Expression with precedence levels
Expression ← Term (("+"/"-") Term)*
Term ← Factor (("*"/"/") Factor)*
Factor ← Number / "(" Expression ")"
```

## A.3 Comparison with Regular Expressions

PEGs and regular expressions are both pattern-matching formalisms, but they have different capabilities and use cases:

| Feature | Regular Expressions | PEGs |
|---------|---------------------|------|
| Recursion | No | Yes |
| Context-Sensitivity | Limited | Yes |
| Backtracking | Implementation-dependent | Yes |
| Ambiguity | Possible | No |
| Lookahead | Limited | Unlimited |
| Capture Groups | Yes | Implementation-dependent |
| Performance | Generally faster | Can be slower without memoization |

### A.3.1 When to Use Regular Expressions

Regular expressions are best suited for:
- Simple pattern matching
- Lexical analysis (tokenization)
- Search and replace operations
- Validation of simple formats (e.g., email addresses, phone numbers)

### A.3.2 When to Use PEGs

PEGs are better suited for:
- Parsing structured languages
- Handling nested constructs
- Context-sensitive parsing
- Building parsers for domain-specific languages

### A.3.3 Converting Between Regular Expressions and PEGs

Many regular expressions can be directly translated to PEGs:

| Regular Expression | PEG Equivalent |
|--------------------|----------------|
| `a` | `"a"` |
| `a\|b` | `"a" / "b"` |
| `a*` | `"a"*` |
| `a+` | `"a"+` |
| `a?` | `"a"?` |
| `[a-z]` | `[a-z]` |
| `(ab)` | `("a" "b")` |
| `^a` | `!. "a"` |
| `a$` | `"a" !.` |

However, some regular expression features, like backreferences, don't have direct equivalents in PEGs.

## A.4 PEG Implementation Considerations

When implementing a PEG parser, there are several important considerations:

### A.4.1 Memoization (Packrat Parsing)

Without memoization, a naive PEG parser can have exponential time complexity in the worst case. Packrat parsing, which memoizes the results of parsing functions, ensures linear time complexity at the cost of increased memory usage.

### A.4.2 Left Recursion

PEGs don't naturally support left recursion. For example, the following rule would cause infinite recursion:

```
Expr ← Expr "+" Term / Term
```

There are several approaches to handling left recursion in PEGs:
- Rewriting the grammar to eliminate left recursion
- Using special algorithms to detect and handle left recursion
- Using operator precedence parsing for expressions

### A.4.3 Error Reporting

PEG parsers can struggle with providing good error messages because they try alternatives silently. To improve error reporting, you can:
- Track the furthest position reached during parsing
- Annotate rules with error messages
- Use a separate error recovery mechanism

### A.4.4 Semantic Actions

To build an AST or perform other actions during parsing, you can attach semantic actions to rules. In our TinyPEG library, we do this by having parsing functions return AST nodes.

## A.5 PEG Tools and Libraries

There are many tools and libraries for working with PEGs:

- **PEG.js**: A JavaScript parser generator based on PEGs
- **ANTLR4**: Supports PEG-like syntax with some extensions
- **Parsec**: A parser combinator library for Haskell that can express PEGs
- **Parboiled**: A PEG parser generator for Java and Scala
- **TatSu**: A PEG parser generator for Python
- **Pest**: A PEG parser generator for Rust

Each of these tools has its own syntax and features, but they all implement the core concepts of PEGs.

## Summary

PEGs provide a powerful and flexible formalism for defining parsers. They combine the expressiveness of context-free grammars with the predictability of recursive descent parsing, making them well-suited for many parsing tasks.

In this appendix, we've covered the syntax and semantics of PEGs, common patterns, comparisons with regular expressions, implementation considerations, and available tools. This information should help you effectively use PEGs in your own projects.