import pandas as pd
from . import file_utils


def write_consolidated_spreadsheet(
    *,
    original_df: pd.DataFrame,
    all_payments_df: pd.DataFrame,
    all_payments_totals_df: pd.DataFrame,
    payee_tuples,
) -> None:
    """Creates a consolidated spreadsheet.

    Spreadsheet will be dumped to documents folder and contain the original input data on one worksheet,
    all the payments table data on one worksheet, and an individual worksheet for each crew
    member with payments in the pay_to column of the database.
    """
    file_path = file_utils.create_new_spreadsheet_central_tz_filepath(
        filename_prefix="payroll_consolidated"
    )

    with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
        original_df.to_excel(writer, sheet_name="Original Data", index=False)
        all_payments_totals_df.to_excel(
            writer, sheet_name="All Payments Totals", index=False
        )
        all_payments_df.to_excel(writer, sheet_name="All Payments", index=False)
        for one_payee_tuple in payee_tuples:
            payee, df = one_payee_tuple
            df.to_excel(writer, sheet_name=payee, index=False)


def write_individual_spreadsheet(
    *,
    pay_to_name: str,
    individual_payments_totals_df: pd.DataFrame,
    individual_payments_df: pd.DataFrame,
) -> None:
    """Creates a single individual's spreadsheet for their own record."""
    clean_payto = pay_to_name.lower().replace(" ", "_")
    file_path = file_utils.create_new_spreadsheet_central_tz_filepath(
        filename_prefix=f"payroll_{clean_payto}"
    )

    with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
        individual_payments_totals_df.to_excel(
            writer, sheet_name="Payment Totals", index=False
        )
        individual_payments_df.to_excel(writer, sheet_name="Payments", index=False)
