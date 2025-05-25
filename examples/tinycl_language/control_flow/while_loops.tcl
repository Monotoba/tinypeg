# While Loops in TinyCL
# Demonstrates iteration and loop control

print("=== While Loop Examples ===");
print("");

# Simple counting loop
print("Counting from 0 to 4:");
var i = 0;
while (i < 5) {
    print("Count: " + i);
    i = i + 1;
}
print("");

# Countdown loop
print("Countdown from 5 to 1:");
var countdown = 5;
while (countdown > 0) {
    print("T-minus " + countdown);
    countdown = countdown - 1;
}
print("Blast off!");
print("");

# Sum calculation
print("Sum of numbers 1 to 10:");
var sum = 0;
var num = 1;
while (num <= 10) {
    sum = sum + num;
    num = num + 1;
}
print("Sum = " + sum);
print("");

# Nested loops
print("Multiplication table (partial):");
var row = 1;
while (row <= 3) {
    var col = 1;
    while (col <= 3) {
        var product = row * col;
        print(row + " x " + col + " = " + product);
        col = col + 1;
    }
    row = row + 1;
}
