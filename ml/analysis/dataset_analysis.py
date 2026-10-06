from pathlib import Path
import pandas as pd


# Project dataset folder
DATASET_DIR = Path(__file__).resolve().parents[2] / "dataset"


def analyze_csv(file_path):
    """Analyze one CSV file and return a summary."""

    df = pd.read_csv(file_path)

    print("\n" + "=" * 70)
    print(f"FILE: {file_path.name}")
    print("=" * 70)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumns:")
    for column in df.columns:
        print(f"  - {column}")

    print("\nData types:")
    print(df.dtypes.to_string())

    print("\nMissing values:")
    missing = df.isna().sum()
    missing = missing[missing > 0]

    if len(missing) == 0:
        print("  None")
    else:
        for column, count in missing.items():
            percentage = (count / len(df)) * 100
            print(f"  {column}: {count:,} ({percentage:.2f}%)")

    print(f"\nDuplicate rows: {df.duplicated().sum():,}")

    print("\nFirst 3 rows:")
    print(df.head(3).to_string(index=False))


def main():
    csv_files = sorted(DATASET_DIR.glob("*.csv"))

    if not csv_files:
        print(f"No CSV files found in: {DATASET_DIR}")
        return

    print("=" * 70)
    print("SMARTMED DATASET ANALYSIS")
    print("=" * 70)
    print(f"Dataset folder: {DATASET_DIR}")
    print(f"CSV files found: {len(csv_files)}")

    for file_path in csv_files:
        analyze_csv(file_path)

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()