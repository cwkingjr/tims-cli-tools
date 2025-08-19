# Using billing export spreadsheet, generate an intermediate reformatted spreadsheet
# in a format conducive to pasting into a copy of the submission template spreadsheet.

import sys
from datetime import datetime
from pathlib import Path
import pandas as pd
import pytz
from rich.pretty import pprint

from . import desc, field, subcat, classes


def check_for_required_fields(
    *, required_fields: list[str], pd_df: pd.DataFrame
) -> None:
    """Check if all required fields are present in the DataFrame."""
    required_field_set = set(required_fields)
    df_columns_set = set(pd_df.columns.to_list())
    missing_fields = required_field_set - df_columns_set
    if missing_fields:
        raise ValueError("Missing required fields: " + ", ".join(missing_fields))


def get_new_row(*, bu: int, subcat: str, desc: str, qty: int = 1) -> dict:
    """Create a new temporary row with the given info."""
    tmp_row = {
        field.BU: bu,
        field.SUB_CATEGORY: subcat,
        field.DESCRIPTION: desc,
        field.QUANTITY: qty,
    }
    return tmp_row


def get_value_from_series_col(*, series: pd.Series, field_name: str):
    mylist = [
        col_value for (col_name, col_value) in series.items() if col_name == field_name
    ]
    if not mylist:
        msg = f"Could not find value for field {field_name} in {series}"
        raise ValueError(msg)
    return mylist[0]


def build_new_rows_from_dataframe_col_values(*, dataframe: pd.DataFrame) -> list[dict]:
    """Creates a list of new row dicts.

    Dict keys included only the 4-5 cols needed for the derived rows. Dict values are
    based on source data column-specific processing rules and the values in those source columns.
    """
    # iterate the rows and build new subordinate rows based upon the data in the pertinent columns
    all_new_rows = []
    for _, row in dataframe.iterrows():
        one_rows_new_rows = create_derived_rows_list(row)
        if one_rows_new_rows:
            all_new_rows.extend(one_rows_new_rows)
    return all_new_rows


def create_cleaned_filepath(
    *,
    in_path=Path,
    filename_prefix: str,
    dt_with_tz: datetime,
    dt_format_str="%Y%m%d_%H%M%S",
) -> Path:
    """Create a new filepath with cleaned up and appended filename."""
    path = Path(in_path)
    filename_no_extension = path.stem
    filename_extension = path.suffix
    path_parent = path.parent
    add_to_filename = f"_{filename_prefix}_{dt_with_tz.strftime(dt_format_str)}"
    cleaned_filename = filename_no_extension.strip().replace(" ", "_")
    new_filename = cleaned_filename + add_to_filename + filename_extension
    cleaned_full_path = path_parent / new_filename
    return cleaned_full_path


def create_derived_rows_list(row: pd.Series) -> list[dict]:  # noqa: PLR0912
    """Create derived rows based on the input row."""

    current_bu = get_value_from_series_col(series=row, field_name=field.BU)
    current_sort_by = get_value_from_series_col(series=row, field_name=field.SORT_BY)

    new_rows = []

    # Drop the NAN columns from the Series so we don't process them
    # NOTE: This keeps the column processors from raising a ValueError for
    # getting called on a column with no value, and by not calling them, we don't
    # get bogus extra rows added for empty columns!!
    # WARNING: Do not remove!
    row = row.dropna()

    for col_name, col_value in row.items():
        if col_name == field.HVF_NO_SPACE:
            new_rows.append(classes.HVFColumnProcessor(row=row).get_derived_row())

        if col_name == field.LIGHT_INSP:
            new_rows.append(
                classes.LIGHT_INSPColumnProcessor(row=row).get_derived_row()
            )

        if col_name == field.MIG_BIRD:
            new_rows.append(classes.MIG_BIRDColumnProcessor(row=row).get_derived_row())

        if col_name == field.WINDSIM:
            new_rows.append(classes.WINDSIMColumnProcessor(row=row).get_derived_row())

        if col_name == field.TTP_INIT_READ:
            new_rows.append(
                classes.TTP_INIT_READColumnProcessor(row=row).get_derived_row()
            )

        if col_name == field.TENSION:
            new_rows.append(classes.TENSIONColumnProcessor(row=row).get_derived_row())

        if col_name == field.MAINT:
            # convert the value to an integer representing minutes
            try:
                # convert time object to total minutes
                total_minutes = col_value.hour * 60 + col_value.minute
            except ValueError as e:
                maintenance_value_error = f"Unexpected {field.MAINT} value format: {col_value}. Expected 'H:MM' time format."
                raise ValueError(maintenance_value_error) from e
            if total_minutes > 0:  # only create a row if there are minutes to bill
                tmp_row = get_new_row(
                    bu=current_bu,
                    subcat=subcat.ADDER,
                    desc=desc.MAINT_MIN_RATE,
                    qty=total_minutes,
                )
                new_rows.append(tmp_row)

        if col_name == field.EXTRA_CANS:
            new_rows.append(
                classes.EXTRA_CANSColumnProcessor(row=row).get_derived_row()
            )

        if col_name == field.MAN_LIFT:
            new_rows.append(classes.MAN_LIFTColumnProcessor(row=row).get_derived_row())

    # once we have the new rows, sort them by the subcategory and description
    new_rows.sort(key=lambda x: (x[field.SUB_CATEGORY], x[field.DESCRIPTION]))

    # after sort, add the sortby value to each new row
    for one_row in new_rows:
        current_sort_by += 1
        one_row[field.SORT_BY] = current_sort_by

    return new_rows


def main() -> None:
    if len(sys.argv) < 2:  # noqa: PLR2004
        pprint(f"Usage: {sys.argv[0]} <input_file>")
        sys.exit(1)

    in_file = sys.argv[1]
    input_df = pd.read_excel(in_file)

    check_for_required_fields(required_fields=field.REQUIRED_INPUT_COLS, pd_df=input_df)

    # typically the provided spreadsheet has more columns than we need, so we select only the ones we need
    wanted_df = input_df[field.REQUIRED_INPUT_COLS]

    # rename columns to match the submission template
    wanted_df = wanted_df.rename(
        columns={
            field.BASE_FOR_INV: field.DESCRIPTION,
            field.ADD_CAN_LEVEL: field.ADD_CAN_PRICE,
            field.HVF_WITH_SPACE: field.HVF_NO_SPACE,
        },
    )

    # add a "SUB CATEGORY" column with a constant value of "BASE"
    wanted_df[field.SUB_CATEGORY] = subcat.BASE

    # add a "QUANTITY" column with a constant value of 1
    wanted_df[field.QUANTITY] = 1

    # sort the rows by the "BU" column
    # this is critical to ensure that eventually the derived rows are grouped with their parent row and everything is in a predictable order
    wanted_df = wanted_df.sort_values(by=[field.BU])

    # add a "SORT_BY" column using a series of integers starting at 1000000 and incrementing by 100
    # this allows us to insert derived rows in between the base rows later
    wanted_df[field.SORT_BY] = range(1000000, 1000000 + 100 * len(wanted_df), 100)

    # add an "EXTRA_CANS" column that includes the value from the structure column only if that column includes an integer value
    # the first can is part of the base price, so we subtract 1 from the value
    wanted_df[field.EXTRA_CANS] = wanted_df[field.STRUCTURE].apply(
        lambda x: x - 1 if isinstance(x, int) and x - 1 > 0 else None,
    )

    # Convert column to dataframe int type that can handle NaN values as we were getting floats before
    wanted_df[field.EXTRA_CANS] = wanted_df[field.EXTRA_CANS].astype(pd.Int64Dtype())

    # reorder the columns to match the submission template
    wanted_df = wanted_df[field.OUTPUT_COLS]

    # now that we have the original data straightened out, let's get on with creating the derived rows
    # pprint(wanted_df)
    # pprint(wanted_df.dtypes)

    derived_rows = build_new_rows_from_dataframe_col_values(
        dataframe=wanted_df.copy(deep=True)
    )
    # build a dataframe so we can concat the new rows into the original rows
    derived_rows_df = pd.DataFrame(derived_rows)
    wanted_df = pd.concat([wanted_df, derived_rows_df], ignore_index=True)

    # sort the final dataframe so the rows are in the customer-specified order in the spreadsheet
    wanted_df = wanted_df.sort_values(by=[field.SORT_BY], ascending=True)

    # create an output file path based upon the old file path but with a name that indicates the
    # output has been transformed and give it a new datetime each time so user can always see
    # when it was generated
    cleaned_path = create_cleaned_filepath(
        in_path=in_file,
        filename_prefix="_transformed",
        dt_with_tz=datetime.now(tz=pytz.timezone("US/Central")),
    )

    # Create a Pandas Excel writer using XlsxWriter as the engine
    writer = pd.ExcelWriter(cleaned_path, engine="xlsxwriter")

    # Convert the DataFrame to an XlsxWriter Excel object
    wanted_df.to_excel(
        writer, sheet_name="Sheet1", index=False
    )  # index=False to avoid writing DataFrame index

    # Get the xlsxwriter workbook and worksheet objects
    workbook = writer.book
    worksheet = writer.sheets["Sheet1"]

    # Define a number format with a thousands separator and two decimal places
    # The '#,##0.00' format string specifies a comma for thousands and two decimal places
    currency_format = workbook.add_format({"num_format": "#,##0.00"})

    # Apply the format to the desired column(s)
    # worksheet.set_column("B:B", None, currency_format)
    row_width = 15
    subcat_row_width = 20
    description_row_width = 50
    worksheet.set_column(2, 2, subcat_row_width)
    worksheet.set_column(3, 3, description_row_width)
    # 5/F-14/O
    worksheet.set_column(5, 14, row_width, currency_format)
    # 16/Q
    worksheet.set_column(16, 16, row_width, currency_format)

    # Close the Pandas Excel writer and output the Excel file
    writer.close()

    pprint(f"Wrote new transformed spreadsheet at: {cleaned_path}")
