
import csv
import json
from collections import Counter

with open("puzzles.csv", encoding="utf-8-sig") as f:
    puzzles = list(csv.DictReader(f))

with open("sample_submission.csv", encoding="utf-8-sig") as f:
    baseline = {
        row["id"]: json.loads(row["program"])
        for row in csv.DictReader(f)
    }


def analyze(puzzle_id):
    puzzle = next(
        p for p in puzzles if p["id"] == puzzle_id
    )

    starting = json.loads(puzzle["starting_values"])
    targets = set(json.loads(puzzle["targets"]))
    program = baseline[puzzle_id]
    limit = int(puzzle["value_limit"])

    registers = [None] * 48

    for i, value in enumerate(starting):
        registers[i] = value

    reached = set(starting)
    first_reached = {}

    operations = Counter()

    for step, instruction in enumerate(program, 1):
        op, i, j, d = instruction

        a = registers[i]
        b = registers[j]

        if a is None or b is None:
            raise ValueError(f"Undefined register at step {step}")

        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        elif op == "/":
            if b == 0 or a % b:
                raise ValueError(f"Invalid division at {step}")
            result = a // b
        else:
            raise ValueError(f"Unknown operator: {op}")

        if result <= 0 or result > limit:
            raise ValueError(f"Invalid result at step {step}")

        registers[d] = result
        reached.add(result)
        operations[op] += 1

        if result in targets and result not in first_reached:
            first_reached[result] = step

    missing = targets - reached

    print("\nPUZZLE:", puzzle_id)
    print("Baseline instructions:", len(program))
    print("Targets:", len(targets))
    print("Reached:", len(targets) - len(missing))
    print("Missing:", len(missing))
    print("Operations:", dict(operations))

    print("\nTARGET GENERATION COSTS")

    previous = 0

    for target in sorted(targets):
        step = first_reached.get(target)

        if step is not None:
            print(
                target,
                "step:", step,
                "cost since previous:", step - previous
            )
            previous = step

    print("\nUNIQUE VALUES:", len(reached))
    print("VALIDATION:", "PASSED" if not missing else "FAILED")


analyze("scored_0001")
