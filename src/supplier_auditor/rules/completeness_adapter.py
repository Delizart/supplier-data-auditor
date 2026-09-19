from typing import List

import pandas as pd

from ..models import AuditIssue


def convert_missing_data_issues(
    issues_df: pd.DataFrame,
) -> List[AuditIssue]:

    issues = []

    for _, row in issues_df.iterrows():
        issues.append(
            AuditIssue(
                supplier_id=str(row["supplier_id"]),
                issue_type=str(row["issue_type"]),
                field=str(row["field"]),
                severity=str(row["severity"]),
                confidence=float(row["confidence"]),
                details=str(row["details"]),
                source="deterministic_rule",
                rule_id="COMPLETENESS_001",
            )
        )

    return issues