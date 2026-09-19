# ============================================================
# SUPPLIER DATA AUDITOR — V0.1
# Module : completeness.py
#
# Objectif :
# Détecter les champs obligatoires qui sont vides ou manquants
# dans la base fournisseurs.
# ============================================================


# Pandas nous permet de manipuler les données sous forme de
# DataFrame (tableau de données).
import pandas as pd


# ------------------------------------------------------------
# 1. DEFINITION DES CHAMPS OBLIGATOIRES
# ------------------------------------------------------------
#
# Ici, nous définissons les colonnes qui doivent normalement
# être renseignées pour chaque fournisseur.
#
# Cette liste représente une PREMIERE HYPOTHESE métier.
# Dans une vraie entreprise, ces règles pourraient être
# configurables selon le contexte.
#
REQUIRED_FIELDS = [
    "supplier_id",
    "supplier_name",
    "address",
    "city",
    "postal_code",
    "country",
    "email",
    "phone",
    "tax_id",
    "registration_number",
]


# ------------------------------------------------------------
# 2. FONCTION DE DETECTION DES DONNEES MANQUANTES
# ------------------------------------------------------------

def check_missing_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Détecte les champs obligatoires manquants.

    Paramètre
    ---------
    df : pd.DataFrame
        La base fournisseurs normalisée.

    Retour
    ------
    pd.DataFrame
        Un tableau contenant une ligne par anomalie détectée.
    """

    # Cette liste va servir à stocker toutes les anomalies
    # que nous allons détecter.
    #
    # Exemple :
    #
    # [
    #     {
    #         "supplier_id": "SUP0010",
    #         "issue_type": "MISSING_DATA",
    #         ...
    #     }
    # ]
    #
    issues = []


    # --------------------------------------------------------
    # 3. PARCOURIR CHAQUE FOURNISSEUR
    # --------------------------------------------------------
    #
    # df.iterrows() permet de parcourir le DataFrame ligne
    # par ligne.
    #
    # "_" représente l'index de la ligne.
    #
    # "row" contient les données du fournisseur.
    #
    for _, row in df.iterrows():

        # On récupère l'identifiant du fournisseur.
        #
        # Exemple :
        # SUP0001
        # SUP0002
        # SUP0003
        #
        supplier_id = row["supplier_id"]


        # ----------------------------------------------------
        # 4. VERIFIER TOUS LES CHAMPS OBLIGATOIRES
        # ----------------------------------------------------
        #
        # Pour chaque fournisseur, on vérifie chaque champ
        # défini dans REQUIRED_FIELDS.
        #
        for field in REQUIRED_FIELDS:

            # Récupère la valeur du champ actuel.
            #
            # Exemple :
            #
            # field = "email"
            #
            # value = "contact@acme.fr"
            #
            # ou :
            #
            # value = NaN
            #
            value = row[field]


            # ------------------------------------------------
            # 5. DETECTER UNE VALEUR MANQUANTE
            # ------------------------------------------------
            #
            # pd.isna(value)
            #
            # permet de détecter les valeurs NaN / None.
            #
            # Exemple :
            #
            # None
            # NaN
            #
            # seront considérés comme manquants.
            #
            #
            # La deuxième condition :
            #
            # str(value).strip() == ""
            #
            # permet également de détecter une chaîne vide
            # ou composée uniquement d'espaces.
            #
            if pd.isna(value) or str(value).strip() == "":


                # --------------------------------------------
                # 6. CREER UN ENREGISTREMENT D'ANOMALIE
                # --------------------------------------------
                #
                # Nous ne faisons pas simplement :
                #
                # print("Email manquant")
                #
                # Nous créons une donnée structurée.
                #
                # C'est très important pour la suite du produit.
                #
                issues.append(
                    {
                        # Quel fournisseur est concerné ?
                        "supplier_id": supplier_id,

                        # Quel type de problème ?
                        "issue_type": "MISSING_DATA",

                        # Quelle colonne est concernée ?
                        "field": field,

                        # Niveau de gravité.
                        #
                        # Pour l'instant, nous mettons HIGH
                        # pour toutes les données manquantes.
                        # Ce sera amélioré plus tard.
                        "severity": "HIGH",

                        # Niveau de confiance.
                        #
                        # Ici nous sommes certains que la valeur
                        # est absente.
                        #
                        # Donc :
                        # 1.0 = 100% de confiance
                        #
                        "confidence": 1.0,

                        # Explication technique de l'anomalie.
                        "details": (
                            f"Required field '{field}' is missing."
                        ),
                    }
                )


    # --------------------------------------------------------
    # 7. TRANSFORMER LES RESULTATS EN DATAFRAME
    # --------------------------------------------------------
    #
    # La fonction retourne un DataFrame.
    #
    # Pourquoi ?
    #
    # Parce que nous voulons pouvoir ensuite :
    #
    # - filtrer les anomalies ;
    # - compter les problèmes ;
    # - calculer les scores ;
    # - exporter vers Excel ;
    # - alimenter le LLM.
    #
    return pd.DataFrame(issues)


# ============================================================
# 8. PROGRAMME PRINCIPAL
# ============================================================
#
# Cette partie est exécutée uniquement lorsqu'on lance :
#
# python src/completeness.py
#
# Elle n'est pas exécutée si le fichier est simplement importé
# depuis un autre module.
#
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # Import de notre fonction de chargement.
    #
    # loader.py est responsable de lire le fichier Excel.
    # --------------------------------------------------------
    from loader import load_suppliers


    # --------------------------------------------------------
    # Import de notre fonction de normalisation.
    #
    # normalization.py prépare les données avant les contrôles.
    # --------------------------------------------------------
    from normalization import normalize_suppliers


    # --------------------------------------------------------
    # 9. CHARGER LE FICHIER EXCEL
    # --------------------------------------------------------

    suppliers = load_suppliers(
        "data/input/suppliers_sample.xlsx"
    )


    # --------------------------------------------------------
    # 10. NORMALISER LES DONNEES
    # --------------------------------------------------------
    #
    # Nous travaillons sur les données normalisées plutôt que
    # directement sur les données brutes.
    #
    normalized = normalize_suppliers(suppliers)


    # --------------------------------------------------------
    # 11. LANCER LE CONTROLE DE COMPLETUDE
    # --------------------------------------------------------

    issues = check_missing_data(normalized)


    # --------------------------------------------------------
    # 12. AFFICHER LES RESULTATS
    # --------------------------------------------------------

    print("\n=== MISSING DATA ISSUES ===")


    # Si aucune anomalie n'est trouvée...
    if issues.empty:

        print("No missing data detected.")


    # Sinon...
    else:

        # Affiche le tableau sans afficher l'index Pandas.
        print(
            issues.to_string(index=False)
        )