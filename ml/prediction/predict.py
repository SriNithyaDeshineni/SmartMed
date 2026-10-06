from pathlib import Path

import joblib
import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_FILE = (
    PROJECT_ROOT
    / "ml"
    / "model"
    / "drug_class_classifier.joblib"
)


def load_model():
    """Load the trained drug-class classification model."""
    return joblib.load(MODEL_FILE)


def predict_drug_class(
    generic,
    dosage_form,
    medicine_type,
    strength,
):
    """Predict drug class, confidence, and top-3 predictions."""

    model = load_model()

    input_data = pd.DataFrame(
        [
            {
                "generic": generic,
                "dosage form": dosage_form,
                "type": medicine_type,
                "strength": strength,
            }
        ]
    )

    # Predicted class
    prediction = model.predict(input_data)[0]

    # Prediction probabilities
    probabilities = model.predict_proba(input_data)[0]

    # Class names
    classes = model.classes_

    # Get indices of top 3 probabilities
    top_indices = probabilities.argsort()[-3:][::-1]

    top_predictions = []

    for index in top_indices:
        top_predictions.append(
            {
                "drug_class": classes[index],
                "confidence": float(probabilities[index]),
            }
        )

    # Confidence of the main prediction
    confidence = float(probabilities[top_indices[0]])

    return {
        "predicted_drug_class": prediction,
        "confidence": confidence,
        "top_predictions": top_predictions,
    }


if __name__ == "__main__":
    result = predict_drug_class(
        generic="Paracetamol",
        dosage_form="Tablet",
        medicine_type="allopathic",
        strength="500 mg",
    )

    print("=" * 60)
    print("SMARTMED ML PREDICTION")
    print("=" * 60)

    print(f"Predicted drug class: {result['predicted_drug_class']}")
    print(f"Confidence: {result['confidence']:.4f}")

    print("\nTop 3 predictions:")

    for position, item in enumerate(result["top_predictions"], start=1):
        print(
            f"{position}. "
            f"{item['drug_class']} "
            f"({item['confidence']:.4f})"
        )