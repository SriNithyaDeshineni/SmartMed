import pandas as pd
from pathlib import Path

DATA_FOLDER = Path("dataset")
CLEAN_FOLDER = Path("dataset/cleaned")

CLEAN_FOLDER.mkdir(exist_ok=True)


def clean_text_columns(df):
    """Remove extra spaces from text columns."""
    for column in df.select_dtypes(include="object").columns:
        df[column] = df[column].apply(
            lambda x: x.strip() if isinstance(x, str) else x
        )
    return df


files = [
    "medicine.csv",
    "manufacturer.csv",
    "generic.csv",
    "indication.csv",
    "drug class.csv",
    "dosage form.csv"
]


for file in files:

    print("\n" + "=" * 70)
    print(f"Cleaning: {file}")
    print("=" * 70)

    input_path = DATA_FOLDER / file
    output_path = CLEAN_FOLDER / file

    # Read CSV
    df = pd.read_csv(input_path)

    print("Original rows:", len(df))

    # Remove completely duplicate rows
    df = df.drop_duplicates()

    # Clean text spaces
    df = clean_text_columns(df)

    # Save cleaned file
    df.to_csv(output_path, index=False)

    print("Cleaned rows:", len(df))
    print("Saved:", output_path)