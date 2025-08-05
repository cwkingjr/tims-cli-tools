# Using billing export spreadsheet, generate an intermediate reformatted spreadsheet
# in a format conducive to pasting into a copy of the submission template spreadsheet.

import sys
from datetime import datetime
import pytz

import pandas as pd

# Fields/columns used for processing
REQUIRED_FIELDS = [
    "BU",
    "Base for Inv.",
    "Structure",
    "TIA Inspection",
    "Additional Canister Level",
    "HVF ",  # note the trailing space in the column name
    "Lighting Inspection Price",
    "Migratory Bird",
    "Windsim",
    "TTP Initial Reading Price",
    "Tension Price",
    "HR.PAY",
    "Site Total",
    "MAINTENANCE",
    "Manlift Charge",
]

OUTPUT_COLUMNS = [
    "SORT_BY",
    "BU",
    "SUB CATEGORY",
    "DESCRIPTION",
    "QUANTITY",
    "TIA Inspection",
    "Additional Canister Price",
    "HVF",  # Note: no trailing space
    "Lighting Inspection Price",
    "Migratory Bird",
    "Windsim",
    "TTP Initial Reading Price",
    "Tension Price",
    "HR.PAY",
    "Site Total",
    "MAINTENANCE",
    "Manlift Charge",
    "Structure",  # leave this column so user can see what we the extra cans source data
    "EXTRA_CANS",  # leave this column so the user can see how many extra cans we derived
]


def check_for_required_fields(df: pd.DataFrame) -> None:
    """Check if all required fields are present in the DataFrame."""
    missing_fields = set(REQUIRED_FIELDS) - set(df.columns)
    if missing_fields:
        raise ValueError("Missing required fields: " + ", ".join(missing_fields))


def get_new_tmp_row(bu: int, subcat: str, desc: str, sortby: int) -> dict:
    """Create a new temporary row with the given info."""
    tmp_row = {
        "BU": bu,
        "SUB CATEGORY": subcat,
        "DESCRIPTION": desc,
        "QUANTITY": 1,
        "SORT_BY": sortby,  # increment sort order
    }
    return tmp_row


def create_derived_rows_df(row) -> pd.DataFrame:
    """Create derived rows based on the input row."""
    current_bu = None
    current_sort_by = None
    while current_bu is None or current_sort_by is None:
        for colname, colvalue in row.items():
            if colname == "SORT_BY":
                current_sort_by = colvalue
            elif colname == "BU":
                current_bu = colvalue

    # create a new DataFrame to hold the derived rows
    created_df = pd.DataFrame(columns=OUTPUT_COLUMNS)

    for colname, value in row.items():
        if colname == "HVF" and value > 0:
            current_sort_by += 1
            tmp_row = get_new_tmp_row(
                current_bu, "ADDER", "Height Verification", current_sort_by
            )
            new_df = pd.DataFrame([tmp_row])
            # Add the tmp_row to the created_df
            created_df = pd.concat([created_df, new_df], ignore_index=True)

        if colname == "Lighting Inspection Price" and value > 0:
            current_sort_by += 1
            tmp_row = get_new_tmp_row(
                current_bu, "ADDER", "Lighting Inspection", current_sort_by
            )
            new_df = pd.DataFrame([tmp_row])
            created_df = pd.concat([created_df, new_df], ignore_index=True)

        if colname == "Migratory Bird" and value > 0:
            current_sort_by += 1
            tmp_row = get_new_tmp_row(
                current_bu, "ADDER", "Bird Watch", current_sort_by
            )
            new_df = pd.DataFrame([tmp_row])
            created_df = pd.concat([created_df, new_df], ignore_index=True)

        if colname == "Windsim" and value > 0:
            current_sort_by += 1
            tmp_row = get_new_tmp_row(current_bu, "ADDER", "Windsim", current_sort_by)
            new_df = pd.DataFrame([tmp_row])
            created_df = pd.concat([created_df, new_df], ignore_index=True)

        if colname == "TTP Initial Reading Price" and value > 0:
            current_sort_by += 1
            tmp_row = get_new_tmp_row(
                current_bu,
                "ADDER",
                "Guy Wire Tension Twist & Plumb Initial Readings",
                current_sort_by,
            )
            new_df = pd.DataFrame([tmp_row])
            created_df = pd.concat([created_df, new_df], ignore_index=True)

        if colname == "Tension Price" and value > 0:
            current_sort_by += 1
            if value == 700:
                tmp_row = get_new_tmp_row(
                    current_bu,
                    "ADDER",
                    "Tension, Twist & Plumb Adjustments on 1-6 Guy Wires",
                    current_sort_by,
                )
            elif value == 850:
                tmp_row = get_new_tmp_row(
                    current_bu,
                    "ADDER",
                    "Tension, Twist & Plumb Adjustments on 7-12 Guy Wires",
                    current_sort_by,
                )
            elif value == 1000:
                tmp_row = get_new_tmp_row(
                    current_bu,
                    "ADDER",
                    "Tension, Twist & Plumb Adjustments on 12 or more Guy Wires",
                    current_sort_by,
                )
            else:
                unknown_tension_value = f"Unexpected Tension Price value: {value}. Only 700, 850, or 1000 are expected."
                raise ValueError(unknown_tension_value)
            new_df = pd.DataFrame([tmp_row])
            created_df = pd.concat([created_df, new_df], ignore_index=True)

        if colname == "MAINTENANCE" and value is not None:
            # convert the value to an integer representing minutes
            try:
                # convert time object to total minutes
                total_minutes = value.hour * 60 + value.minute
            except ValueError as e:
                maintenance_value_error = f"Unexpected MAINTENANCE value format: {value}. Expected 'H:MM' time format."
                raise ValueError(maintenance_value_error) from e
            if total_minutes > 0:  # only create a row if there are minutes to bill
                current_sort_by += 1
                tmp_row = get_new_tmp_row(
                    current_bu, "ADDER", "Maintenance Minute Rate", current_sort_by
                )
                tmp_row["QUANTITY"] = total_minutes
                new_df = pd.DataFrame([tmp_row])
                created_df = pd.concat([created_df, new_df], ignore_index=True)

        if colname == "Manlift Charge" and value > 0:
            current_sort_by += 1
            tmp_row = get_new_tmp_row(
                current_bu,
                "WORK AUTHORIZATION",
                "Manlift Rental Cost",
                current_sort_by,
            )
            new_df = pd.DataFrame([tmp_row])
            created_df = pd.concat([created_df, new_df], ignore_index=True)

    # return dataframe with all the derived rows
    return created_df


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
    wanted_df = input_df[REQUIRED_FIELDS]

    # rename columns to match the submission template
    wanted_df = wanted_df.rename(
        columns={
            "Base for Inv.": "DESCRIPTION",
            "Additional Canister Level": "Additional Canister Price",
            "HVF ": "HVF",  # remove trailing space
        },
    )

    # add a "SUB CATEGORY" column with a constant value of "BASE"
    wanted_df["SUB CATEGORY"] = "BASE"

    # add a "QUANTITY" column with a constant value of 1
    wanted_df["QUANTITY"] = 1

    # sort the rows by the "BU" column
    # this is critical to ensure that the derived rows are grouped with their parent row and everything is in a predictable order
    wanted_df = wanted_df.sort_values(by=["BU"])
    # add a "SORT_BY" column using a series of integers starting at 1000000 and incrementing by 100
    # this allows us to insert derived rows in between the base rows later
    wanted_df["SORT_BY"] = range(1000000, 1000000 + 100 * len(wanted_df), 100)

    # add an "EXTRA_CANS" column that includes the value from the "Additional Canister Level" column only if that column includes an integer value
    # the first can is part of the base price, so we subtract 1 from the value
    wanted_df["EXTRA_CANS"] = wanted_df["Structure"].apply(
        lambda x: x - 1 if isinstance(x, int) and x - 1 > 0 else None,
    )

    # reorder the columns to match the submission template
    wanted_df = wanted_df[OUTPUT_COLUMNS]

    # now that we have the original data straightened out, let's get on with creating the derived rows

    # iterate the rows and build new subordinate rows based upon the data in the pertinent columns
    for _, row in wanted_df.iterrows():
        row_df = create_derived_rows_df(row)
        if not row_df.empty:
            wanted_df = pd.concat([wanted_df, row_df], ignore_index=True)

    wanted_df = wanted_df.sort_values(by=["SORT_BY"], ascending=True)

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
