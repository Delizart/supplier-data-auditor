import pandas as pd

from supplier_auditor.rules.completeness_adapter import (
    convert_missing_data_issues,
)
from supplier_auditor.rules.validation_adapter import (
    convert_contact_issues,
)


def test_missing_data_adapter():

    df = pd.DataFrame(
        [
            {
                "supplier_id": "SUP0010",
                "issue_type": "MISSING_DATA",
                "field": "email",
                "severity": "HIGH",
                "confidence": 1.0,
                "details": "Required field 'email' is missing.",
            }
        ]
    )

    issues = convert_missing_data_issues(df)

    assert len(issues) == 1
    assert issues[0].supplier_id == "SUP0010"
    assert issues[0].rule_id == "COMPLETENESS_001"


def test_contact_adapter():

    df = pd.DataFrame(
        [
            {
                "supplier_id": "SUP0011",
                "issue_type": "INVALID_EMAIL",
                "field": "email",
                "severity": "MEDIUM",
                "confidence": 0.98,
                "details": "Invalid email format",
            },
            {
                "supplier_id": "SUP0031",
                "issue_type": "INVALID_PHONE",
                "field": "phone",
                "severity": "MEDIUM",
                "confidence": 0.98,
                "details": "Invalid phone format",
            },
        ]
    )

    issues = convert_contact_issues(df)

    assert len(issues) == 2
    assert issues[0].rule_id == "EMAIL_FORMAT_001"
    assert issues[1].rule_id == "PHONE_FORMAT_001"