import pytest
from tims_cli_tools.ensure import (
    ensure_data_type,
    ensure_float,
    ensure_int,
    ensure_money,
    float_to_money_str,
    any_numeric_representation_to_float,
)


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


def test_ensure_money_valid(df_series_input_cols):
    result = ensure_money(number="$1,234.56", col_name="TEST", row=df_series_input_cols)
    assert result == True


@pytest.mark.parametrize(
    "testvalue, expected",
    [
        ("$1,234.56", 1234.56),
        ("1,234.56", 1234.56),
        ("234.56", 234.56),
        ("234.500000", 234.5),
        (1234, 1234.0),
        (1234.50, 1234.5),
    ],
)
def test_any_numeric_representation_to_float(testvalue, expected):
    assert any_numeric_representation_to_float(testvalue) == expected


def test_float_to_money_str():
    assert float_to_money_str(1000.00) == "1,000.00"
