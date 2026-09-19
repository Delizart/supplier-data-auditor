from typing import Any

import pandas as pd

from .rules.completeness_adapter import convert_missing_data_issues


def check_missing_data(file_path: str) -> dict[str, Any]:
    """
    Check required supplier fields for missing values.
    """

    df = pd.read_excel(file_path)

    required_fields = [
        "supplier_name",
        "email",
        "phone",
        "address",
        "postal_code",
        "country",
        "tax_id",
    ]

    issues = []

    for field in required_fields:

        if field not in df.columns:
            continue

        missing = df[field].isna() | (
            df[field].astype(str).str.strip() == ""
        )

        for _, row in df[missing].iterrows():

            issues.append(
                {
                    "supplier_id": str(row["supplier_id"]),
                    "issue_type": "MISSING_DATA",
                    "field": field,
                    "severity": "HIGH",
                    "confidence": 1.0,
                    "details": (
                        f"Required field '{field}' is missing."
                    ),
                }
            )

    return {
        "total_issues": len(issues),
        "issues": issues,
    }