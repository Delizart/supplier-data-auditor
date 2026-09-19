from supplier_auditor.audit_engine import AuditEngine
from supplier_auditor.models import AuditIssue


def test_add_issue():

    engine = AuditEngine()

    issue = AuditIssue(
        supplier_id="SUP0011",
        issue_type="INVALID_EMAIL",
        field="email",
        severity="MEDIUM",
        confidence=0.98,
        details="Invalid email format",
        rule_id="EMAIL_FORMAT_001",
    )

    engine.add_issue(issue)

    assert len(engine.get_issues()) == 1
    assert engine.get_issues()[0].supplier_id == "SUP0011"

def test_summary():

    engine = AuditEngine()

    engine.add_issue(
        AuditIssue(
            supplier_id="SUP0011",
            issue_type="INVALID_EMAIL",
            field="email",
            severity="MEDIUM",
            confidence=0.98,
            details="Invalid email",
        )
    )

    engine.add_issue(
        AuditIssue(
            supplier_id="SUP0021",
            issue_type="INVALID_EMAIL",
            field="email",
            severity="MEDIUM",
            confidence=0.98,
            details="Invalid email",
        )
    )

    assert engine.summary()["INVALID_EMAIL"] == 2