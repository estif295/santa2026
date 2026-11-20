
import csv
import json

with open("puzzles.csv", encoding="utf-8-sig") as f:
    puzzles = list(csv.DictReader(f))

with open("sample_submission.csv", encoding="utf-8-sig") as f:
    submissions = list(csv.DictReader(f))

puzzle = next(p for p in puzzles if p["id"] == "scored_0001")
submission = next(s for s in submissions if s["id"] == "scored_0001")

starting = json.loads(puzzle["starting_values"])
targets = set(json.loads(puzzle["targets"]))
program = json.loads(submission["program"])

registers = [None] * 48

for i, value in enumerate(starting):
    registers[i] = value

print("TARGET CONSTRUCTION ANALYSIS")
print("=" * 65)

for step, (op, a, b, d) in enumerate(program, 1):

    x = registers[a]
    y = registers[b]

    if op == "+":
        result = x + y
    elif op == "-":
        result = x - y
    elif op == "*":
        result = x * y
    else:
        result = x // y

    registers[d] = result

    if result in targets:
        print("\nTARGET FOUND!")
        print("Step:", step)
        print("Target:", result)
        print("Operation:", x, op, y)
        print("Source registers:", a, b)
        print("Destination:", d)
