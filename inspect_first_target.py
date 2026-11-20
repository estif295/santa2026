
import csv
import json

with open("puzzles.csv", encoding="utf-8-sig") as f:
    puzzles = list(csv.DictReader(f))

with open("sample_submission.csv", encoding="utf-8-sig") as f:
    submissions = list(csv.DictReader(f))

puzzle = next(p for p in puzzles if p["id"] == "scored_0001")
submission = next(s for s in submissions if s["id"] == "scored_0001")

starting = json.loads(puzzle["starting_values"])
targets = json.loads(puzzle["targets"])
program = json.loads(submission["program"])

registers = [None] * 48

for i, value in enumerate(starting):
    registers[i] = value

print("STARTING VALUES:", starting)
print("FIRST TARGET:", targets[0])
print("VALUE LIMIT:", puzzle["value_limit"])

print("\nINITIAL REGISTERS")
for i, value in enumerate(registers):
    if value is not None:
        print(f"R{i} = {value}")

print("\nFIRST TARGET GENERATION")

for step, (op, a, b, d) in enumerate(program, 1):
    x = registers[a]
    y = registers[b]

    if x is None or y is None:
        continue

    if op == "+":
        result = x + y
    elif op == "-":
        if x <= y:
            continue
        result = x - y
    elif op == "*":
        result = x * y
    elif op == "/":
        if y == 0 or x % y != 0:
            continue
        result = x // y
    else:
        continue

    if result > int(puzzle["value_limit"]):
        continue

    registers[d] = result

    if result == targets[0]:
        print("TARGET FOUND!")
        print("Step:", step)
        print("Operation:", op)
        print("Source registers:", a, b)
        print("Destination:", d)
        print("Result:", result)
        break
