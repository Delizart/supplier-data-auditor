from typing import List

from .models import AuditIssue


class AuditEngine:

    def __init__(self):
        self.issues: List[AuditIssue] = []

    def add_issue(self, issue: AuditIssue) -> None:
        self.issues.append(issue)

    def get_issues(self) -> List[AuditIssue]:
        return self.issues

    def summary(self) -> dict:
        summary = {}

        for issue in self.issues:
            summary[issue.issue_type] = (
                summary.get(issue.issue_type, 0) + 1
            )

        return summary