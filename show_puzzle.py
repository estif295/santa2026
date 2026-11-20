
import csv
import json

with open("practice_puzzles.csv", encoding="utf-8-sig") as file:
    puzzles = list(csv.DictReader(file))

puzzle = puzzles[0]

starting_values = json.loads(puzzle["starting_values"])
targets = json.loads(puzzle["targets"])

print("PUZZLE:", puzzle["id"])
print("Starting values:", starting_values)
print("\nTargets:")
for number in targets:
    print(number)

print("\nNumber of targets:", len(targets))
print("Value limit:", puzzle["value_limit"])
print("Registers:", puzzle["registers"])
