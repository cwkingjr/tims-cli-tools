import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import pytz
from rich.pretty import pprint
import tomllib


def get_toml_data() -> dict:
    home = Path.home()
    config_path = home / ".config/tims_tools/tims_tools.toml"
    try:
        with Path.open(config_path, "rb") as f:
            toml_data = tomllib.load(f)
    except OSError() as e:
        msg = f"Problem with loading config file. Expected config file at {config_path}"
        raise OSError(msg) from e

    return toml_data


def main():
    if len(sys.argv) < 2:
        pprint(f"Usage: {sys.argv[0]} BUN")
        sys.exit(1)

    timezone_name = "US/Central"
    # Create a tzinfo object from the timezone name
    tz = pytz.timezone(timezone_name)

    bun = sys.argv[1]
    bun = int(bun.strip())

    toml_data = get_toml_data()
    master_tracker_path = Path(toml_data["tims_bu_info"]["master_tracker_path"])
    input_df = pd.read_excel(master_tracker_path)

    fields = [
        "BU",
        "Crew",
        "Site Name",
        "Region",
        "Address",
        "City",
        "County",
        "State",
        "Zip Code",
        "Lat",
        "Long",
    ]
    bun_df = input_df[fields]
    bun_df = bun_df.loc[bun_df["BU"] == bun]
    print(bun_df.transpose())


if __name__ == "__main__":
    main()
