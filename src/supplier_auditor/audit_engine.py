from typing import List

import pandas as pd

import issue

from .models import AuditIssue

from .llm.client import explain_issue
from .llm.models import IssueExplanation

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

    def explain_issue(self, issue: AuditIssue) -> IssueExplanation:
        return explain_issue(
            issue_type=issue.issue_type,
            field=issue.field or "",
            severity=issue.severity,
            details=issue.details,
        )

    def explain_all_issues(self) -> dict[str, IssueExplanation]:
        explanations = {}

        for issue in self.issues:
            key = f"{issue.supplier_id}:{issue.issue_type}:{issue.field}"

            explanations[key] = self.explain_issue(issue)

        return explanations 