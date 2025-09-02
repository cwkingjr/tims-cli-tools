import sys
from pathlib import Path
from .file_utils import get_toml_data

import pandas as pd
from rich.pretty import pprint

CONFIG_FILE = Path.home() / ".config/tims_tools/tims_bu_info.toml"


def main():
    if len(sys.argv) < 2:  # noqa: PLR2004
        pprint("Whoops, no BU passed in")
        pprint("Usage: tims_bu_info <BUN>")
        pprint("Example: tims_bu_info 22222223")
        sys.exit(1)

    # grab the bu number passed in and clean it up
    bun = sys.argv[1]
    bun = int(bun.strip())

    toml_data = get_toml_data(config_path=CONFIG_FILE)

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
