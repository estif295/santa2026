
import csv
import json
from collections import Counter

with open("puzzles.csv", encoding="utf-8-sig") as f:
    puzzles = list(csv.DictReader(f))

with open("sample_submission.csv", encoding="utf-8-sig") as f:
    submissions = list(csv.DictReader(f))

puzzle = next(p for p in puzzles if p["id"] == "scored_0001")
submission = next(s for s in submissions if s["id"] == "scored_0001")

starting = json.loads(puzzle["starting_values"])
targets = json.loads(puzzle["targets"])
program = json.loads(submission["program"])

values = starting.copy()
generated = Counter()
target_set = set(targets)
first_reached = {}

for step, (op, i, j, d) in enumerate(program, 1):
    a, b = values[i], values[j]

    if op == "+":
        result = a + b
    elif op == "-":
        result = a - b
    elif op == "*":
        result = a * b
    else:
        result = a // b

    values.append(None) if d >= len(values) else None

    if d == len(values):
        values.append(result)
    else:
        values[d] = result

    generated[result] += 1

    if result in target_set and result not in first_reached:
        first_reached[result] = step

print("PUZZLE OPTIMIZATION ANALYSIS")
print("=" * 50)

print("Starting values:", starting)
print("Targets:", len(targets))
print("Instructions:", len(program))

print("\nTARGET GENERATION STEPS")

for target in targets:
    print(target, "->", first_reached.get(target, "MISSING"))

print("\nMOST FREQUENT GENERATED VALUES")

for value, count in generated.most_common(20):
    print(value, "generated", count, "times")

print("\nUNIQUE VALUES GENERATED:", len(generated))
