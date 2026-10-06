from pathlib import Path

import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "ml"
    / "preprocessing"
    / "output"
    / "ml_training_data.csv"
)

MODEL_DIR = PROJECT_ROOT / "ml" / "model"


def main():
    print("Loading training dataset...")

    df = pd.read_csv(INPUT_FILE)

    print(f"Total rows: {len(df):,}")
    print(f"Total classes: {df['drug_class'].nunique()}")

    # Features
    feature_columns = [
        "generic",
        "dosage form",
        "type",
        "strength",
    ]

    target_column = "drug_class"

    data = df[feature_columns + [target_column]].copy()

    # Handle missing feature values
    for column in feature_columns:
        data[column] = data[column].fillna("Unknown").astype(str)

    data[target_column] = data[target_column].astype(str)

    X = data[feature_columns]
    y = data[target_column]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    print("\n" + "=" * 60)
    print("TRAINING MODEL")
    print("=" * 60)

    print(f"Training samples: {len(X_train):,}")
    print(f"Testing samples:  {len(X_test):,}")

    # Feature engineering
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "generic_text",
                TfidfVectorizer(
                    lowercase=True,
                    ngram_range=(1, 2),
                    min_df=2,
                    max_features=10000,
                ),
                "generic",
            ),
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                ["dosage form", "type"],
            ),
            (
                "strength_text",
                TfidfVectorizer(
                    lowercase=True,
                    ngram_range=(1, 2),
                    min_df=2,
                ),
                "strength",
            ),
        ]
    )

    # Classification model
    classifier = LogisticRegression(
        max_iter=1000,
        random_state=42,
    )

    # Complete ML pipeline
    model = Pipeline(
        steps=[
            ("preprocessing", preprocessor),
            ("classifier", classifier),
        ]
    )

    print("\nTraining...")
    model.fit(X_train, y_train)

    print("Training completed.")

    # Predictions
    print("\nGenerating predictions...")
    y_pred = model.predict(X_test)

    # Evaluation
    accuracy = accuracy_score(y_test, y_pred)

    print("\n" + "=" * 60)
    print("MODEL EVALUATION")
    print("=" * 60)

    print(f"\nAccuracy: {accuracy:.4f}")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            y_pred,
            zero_division=0,
        )
    )

    # Save model
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    model_file = MODEL_DIR / "drug_class_classifier.joblib"

    import joblib

    joblib.dump(model, model_file)

    print("=" * 60)
    print("MODEL SAVED")
    print("=" * 60)
    print(f"File: {model_file}")


if __name__ == "__main__":
    main()