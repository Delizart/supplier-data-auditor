from typing import List

import pandas as pd

from .models import AuditIssue


class AuditEngine:

    def __init__(self):
        self.issues: List[AuditIssue] = []

    def add_issue(self, issue: AuditIssue) -> None:
        self.issues.append(issue)

    def add_issues(self, issues: List[AuditIssue]) -> None:
        self.issues.extend(issues)

    def get_issues(self) -> List[AuditIssue]:
        return self.issues

    def summary(self) -> dict:
        summary = {}

        for issue in self.issues:
            summary[issue.issue_type] = (
                summary.get(issue.issue_type, 0) + 1
            )

        return summary

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "supplier_id": issue.supplier_id,
                    "issue_type": issue.issue_type,
                    "field": issue.field,
                    "severity": issue.severity,
                    "confidence": issue.confidence,
                    "details": issue.details,
                    "source": issue.source,
                    "rule_id": issue.rule_id,
                }
                for issue in self.issues
            ]
        )