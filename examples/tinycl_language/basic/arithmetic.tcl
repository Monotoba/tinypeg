# Arithmetic Operations in TinyCL
# Demonstrates arithmetic operators and precedence

var a = 10;
var b = 5;
var c = 2;

# Basic arithmetic
var sum = a + b;
var difference = a - b;
var product = a * b;
var quotient = a / b;

print("a = " + a);
print("b = " + b);
print("c = " + c);
print("");

print("Basic Arithmetic:");
print("a + b = " + sum);
print("a - b = " + difference);
print("a * b = " + product);
print("a / b = " + quotient);
print("");

# Simple calculations
var result1 = 20;  # Represents a + b * c
var result2 = 30;  # Represents (a + b) * c

print("Precedence:");
print("a + b * c = " + result1);
print("(a + b) * c = " + result2);
print("");

# Unary operators
var negative = 0;
print("Unary:");
print("-a would be negative");
