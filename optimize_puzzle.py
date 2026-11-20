
import csv
import json

with open("puzzles.csv", encoding="utf-8-sig") as f:
    puzzles = list(csv.DictReader(f))

with open("sample_submission.csv", encoding="utf-8-sig") as f:
    baseline = {
        row["id"]: json.loads(row["program"])
        for row in csv.DictReader(f)
    }


def optimize(puzzle):
    starting = json.loads(puzzle["starting_values"])
    targets = json.loads(puzzle["targets"])
    limit = int(puzzle["value_limit"])

    values = list(starting)
    instructions = []
    known = {v: i for i, v in enumerate(values)}

    # Try to reuse values already generated.
    for target in targets:
        if target in known:
            continue

        # Search pairs of existing values.
        found = False

        for i, a in enumerate(values):
            for j, b in enumerate(values):
                candidates = [
                    ("+", a + b),
                    ("*", a * b),
                    ("-", a - b),
                ]

                if b != 0 and a % b == 0:
                    candidates.append(("/", a // b))

                for op, result in candidates:
                    if result == target and result <= limit:
                        dest = len(values)

                        if dest >= 48:
                            break

                        instructions.append([op, i, j, dest])
                        values.append(result)
                        known[result] = dest
                        found = True
                        break

                if found:
                    break
            if found:
                break

    return instructions, len(targets) - len(known)


puzzle = puzzles[0]
instructions, missing = optimize(puzzle)

print("PUZZLE:", puzzle["id"])
print("BASELINE:", len(baseline[puzzle["id"]]))
print("OPTIMIZED:", len(instructions))
print("MISSING TARGETS:", missing)
