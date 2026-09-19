from dataclasses import dataclass
from typing import Optional


@dataclass
class AuditIssue:
    supplier_id: str
    issue_type: str
    field: Optional[str]
    severity: str
    confidence: float
    details: str
    source: str = "deterministic_rule"
    rule_id: Optional[str] = None