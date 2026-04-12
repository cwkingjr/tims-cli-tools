import pytest

from tims_cli_tools.invoice_transform import get_value_from_series_col
from tims_cli_tools import field


def test_get_value_from_series_col(df_series_input_cols, eight_twos):
    assert (
        get_value_from_series_col(series=df_series_input_cols, field_name=field.BU)
        == eight_twos
    )


def test_get_value_from_series_col_missing_col(df_series_input_cols):
    del df_series_input_cols[field.BU]
    with pytest.raises(ValueError):
        get_value_from_series_col(series=df_series_input_cols, field_name=field.BU)
