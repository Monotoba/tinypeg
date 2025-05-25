# Contributing to TinyPEG

Thank you for your interest in contributing to TinyPEG! This project is a complete PEG parser library with a fully-functional TinyCL (Tiny C-Like Language) programming language implementation.

## 🎯 Project Overview

TinyPEG is an educational and production-ready project that demonstrates:
- Complete PEG (Parsing Expression Grammar) implementation
- Full programming language implementation (TinyCL - Tiny C-Like Language)
- Multi-target code compilation (Python and C)
- Professional-level language design techniques

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- Git

### Setup Development Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/tinypeg.git
   cd tinypeg
   ```

2. **Create virtual environment** (optional but recommended)
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install in development mode**
   ```bash
   pip install -e .
   ```

4. **Run tests to verify setup**
   ```bash
   python examples/tinycl_language/comprehensive_test.py
   python examples/peg_usage/basic/simple_parser.py
   ```

## 📁 Project Structure

```
tinypeg/
├── src/
│   ├── peg/                 # Core PEG parser library
│   └── tinycl/             # TinyCL language implementation
├── examples/
│   ├── peg_usage/          # Examples of using the PEG library
│   └── tinycl_language/    # Programs written in TinyCL
├── docs/                   # Documentation
├── tests/                  # Test suite
└── doc_tools/              # Documentation utilities
```

## 🛠️ How to Contribute

### Types of Contributions Welcome

1. **Bug Reports** - Found an issue? Please report it!
2. **Feature Requests** - Ideas for new features or improvements
3. **Code Contributions** - Bug fixes, new features, optimizations
4. **Documentation** - Improvements to docs, examples, tutorials
5. **Examples** - New TinyCL programs or PEG usage examples

### Contribution Process

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test your changes**
   ```bash
   python examples/tinycl_language/comprehensive_test.py
   ```
5. **Commit with clear messages**
   ```bash
   git commit -m "Add: Brief description of your changes"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request**

### Code Style Guidelines

- **Python Style**: Follow PEP 8
- **Documentation**: Include docstrings for new functions/classes
- **Comments**: Use clear, concise comments
- **Testing**: Add tests for new features

### Areas for Contribution

#### 🔧 Core Library Enhancements
- Performance optimizations
- Additional PEG operators
- Better error messages
- Memory usage improvements

#### 🌟 TinyCL Language Extensions
- For loops: `for (init; condition; update) { ... }`
- Exception handling: `try-catch-finally`
- More data types: floats, dictionaries
- Standard library functions
- Module system

#### 🎯 Compilation Targets
- JavaScript code generation
- WebAssembly compilation
- Bytecode generation
- LLVM IR generation

#### 📚 Documentation & Examples
- More TinyCL example programs
- Advanced PEG usage tutorials
- Video tutorials
- Interactive documentation

#### 🧪 Testing & Quality
- Additional test cases
- Performance benchmarks
- Fuzzing tests
- Integration tests

## 📝 Reporting Issues

When reporting issues, please include:
- Python version
- Operating system
- Clear description of the problem
- Minimal code example that reproduces the issue
- Expected vs actual behavior

## 💡 Feature Requests

For feature requests, please describe:
- The use case or problem you're trying to solve
- Proposed solution or implementation approach
- Any alternatives you've considered
- Examples of how it would be used

## 🎓 Learning Resources

- **PEG Parsing**: [Wikipedia - Parsing Expression Grammar](https://en.wikipedia.org/wiki/Parsing_expression_grammar)
- **Language Implementation**: Check out the `docs/ebook/` directory
- **Examples**: Explore `examples/` for practical usage patterns

## 📄 License

By contributing to TinyPEG, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in the project documentation and release notes.

---

## 👤 Author

**Randall Morgan** - Project creator and maintainer

## 📄 Copyright

Copyright © 2024 Randall Morgan. All rights reserved.

---

**Thank you for contributing to TinyPEG!** 🎉
