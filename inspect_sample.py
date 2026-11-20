
import csv
import json

with open("sample_submission.csv", "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    row = next(reader)

print("PUZZLE ID:", row["id"])

program = json.loads(row["program"])

print("TOTAL INSTRUCTIONS:", len(program))
print("\nFIRST 10 INSTRUCTIONS:")

for i, instruction in enumerate(program[:10]):
    print(i, instruction)
