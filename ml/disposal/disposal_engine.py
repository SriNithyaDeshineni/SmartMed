from datetime import date
from typing import Optional


# Only classes explicitly identified in our current project rules
# as cytotoxic are included here.
#
# IMPORTANT:
# Do not add a drug class here only because its name sounds
# hazardous or because the ML model predicted it.
CYTOTOXIC_CLASSES = {
    "Cytotoxic Chemotherapy",
    "Cytotoxic immunosuppressants",
    "Hormonal Chemotherapy",
    "Immunological Chemotherapy",
}


def get_expiry_status(expiry_date: Optional[str]) -> str:
    """Determine expiry status from the package expiry date."""

    if expiry_date is None or expiry_date == "":
        return "EXPIRY_UNKNOWN"

    try:
        expiry = date.fromisoformat(expiry_date)
    except ValueError:
        return "INVALID_EXPIRY_DATE"

    today = date.today()

    if expiry < today:
        return "EXPIRED"

    return "NOT_EXPIRED"


def get_disposal_guidance(
    drug_class: str,
    expiry_date: Optional[str],
) -> dict:
    """Return rule-based disposal guidance."""

    expiry_status = get_expiry_status(expiry_date)

    # Expiry date is missing.
    if expiry_status == "EXPIRY_UNKNOWN":
        return {
            "expiry_status": "EXPIRY_UNKNOWN",
            "handling_category": "EXPIRY_VERIFICATION_REQUIRED",
            "recommended_route": "VERIFY_PACKAGE_EXPIRY_DATE",
            "warning": (
                "Check the actual expiry date printed on the "
                "medicine package before disposal."
            ),
        }

    # Expiry date could not be interpreted.
    if expiry_status == "INVALID_EXPIRY_DATE":
        return {
            "expiry_status": "INVALID_EXPIRY_DATE",
            "handling_category": "EXPIRY_VERIFICATION_REQUIRED",
            "recommended_route": "VERIFY_PACKAGE_EXPIRY_DATE",
            "warning": (
                "The expiry date could not be read correctly. "
                "Verify the package before disposal."
            ),
        }

    # Medicine is not expired.
    if expiry_status == "NOT_EXPIRED":
        return {
            "expiry_status": "NOT_EXPIRED",
            "handling_category": "NOT_EXPIRED",
            "recommended_route": (
                "NO_EXPIRED_MEDICINE_DISPOSAL_REQUIRED"
            ),
            "warning": (
                "This medicine is not expired according to "
                "the provided package expiry date."
            ),
        }

    # Expired cytotoxic medicine.
    if drug_class in CYTOTOXIC_CLASSES:
        return {
            "expiry_status": "EXPIRED",
            "handling_category": "CYTOTOXIC_PHARMACEUTICAL_WASTE",
            "recommended_route": (
                "RETURN_TO_MANUFACTURER_OR_AUTHORIZED_"
                "TREATMENT_FACILITY_FOR_CYTOTOXIC_TREATMENT"
            ),
            "warning": (
                "Handle as cytotoxic pharmaceutical waste. "
                "Use the manufacturer/supplier return route or "
                "an authorized treatment facility."
            ),
        }

    # Other expired/discarded medicines.
    return {
        "expiry_status": "EXPIRED",
        "handling_category": "PHARMACEUTICAL_WASTE",
        "recommended_route": (
            "RETURN_TO_MANUFACTURER_OR_AUTHORIZED_INCINERATION"
        ),
        "warning": (
            "Use an authorized pharmaceutical-waste route. "
            "Do not dispose of the medicine by household destruction."
        ),
    }


if __name__ == "__main__":
    result = get_disposal_guidance(
        drug_class="Non opioid analgesics",
        expiry_date=None,
    )

    print("=" * 60)
    print("SMARTMED DISPOSAL GUIDANCE")
    print("=" * 60)

    for key, value in result.items():
        print(f"{key}: {value}")