
import pandas as pd
import json

puzzles = pd.read_csv("practice_puzzles.csv")
sample = pd.read_csv("sample_submission.csv")

print("BASELINE ANALYSIS")
print("=" * 50)

for _, row in sample.head(5).iterrows():
    program = json.loads(row["program"])

    counts = {}
    for instruction in program:
        op = instruction[0]
        counts[op] = counts.get(op, 0) + 1

    print("\nPuzzle:", row["id"])
    print("Total instructions:", len(program))
    print("Operations:", counts)

print("\nPRACTICE PUZZLE ANALYSIS")
print("=" * 50)

for _, row in puzzles.head(10).iterrows():
    starting = json.loads(row["starting_values"])
    targets = json.loads(row["targets"])

    print("\nID:", row["id"])
    print("Starting values:", starting)
    print("Number of targets:", len(targets))
    print("Lower bound:", row["lower_bound"])
    print("Family:", row["family"])
