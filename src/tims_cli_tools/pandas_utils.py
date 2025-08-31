import pandas as pd
from rich.pretty import pprint


def check_for_required_fields(
    *, required_fields: list[str], pd_df: pd.DataFrame
) -> None:
    """Check if all required fields are present in the DataFrame."""
    required_field_set = set(required_fields)
    df_columns_set = set(pd_df.columns.to_list())
    missing_fields = required_field_set - df_columns_set
    if missing_fields:
        raise ValueError("Missing required fields: " + ", ".join(missing_fields))


def get_value_from_series_col(*, series: pd.Series, column_name: str):
    """Iterates the series to find the column name and returns the value.

    Raises ValueError if the column value isn't found.
    """
    mylist = [
        col_value for (col_name, col_value) in series.items() if col_name == column_name
    ]
    if not mylist:
        msg = f"Could not find value for column '{column_name}' in {series}"
        raise ValueError(msg)

    return mylist[0]


def pprint_as_dataframe(*, message=None, content) -> None:
    """Pretty Prints message if provided, then content as pd.Dataframe."""
    if message:
        pprint(message)
    pprint(pd.DataFrame(data=content))
