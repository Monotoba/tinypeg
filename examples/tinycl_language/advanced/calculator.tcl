# Calculator in TinyCL
# A more complex program demonstrating multiple features

print("=== TinyCL Calculator ===");
print("");

# Calculator functions
func add(a, b) {
    return a + b;
}

func subtract(a, b) {
    return a - b;
}

func multiply(a, b) {
    return a * b;
}

func divide(a, b) {
    return a / b;
}

func power(base, exp) {
    var result = 1;
    var i = 0;
    while (i < exp) {
        result = result * base;
        i = i + 1;
    }
    return result;
}

# Test values
var x = 12;
var y = 4;

print("Calculator Operations:");
print("x = " + x);
print("y = " + y);
print("");

# Basic operations
print("Basic Operations:");
print("add(" + x + ", " + y + ") = " + add(x, y));
print("subtract(" + x + ", " + y + ") = " + subtract(x, y));
print("multiply(" + x + ", " + y + ") = " + multiply(x, y));
print("divide(" + x + ", " + y + ") = " + divide(x, y));
print("");

# Power function
print("Power Operations:");
print("power(2, 3) = " + power(2, 3));
print("power(5, 2) = " + power(5, 2));
print("");

# Complex calculations
var a = 5;
var b = 3;
var c = 2;

var complex1 = add(multiply(a, b), c);  # (5 * 3) + 2 = 17
var complex2 = multiply(add(a, b), c);  # (5 + 3) * 2 = 16

print("Complex Calculations:");
print("(a * b) + c = " + complex1);
print("(a + b) * c = " + complex2);
print("");

# Array of results
var results = [complex1, complex2, power(a, c)];
print("Results array:");
var i = 0;
while (i < 3) {
    print("results[" + i + "] = " + results[i]);
    i = i + 1;
}
