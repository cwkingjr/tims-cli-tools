import pytest

from tims_cli_tools.tims_invoice_transformer import (
    # ensure_int,
    check_for_required_fields,
    # create_cleaned_filepath,
    get_value_from_series_col,
    # build_new_rows_from_dataframe_col_values,
)
from tims_cli_tools import field

import pandas as pd

TWOS = 22222222  # shut up linter


@pytest.fixture
def df_clean_input_cols():
    return pd.DataFrame(
        data={
            field.BU: [TWOS],
            field.STRUCTURE: ["3"],
            field.BASE_FOR_INV: ["Inspection"],
            field.TIA_INSP: [1],
            field.ADD_CAN_LEVEL: [3],
            field.HVF_NO_SPACE: [1],
            field.LIGHT_INSP: [1],
            field.MIG_BIRD: [1],
            field.WINDSIM: [1],
            field.TTP_INIT_READ: [1],
            field.TENSION: [1],
            field.HR_PAY: [100.0],
            field.SITE_TOTAL: [200.0],
            field.MAINT: ["00:00:15"],
            field.MAN_LIFT: ["$1234.56"],
        },
    )


def test_check_for_required_fields_valid(df_clean_input_cols):
    assert (
        check_for_required_fields(
            required_fields=field.CLEAN_REQUIRED_INPUT_COLS,
            pd_df=df_clean_input_cols,
        )
        is None
    )


def test_check_for_required_fields_invalid(df_clean_input_cols):
    # remove a required field to test the failure case
    del df_clean_input_cols[field.BU]
    with pytest.raises(ValueError):
        assert check_for_required_fields(
            required_fields=field.CLEAN_REQUIRED_INPUT_COLS, pd_df=df_clean_input_cols
        )


def test_get_value_from_series_col(df_clean_input_cols):
    _, my_series = next(df_clean_input_cols.iterrows())
    assert get_value_from_series_col(series=my_series, field_name=field.BU) == TWOS


def test_get_value_from_series_col_missing_col(df_clean_input_cols):
    _, my_series = next(df_clean_input_cols.iterrows())
    del my_series[field.BU]
    with pytest.raises(ValueError):
        get_value_from_series_col(series=my_series, field_name=field.BU)


# def test_build_new_rows_from_dataframe_col_values():
#     ...

# @pytest.mark.parametrize(
#     "number, col_name, expected",
#     [
#         (3, field.HVF, True),
#         (3.5, field.HVF, True),
#         (None, field.HVF, False),
#         ("string", field.HVF, False),
#         (3, "non_existent_field", False),  # Non-existent field
#     ],
# )
# def test_ensure_int(number, col_name, expected, pd_series):
#     assert ensure_int(number=number, col_name=col_name, row=pd_series) == expected

# ty reporting a bunch of these errors
# error[invalid-argument-type]: Argument to function `ensure_int` is incorrect
#    --> src/tims_cli_tools/tims_invoice_transformer.py:215:13
#     |
# 213 |         if col_name == field.EXTRA_CANS and ensure_int(
# 214 |             number=col_value,
# 215 |             col_name=col_name,
#     |             ^^^^^^^^^^^^^^^^^ Expected `str`, found `Hashable`
# 216 |             row=row,
# 217 |         ):
#     |
# info: Function defined here
#   --> src/tims_cli_tools/tims_invoice_transformer.py:48:5
#    |
# 48 | def ensure_int(*, number=None, col_name: str, row: pd.Series) -> bool:
#    |     ^^^^^^^^^^                 ------------- Parameter declared here
# 49 |     """Make sure col with expected integers have a legit value."""
# 50 |     try:
#    |
# info: rule `invalid-argument-type` is enabled by default
