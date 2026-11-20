import csv
import json

PUZZLE_ID = "scored_0001"

with open("puzzles.csv", encoding="utf-8-sig") as f:
    puzzles = list(csv.DictReader(f))

with open("sample_submission.csv", encoding="utf-8-sig") as f:
    submissions = list(csv.DictReader(f))

puzzle = next(p for p in puzzles if p["id"] == PUZZLE_ID)
submission = next(s for s in submissions if s["id"] == PUZZLE_ID)

starting = json.loads(puzzle["starting_values"])
targets = set(json.loads(puzzle["targets"]))
program = json.loads(submission["program"])

registers = [None] * 48

for i, value in enumerate(starting):
    registers[i] = value

print("FIRST 80 INSTRUCTIONS")
print("=" * 90)

for step, (op, a, b, d) in enumerate(program, 1):
    x = registers[a]
    y = registers[b]

    if op == "+":
        result = x + y
    elif op == "-":
        result = x - y
    elif op == "*":
        result = x * y
    elif op == "/":
        result = x // y

    registers[d] = result

    if step <= 80:
        target_mark = "  TARGET!" if result in targets else ""
        print(
            f"{step:4} | {op} | R{a}={x} | R{b}={y} "
            f"| R{d}={result} | R4={registers[4]} "
            f"| R5={registers[5]}{target_mark}"
        )