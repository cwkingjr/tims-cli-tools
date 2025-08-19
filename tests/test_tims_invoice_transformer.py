import pytest

from tims_cli_tools.tims_invoice_transformer import (
    check_for_required_fields,
    # create_cleaned_filepath,
    get_value_from_series_col,
    # build_new_rows_from_dataframe_col_values,
)
from tims_cli_tools import field


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


def test_get_value_from_series_col(df_series_input_cols, eight_twos):
    assert (
        get_value_from_series_col(series=df_series_input_cols, field_name=field.BU)
        == eight_twos
    )


def test_get_value_from_series_col_missing_col(df_series_input_cols):
    del df_series_input_cols[field.BU]
    with pytest.raises(ValueError):
        get_value_from_series_col(series=df_series_input_cols, field_name=field.BU)
