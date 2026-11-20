
import csv
import json

with open("puzzles.csv", encoding="utf-8-sig") as f:
    puzzles = list(csv.DictReader(f))

with open("sample_submission.csv", encoding="utf-8-sig") as f:
    submissions = {
        row["id"]: json.loads(row["program"])
        for row in csv.DictReader(f)
    }

puzzle = puzzles[0]
program = submissions[puzzle["id"]]
targets = set(json.loads(puzzle["targets"]))

registers = json.loads(puzzle["starting_values"])
seen = set(registers)
last_target_step = 0
found = set()

print("PUZZLE:", puzzle["id"])
print("STARTING:", registers)
print("TARGET COUNT:", len(targets))
print("\nTARGET GENERATION DETAILS")
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
    else:
        raise ValueError("Unknown operation: " + str(op))

    registers[d] = result
    seen.add(result)

    if result in targets and result not in found:
        found.add(result)
        cost = step - last_target_step
        print(
            f"Target {len(found):02d}: "
            f"{result} | Step: {step} | "
            f"Instructions since previous target: {cost}"
        )
        last_target_step = step

print("\nVALIDATION")
print("Total instructions:", len(program))
print("Targets reached:", len(found))
print("Targets missing:", len(targets - found))
print("All targets reached:", targets.issubset(found))
