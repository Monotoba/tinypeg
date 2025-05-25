# If Statements in TinyCL
# Demonstrates conditional logic

var x = 15;
var y = 10;

print("x = " + x);
print("y = " + y);
print("");

# Simple if statement
if (x > y) {
    print("x is greater than y");
}

# If-else statement
if (x < y) {
    print("x is less than y");
} else {
    print("x is not less than y");
}

# Nested if statements
if (x > 0) {
    if (y > 0) {
        print("Both x and y are positive");
    } else {
        print("x is positive, y is not");
    }
} else {
    print("x is not positive");
}

# Complex conditions with logical operators
var age = 25;
var hasLicense = true;

if (age >= 18 && hasLicense) {
    print("Can drive");
} else {
    print("Cannot drive");
}

# Multiple conditions
var score = 85;
if (score >= 90) {
    print("Grade: A");
} else {
    if (score >= 80) {
        print("Grade: B");
    } else {
        if (score >= 70) {
            print("Grade: C");
        } else {
            print("Grade: F");
        }
    }
}
