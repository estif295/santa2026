import csv
import json

with open("puzzles.csv", newline="", encoding="utf-8-sig") as f:
    puzzles = list(csv.DictReader(f))

with open("sample_submission.csv", newline="", encoding="utf-8-sig") as f:
    submissions = list(csv.DictReader(f))

puzzle = next(p for p in puzzles if p["id"] == "scored_0001")
submission = next(s for s in submissions if s["id"] == "scored_0001")

program = json.loads(submission["program"])
targets = json.loads(puzzle["targets"])

registers = [None] * 48
for i, value in enumerate(json.loads(puzzle["initial_values"])):
    registers[i] = value

target = targets[0]

print("FIRST TARGET:", target)
print("INSTRUCTIONS THAT BUILD IT")
print("-" * 65)

for step, (op, i, j, d) in enumerate(program, 1):
    a, b = registers[i], registers[j]

    if op == "+":
        result = a + b
    elif op == "-":
        result = a - b
    elif op == "*":
        result = a * b
    elif op == "/":
        result = a // b

    registers[d] = result

    if step <= 75:
        print(
            f"{step:4} | {op} | "
            f"R{i}={a} | R{j}={b} | "
            f"R{d}={result}"
        )

    if result == target:
        print("\nFIRST TARGET REACHED AT STEP:", step)
        break