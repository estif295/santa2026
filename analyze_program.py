
import csv
import json

with open("sample_submission.csv", encoding="utf-8-sig") as f:
    row = next(csv.DictReader(f))

program = json.loads(row["program"])

print("Puzzle:", row["id"])
print("Total instructions:", len(program))

print("\nInstruction counts:")

counts = {}

for instruction in program:
    operation = instruction[0]
    counts[operation] = counts.get(operation, 0) + 1

for operation, count in counts.items():
    print(operation, ":", count)

print("\nLast 10 instructions:")

for i, instruction in enumerate(program[-10:]):
    print(len(program) - 10 + i, instruction)
