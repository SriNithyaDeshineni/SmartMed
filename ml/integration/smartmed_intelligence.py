from pathlib import Path
import sys
import json

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

# Allow this script to import the disposal engine
sys.path.append(str(PROJECT_ROOT / "ml" / "disposal"))

from disposal_engine import get_disposal_guidance


def load_model():
    """Load the trained ML model."""
    return joblib.load(MODEL_FILE)


def analyze_medicine(
    generic,
    dosage_form,
    medicine_type,
    strength,
    expiry_date,
):
    """Run ML classification followed by disposal guidance."""

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

    # ML prediction
    predicted_class = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]
    classes = model.classes_

    # Get top 3 predictions
    top_indices = probabilities.argsort()[-3:][::-1]

    top_predictions = []

    for index in top_indices:
        top_predictions.append(
            {
                "drug_class": classes[index],
                "confidence": float(probabilities[index]),
            }
        )

    confidence = float(probabilities[top_indices[0]])

    # Rule-based disposal guidance
    disposal = get_disposal_guidance(
        drug_class=predicted_class,
        expiry_date=expiry_date,
    )

    return {
        "predicted_drug_class": predicted_class,
        "confidence": confidence,
        "top_predictions": top_predictions,
        "disposal_guidance": disposal,
    }


if __name__ == "__main__":
    result = analyze_medicine(
        generic="Paracetamol",
        dosage_form="Tablet",
        medicine_type="allopathic",
        strength="500 mg",
        expiry_date="2026-01-01",
    )

    print(json.dumps(result, indent=2))