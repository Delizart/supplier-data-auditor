from pathlib import Path
import pandas as pd


def load_suppliers(file_path: str | Path) -> pd.DataFrame:
    """
    Load supplier data from an Excel file.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_excel(file_path)

    if df.empty:
        raise ValueError("The supplier file is empty.")

    return df


if __name__ == "__main__":
    file_path = "data/input/suppliers_sample.xlsx"

    suppliers = load_suppliers(file_path)

    print("Dataset loaded successfully.")
    print(f"Rows: {len(suppliers)}")
    print(f"Columns: {len(suppliers.columns)}")
    print("\nColumns:")
    print(suppliers.columns.tolist())