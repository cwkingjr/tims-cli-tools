from datetime import datetime
from pathlib import Path
import tomllib
from jsonschema import exceptions as jsonschema_exceptions
from jsonschema import validate
import pytz


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
    add_to_filename = f"_{filename_prefix}_{dt_with_tz.strftime(dt_format_str)}"
    cleaned_filename = filename_no_extension.strip().replace(" ", "_")
    new_filename = cleaned_filename + add_to_filename + filename_extension
    cleaned_full_path = Path("~/Documents/" + new_filename).expanduser()
    return cleaned_full_path


def create_new_spreadsheet_central_tz_filepath(
    *,
    filename_prefix: str,
) -> Path:
    """Create a new filepath for a spreadsheet file."""

    dt_format_str = "%Y%m%d_%H%M%S"
    dt_with_tz = datetime.now(tz=pytz.timezone("US/Central"))
    filename = f"{filename_prefix}_{dt_with_tz.strftime(dt_format_str)}.xlsx"
    full_path = Path(f"~/Documents/{filename}").expanduser()
    return full_path


def get_toml_data(*, config_path) -> dict:
    if not Path.exists(config_path):
        msg = f"Whoops, no config file exists at {config_path}. Please see the repo directions and make sure you have the config file in this location."
        raise ValueError(msg)

    try:
        with Path.open(config_path, "rb") as f:
            toml_data = tomllib.load(f)
    except OSError as e:
        msg = "Problem with loading toml data from the config file. Please check the settings in your toml file to ensure they match the example toml file in the repo."
        raise OSError(msg) from e

    return toml_data


def validate_toml_data(*, toml_data, json_schema):
    try:
        validate(instance=toml_data, schema=json_schema)
        # print("TOML file is valid against the schema.")
    except jsonschema_exceptions.ValidationError as e:
        msg = f"TOML file Validation error: {e}."
        raise ValueError(msg) from e
