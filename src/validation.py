# ============================================================
# SUPPLIER DATA AUDITOR — V0.1
# Module : validation.py
#
# Objectif :
# Détecter les emails et téléphones dont le format semble
# incorrect.
#
# IMPORTANT :
# Ces contrôles sont déterministes.
# Aucun LLM n'est nécessaire.
# ============================================================


import re
import pandas as pd
import phonenumbers


# ------------------------------------------------------------
# 1. VALIDATION EMAIL
# ------------------------------------------------------------

def is_valid_email(value) -> bool:
    """
    Vérifie si une valeur ressemble à une adresse email valide.

    Retourne :
        True  → format valide
        False → format invalide
    """

    # Si la valeur est vide, on ne la traite pas comme un
    # email invalide.
    #
    # Pourquoi ?
    #
    # Parce que "email manquant" est déjà géré par
    # completeness.py.
    #
    if pd.isna(value) or str(value).strip() == "":
        return True

    email = str(value).strip()

    # Expression régulière simple pour vérifier la structure
    # générale d'une adresse email.
    #
    # Exemple valide :
    # contact@entreprise.fr
    #
    # Exemple invalide :
    # contact@entreprise
    #
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return bool(re.match(pattern, email))


# ------------------------------------------------------------
# 2. VALIDATION TELEPHONE
# ------------------------------------------------------------

def is_valid_phone(value, default_region="FR") -> bool:
    """
    Vérifie si un numéro de téléphone est valide.

    default_region="FR" signifie que les numéros sans indicatif
    international seront interprétés comme des numéros français.
    """

    # Même logique que pour l'email :
    # un téléphone manquant est traité par completeness.py.
    if pd.isna(value) or str(value).strip() == "":
        return True

    phone = str(value).strip()

    try:

        # Analyse du numéro avec la bibliothèque phonenumbers.
        parsed_number = phonenumbers.parse(
            phone,
            default_region
        )

        # Vérifie si le numéro correspond à un numéro possible
        # et valide.
        return phonenumbers.is_valid_number(parsed_number)

    except phonenumbers.NumberParseException:

        # Si phonenumbers n'arrive pas à interpréter le numéro,
        # nous considérons le numéro comme invalide.
        return False


# ------------------------------------------------------------
# 3. CONTROLE DE LA BASE FOURNISSEURS
# ------------------------------------------------------------

def check_contact_information(df: pd.DataFrame) -> pd.DataFrame:
    """
    Vérifie les emails et téléphones de tous les fournisseurs.

    Retourne un DataFrame contenant les anomalies détectées.
    """

    issues = []

    # Parcourt chaque fournisseur.
    for _, row in df.iterrows():

        supplier_id = row["supplier_id"]

        # ----------------------------------------------------
        # EMAIL
        # ----------------------------------------------------

        email = row["email"]

        if not is_valid_email(email):

            issues.append(
                {
                    "supplier_id": supplier_id,
                    "issue_type": "INVALID_EMAIL",
                    "field": "email",
                    "severity": "MEDIUM",
                    "confidence": 0.98,
                    "details": f"Invalid email format: {email}",
                }
            )


        # ----------------------------------------------------
        # TELEPHONE
        # ----------------------------------------------------

        phone = row["phone"]

        if not is_valid_phone(phone):

            issues.append(
                {
                    "supplier_id": supplier_id,
                    "issue_type": "INVALID_PHONE",
                    "field": "phone",
                    "severity": "MEDIUM",
                    "confidence": 0.98,
                    "details": f"Invalid phone format: {phone}",
                }
            )


    # Transformation de la liste en DataFrame.
    return pd.DataFrame(issues)


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

if __name__ == "__main__":

    # Import du loader.
    from loader import load_suppliers

    # Import de la normalisation.
    from normalization import normalize_suppliers


    # --------------------------------------------------------
    # CHARGEMENT
    # --------------------------------------------------------

    suppliers = load_suppliers(
        "data/input/suppliers_sample.xlsx"
    )


    # --------------------------------------------------------
    # NORMALISATION
    # --------------------------------------------------------

    normalized = normalize_suppliers(suppliers)


    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    issues = check_contact_information(normalized)


    # --------------------------------------------------------
    # AFFICHAGE
    # --------------------------------------------------------

    print("\n=== CONTACT VALIDATION ISSUES ===")

    if issues.empty:

        print("No invalid emails or phones detected.")

    else:

        print(
            issues.to_string(index=False)
        )