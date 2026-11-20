
import csv
import json

with open("practice_puzzles.csv", encoding="utf-8-sig") as f:
    puzzles = list(csv.DictReader(f))

print("TOTAL PRACTICE PUZZLES:", len(puzzles))

for puzzle in puzzles[:5]:
    print("\nID:", puzzle["id"])
    print("Starting values:", puzzle["starting_values"])
    print("Targets:", len(json.loads(puzzle["targets"])))
    print("Registers:", puzzle["registers"])
    print("Family:", puzzle["family"])
    print("Difficulty:", puzzle["design_tier"])
    print("Lower bound:", puzzle["lower_bound"])
