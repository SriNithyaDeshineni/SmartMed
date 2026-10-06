import pandas as pd
from pathlib import Path

DATA_FOLDER = Path("dataset")

files = [
    "medicine.csv",
    "manufacturer.csv",
    "generic.csv",
    "indication.csv",
    "drug class.csv",
    "dosage form.csv"
]

for file in files:
    path = DATA_FOLDER / file

    print("\n" + "=" * 70)
    print(f"FILE: {file}")
    print("=" * 70)

    df = pd.read_csv(path)

    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    print("\nColumn names:")
    for column in df.columns:
        print(" -", column)

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:", df.duplicated().sum())