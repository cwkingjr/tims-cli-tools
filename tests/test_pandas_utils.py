from tims_cli_tools.pandas_utils import check_for_required_fields
from tims_cli_tools import field
import pytest


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
