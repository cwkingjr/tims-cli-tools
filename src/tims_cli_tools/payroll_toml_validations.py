from rich.pretty import pprint
from . import field
import sys
from collections import Counter

CREW_LEAD_NAME = "crew_lead_name"
NAME = "name"
PAY_TYPE_KEY = "pay_type_key"


def get_create_crew_spreadsheets(*, create_crew_spreadsheets) -> bool:
    """Print the status to the command line."""
    if create_crew_spreadsheets == "Y":
        pprint("Create individual spreadsheets: Yes")
        return True
    else:
        pprint("Create individual spreadsheets: No")
        return False


def get_process_logging(*, process_logging) -> bool:
    """Print the status to the command line."""
    if process_logging == "Y":
        pprint("Extra process logging: Yes")
        return True
    else:
        pprint("Extra process logging: No")
        return False


def print_crew_lead_info(*, crew_leads) -> None:
    """Print crew lead info to command line."""
    crew_lead_names = sorted(
        [x[NAME] + " (" + x[PAY_TYPE_KEY] + ")" for x in crew_leads]
    )
    pprint(f"Found crew leads: {crew_lead_names}")


def print_crew_second_info(*, crew_seconds) -> None:
    """Print crew second info to command line."""
    crew_second_info = sorted(
        [
            x[NAME] + " (" + x[PAY_TYPE_KEY] + ") with " + x[CREW_LEAD_NAME]
            for x in crew_seconds
        ]
    )
    pprint(f"Found crew seconds: {crew_second_info}")


def verify_crew_lead_pay_types_are_valid(*, crew_leads) -> None:
    """Pay types must match one of valid types."""
    for x in crew_leads:
        if x[PAY_TYPE_KEY] not in field.PAYROLL_VALID_CREW_LEAD_PAY_TYPES:
            pprint(
                f"ERROR: Found crew lead '{x[NAME]}' with invalid pay_key_type of '{x[PAY_TYPE_KEY]}'."
            )
            sys.exit(1)


def verify_crew_second_pay_types_are_valid(*, crew_seconds) -> None:
    """Pay types must match one of valid types."""
    for x in crew_seconds:
        if x[PAY_TYPE_KEY] not in field.PAYROLL_VALID_CREW_SECOND_PAY_TYPES:
            pprint(
                f"ERROR: Found crew second '{x[NAME]}' with invalid pay_key_type of '{x[PAY_TYPE_KEY]}'."
            )
            sys.exit(1)


def verify_crew_leads_listed_in_seconds_exist(*, crew_seconds, crew_leads) -> None:
    crew_lead_names = [x[NAME] for x in crew_leads]

    for x in crew_seconds:
        if x[CREW_LEAD_NAME] not in crew_lead_names:
            pprint(
                f"ERROR: Found non-existent crew lead of '{x[CREW_LEAD_NAME]}' for crew second '{x[NAME]}'."
            )
            sys.exit(1)


def verify_same_number_of_leads_and_seconds(*, crew_seconds, crew_leads) -> None:
    """Must have crews of one lead and one second."""
    lead_count = len(crew_leads)
    second_count = len(crew_seconds)
    if lead_count != second_count:
        pprint(
            f"ERROR: Found mismatching number of leads ({lead_count}) and seconds ({second_count})."
        )
        sys.exit(1)


def verify_no_duplicate_second_names(*, crew_seconds) -> None:
    """Make sure no seconds names are duplicated."""
    seconds_names = [x[NAME] for x in crew_seconds]
    if len(seconds_names) != len(set(seconds_names)):
        # hmm. we have at least one duplicate name
        # so lets push out the list by counts
        pprint(
            "ERROR: Whoops, found at least one set of duplicated second names. Please fix the config file and try again."
        )
        name_counts = Counter(seconds_names)
        pprint(f"{name_counts}")
        sys.exit(1)


def verify_no_duplicate_lead_names(*, crew_leads) -> None:
    """Make sure no lead names are duplicated."""
    lead_names = [x[NAME] for x in crew_leads]
    if len(lead_names) != len(set(lead_names)):
        # hmm. we have at least one duplicate name
        # so lets push out the list by counts
        pprint(
            "ERROR: Whoops, found at least one set of duplicated lead names. Please fix the config file and try again."
        )
        name_counts = Counter(lead_names)
        pprint(f"{name_counts}")
        sys.exit(1)


def verify_no_duplicate_second_crew_lead_names(*, crew_seconds) -> None:
    """Make sure no seconds crew lead names are duplicated."""
    names = [x[CREW_LEAD_NAME] for x in crew_seconds]
    if len(names) != len(set(names)):
        # hmm. we have at least one duplicate name
        # so lets push out the list by counts
        pprint(
            "ERROR: Whoops, found at least one set of duplicated second crew lead names. Please fix the config file and try again."
        )
        name_counts = Counter(names)
        pprint(f"{name_counts}")
        sys.exit(1)
