# TinyCL - Tiny C-Like Language

TinyCL is a simple programming language implemented using the TinyPEG library. It's meant to be used as a PEG parsing example for teaching PEG parser development and use.

## Features

- Variables and assignments
- Arithmetic operations
- Control structures (if statements and while loops)
- Print statements for output
- Comments

## Implementation

- **parser.py**: The TinyCL parser implementation using the TinyPEG library.
- **docs/grammar.md**: The grammar specification for the TinyCL language.

## Current Status

The original TinyCL implementation has some issues that are being addressed. For working implementations of TinyCL, see the following examples:

- **Standalone TinyCL** (`examples/peg_usage/language_parsers/standalone_tinycl.py`): A complete implementation that doesn't depend on the TinyPEG library.
- **Minimal TinyCL** (`examples/peg_usage/language_parsers/minimal_tinycl.py`): A minimal implementation using the fixed PEG parser.

## Usage

For examples of how to use TinyCL, see the `examples` directory at the project root.
