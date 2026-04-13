from typing import Protocol, runtime_checkable
import pandas as pd


@runtime_checkable
class DataFrameReader(Protocol):
    def read_excel(self, path: str) -> pd.DataFrame: ...


class PandasExcelReader:
    def read_excel(self, path: str) -> pd.DataFrame:
        return pd.read_excel(path)
