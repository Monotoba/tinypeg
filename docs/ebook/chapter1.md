# Chapter 1: Introduction to Parsing Expression Grammars (PEG)

## What is a Parser?

A parser is a software component that takes input data (typically text) and builds a data structure – often some kind of parse tree, abstract syntax tree, or other hierarchical structure – giving a structural representation of the input while checking for correct syntax. Parsers are a fundamental component in compilers, interpreters, and many other language processing tools.

## What is a Parsing Expression Grammar (PEG)?

Parsing Expression Grammar (PEG) is a type of analytic formal grammar, i.e., a formal grammar that describes a formal language in terms of a set of rules for recognizing strings in the language. PEGs are similar to context-free grammars (CFGs), but they have a different interpretation: a PEG specifies a parsing algorithm for the language it defines.

The key difference between PEGs and CFGs is that PEGs use ordered choice instead of unordered choice. This means that when there are multiple parsing options, a PEG will try them in order and take the first one that matches. This eliminates ambiguity in the grammar, making PEGs suitable for top-down parsing.

## Key Features of PEGs

1. **Ordered Choice**: When multiple alternatives are available, they are tried in order, and the first one that matches is used.

2. **Unlimited Lookahead**: PEGs can look ahead in the input stream without consuming any input, which allows for more powerful pattern matching.

3. **No Left Recursion**: PEGs cannot directly express left-recursive rules, but there are techniques to handle this limitation.

4. **Deterministic Parsing**: PEGs always produce a single parse tree for a given input, eliminating ambiguity.

## Basic PEG Operators

PEGs use the following basic operators:

- **Sequence (`e1 e2`)**: Match expression `e1` followed by expression `e2`.
- **Ordered Choice (`e1 / e2`)**: Try to match expression `e1`; if it fails, try to match expression `e2`.
- **Zero-or-More (`e*`)**: Match expression `e` zero or more times.
- **One-or-More (`e+`)**: Match expression `e` one or more times.
- **Optional (`e?`)**: Match expression `e` zero or one time.
- **And-Predicate (`&e`)**: Succeed if expression `e` matches, but do not consume any input.
- **Not-Predicate (`!e`)**: Succeed if expression `e` does not match, and do not consume any input.

## Example PEG Grammar

Here's a simple PEG grammar for arithmetic expressions:

```
Expression <- Term (('+' / '-') Term)*
Term       <- Factor (('*' / '/') Factor)*
Factor     <- Number / '(' Expression ')'
Number     <- [0-9]+
```

This grammar defines an arithmetic expression as a term followed by zero or more additions or subtractions of terms. A term is a factor followed by zero or more multiplications or divisions of factors. A factor is either a number or a parenthesized expression. A number is one or more digits.

## Why Use PEGs?

PEGs offer several advantages over other parsing approaches:

1. **Simplicity**: PEGs are easy to understand and implement.
2. **Power**: PEGs can express a wide range of languages, including some that are not context-free.
3. **Determinism**: PEGs always produce a single parse tree, eliminating ambiguity.
4. **Efficiency**: PEG parsers can be implemented efficiently using techniques like packrat parsing.

## Limitations of PEGs

PEGs also have some limitations:

1. **No Left Recursion**: PEGs cannot directly express left-recursive rules, which can make some grammars more complex.
2. **Ordered Choice**: The ordered choice operator can sometimes lead to unexpected behavior if the grammar is not carefully designed.
3. **Backtracking**: Naive PEG parsers can be inefficient due to backtracking, although techniques like packrat parsing can mitigate this.

## Conclusion

Parsing Expression Grammars (PEGs) are a powerful tool for defining and parsing formal languages. They offer a simple, deterministic approach to parsing that is well-suited for many applications, including programming languages, data formats, and domain-specific languages.

In the next chapter, we'll explore how to implement a PEG parser in Python using the TinyPEG library.