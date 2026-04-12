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


@pytest.fixture
def full_width_df():
    return pd.DataFrame(
        data={
            "SORT_BY": [1, 2],
            "BU": [12345, 67890],
            "SUB CATEGORY": ["BASE", "ADDER"],
            "DESCRIPTION": ["Description A", "Description B"],
            "QUANTITY": [1, 2],
            "TIA Inspection": [100.0, 200.0],
            "Additional Canister Price": [10.0, 20.0],
            "HVF": [5.0, 10.0],
            "Lighting Inspection Price": [3.0, 6.0],
            "Migratory Bird": [2.0, 4.0],
            "Windsim": [1.0, 2.0],
            "TTP Initial Reading Price": [1.5, 3.0],
            "Tension Price": [10.0, 20.0],
            "HR.PAY": [50.0, 100.0],
            "Site Total": [500.0, 1000.0],
            "MAINTENANCE": ["00:30", "01:00"],
            "Manlift Charge": [25.0, 50.0],
            "Structure": [3, 5],
            "X_CANS": [2, 4],
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

    def test_write_with_full_columns_exercises_all_width_branches(self, full_width_df):
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            output_path = Path(f.name)

        try:
            writer = XlsxInvoiceWriter()
            writer.write(full_width_df, output_path)

            assert output_path.exists()
            assert output_path.stat().st_size > 0
        finally:
            output_path.unlink(missing_ok=True)

    def test_write_multiple_rows(self):
        df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": ["x", "y", "z", "w", "v"]})
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            output_path = Path(f.name)

        try:
            writer = XlsxInvoiceWriter()
            writer.write(df, output_path)

            result_df = pd.read_excel(output_path, header=None)
            assert len(result_df) == 6
        finally:
            output_path.unlink(missing_ok=True)


class TestInvoiceWriterProtocol:
    def test_xlsx_writer_implements_protocol(self):
        writer = XlsxInvoiceWriter()
        assert isinstance(writer, InvoiceWriter)
