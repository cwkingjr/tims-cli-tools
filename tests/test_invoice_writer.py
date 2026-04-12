from pathlib import Path
import tempfile

import pandas as pd
import pytest

from tims_cli_tools.invoice_writer import InvoiceWriter, XlsxInvoiceWriter


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        data={
            "Col1": ["A", "B", "C"],
            "Col2": [1, 2, 3],
            "Col3": [1.5, 2.5, 3.5],
        }
    )


class TestXlsxInvoiceWriter:
    def test_write_creates_file(self, sample_df):
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            output_path = Path(f.name)

        try:
            writer = XlsxInvoiceWriter()
            writer.write(sample_df, output_path)

            assert output_path.exists()
            assert output_path.stat().st_size > 0
        finally:
            output_path.unlink(missing_ok=True)

    def test_write_contains_data(self, sample_df):
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            output_path = Path(f.name)

        try:
            writer = XlsxInvoiceWriter()
            writer.write(sample_df, output_path)

            result_df = pd.read_excel(output_path, header=None)
            assert len(result_df) > 0
        finally:
            output_path.unlink(missing_ok=True)


class TestInvoiceWriterProtocol:
    def test_xlsx_writer_implements_protocol(self):
        writer = XlsxInvoiceWriter()
        assert isinstance(writer, InvoiceWriter)
