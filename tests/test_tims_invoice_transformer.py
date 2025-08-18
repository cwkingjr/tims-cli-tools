import pytest
from tims_cli_tools.ensure import ensure_data_type, ensure_float, ensure_int
from tims_cli_tools.tims_invoice_transformer import (
    check_for_required_fields,
    # create_cleaned_filepath,
    get_value_from_series_col,
    # build_new_rows_from_dataframe_col_values,
)
from tims_cli_tools import field

TWOS = 22222222  # shut up linter


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


def test_get_value_from_series_col(df_series_input_cols):
    assert (
        get_value_from_series_col(series=df_series_input_cols, field_name=field.BU)
        == TWOS
    )


def test_get_value_from_series_col_missing_col(df_series_input_cols):
    del df_series_input_cols[field.BU]
    with pytest.raises(ValueError):
        get_value_from_series_col(series=df_series_input_cols, field_name=field.BU)


def test_ensure_data_type_int(df_series_input_cols):
    result = ensure_data_type(
        data_type="int", func=int, number=5, col_name="TEST", row=df_series_input_cols
    )
    assert result == True


def test_ensure_data_type_invalid_convert_raises(df_series_input_cols):
    with pytest.raises(ValueError):
        ensure_data_type(
            data_type="int",
            func=int,
            number="blahblah",
            col_name="TEST",
            row=df_series_input_cols,
        )


def test_ensure_data_type_valid_convert(df_series_input_cols):
    result = ensure_data_type(
        data_type="float",
        func=float,
        number=5.0,
        col_name="TEST",
        row=df_series_input_cols,
    )
    assert result == True


def test_ensure_int_valid(df_series_input_cols):
    result = ensure_int(number=5, col_name="TEST", row=df_series_input_cols)
    assert result == True


def test_ensure_float_valid(df_series_input_cols):
    result = ensure_float(number=5, col_name="TEST", row=df_series_input_cols)
    assert result == True


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
