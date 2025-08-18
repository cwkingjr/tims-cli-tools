from toolz import curry
import pandas as pd


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
ensure_int = ensure_data_type(data_type="integer", func=int)
