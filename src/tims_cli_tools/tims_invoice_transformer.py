# Using billing export spreadsheet, generate an intermediate reformatted spreadsheet
# in a format conducive to pasting into a copy of the submission template spreadsheet.

import sys
from datetime import datetime
import pytz
import pandas as pd
from . import field, desc, price, subcat


def check_for_required_fields(df: pd.DataFrame) -> None:
    """Check if all required fields are present in the DataFrame."""
    missing_fields = set(field.REQUIRED_FIELDS) - set(df.columns)
    if missing_fields:
        raise ValueError("Missing required fields: " + ", ".join(missing_fields))


def get_new_row(*, bu: int, subcat: str, desc: str, qty: int = 1, sortby: int) -> dict:
    """Create a new temporary row with the given info."""
    tmp_row = {
        field.BU: bu,
        field.SUB_CATEGORY: subcat,
        field.DESCRIPTION: desc,
        field.QUANTITY: qty,
        field.SORT_BY: sortby,  # increment sort order
    }
    return tmp_row


def create_derived_rows_df(row: pd.Series) -> pd.DataFrame:
    """Create derived rows based on the input row."""
    current_bu = None
    current_sort_by = None
    while current_bu is None or current_sort_by is None:
        for colname, colvalue in row.items():
            if colname == field.SORT_BY:
                current_sort_by = colvalue
            elif colname == field.BU:
                current_bu = colvalue

    new_rows = []

    for col_name, col_value in row.items():
        if col_name == field.HVF and col_value > 0:
            current_sort_by += 1
            tmp_row = get_new_row(
                bu=current_bu,
                subcat=subcat.ADDER,
                desc=desc.HEIGHT_VERIF,
                sortby=current_sort_by,
            )
            new_rows.append(tmp_row)

        if col_name == field.LIGHT_INSP and col_value > 0:
            current_sort_by += 1
            tmp_row = get_new_row(
                bu=current_bu,
                subcat=subcat.ADDER,
                desc=desc.LIGHT_INSP,
                sortby=current_sort_by,
            )
            new_rows.append(tmp_row)

        if col_name == field.MIG_BIRD and col_value > 0:
            current_sort_by += 1
            tmp_row = get_new_row(
                bu=current_bu,
                subcat=subcat.ADDER,
                desc=desc.BIRD_WATCH,
                sortby=current_sort_by,
            )
            new_rows.append(tmp_row)

        if col_name == field.WINDSIM and col_value > 0:
            current_sort_by += 1
            tmp_row = get_new_row(
                bu=current_bu,
                subcat=subcat.ADDER,
                desc=desc.WINDSIM,
                sortby=current_sort_by,
            )
            new_rows.append(tmp_row)

        if col_name == field.TTP_INIT_READ and col_value > 0:
            current_sort_by += 1
            tmp_row = get_new_row(
                bu=current_bu,
                subcat=subcat.ADDER,
                desc=desc.GUY_TTP_INIT,
                sortby=current_sort_by,
            )
            new_rows.append(tmp_row)

        if col_name == field.TENSION and col_value > 0:
            current_sort_by += 1

            # get a temp row and just change the desc below
            tmp_row = get_new_row(
                bu=current_bu,
                subcat=subcat.ADDER,
                desc=desc.GUY_TTP_1_6,
                sortby=current_sort_by,
            )

            # set the correct desc
            if col_value == price.PRICE_700:
                tmp_row[field.DESCRIPTION] = desc.GUY_TTP_1_6
            elif col_value == price.PRICE_850:
                tmp_row[field.DESCRIPTION] = desc.GUY_TTP_7_12
            elif col_value == price.PRICE_1000:
                tmp_row[field.DESCRIPTION] = desc.GUY_TTP_12_PLUS
            else:
                unknown_tension_value = f"Unexpected Tension Price value: {col_value}."
                raise ValueError(unknown_tension_value)
            new_rows.append(tmp_row)

        if col_name == field.MAINT and col_value is not None:
            # convert the value to an integer representing minutes
            try:
                # convert time object to total minutes
                total_minutes = col_value.hour * 60 + col_value.minute
            except ValueError as e:
                maintenance_value_error = f"Unexpected {field.MAINT} value format: {col_value}. Expected 'H:MM' time format."
                raise ValueError(maintenance_value_error) from e
            if total_minutes > 0:  # only create a row if there are minutes to bill
                current_sort_by += 1
                tmp_row = get_new_row(
                    bu=current_bu,
                    subcat=subcat.ADDER,
                    desc=desc.MAINT_MIN_RATE,
                    qty=total_minutes,
                    sortby=current_sort_by,
                )
                new_rows.append(tmp_row)

        if col_name == field.EXTRA_CANS and col_value > 0:
            # set the quantity to the number of extra cans (value)
            current_sort_by += 1
            tmp_row = get_new_row(
                bu=current_bu,
                subcat=subcat.BASE,
                desc=desc.ADDITIONAL_CAN,
                qty=col_value,
                sortby=current_sort_by,
            )
            new_rows.append(tmp_row)

        if col_name == field.MAN_LIFT and col_value > 0:
            current_sort_by += 1
            tmp_row = get_new_row(
                bu=current_bu,
                subcat=subcat.WORK_AUTH,
                desc=desc.MANLIFT_RENTAL,
                sortby=current_sort_by,
            )
            new_rows.append(tmp_row)

        new_df = pd.DataFrame(new_rows)

    # return dataframe with all the derived rows
    return new_df


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input_file>")
        sys.exit(1)

    timezone_name = "US/Central"
    # Create a tzinfo object from the timezone name
    tz = pytz.timezone(timezone_name)

    in_file = sys.argv[1]
    input_df = pd.read_excel(in_file)

    check_for_required_fields(input_df)

    # typically the provided spreadsheet has more columns than we need, so we select only the ones we need
    wanted_df = input_df[field.REQUIRED_FIELDS]

    # rename columns to match the submission template
    wanted_df = wanted_df.rename(
        columns={
            "Base for Inv.": field.DESCRIPTION,
            "Additional Canister Level": field.ADD_CAN,
            "HVF ": field.HVF,  # remove trailing space
        },
    )

    # add a "SUB CATEGORY" column with a constant value of "BASE"
    wanted_df[field.SUB_CATEGORY] = subcat.BASE

    # add a "QUANTITY" column with a constant value of 1
    wanted_df[field.QUANTITY] = 1

    # sort the rows by the "BU" column
    # this is critical to ensure that the derived rows are grouped with their parent row and everything is in a predictable order
    wanted_df = wanted_df.sort_values(by=[field.BU])
    # add a "SORT_BY" column using a series of integers starting at 1000000 and incrementing by 100
    # this allows us to insert derived rows in between the base rows later
    wanted_df[field.SORT_BY] = range(1000000, 1000000 + 100 * len(wanted_df), 100)

    # add an "EXTRA_CANS" column that includes the value from the "Additional Canister Level" column only if that column includes an integer value
    # the first can is part of the base price, so we subtract 1 from the value
    wanted_df[field.EXTRA_CANS] = wanted_df[field.STRUCTURE].apply(
        lambda x: x - 1 if isinstance(x, int) and x - 1 > 0 else None,
    )

    # reorder the columns to match the submission template
    wanted_df = wanted_df[field.OUTPUT_COLUMNS]

    # now that we have the original data straightened out, let's get on with creating the derived rows

    # iterate the rows and build new subordinate rows based upon the data in the pertinent columns
    for _, row in wanted_df.iterrows():
        row_df = create_derived_rows_df(row)
        if not row_df.empty:
            wanted_df = pd.concat([wanted_df, row_df], ignore_index=True)

    wanted_df = wanted_df.sort_values(by=[field.SORT_BY], ascending=True)

    # if the infile is a path, get the path portion
    if "/" in in_file:
        out_file = (
            in_file.split("/")[-1]
            .strip()
            .replace(" ", "_")
            .replace(
                ".xlsx",
                f"_transformed_{datetime.now(tz=tz).strftime('%Y%m%d_%H%M%S')}.xlsx",
            )
        )
    else:
        # if the infile is just a filename
        out_file = (
            in_file.strip()
            .replace(" ", "_")
            .replace(
                ".xlsx",
                f"_transformed_{datetime.now(tz=tz).strftime('%Y%m%d_%H%M%S')}.xlsx",
            )
        )

    wanted_df.to_excel(
        out_file,
        index=False,
    )
