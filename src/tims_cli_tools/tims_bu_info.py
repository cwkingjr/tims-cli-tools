import sys
import tomllib
from pathlib import Path

import pandas as pd
from rich.pretty import pprint

PATH_SUFFIX = ".config/tims_tools/tims_tools.toml"


def get_toml_data() -> dict:
    home = Path.home()
    config_path = home / PATH_SUFFIX

    if not Path.exists(config_path):
        pprint(f"Whoops, no config file exists at {config_path}")
        pprint(
            "Please see the repo directions and make sure you have the config file in this location."
        )
        sys.exit(1)

    try:
        with Path.open(config_path, "rb") as f:
            toml_data = tomllib.load(f)
    except IOError as e:
        msg = f"Problem with loading toml data from the config file. Please check the settings in your config file to ensure they match the config file in the repo."
        raise OSError(msg) from e

    return toml_data


def main():
    if len(sys.argv) < 2:
        pprint("Whoops, no BU passed in")
        pprint("Usage: tims_bu_info <BUN>")
        pprint("Example: tims_bu_info 22222223")
        sys.exit(1)

    # grab the bu number passed in and clean it up
    bun = sys.argv[1]
    bun = int(bun.strip())

    toml_data = get_toml_data()

    if "tims_bu_info" not in toml_data:
        pprint("Whoops, couldn't find '[tims_bu_info]' section in your config file.")
        sys.exit(1)

    if "master_tracker_path" not in toml_data["tims_bu_info"]:
        pprint("Whoops, couldn't find 'master_tracker_path' in your config file.")
        sys.exit(1)

    try:
        # pull the tracker path out of the toml settings
        master_tracker_path = Path(toml_data["tims_bu_info"]["master_tracker_path"])
    except ValueError as e:
        msg = "Sorry, looks like something is wrong with the content of your config file. Please compare to the tims_tools.toml in the GitHub repo."
        raise ValueError(msg) from e

    try:
        # read the spreadsheet into a dataframe
        input_df = pd.read_excel(master_tracker_path)
    except OSError as e:
        msg = f"Problem reading master tracker xlsx from {master_tracker_path}"
        raise OSError(msg) from e

    # should probably live in field.py
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

    # the tracker has a lot of fields we don't need, so load the bun_df with only the fields we want
    bun_df = input_df[fields]

    # Find the row that matches the bun passed in
    bun_df = bun_df.loc[bun_df["BU"] == bun]

    # If we didn't find that bun, let the user know
    if bun_df.empty:
        print(f"Sorry, no BU with that number ({bun}) found.")
    else:
        # print the row vertically to make it easier to see, copy, etc
        print(bun_df.transpose())


if __name__ == "__main__":
    main()
