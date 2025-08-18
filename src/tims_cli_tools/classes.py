import pandas as pd
from . import field, subcat, desc, price, ensure


class BaseColumnProcessor:
    """Base class for column processors"""

    def __init__(self, row: pd.Series):
        self.column_name: str = None
        self.row: pd.Series = row
        self.quantity: int = 1
        self.sub_category: str | None = None
        self.description: str | None = None

    def _get_column_value(self, column_name: str):
        """Pull the column value from the row based upon the column_name."""
        mylist = [
            col_value
            for (col_name, col_value) in self.row.items()
            if col_name == column_name
        ]

        if not mylist:
            msg = f"Could not find value for field {column_name} in {self.row}"
            raise ValueError(msg)
        return mylist[0]

    def _column_value_contains_valid_data() -> bool:
        """Make sure we can cast the column data to the required type."""
        raise NotImplementedError

    def get_derived_row(self) -> dict:
        """Get new/derived row based upon processing rules for the column_name."""
        self._column_value_contains_valid_data()
        tmp_row = {
            field.BU: self._get_column_value(column_name=field.BU),
            field.SUB_CATEGORY: self.sub_category,
            field.DESCRIPTION: self.description,
            field.QUANTITY: self.quantity,
        }
        return tmp_row


class FloatColumnProcessor(BaseColumnProcessor):
    """Adds float processing"""

    def __init__(self, row: pd.Series):
        super().__init__(row=row)

    def _column_value_contains_valid_data(self) -> bool:
        ensure.ensure_float(
            number=self._get_column_value(column_name=self.column_name),
            col_name=self.column_name,
            row=self.row,
        )


class IntColumnProcessor(BaseColumnProcessor):
    """Adds int info and processing"""

    def __init__(self, row: pd.Series):
        super().__init__(row=row)

    def _column_value_contains_valid_data(self) -> bool:
        ensure.ensure_int(
            number=self._get_column_value(column_name=self.column_name),
            col_name=self.column_name,
            row=self.row,
        )


class HVTColumnProcessor(FloatColumnProcessor):
    """HVT"""

    def __init__(self, row: pd.Series):
        super().__init__(row=row)
        self.sub_category = subcat.ADDER
        self.description = desc.HEIGHT_VERIF
        self.column_name = field.HVF_NO_SPACE
