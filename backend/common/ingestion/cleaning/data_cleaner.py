import pandas as pd


class DataCleaner:

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = df.columns.str.strip()
        df = df.dropna(how="all")
        return df
