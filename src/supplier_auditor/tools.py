from typing import Any

import pandas as pd

from .rules.completeness_adapter import convert_missing_data_issues

import re


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

def validate_contacts(file_path: str) -> dict:
    """
    Validate supplier email and phone formats.
    """

    df = pd.read_excel(file_path)

    issues = []

    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    phone_pattern = r"^\+?[0-9][0-9\s\-().]{6,}$"

    for _, row in df.iterrows():

        supplier_id = str(row["supplier_id"])

        # -------------------------
        # Email
        # -------------------------

        email = row.get("email")

        if pd.notna(email):

            email = str(email).strip()

            if not re.match(email_pattern, email):

                issues.append(
                    {
                        "supplier_id": supplier_id,
                        "issue_type": "INVALID_EMAIL",
                        "field": "email",
                        "severity": "MEDIUM",
                        "confidence": 0.98,
                        "details": (
                            f"Invalid email format: {email}"
                        ),
                    }
                )

        # -------------------------
        # Phone
        # -------------------------

        phone = row.get("phone")

        if pd.notna(phone):

            phone = str(phone).strip()

            if not re.match(phone_pattern, phone):

                issues.append(
                    {
                        "supplier_id": supplier_id,
                        "issue_type": "INVALID_PHONE",
                        "field": "phone",
                        "severity": "MEDIUM",
                        "confidence": 0.98,
                        "details": (
                            f"Invalid phone format: {phone}"
                        ),
                    }
                )

    return {
        "total_issues": len(issues),
        "issues": issues,
    }