from tims_cli_tools.classes import HVFColumnProcessor


def test_HVFColumnProcessor(df_series_input_cols):
    expected = {
        "BU": 22222222,
        "DESCRIPTION": "Height Verification",
        "QUANTITY": 1,
        "SUB CATEGORY": "ADDER",
    }
    assert HVFColumnProcessor(row=df_series_input_cols).get_derived_row() == expected
