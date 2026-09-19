from pathlib import Path
import pandas as pd

from loader import load_suppliers


def profile_suppliers(df: pd.DataFrame) -> dict:
    """
    Generate a basic data quality profile for the supplier dataset.
    """

    profile = {
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": {},
    }

    for column in df.columns:
        series = df[column]

        profile["columns"][column] = {
            "dtype": str(series.dtype),
            "missing_count": int(series.isna().sum()),
            "missing_rate": round(float(series.isna().mean()), 4),
            "unique_count": int(series.nunique(dropna=True)),
        }

    return profile


if __name__ == "__main__":

    file_path = Path("data/input/suppliers_sample.xlsx")

    suppliers = load_suppliers(file_path)

    profile = profile_suppliers(suppliers)

    print("\n=== SUPPLIER DATA PROFILE ===")
    print(f"Rows: {profile['row_count']}")
    print(f"Columns: {profile['column_count']}")

    print("\n=== COLUMN PROFILE ===")

    for column, information in profile["columns"].items():

        print(
            f"{column:25} | "
            f"type={information['dtype']:10} | "
            f"missing={information['missing_count']:3} "
            f"({information['missing_rate']:.1%}) | "
            f"unique={information['unique_count']:3}"
        )