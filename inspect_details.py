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

print("PUZZLE:", puzzle["id"])
print("STARTING VALUES:", starting)
print("TARGET COUNT:", len(targets))
print("TARGETS:", targets)
print("VALUE LIMIT:", puzzle["value_limit"])
print("PROGRAM LENGTH:", len(program))

print("\nFIRST 40 INSTRUCTIONS:")
for i, instruction in enumerate(program[:40]):
    print(i, instruction)

print("\nLAST 20 INSTRUCTIONS:")
for i, instruction in enumerate(program[-20:]):
    print(len(program) - 20 + i, instruction)
