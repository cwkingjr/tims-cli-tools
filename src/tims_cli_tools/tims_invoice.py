import argparse
from pathlib import Path
import pandas as pd
from rich.pretty import pprint

from .file_utils import create_cleaned_filepath, get_current_central_time
from .invoice_config import InvoiceConfig
from .invoice_transform import transform_input_dataframe
from .invoice_writer import InvoiceWriter, XlsxInvoiceWriter


def run(
    input_path: str,
    config: InvoiceConfig | None = None,
    writer: InvoiceWriter | None = None,
    now_func=None,
) -> None:
    if config is None:
        config = InvoiceConfig()
    if writer is None:
        writer = XlsxInvoiceWriter()
    if now_func is None:
        now_func = get_current_central_time

    input_path_obj = Path(input_path)
    if not input_path_obj.is_file():
        msg = f"Error: The input-path '{input_path}' is not a valid file path."
        raise FileNotFoundError(msg)

    input_df = pd.read_excel(input_path)

    transformed_df = transform_input_dataframe(input_df)

    output_path = create_cleaned_filepath(
        in_path=input_path_obj,
        filename_prefix="_transformed_invoice",
        dt_with_tz=now_func(),
    )

    writer.write(transformed_df, output_path)

    pprint(f"Wrote new transformed spreadsheet at: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read input file from path and generate transformed invoice spreadsheet.",
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
