import csv
import json

with open("puzzles.csv", encoding="utf-8-sig") as f:
    puzzles = list(csv.DictReader(f))

puzzle = next(p for p in puzzles if p["id"] == "scored_0001")

starting = json.loads(puzzle["starting_values"])
targets = json.loads(puzzle["targets"])

print("STARTING VALUES:", starting)
print("TARGET COUNT:", len(targets))

print("\nTARGETS CREATED USING STARTING VALUES")
print("=" * 70)

for target in targets:
    for value in starting:
        operations = [
            ("+", value + target),
            ("-", value - target),
            ("*", value * target),
        ]

        if target != 0 and value % target == 0:
            operations.append(("/", value // target))

        if value != 0 and target % value == 0:
            operations.append(("/", target // value))

        for op, result in operations:
            if result in targets:
                print(f"{value} {op} {target} = {result}")