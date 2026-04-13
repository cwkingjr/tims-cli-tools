from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
import pandas as pd
from rich.pretty import pprint
import argparse
import io
import json

from . import (
    file_utils,
    payroll_toml_json_schema,
    payroll_toml_validations as ptv,
)
from .invoice_transform import add_extra_cans_column
from .payroll_config import PayrollConfig
from .payroll_classes import Crews, build_crews, build_additional_pay
from .payroll_calculations import PayrollCalculator, extract_payment_input
from .payroll_repository import PaymentRepository, create_repository
from .payroll_writers import (
    ConsolidatedSpreadsheetWriter,
    IndividualSpreadsheetWriter,
    XlsxConsolidatedSpreadsheetWriter,
    XlsxIndividualSpreadsheetWriter,
)
from .payroll_classes import AdditionalPay
from .readers import DataFrameReader, PandasExcelReader


@dataclass
class ProcessPayrollConfig:
    input_df: pd.DataFrame
    crews: Crews
    additional_pay: AdditionalPay
    repository: PaymentRepository
    create_crew_spreadsheets: bool
    consolidated_writer: ConsolidatedSpreadsheetWriter
    individual_writer: IndividualSpreadsheetWriter | None = None


def process_payroll(config: ProcessPayrollConfig) -> None:
    calculator = PayrollCalculator(
        crews=config.crews, additional_pay=config.additional_pay
    )

    for _, row in config.input_df.iterrows():
        input_data = extract_payment_input(row)

        lead_payment = calculator.calculate_lead_payment(input_data)
        config.repository.insert(lead_payment)

        second_payment = calculator.calculate_second_payment(input_data)
        config.repository.insert(second_payment)

    all_payments_df = config.repository.get_all()
    all_payments_totals = config.repository.get_all_totals()
    payee_tuples = [
        config.repository.get_by_payee(pay_to=crew.lead.name)
        for crew in config.crews.crews
    ] + [
        config.repository.get_by_payee(pay_to=crew.second.name)
        for crew in config.crews.crews
    ]

    config.consolidated_writer.write(
        original_df=config.input_df,
        all_payments_df=all_payments_df,
        all_payments_totals_df=all_payments_totals,
        payee_tuples=payee_tuples,
    )

    if config.create_crew_spreadsheets and config.individual_writer is not None:
        for payee_name, payee_df in payee_tuples:
            individual_totals = config.repository.get_individual_totals(
                pay_to=payee_name
            )
            config.individual_writer.write(
                pay_to_name=payee_name,
                individual_payments_totals_df=individual_totals,
                individual_payments_df=payee_df,
            )


def run(
    input_path: str,
    config: PayrollConfig | None = None,
    consolidated_writer: ConsolidatedSpreadsheetWriter | None = None,
    individual_writer: IndividualSpreadsheetWriter | None = None,
    reader: DataFrameReader | None = None,
) -> None:
    if config is None:
        config = PayrollConfig()
    if consolidated_writer is None:
        consolidated_writer = XlsxConsolidatedSpreadsheetWriter()
    if reader is None:
        reader = PandasExcelReader()

    pprint("Starting tims_payroll.")

    input_path_obj = Path(input_path)
    if not input_path_obj.is_file():
        msg = f"Error: The input-path '{input_path}' is not a valid file path."
        raise FileNotFoundError(msg)

    input_df = reader.read_excel(input_path)

    pprint(f"Loading config file data from {config.config_file}.")
    toml_data = file_utils.get_toml_data(config_path=config.config_file)
    json_schema = json.load(io.StringIO(payroll_toml_json_schema.JSON_SCHEMA_STR))

    pprint("Validating config file against config file data schema.")
    file_utils.validate_toml_data(toml_data=toml_data, json_schema=json_schema)

    create_crew_spreadsheets = ptv.get_create_crew_spreadsheets(
        create_crew_spreadsheets=toml_data["processing_info"][
            "create_crew_spreadsheets"
        ]
    )

    ptv.verify_crew_lead_pay_types_are_valid(crew_leads=toml_data["crew_lead"])
    ptv.verify_crew_second_pay_types_are_valid(crew_seconds=toml_data["crew_second"])
    ptv.verify_crew_leads_listed_in_seconds_exist(
        crew_seconds=toml_data["crew_second"], crew_leads=toml_data["crew_lead"]
    )
    ptv.verify_same_number_of_leads_and_seconds(
        crew_seconds=toml_data["crew_second"], crew_leads=toml_data["crew_lead"]
    )
    ptv.verify_no_duplicate_second_names(crew_seconds=toml_data["crew_second"])
    ptv.verify_no_duplicate_lead_names(crew_leads=toml_data["crew_lead"])
    ptv.verify_no_duplicate_second_crew_lead_names(
        crew_seconds=toml_data["crew_second"]
    )

    crews = build_crews(
        config_crew_leads=toml_data["crew_lead"],
        config_crew_seconds=toml_data["crew_second"],
        config_pay_types=toml_data["pay_type"],
    )
    pprint("Found config data for these crews:")
    pprint(crews)

    additional_pay = build_additional_pay(config_add_pay=toml_data["additional_pay"])
    pprint("Found config data for these additional pay rates:")
    pprint(additional_pay)

    input_df = add_extra_cans_column(input_df)

    repository = create_repository(config.db_file)

    if create_crew_spreadsheets and individual_writer is None:
        individual_writer = XlsxIndividualSpreadsheetWriter()

    try:
        pprint("Writing consolidated payroll spreadsheet to your Documents folder.")
        process_payroll(
            ProcessPayrollConfig(
                input_df=input_df,
                crews=crews,
                additional_pay=additional_pay,
                repository=repository,
                create_crew_spreadsheets=create_crew_spreadsheets,
                consolidated_writer=consolidated_writer,
                individual_writer=individual_writer,
            )
        )
    finally:
        repository.close()
        with suppress(OSError):
            config.db_file.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read input file from path and generate payroll spreadsheets.",
    )
    parser.add_argument(
        "-i",
        "--input-path",
        type=str,
        required=True,
        help="Path to the xlsx input spreadsheet.",
    )

    args = parser.parse_args()
    run(args.input_path)
