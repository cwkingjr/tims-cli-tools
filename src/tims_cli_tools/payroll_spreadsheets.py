import pandas as pd

from .payroll_writers import (
    XlsxConsolidatedSpreadsheetWriter,
    XlsxIndividualSpreadsheetWriter,
)


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
    writer = XlsxConsolidatedSpreadsheetWriter()
    writer.write(
        original_df=original_df,
        all_payments_df=all_payments_df,
        all_payments_totals_df=all_payments_totals_df,
        payee_tuples=payee_tuples,
    )


def write_individual_spreadsheet(
    *,
    pay_to_name: str,
    individual_payments_totals_df: pd.DataFrame,
    individual_payments_df: pd.DataFrame,
) -> None:
    """Creates a single individual's spreadsheet for their own record."""
    writer = XlsxIndividualSpreadsheetWriter()
    writer.write(
        pay_to_name=pay_to_name,
        individual_payments_totals_df=individual_payments_totals_df,
        individual_payments_df=individual_payments_df,
    )
