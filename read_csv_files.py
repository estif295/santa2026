
import csv
from pathlib import Path

files = list(Path(".").rglob("*.csv"))

print("CSV FILES FOUND:", len(files))

for file in files:
    print("\n" + "=" * 50)
    print("FILE:", file.name)

    with open(file, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        print("COLUMNS:", reader.fieldnames)

        for i, row in enumerate(reader):
            if i == 2:
                break

            print("\nROW", i + 1)

            for key, value in row.items():
                print(key, ":", str(value)[:200])
