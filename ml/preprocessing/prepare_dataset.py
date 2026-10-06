from pathlib import Path
import pandas as pd


# Locate the project dataset folder
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_DIR = PROJECT_ROOT / "dataset"
OUTPUT_DIR = PROJECT_ROOT / "ml" / "preprocessing" / "output"


def main():
    # Create output folder
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load original datasets
    medicine = pd.read_csv(DATASET_DIR / "medicine.csv")
    generic = pd.read_csv(DATASET_DIR / "generic.csv")

    print("Loading datasets...")
    print(f"Medicine rows: {len(medicine):,}")
    print(f"Generic rows: {len(generic):,}")

    # Keep only the generic columns needed for our ML dataset
    generic_info = generic[
        [
            "generic name",
            "drug class",
            "indication",
            "therapeutic class description",
        ]
    ].copy()

    # Rename columns for easier Python/ML use
    generic_info = generic_info.rename(
        columns={
            "generic name": "generic",
            "drug class": "drug_class",
            "therapeutic class description": "therapeutic_class",
        }
    )

    # Merge medicine information with generic information
    merged = medicine.merge(
        generic_info,
        on="generic",
        how="left",
    )

    # Remove exact duplicate rows, if any
    merged = merged.drop_duplicates()

    # Standardize missing text values
    text_columns = [
        "generic",
        "strength",
        "package container",
        "Package Size",
        "drug_class",
        "indication",
        "therapeutic_class",
    ]

    for column in text_columns:
        if column in merged.columns:
            merged[column] = merged[column].fillna("Unknown").astype(str).str.strip()

    # Save the ML-ready dataset
    output_file = OUTPUT_DIR / "medicine_enriched.csv"
    merged.to_csv(output_file, index=False)

    print("\n" + "=" * 60)
    print("PREPROCESSING COMPLETE")
    print("=" * 60)

    print(f"Output file: {output_file}")
    print(f"Rows: {len(merged):,}")
    print(f"Columns: {len(merged.columns)}")

    print("\nColumns:")
    for column in merged.columns:
        print(f"  - {column}")

    print("\nDrug class coverage:")
    known_classes = (merged["drug_class"] != "Unknown").sum()
    unknown_classes = (merged["drug_class"] == "Unknown").sum()

    print(f"  Known: {known_classes:,}")
    print(f"  Unknown: {unknown_classes:,}")

    print("\nSaved successfully.")


if __name__ == "__main__":
    main()