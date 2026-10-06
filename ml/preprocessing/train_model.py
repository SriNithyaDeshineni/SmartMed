from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    ConfusionMatrixDisplay,
)
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
GRAPH_DIR = PROJECT_ROOT / "ml" / "model" / "evaluation"


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

    report = classification_report(
        y_test,
        y_pred,
        output_dict=True,
        zero_division=0,
    )

    macro_precision = report["macro avg"]["precision"]
    macro_recall = report["macro avg"]["recall"]
    macro_f1 = report["macro avg"]["f1-score"]

    print("\n" + "=" * 60)
    print("MODEL EVALUATION")
    print("=" * 60)

    print(f"\nAccuracy: {accuracy:.4f}")
    print(f"Macro Precision: {macro_precision:.4f}")
    print(f"Macro Recall:    {macro_recall:.4f}")
    print(f"Macro F1:        {macro_f1:.4f}")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            y_pred,
            zero_division=0,
        )
    )

    # Create evaluation directory
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------
    # Graph 1: Overall evaluation metrics
    # ---------------------------------------------------------

    metrics = {
        "Accuracy": accuracy,
        "Macro Precision": macro_precision,
        "Macro Recall": macro_recall,
        "Macro F1": macro_f1,
    }

    plt.figure(figsize=(8, 5))

    plt.bar(
        list(metrics.keys()),
        list(metrics.values()),
    )

    plt.ylim(0, 1.0)
    plt.ylabel("Score")
    plt.title("SmartMed Drug-Class Classification Performance")
    plt.xticks(rotation=20)
    plt.tight_layout()

    metrics_file = GRAPH_DIR / "evaluation_metrics.png"
    plt.savefig(metrics_file, dpi=200)
    plt.close()

    print(f"\nSaved graph: {metrics_file}")

    # ---------------------------------------------------------
    # Graph 2: Confusion matrix for the most common classes
    # ---------------------------------------------------------

    class_counts = y_test.value_counts()

    top_classes = class_counts.head(15).index.tolist()

    mask = y_test.isin(top_classes)

    y_test_top = y_test[mask]
    y_pred_top = pd.Series(
        y_pred,
        index=y_test.index,
    )[mask]

    plt.figure(figsize=(12, 10))

    ConfusionMatrixDisplay.from_predictions(
        y_test_top,
        y_pred_top,
        labels=top_classes,
        xticks_rotation=90,
        cmap="Blues",
        colorbar=False,
    )

    plt.title("Confusion Matrix - Top 15 Drug Classes")
    plt.tight_layout()

    confusion_file = GRAPH_DIR / "confusion_matrix_top15.png"
    plt.savefig(confusion_file, dpi=200)
    plt.close()

    print(f"Saved graph: {confusion_file}")

    # ---------------------------------------------------------
    # Save evaluation summary
    # ---------------------------------------------------------

    summary_file = GRAPH_DIR / "evaluation_summary.txt"

    with open(summary_file, "w", encoding="utf-8") as file:
        file.write("SMARTMED ML MODEL EVALUATION\n")
        file.write("=" * 60 + "\n\n")
        file.write(f"Training samples: {len(X_train):,}\n")
        file.write(f"Testing samples: {len(X_test):,}\n")
        file.write(f"Drug classes: {y.nunique()}\n\n")
        file.write(f"Accuracy: {accuracy:.4f}\n")
        file.write(f"Macro Precision: {macro_precision:.4f}\n")
        file.write(f"Macro Recall: {macro_recall:.4f}\n")
        file.write(f"Macro F1: {macro_f1:.4f}\n")

    print(f"Saved evaluation summary: {summary_file}")

    # ---------------------------------------------------------
    # Save model
    # ---------------------------------------------------------

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    model_file = MODEL_DIR / "drug_class_classifier.joblib"

    joblib.dump(model, model_file)

    print("\n" + "=" * 60)
    print("MODEL SAVED")
    print("=" * 60)

    print(f"File: {model_file}")

    print("\nEvaluation completed successfully.")


if __name__ == "__main__":
    main()