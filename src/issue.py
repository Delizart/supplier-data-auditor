# ============================================================
# SUPPLIER DATA AUDITOR
# Module : issue.py
#
# Objectif :
# Définir la structure standard d'une anomalie.
# ============================================================


from dataclasses import dataclass
from typing import Optional


@dataclass
class Issue:
    """
    Représente une anomalie détectée sur un fournisseur.
    """

    supplier_id: str

    issue_type: str

    field: Optional[str]

    severity: str

    confidence: float

    details: str