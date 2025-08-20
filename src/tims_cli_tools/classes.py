import pandas as pd
from . import field, subcat, desc, ensure, price
import copy


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

        my_value = mylist[0]

        return my_value

    def _get_my_column_value(self):
        return self._get_column_value(self.column_name)

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


class MoneyColumnProcessor(BaseColumnProcessor):
    """Adds money_str ($1,234.56) processing"""

    def __init__(self, row: pd.Series):
        super().__init__(row=row)

    def _column_value_contains_valid_data(self) -> None:
        ensure.ensure_money(
            number=self._get_my_column_value(),
            col_name=self.column_name,
            row=self.row,
        )

    def _get_my_compare_value(self):
        my_value = super()._get_my_column_value()
        isolated_value = copy.deepcopy(my_value)
        my_compare_value = ensure.any_numeric_representation_to_float(isolated_value)
        return my_compare_value


class IntColumnProcessor(BaseColumnProcessor):
    """Adds int info and processing"""

    def __init__(self, row: pd.Series):
        super().__init__(row=row)

    def _column_value_contains_valid_data(self) -> None:
        ensure.ensure_int(
            number=self._get_my_column_value(),
            col_name=self.column_name,
            row=self.row,
        )


class HVFColumnProcessor(MoneyColumnProcessor):
    def __init__(self, row: pd.Series):
        super().__init__(row=row)
        self.sub_category = subcat.ADDER
        self.description = desc.HEIGHT_VERIF
        self.column_name = field.HVF_NO_SPACE


class LIGHT_INSPColumnProcessor(MoneyColumnProcessor):
    def __init__(self, row: pd.Series):
        super().__init__(row=row)
        self.sub_category = subcat.ADDER
        self.description = desc.LIGHT_INSP
        self.column_name = field.LIGHT_INSP


class MIG_BIRDColumnProcessor(MoneyColumnProcessor):
    def __init__(self, row: pd.Series):
        super().__init__(row=row)
        self.sub_category = subcat.ADDER
        self.description = desc.BIRD_WATCH
        self.column_name = field.MIG_BIRD


class WINDSIMColumnProcessor(MoneyColumnProcessor):
    def __init__(self, row: pd.Series):
        super().__init__(row=row)
        self.sub_category = subcat.ADDER
        self.description = desc.WINDSIM
        self.column_name = field.WINDSIM


class TTP_INIT_READColumnProcessor(MoneyColumnProcessor):
    def __init__(self, row: pd.Series):
        super().__init__(row=row)
        self.sub_category = subcat.ADDER
        self.description = desc.GUY_TTP_INIT
        self.column_name = field.TTP_INIT_READ


class MAN_LIFTColumnProcessor(MoneyColumnProcessor):
    def __init__(self, row: pd.Series):
        super().__init__(row=row)
        self.sub_category = subcat.WORK_AUTH
        self.description = desc.MANLIFT_RENTAL
        self.column_name = field.MAN_LIFT


class EXTRA_CANSColumnProcessor(IntColumnProcessor):
    def __init__(self, row: pd.Series):
        super().__init__(row=row)
        self.sub_category = subcat.BASE
        self.description = desc.ADDITIONAL_CAN
        self.column_name = field.EXTRA_CANS

    def _column_value_contains_valid_data(self) -> None:
        super()._column_value_contains_valid_data()
        self.quantity = self._get_my_column_value()


class TENSIONColumnProcessor(MoneyColumnProcessor):
    def __init__(self, row: pd.Series):
        super().__init__(row=row)
        self.sub_category = subcat.ADDER
        self.description = None
        self.column_name = field.TENSION

    def _column_value_contains_valid_data(self) -> None:
        super()._column_value_contains_valid_data()

        my_value = self._get_my_column_value()
        my_compare_value = self._get_my_compare_value()

        # set correct description based upon price
        if my_compare_value == price.PRICE_700:
            self.description = desc.GUY_TTP_1_6
        elif my_compare_value == price.PRICE_850:
            self.description = desc.GUY_TTP_7_12
        elif my_compare_value == price.PRICE_1000:
            self.description = desc.GUY_TTP_12_PLUS
        else:
            unknown_tension_value = (
                f"Unexpected Tension Price value: {my_value} on row\n{self.row}."
            )
            raise ValueError(unknown_tension_value)


class MAINTColumnProcessor(BaseColumnProcessor):
    def __init__(self, row: pd.Series):
        super().__init__(row=row)
        self.sub_category = subcat.ADDER
        self.description = desc.MAINT_MIN_RATE
        self.column_name = field.MAINT
        self.time = None

    def _column_value_contains_valid_data(self) -> None:
        self.time = self._get_my_column_value()

        # convert the value to an integer representing minutes
        try:
            # convert time object to total minutes
            self.quantity = self.time.hour * 60 + self.time.minute
        except ValueError as e:
            maintenance_value_error = f"Unexpected {field.MAINT} value of: {self.time}. Expected H:MM time format."
            raise ValueError(maintenance_value_error) from e
