from tims_cli_tools.classes import HVTColumnProcessor


def test_HVTColumnProcessor(df_series_input_cols):
    expected = {
        "BU": 22222222,
        "DESCRIPTION": "Height Verification",
        "QUANTITY": 1,
        "SUB CATEGORY": "ADDER",
    }
    assert HVTColumnProcessor(row=df_series_input_cols).get_derived_row() == expected
