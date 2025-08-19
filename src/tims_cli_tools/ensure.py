from toolz import curry
import pandas as pd


def any_numeric_representation_to_float(value) -> float:
    """Just need a way to ensure we can compare incoming column values as numbers."""
    if isinstance(value, float):
        return value
    elif isinstance(value, int):
        return float(value)
    elif isinstance(value, str):
        value = value.replace("$", "").replace(",", "")
        return float(value)
    else:
        msg = f"Got non int, float, or money_str of {value}."
        raise ValueError(msg)


def money_str_to_float(money: str) -> float:
    """Remove `$,` and convert to float.

    Use this after calling ensure_money to ensure you won't raise error here.

    Float is not dangerous in this instance as we only ever
    deal with values to two decimal places (1,234.56).
    """
    if isinstance(money, str):
        float(money.replace("$", "").replace(",", ""))
    elif isinstance(money, int | float):
        float(money)


@curry
def ensure_data_type(*, data_type, func, number, col_name: str, row: pd.Series) -> bool:
    """Make sure col with expected ints/floats have a legit value."""
    try:
        func(number)
    except ValueError as e:
        msg = f"Whoops, was expecting a {data_type} value in col '{col_name}' but got '{number}' on row:\n{row}"
        raise ValueError(msg) from e
    else:
        return True


# curried functions
ensure_float = ensure_data_type(data_type="float", func=float)
ensure_int = ensure_data_type(data_type="int", func=int)
ensure_money = ensure_data_type(data_type="money_str", func=money_str_to_float)


# maybe shouldn't live here, but since we have to go from str to float
# to validate money cols, we need to be able to get back
def float_to_money_str(money: float) -> str:
    """Convert float to a money str reprensentation (1,234.56)

    Leaving off $ because it is not needed on paste and just makes it harder
    to validate generated spreadsheet.
    """
    return f"{money:,.2f}"  # float with commas and two decimal places
