# Arrays in TinyCL
# Demonstrates array creation, access, and operations

print("=== Array Examples ===");
print("");

# Array creation
var numbers = [1, 2, 3, 4, 5];
var mixed = [10, "hello", true, 'A'];
var empty = [];

print("Array Creation:");
print("numbers[0] = " + numbers[0]);
print("numbers[4] = " + numbers[4]);
print("mixed[1] = " + mixed[1]);
print("mixed[2] = " + mixed[2]);
print("");

# Array processing with loops
print("Processing arrays with loops:");
var i = 0;
var total = 0;
while (i < 5) {
    print("numbers[" + i + "] = " + numbers[i]);
    total = total + numbers[i];
    i = i + 1;
}
print("Total sum = " + total);
print("");

# Arrays with variables
var x = 100;
var y = 200;
var z = 300;
var variables = [x, y, z];

print("Array with variables:");
var j = 0;
while (j < 3) {
    print("variables[" + j + "] = " + variables[j]);
    j = j + 1;
}
print("");

# Nested array access in expressions
var data = [10, 20, 30, 40, 50];
var index = 2;
var value = data[index] * 2;
print("data[" + index + "] * 2 = " + value);

# Array in function
func sum_array(arr) {
    var sum = 0;
    var k = 0;
    while (k < 3) {  # Simplified - assume 3 elements
        sum = sum + arr[k];
        k = k + 1;
    }
    return sum;
}

var test_array = [5, 10, 15];
var array_sum = sum_array(test_array);
print("sum_array([5, 10, 15]) = " + array_sum);
