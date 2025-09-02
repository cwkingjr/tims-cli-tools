import sys
from datetime import time
from pathlib import Path
import pandas as pd
from rich.pretty import pprint
from . import (
    field,
    price,
    pandas_utils,
    file_utils,
    payroll_toml_json_schema,
    payroll_toml_validations as ptv,
    payroll_spreadsheets,
    payroll_sql,
)
from .payroll_classes import (
    Crews,
    build_crews,
    build_additional_pay,
)
import io
import json
import duckdb
from duckdb import DuckDBPyConnection

CONFIG_FILE = Path.home() / ".config/tims_tools/tims_payroll.toml"
DB_FILE = Path.home() / ".config/tims_tools/tmp_payroll.db"

# TODO: Add arg parsing for input file, maybe individual spreadsheets, config file validation only
# TODO: refactor across apps and create/update all tests


def bogus_for_coverage() -> str:
    """Bogus fn to get this file added to coverage."""
    return "TODO: Delete me."


def load_payments_into_db(*, con: DuckDBPyConnection, df: pd.DataFrame, crews, add_pay):  # noqa: PLR0912,PLR0915
    """Process the rows and write payments records into database."""
    for _, row in df.iterrows():
        bu = pandas_utils.get_value_from_series_col(series=row, column_name=field.BU)

        inspection_date = pandas_utils.get_value_from_series_col(
            series=row, column_name=field.DATE
        )

        crew_lead = pandas_utils.get_value_from_series_col(
            series=row, column_name=field.CREW
        )

        tia_inspection = pandas_utils.get_value_from_series_col(
            series=row, column_name=field.TIA_INSP
        )

        extra_cans = pandas_utils.get_value_from_series_col(
            series=row, column_name=field.EXTRA_CANS
        )
        if not isinstance(extra_cans, int | float):
            additional_canister_level_pay = 0.0
            extra_cans_count = 0
        elif int(extra_cans) > 0:
            additional_canister_level_pay = add_pay.extra_cans_each * extra_cans
            extra_cans_count = int(extra_cans)
        else:
            additional_canister_level_pay = 0.0
            extra_cans_count = 0

        hvf = pandas_utils.get_value_from_series_col(
            series=row, column_name=field.HVF_WITH_SPACE
        )
        if not isinstance(hvf, int | float):
            hvf_pay = 0.0
        elif float(hvf) > 0.0:
            hvf_pay = add_pay.hvf
        else:
            hvf_pay = 0.0

        lighting_inspection_price = pandas_utils.get_value_from_series_col(
            series=row, column_name=field.LIGHT_INSP
        )
        if not isinstance(lighting_inspection_price, int | float):
            lighting_inspection_pay = 0.0
        elif float(lighting_inspection_price) > 0.0:
            lighting_inspection_pay = add_pay.lighting_inspection
        else:
            lighting_inspection_pay = 0.0

        migratory_bird = pandas_utils.get_value_from_series_col(
            series=row, column_name=field.MIG_BIRD
        )
        if not isinstance(migratory_bird, int | float):
            migratory_bird_pay = 0.0
        elif float(migratory_bird) > 0.0:
            migratory_bird_pay = add_pay.migratory_bird
        else:
            migratory_bird_pay = 0.0

        windsim = pandas_utils.get_value_from_series_col(
            series=row, column_name=field.WINDSIM
        )
        if not isinstance(windsim, int | float):
            windsim_pay = 0.0
        elif float(windsim) > 0.0:
            windsim_pay = add_pay.windsim
        else:
            windsim_pay = 0.0

        tension = pandas_utils.get_value_from_series_col(
            series=row, column_name=field.TENSION
        )
        if not isinstance(migratory_bird, int | float):
            tension_pay = 0.0
        elif float(tension) == price.PRICE_700:
            tension_pay = add_pay.tension_700
        elif float(tension) == price.PRICE_850:
            tension_pay = add_pay.tension_850
        elif float(tension) == price.PRICE_1000:
            tension_pay = add_pay.tension_1000
        else:
            tension_pay = 0.0

        maint = pandas_utils.get_value_from_series_col(
            series=row, column_name=field.MAINT
        )
        if isinstance(maint, time) and (maint.hour > 0 or maint.minute > 0):
            minutes = maint.hour * 60 + maint.minute
            pay_per_minute = add_pay.hr_pay_per_hour / 60
            hr_pay_pay = minutes * pay_per_minute
        else:
            hr_pay_pay = 0.0

        ecs_concealment_type = pandas_utils.get_value_from_series_col(
            series=row, column_name=field.ECS_CONCEALMENT_TYPE
        )

        structure_type = pandas_utils.get_value_from_series_col(
            series=row, column_name=field.STRUCTURE_TYPE
        )
        structure_type = structure_type.strip()
        if (
            structure_type.lower() == "mp"
            and isinstance(ecs_concealment_type, str)
            and ecs_concealment_type.strip().lower() == "flagpole"
        ):
            structure_type = "MP_CANS"

        my_crew = crews.get_crew_by_lead_spreadsheet_name(
            spreadsheet_name=crew_lead.strip()
        )
        lead_name = my_crew.lead.name
        second_name = my_crew.second.name

        if not isinstance(tia_inspection, int | float):
            tia_inspection = 0.0
        else:
            # This will be the pay for the structure type based upon the person's PayType
            tia_inspection_lead = my_crew.lead.pay_type.get_pay_by_str(structure_type)
            tia_inspection_second = my_crew.second.pay_type.get_pay_by_str(
                structure_type
            )

        common_total = (
            additional_canister_level_pay
            + hvf_pay
            + lighting_inspection_pay
            + migratory_bird_pay
            + windsim_pay
            + tension_pay
            + hr_pay_pay
        )

        lead_site_total = tia_inspection_lead + common_total
        second_site_total = tia_inspection_second + common_total

        #
        # pay the lead
        #

        payroll_sql.insert_payment(
            con=con,
            bu=bu,
            inspection_date=inspection_date,
            crew_lead=lead_name,
            pay_to=lead_name,
            structure_type=structure_type,
            tia_inspection=tia_inspection_lead,
            additional_canister_level=additional_canister_level_pay,
            hvf=hvf_pay,
            lighting_inspection_price=lighting_inspection_pay,
            migratory_bird=migratory_bird_pay,
            windsim=windsim_pay,
            tension=tension_pay,
            hr_pay=hr_pay_pay,
            site_total=lead_site_total,
            maintenance=maint,
            extra_cans=extra_cans_count,
        )

        #
        # Pay the second
        #

        payroll_sql.insert_payment(
            con=con,
            bu=bu,
            inspection_date=inspection_date,
            crew_lead=lead_name,
            pay_to=second_name,
            structure_type=structure_type,
            tia_inspection=tia_inspection_second,
            additional_canister_level=additional_canister_level_pay,
            hvf=hvf_pay,
            lighting_inspection_price=lighting_inspection_pay,
            migratory_bird=migratory_bird_pay,
            windsim=windsim_pay,
            tension=tension_pay,
            hr_pay=hr_pay_pay,
            site_total=second_site_total,
            maintenance=maint,
            extra_cans=extra_cans_count,
        )


def get_pay_to_dataframes(
    *, con: DuckDBPyConnection, crews: Crews
) -> list[tuple[str, pd.DataFrame]]:
    """Returns a list of tuples that contain the payee name and the payee dataframe."""
    payee_tuples = []  # (name, dataframe)

    for crew in crews.crews:
        lead_tuple = payroll_sql.get_payments_by_pay_to(con=con, pay_to=crew.lead.name)
        payee_tuples.append(lead_tuple)
        second_tuple = payroll_sql.get_payments_by_pay_to(
            con=con, pay_to=crew.second.name
        )
        payee_tuples.append(second_tuple)
    return payee_tuples


def main() -> None:  # noqa: PLR0915
    if len(sys.argv) < 2:  # noqa: PLR2004
        pprint(f"Usage: {sys.argv[0]} <input_file>")
        sys.exit(1)

    in_file = sys.argv[1]
    input_df = pd.read_excel(in_file)

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

    #
    # Build out some data structures to make it easier to process rows
    #

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

    db_file = Path(DB_FILE)

    if db_file.exists():
        try:
            db_file.unlink()
        except OSError as e:
            pprint(f"Error deleting file '{DB_FILE}': {e}")

    # add an "EXTRA_CANS" column that includes the value from the structure column only if that column includes an integer value
    # the first can is part of the base price, so we subtract 1 from the value
    input_df[field.EXTRA_CANS] = input_df[field.STRUCTURE].apply(
        lambda x: x - 1 if isinstance(x, int) and x - 1 > 0 else None,
    )

    # Convert column to dataframe int type that can handle NaN values as we were getting floats before
    input_df[field.EXTRA_CANS] = input_df[field.EXTRA_CANS].astype(pd.Int64Dtype())

    con = duckdb.connect(database=DB_FILE)
    con.execute(payroll_sql.CREATE_PAYMENTS_TABLE_SEQUENCE)
    con.execute(payroll_sql.CREATE_PAYMENTS_TABLE_SQL)

    load_payments_into_db(con=con, df=input_df, crews=crews, add_pay=add_pay)

    all_payments_df = payroll_sql.get_all_payments(con=con)
    all_payments_totals = payroll_sql.get_all_payments_totals(con=con)
    payee_tuples = get_pay_to_dataframes(con=con, crews=crews)

    pprint("Writing consolidated payroll spreadsheet to your Documents folder.")
    payroll_spreadsheets.write_consolidated_spreadsheet(
        original_df=input_df,
        all_payments_df=all_payments_df,
        all_payments_totals_df=all_payments_totals,
        payee_tuples=payee_tuples,
    )

    if create_crew_spreadsheets:
        for one_tuple in payee_tuples:
            pay_to, payee_df = one_tuple
            ind_tots_df = payroll_sql.get_individual_payments_totals(
                con=con, pay_to=pay_to
            )
            payroll_spreadsheets.write_individual_spreadsheet(
                pay_to_name=pay_to,
                individual_payments_totals_df=ind_tots_df,
                individual_payments_df=payee_df,
            )
            pprint(f"Writing individual payroll spreadsheet for {pay_to}.")

    con.close()
    # delete db file
