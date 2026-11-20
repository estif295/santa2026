
import pandas as pd
import json

df = pd.read_csv("sample_submission.csv")

row = df[df["id"] == "scored_0001"].iloc[0]
program = json.loads(row["program"])

print("FIRST 40 INSTRUCTIONS")
print("=" * 50)

for i, instruction in enumerate(program[:40]):
    print(i, instruction)

print("\nLAST 20 INSTRUCTIONS")
print("=" * 50)

for i, instruction in enumerate(program[-20:], start=len(program)-20):
    print(i, instruction)
