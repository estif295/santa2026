
import csv
import json

with open("puzzles.csv", encoding="utf-8-sig") as f:
    puzzles = list(csv.DictReader(f))

with open("sample_submission.csv", encoding="utf-8-sig") as f:
    submissions = list(csv.DictReader(f))

puzzle = next(p for p in puzzles if p["id"] == "scored_0001")
submission = next(s for s in submissions if s["id"] == "scored_0001")

starting_values = json.loads(puzzle["starting_values"])
targets = set(json.loads(puzzle["targets"]))
program = json.loads(submission["program"])

registers = [None] * 48

for i, value in enumerate(starting_values):
    registers[i] = value

found = set()
first_hits = {}

for step, instruction in enumerate(program, start=1):
    op, a, b, d = instruction

    x = registers[a]
    y = registers[b]

    if x is None or y is None:
        print("ERROR: Undefined register at step", step)
        break

    if op == "+":
        result = x + y
    elif op == "-":
        result = x - y
    elif op == "*":
        result = x * y
    elif op == "/":
        if y == 0 or x % y != 0:
            print("ERROR: Invalid division at step", step)
            break
        result = x // y
    else:
        print("ERROR: Unknown operation", op)
        break

    registers[d] = result

    if result in targets and result not in found:
        found.add(result)
        first_hits[result] = step

print("\nBASELINE TARGET ANALYSIS")
print("=" * 50)
print("Starting values:", starting_values)
print("Total targets:", len(targets))
print("Program instructions:", len(program))
print("Targets reached:", len(found))
print("Targets not reached:", len(targets - found))

print("\nFIRST TARGETS REACHED")
print("-" * 50)

for target, step in sorted(first_hits.items(), key=lambda item: item[1]):
    print("Step:", step, "| Target:", target)

print("\nTARGETS NOT REACHED")
for target in sorted(targets - found):
    print(target)
