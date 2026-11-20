
import csv
import json

with open("puzzles.csv", encoding="utf-8-sig") as f:
    puzzles = list(csv.DictReader(f))

with open("sample_submission.csv", encoding="utf-8-sig") as f:
    submissions = {
        row["id"]: json.loads(row["program"])
        for row in csv.DictReader(f)
    }

puzzle = next(p for p in puzzles if p["id"] == "scored_0001")

registers = [None] * 48

starting = json.loads(puzzle["starting_values"])
targets = set(json.loads(puzzle["targets"]))
limit = int(puzzle["value_limit"])

for i, value in enumerate(starting):
    registers[i] = value

program = submissions["scored_0001"]
covered = set(starting)

print("PUZZLE:", puzzle["id"])
print("STARTING:", starting)
print("TARGET COUNT:", len(targets))
print("PROGRAM LENGTH:", len(program))

print("\nTARGET GENERATION DETAILS")
print("-" * 70)

for step, (op, i, j, d) in enumerate(program, 1):

    a = registers[i]
    b = registers[j]

    if op == "+":
        result = a + b
    elif op == "-":
        result = a - b
    elif op == "*":
        result = a * b
    elif op == "/":
        result = a // b
        assert a % b == 0

    assert 0 < result <= limit

    registers[d] = result

    if result in targets and result not in covered:
        covered.add(result)
        print(
            "Step:", step,
            "| Target:", result,
            "| Operation:", op,
            "| Registers:", i, j, d
        )

print("\nFINAL RESULTS")
print("Targets covered:", len(covered.intersection(targets)))
print("Targets missing:", len(targets - covered))
print("Missing values:", sorted(targets - covered))
