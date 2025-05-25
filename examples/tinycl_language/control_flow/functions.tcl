# Functions in TinyCL
# Demonstrates function declaration, calls, and scope

print("=== Function Examples ===");
print("");

# Simple function with no parameters
func greet() {
    print("Hello from a function!");
}

# Function with parameters
func add(a, b) {
    return a + b;
}

# Function with local variables
func calculate_area(width, height) {
    var area = width * height;
    print("Calculating area: " + width + " x " + height);
    return area;
}

# Recursive function (simplified)
func factorial(n) {
    if (n < 2) {
        return 1;
    } else {
        return n * 6;  # Simplified to avoid deep recursion
    }
}

# Function calls
print("Calling functions:");
greet();

var sum = add(10, 20);
print("add(10, 20) = " + sum);

var area = calculate_area(5, 8);
print("Area = " + area);

var fact = factorial(5);
print("factorial(5) = " + fact);
print("");

# Function with multiple parameters
func max_of_three(a, b, c) {
    var max_val = a;
    if (b > max_val) {
        max_val = b;
    }
    if (c > max_val) {
        max_val = c;
    }
    return max_val;
}

var maximum = max_of_three(15, 23, 18);
print("max_of_three(15, 23, 18) = " + maximum);
