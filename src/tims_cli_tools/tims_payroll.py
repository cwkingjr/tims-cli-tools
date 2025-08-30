import sys
from datetime import datetime, time
from pathlib import Path
import pandas as pd
import pytz
from rich.pretty import pprint
from . import (
    field,
    pandas_utils,
    file_utils,
    payroll_toml_json_schema,
    payroll_toml_validations,
)
import io
import json

CONFIG_FILE = Path.home() / ".config/tims_tools/tims_payroll.toml"

# TODO: Add arg parsing for input file, maybe individual spreadsheets, config file validation only
# TODO: read input spreadsheet, grab needed columns, generate new cols
# TODO: create in-memory database, table(s)
# TODO: for each row, create db row for each crew member with zeros, then update columns based upon column processing
# TODO: create consolidated output spreadsheet
# TODO: create individual crew member spreadsheets
# TODO: refactor across apps and create/update all tests
# TODO: add justfile, coverage,
# TODO: Update all readme files


def main() -> None:  # noqa: PLR0912, PLR0915
    # if len(sys.argv) < 2:  # noqa: PLR2004
    #     pprint(f"Usage: {sys.argv[0]} <input_file>")
    #     sys.exit(1)

    # in_file = sys.argv[1]
    # input_df = pd.read_excel(in_file)

    pprint(f"Loading config file data from {CONFIG_FILE}.")
    toml_data = file_utils.get_toml_data(config_path=CONFIG_FILE)
    json_schema = json.load(io.StringIO(payroll_toml_json_schema.JSON_SCHEMA_STR))
    pprint("Validating config file against config file data schema.")
    file_utils.validate_toml_data(toml_data=toml_data, json_schema=json_schema)

    create_crew_spreadsheets = toml_data["processing_info"]["create_crew_spreadsheets"]
    process_logging = toml_data["processing_info"]["process_logging"]
    crew_leads = toml_data["crew_lead"]
    crew_seconds = toml_data["crew_second"]
    pay_types = toml_data["pay_type"]
    additional_pay = toml_data["additional_pay"]

    create_crew_spreadsheets = payroll_toml_validations.get_create_crew_spreadsheets(
        create_crew_spreadsheets=create_crew_spreadsheets
    )

    process_logging = payroll_toml_validations.get_process_logging(
        process_logging=process_logging
    )

    pprint("Checking configuration information for errors and rule violations.")
    payroll_toml_validations.print_crew_lead_info(crew_leads=crew_leads)
    payroll_toml_validations.print_crew_second_info(crew_seconds=crew_seconds)
    payroll_toml_validations.verify_crew_lead_pay_types_are_valid(crew_leads=crew_leads)
    payroll_toml_validations.verify_crew_second_pay_types_are_valid(
        crew_seconds=crew_seconds
    )
    payroll_toml_validations.verify_crew_leads_listed_in_seconds_exist(
        crew_seconds=crew_seconds, crew_leads=crew_leads
    )
    payroll_toml_validations.verify_same_number_of_leads_and_seconds(
        crew_seconds=crew_seconds, crew_leads=crew_leads
    )
    payroll_toml_validations.verify_no_duplicate_second_names(crew_seconds=crew_seconds)
    payroll_toml_validations.verify_no_duplicate_lead_names(crew_leads=crew_leads)
    payroll_toml_validations.verify_no_duplicate_second_crew_lead_names(
        crew_seconds=crew_seconds
    )

    pprint("Found these pay types:")
    pay_types_df = pd.DataFrame(data=pay_types)
    pprint(pay_types_df)

    """
    "create_crew_spreadsheets='Y'"
    "process_logging='Y'"
    "crew_leads=[{'name': 'Chris Downing', 'spreadsheet_name': 'Chris Downing', 'pay_type_key': 'LEAD_STD'}, {'name': 'Dave McMillin', 'spreadsheet_name': 'Dave', 'pay_type_key': 'LEAD_STD'}, {'name': 'Manuel Gomez', 'spreadsheet_name': 'Manuel', 'pay_type_key': 'LEAD_STD'}, {'name': 'Stephen Simpson', 'spreadsheet_name': 'Stephen Simpson', 'pay_type_key': 'EQ_SPLIT'}]"
    "crew_seconds=[{'name': 'John Green', 'spreadsheet_name': 'John', 'pay_type_key': '3T2', 'crew_lead_spreadsheet_name': 'Chris Downing'}, {'name': 'Mikey Clark', 'spreadsheet_name': 'Mikey', 'pay_type_key': 'EQ_SPLIT', 'crew_lead_spreadsheet_name': 'Stephen Simpson'}, {'name': 'Roberto Cruz', 'spreadsheet_name': 'Roberto', 'pay_type_key': '3T2', 'crew_lead_spreadsheet_name': 'Dave'}, {'name': 'Zach Higman', 'spreadsheet_name': 'Zach', 'pay_type_key': '1T2', 'crew_lead_spreadsheet_name': 'Manuel'}]"
    "pay_types=[{'name': 'Lead TIA Inspection Pay', 'pay_type_key': 'LEAD_STD', 'guyed': 189.0, 'ss': 126.0, 'mp': 116.0, 'mp_cans': 230.0}, {'name': 'Lead/Second Even Split TIA Inspection Pay', 'pay_type_key': 'EQ_SPLIT', 'guyed': 183.0, 'ss': 125.5, 'mp': 114.5, 'mp_cans': 207.5}, {'name': '1st Tier Second TIA Inspection Pay', 'pay_type_key': '1T2', 'guyed': 154.0, 'ss': 108.0, 'mp': 97.0, 'mp_cans': 185.0}, {'name': '2nd Tier Second TIA Inspection Pay', 'pay_type_key': '2T2', 'guyed': 165.0, 'ss': 117.0, 'mp': 104.0, 'mp_cans': 185.0}, {'name': '3nd Tier Second TIA Inspection Pay', 'pay_type_key': '3T2', 'guyed': 177.0, 'ss': 125.0, 'mp': 113.0, 'mp_cans': 185.0}]"
    "additional_pay={'extra_cans_each': 25.0, 'hvf': 12.0, 'lighting_inspection': 12.0, 'migratory_bird': 20.0, 'windsim': 35.0, 'ttp_inititial_reading': 0.0, 'tension_700': 75.0, 'tension_850': 90.0, 'tension_1000': 120.0, 'hr_pay_per_hour': 30.0}"    
    """

    # pandas_utils.check_for_required_fields(
    #     required_fields=field.PAYROLL_REQUIRED_INPUT_COLS, pd_df=input_df
    # )

    # # typically the provided spreadsheet has more columns than we need, so we select only the ones we need
    # wanted_df = input_df[field.PAYROLL_REQUIRED_INPUT_COLS]
