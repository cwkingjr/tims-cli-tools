import sys
from datetime import datetime
import pandas as pd
import pytz
from pathlib import Path
from rich.pretty import pprint

from .file_utils import create_cleaned_filepath
from .invoice_config import InvoiceConfig
from .invoice_transform import transform_input_dataframe
from .invoice_writer import InvoiceWriter, XlsxInvoiceWriter


def run(
    input_path: str,
    config: InvoiceConfig | None = None,
    writer: InvoiceWriter | None = None,
) -> None:
    if config is None:
        config = InvoiceConfig()
    if writer is None:
        writer = XlsxInvoiceWriter()

    input_path_obj = Path(input_path)
    if not input_path_obj.is_file():
        pprint(f"Usage: {sys.argv[0]} <input_file>")
        sys.exit(1)

    input_df = pd.read_excel(input_path)

    transformed_df = transform_input_dataframe(input_df)

    output_path = create_cleaned_filepath(
        in_path=input_path_obj,
        filename_prefix="_transformed_invoice",
        dt_with_tz=datetime.now(tz=pytz.timezone("US/Central")),
    )

    writer.write(transformed_df, output_path)

    pprint(f"Wrote new transformed spreadsheet at: {output_path}")


def main() -> None:
    if len(sys.argv) < 2:
        pprint(f"Usage: {sys.argv[0]} <input_file>")
        sys.exit(1)

    run(sys.argv[1])
