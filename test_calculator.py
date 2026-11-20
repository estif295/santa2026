
# Initial registers
registers = [3, 5, 12, 15]

# Perform arithmetic operations
def calculate(operation, a, b):
    if operation == "+":
        return a + b
    elif operation == "-":
        return a - b
    elif operation == "*":
        return a * b
    elif operation == "/":
        if b == 0 or a % b != 0:
            raise ValueError("Division must be exact")
        return a // b

# Example: 3 * 5
result = calculate("*", registers[0], registers[1])

registers.append(result)

print("Registers:", registers)
print("New result:", result)
