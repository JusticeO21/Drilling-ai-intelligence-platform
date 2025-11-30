import pandas as pd


class StructuredFileLoader:
    """Loads CSV or Excel files."""

    def load(self, file_path: str) -> pd.DataFrame:
        if file_path.endswith(".csv"):
            return pd.read_csv(file_path)
        if file_path.endswith((".xlsx", ".xls")):
            return pd.read_excel(file_path)
        raise ValueError("Unsupported file type")
