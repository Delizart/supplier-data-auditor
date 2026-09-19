import pandas as pd


def normalize_text(value):
    """
    Normalize a text value for comparison.

    - Convert to string
    - Remove leading/trailing spaces
    - Convert multiple spaces to one
    - Convert to lowercase
    """
    if pd.isna(value):
        return None

    value = str(value).strip()
    value = " ".join(value.split())
    value = value.lower()

    return value


def normalize_suppliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a normalized copy of the supplier dataset.
    Original data remains untouched.
    """

    normalized = df.copy()

    text_columns = [
        "supplier_name",
        "address",
        "city",
        "country",
        "email",
        "phone",
        "tax_id",
        "registration_number",
    ]

    for column in text_columns:
        normalized[column] = normalized[column].apply(normalize_text)

# Registration numbers must be strings without Excel's ".0"
    normalized["registration_number"] = normalized["registration_number"].apply(
        lambda x: None
        if x is None
        else str(x).replace(".0", "")
    )

    # Codes and identifiers must remain strings
    normalized["postal_code"] = (
        normalized["postal_code"]
        .apply(lambda x: None if pd.isna(x) else str(int(x)).zfill(5))
    )

    return normalized


if __name__ == "__main__":

    from loader import load_suppliers

    suppliers = load_suppliers(
        "data/input/suppliers_sample.xlsx"
    )

    normalized = normalize_suppliers(suppliers)

    print("\n=== ORIGINAL ===")
    print(suppliers.head(3).to_string())

    print("\n=== NORMALIZED ===")
    print(normalized.head(3).to_string())