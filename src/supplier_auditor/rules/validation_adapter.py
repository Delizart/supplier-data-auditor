from typing import List

import pandas as pd

from ..models import AuditIssue


def convert_contact_issues(
    issues_df: pd.DataFrame,
) -> List[AuditIssue]:

    issues = []

    for _, row in issues_df.iterrows():
        issue_type = str(row["issue_type"])

        if issue_type == "INVALID_EMAIL":
            rule_id = "EMAIL_FORMAT_001"
        elif issue_type == "INVALID_PHONE":
            rule_id = "PHONE_FORMAT_001"
        else:
            rule_id = "CONTACT_VALIDATION_001"

        issues.append(
            AuditIssue(
                supplier_id=str(row["supplier_id"]),
                issue_type=issue_type,
                field=str(row["field"]),
                severity=str(row["severity"]),
                confidence=float(row["confidence"]),
                details=str(row["details"]),
                source="deterministic_rule",
                rule_id=rule_id,
            )
        )

    return issues