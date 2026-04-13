from datetime import time

import pandas as pd

from . import field, invoice_classes, subcat, pandas_utils


def get_value_from_series_col(*, series: pd.Series, field_name: str):
    """Get value from series by field name. Raises ValueError if not found."""
    return pandas_utils.get_value_from_series_col(series=series, column_name=field_name)


def add_extra_cans_column(df: pd.DataFrame) -> pd.DataFrame:
    def _calc_extra_cans(x):
        if isinstance(x, int) and x - 1 > 0:
            return x - 1
        if isinstance(x, float) and x.is_integer() and x - 1 > 0:
            return int(x - 1)
        try:
            int_val = int(x)
            if int_val - 1 > 0:
                return int_val - 1
        except TypeError, ValueError:
            pass
        return None

    df[field.EXTRA_CANS] = df[field.STRUCTURE].apply(_calc_extra_cans)
    df[field.EXTRA_CANS] = df[field.EXTRA_CANS].astype(pd.Int64Dtype())
    return df


def reformat_maintenance_to_string(df: pd.DataFrame) -> pd.DataFrame:
    def time_to_string(val):
        if isinstance(val, time):
            return val.strftime("%H:%M")
        return val

    df[field.MAINT] = df[field.MAINT].apply(time_to_string)
    return df


def create_derived_rows_list(row: pd.Series) -> list[dict]:
    """Create derived rows based on the input row."""
    current_sort_by = get_value_from_series_col(series=row, field_name=field.SORT_BY)
    new_rows = []

    row = row.dropna()

    for col_name, col_value in row.items():
        if col_name == field.HVF_NO_SPACE:
            new_rows.append(
                invoice_classes.HVFColumnProcessor(row=row).get_derived_row()
            )
        elif col_name == field.LIGHT_INSP:
            new_rows.append(
                invoice_classes.LIGHT_INSPColumnProcessor(row=row).get_derived_row()
            )
        elif col_name == field.MIG_BIRD:
            new_rows.append(
                invoice_classes.MIG_BIRDColumnProcessor(row=row).get_derived_row()
            )
        elif col_name == field.WINDSIM:
            new_rows.append(
                invoice_classes.WINDSIMColumnProcessor(row=row).get_derived_row()
            )
        elif col_name == field.TTP_INIT_READ:
            new_rows.append(
                invoice_classes.TTP_INIT_READColumnProcessor(row=row).get_derived_row()
            )
        elif col_name == field.TENSION:
            new_rows.append(
                invoice_classes.TENSIONColumnProcessor(row=row).get_derived_row()
            )
        elif (
            col_name == field.MAINT
            and isinstance(col_value, time)
            and (col_value.hour > 0 or col_value.minute > 0)
        ):
            new_rows.append(
                invoice_classes.MAINTColumnProcessor(row=row).get_derived_row()
            )
        elif col_name == field.EXTRA_CANS:
            new_rows.append(
                invoice_classes.EXTRA_CANSColumnProcessor(row=row).get_derived_row()
            )
        elif col_name == field.MAN_LIFT:
            new_rows.append(
                invoice_classes.MAN_LIFTColumnProcessor(row=row).get_derived_row()
            )

    new_rows.sort(key=lambda x: (x[field.SUB_CATEGORY], x[field.DESCRIPTION]))

    for one_row in new_rows:
        current_sort_by += 1
        one_row[field.SORT_BY] = current_sort_by

    return new_rows


def build_derived_rows(dataframe: pd.DataFrame) -> list[dict]:
    """Creates a list of new row dicts from dataframe."""
    all_new_rows = []
    for _, row in dataframe.iterrows():
        one_rows_new_rows = create_derived_rows_list(row)
        if one_rows_new_rows:
            all_new_rows.extend(one_rows_new_rows)
    return all_new_rows


def transform_input_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Transform input dataframe to output format. Pure function, no I/O."""
    pandas_utils.check_for_required_fields(
        required_fields=field.REQUIRED_INPUT_COLS, pd_df=df
    )

    wanted_df = df[field.REQUIRED_INPUT_COLS].copy()

    wanted_df = wanted_df.rename(
        columns={
            field.BASE_FOR_INV: field.DESCRIPTION,
            field.ADD_CAN_LEVEL: field.ADD_CAN_PRICE,
            field.HVF_WITH_SPACE: field.HVF_NO_SPACE,
        },
    )

    wanted_df[field.SUB_CATEGORY] = subcat.BASE
    wanted_df[field.QUANTITY] = 1

    wanted_df = wanted_df.sort_values(by=[field.BU])

    wanted_df[field.SORT_BY] = range(1000000, 1000000 + 100 * len(wanted_df), 100)

    wanted_df = add_extra_cans_column(wanted_df)

    wanted_df = wanted_df[field.OUTPUT_COLS]

    derived_rows = build_derived_rows(wanted_df.copy(deep=True))
    derived_rows_df = pd.DataFrame(derived_rows)
    wanted_df = pd.concat([wanted_df, derived_rows_df], ignore_index=True)

    wanted_df = wanted_df.sort_values(by=[field.SORT_BY], ascending=True)

    wanted_df = reformat_maintenance_to_string(wanted_df)

    return wanted_df
