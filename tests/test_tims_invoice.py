import sys
from datetime import time
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

from tims_cli_tools import field
from tims_cli_tools.invoice_transform import get_value_from_series_col
from tims_cli_tools.invoice_writer import InvoiceWriter
from tims_cli_tools.tims_invoice import run


def test_get_value_from_series_col(df_series_input_cols, eight_twos):
    assert (
        get_value_from_series_col(series=df_series_input_cols, field_name=field.BU)
        == eight_twos
    )


def test_get_value_from_series_col_missing_col(df_series_input_cols):
    del df_series_input_cols[field.BU]
    with pytest.raises(ValueError):
        get_value_from_series_col(series=df_series_input_cols, field_name=field.BU)


@pytest.fixture
def sample_input_df():
    return pd.DataFrame(
        data={
            field.BU: [12345678],
            field.STRUCTURE: [3],
            field.BASE_FOR_INV: ["Inspection"],
            field.TIA_INSP: ["1,000.00"],
            field.ADD_CAN_LEVEL: [3],
            field.HVF_WITH_SPACE: ["1,000.00"],
            field.LIGHT_INSP: ["1,000.00"],
            field.MIG_BIRD: ["1,000.00"],
            field.WINDSIM: ["1,000.00"],
            field.TTP_INIT_READ: ["1,000.00"],
            field.TENSION: ["700.00"],
            field.HR_PAY: ["122.50"],
            field.SITE_TOTAL: ["1,000.00"],
            field.MAINT: [time(hour=0, minute=15)],
            field.MAN_LIFT: ["$1,234.56"],
        }
    )


class TestRun:
    def test_run_with_missing_file_exits(self, tmp_path):
        nonexistent_path = tmp_path / "nonexistent.xlsx"

        with patch.object(sys, "argv", ["tims_invoice", str(nonexistent_path)]):
            with pytest.raises(SystemExit) as exc_info:
                run(str(nonexistent_path))
            assert exc_info.value.code == 1

    def test_run_with_custom_writer(self, sample_input_df, tmp_path):
        input_path = tmp_path / "input.xlsx"
        sample_input_df.to_excel(input_path, index=False)

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        captured_output = StringIO()

        class MockInvoiceWriter:
            write_called = False

            def write(self, df, output_path):
                MockInvoiceWriter.write_called = True
                MockInvoiceWriter.df = df
                MockInvoiceWriter.output_path = output_path

        mock_writer = MockInvoiceWriter()

        with patch("tims_cli_tools.tims_invoice.create_cleaned_filepath") as mock_path:
            mock_output = output_dir / "_transformed_invoice_001.xlsx"
            mock_path.return_value = mock_output

            with patch("sys.stdout", captured_output):
                run(str(input_path), writer=mock_writer)

        assert MockInvoiceWriter.write_called
        assert mock_writer.df is not None


class TestMain:
    def test_main_with_no_args_exits(self):
        with patch.object(sys, "argv", ["tims_invoice"]):
            with pytest.raises(SystemExit) as exc_info:
                from tims_cli_tools.tims_invoice import main

                main()
            assert exc_info.value.code == 1


class TestIntegration:
    def test_run_integration_with_mocked_writer(self, sample_input_df, tmp_path):
        input_path = tmp_path / "input.xlsx"
        sample_input_df.to_excel(input_path, index=False)

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        class CapturingWriter(InvoiceWriter):
            captured_df: pd.DataFrame | None = None
            captured_path: Path | None = None

            def write(self, df: pd.DataFrame, output_path: Path) -> None:
                CapturingWriter.captured_df = df
                CapturingWriter.captured_path = output_path

        with patch("tims_cli_tools.tims_invoice.create_cleaned_filepath") as mock_path:
            mock_output = output_dir / "_transformed_invoice_001.xlsx"
            mock_path.return_value = mock_output

            run(str(input_path), writer=CapturingWriter())

        assert CapturingWriter.captured_df is not None
        assert CapturingWriter.captured_path == mock_output
        assert len(CapturingWriter.captured_df) > 0
