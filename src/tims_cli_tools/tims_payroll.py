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
    payroll_toml_validations as ptv,
    payroll_classes,
)
from .payroll_classes import (
    build_crews,
    build_additional_pay,
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

    #
    # Process the config info
    #

    pprint(f"Loading config file data from {CONFIG_FILE}.")
    toml_data = file_utils.get_toml_data(config_path=CONFIG_FILE)
    json_schema = json.load(io.StringIO(payroll_toml_json_schema.JSON_SCHEMA_STR))

    pprint("Validating config file against config file data schema.")
    file_utils.validate_toml_data(toml_data=toml_data, json_schema=json_schema)

    create_crew_spreadsheets = toml_data["processing_info"]["create_crew_spreadsheets"]
    create_crew_spreadsheets = ptv.get_create_crew_spreadsheets(
        create_crew_spreadsheets=create_crew_spreadsheets
    )

    process_logging = toml_data["processing_info"]["process_logging"]
    process_logging = ptv.get_process_logging(process_logging=process_logging)

    crew_leads = toml_data["crew_lead"]
    crew_seconds = toml_data["crew_second"]
    pay_types = toml_data["pay_type"]
    additional_pay = toml_data["additional_pay"]

    pprint("Checking configuration information for errors and rule violations.")

    ptv.verify_crew_lead_pay_types_are_valid(crew_leads=crew_leads)
    ptv.verify_crew_second_pay_types_are_valid(crew_seconds=crew_seconds)
    ptv.verify_crew_leads_listed_in_seconds_exist(
        crew_seconds=crew_seconds, crew_leads=crew_leads
    )
    ptv.verify_same_number_of_leads_and_seconds(
        crew_seconds=crew_seconds, crew_leads=crew_leads
    )
    ptv.verify_no_duplicate_second_names(crew_seconds=crew_seconds)
    ptv.verify_no_duplicate_lead_names(crew_leads=crew_leads)
    ptv.verify_no_duplicate_second_crew_lead_names(crew_seconds=crew_seconds)

    pandas_utils.pprint_as_dataframe(
        message="Found these pay types:", content=pay_types
    )

    # Build out some data structures to make it easier to process rows

    crews = build_crews(
        config_crew_leads=crew_leads,
        config_crew_seconds=crew_seconds,
        config_pay_types=pay_types,
    )
    pprint("Found config data for these crews:")
    pprint(crews)

    add_pay = build_additional_pay(config_add_pay=additional_pay)
    pprint("Found config data for these additional pay rates:")
    pprint(add_pay)

    # Load up the spreadsheet data

    # pandas_utils.check_for_required_fields(
    #     required_fields=field.PAYROLL_REQUIRED_INPUT_COLS, pd_df=input_df
    # )

    # # typically the provided spreadsheet has more columns than we need, so we select only the ones we need
    # wanted_df = input_df[field.PAYROLL_REQUIRED_INPUT_COLS]
