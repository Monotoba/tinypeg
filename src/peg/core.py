# src/peg/core.py

class ParseError(Exception):
    """Custom error for parsing issues."""
    pass

class ParserContext:
    """Context class to hold the parsing state."""

    def __init__(self, text):
        self.text = text
        self.pos = 0

    def eof(self):
        return self.pos >= len(self.text)

    def peek(self):
        return self.text[self.pos] if not self.eof() else None

    def consume(self):
        """Advance the position by one character."""
        char = self.peek()
        self.pos += 1
        return char


class Expression:
    """Base class for expressions."""
    def parse(self, ctx):
        raise NotImplementedError("Subclasses should implement this method.")


class Reference(Expression):
    """Reference to another rule or pattern in the grammar."""
    
    def __init__(self, name):
        """
        Initialize a reference to another rule or pattern.
        
        Args:
            name: The name of the rule or pattern being referenced
        """
        self.name = name
        
    def parse(self, ctx):
        # This will be implemented by the grammar system
        # that resolves references to actual rules
        raise NotImplementedError("Reference parsing is handled by the grammar system")


if __name__ == "__main__":
    # Main guard for testing core functionality.
    try:
        print("Testing core.py functionality...")
        ctx = ParserContext("test input")
        print(f"Initial position: {ctx.pos}, EOF: {ctx.eof()}")
        ctx.consume()
        print(f"Position after consume: {ctx.pos}, Peek: {ctx.peek()}")
    except Exception as e:
        print(f"Error in core.py main guard: {e}")
