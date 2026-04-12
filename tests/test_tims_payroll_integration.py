from datetime import date, time

import pandas as pd
import pytest
from unittest.mock import patch

from tims_cli_tools import field
from tims_cli_tools.payroll_config import PayrollConfig


class TestPayrollRunIntegration:
    """Integration tests for the payroll run() function."""

    @pytest.fixture
    def temp_config_file(self, tmp_path):
        config_content = """
[processing_info]
create_crew_spreadsheets = "Y"
process_logging = "N"

[[pay_type]]
name = "Lead TIA Inspection Pay"
pay_type_key = "LEAD_STD"
guyed = 5.0
ss = 3.0
mp = 4.0
mp_cans = 7.0

[[pay_type]]
name = "1st Tier Second TIA Inspection Pay"
pay_type_key = "1T2"
guyed = 3.0
ss = 2.0
mp = 3.0
mp_cans = 6.0

[[crew_lead]]
name = "John Doe"
spreadsheet_name = "John"
pay_type_key = "LEAD_STD"

[[crew_second]]
name = "Jane Doe"
pay_type_key = "1T2"
crew_lead_name = "John Doe"

[additional_pay]
extra_cans_each = 1.0
hr_pay_per_hour = 60.0
hvf = 10.0
lighting_inspection = 5.0
migratory_bird = 2.5
tension_1000 = 15.0
tension_700 = 10.0
tension_850 = 12.0
ttp_initial_reading = 3.0
windsim = 4.0
"""
        config_path = tmp_path / "tims_payroll.toml"
        config_path.write_text(config_content.strip())
        return config_path

    @pytest.fixture
    def temp_db_file(self, tmp_path):
        db_path = tmp_path / "test_payroll.db"
        yield db_path
        if db_path.exists():
            db_path.unlink()

    @pytest.fixture
    def temp_input_excel(self, tmp_path):
        df = pd.DataFrame(
            data={
                field.BU: [12345],
                field.DATE: [date(2025, 1, 15)],
                field.INVOICED: ["Yes"],
                field.CREW: ["John"],
                field.STRUCTURE: [3],
                field.BASE_FOR_INV: ["Inspection"],
                field.TIA_INSP: [100.0],
                field.ADD_CAN_LEVEL: [3],
                field.HVF_WITH_SPACE: [1.0],
                field.LIGHT_INSP: [1.0],
                field.MIG_BIRD: [1.0],
                field.WINDSIM: [1.0],
                field.TTP_INIT_READ: [1.0],
                field.TENSION: [700.0],
                field.HR_PAY: [60.0],
                field.SITE_TOTAL: [100.0],
                field.MAINT: [time(hour=0, minute=30)],
                field.MAN_LIFT: [100.0],
                field.ECS_CONCEALMENT_TYPE: [None],
                field.STRUCTURE_TYPE: ["Guyed"],
            }
        )
        input_path = tmp_path / "input.xlsx"
        df.to_excel(input_path, index=False)
        return input_path

    def test_run_with_valid_inputs(
        self, temp_config_file, temp_db_file, temp_input_excel, tmp_path
    ):
        from tims_cli_tools import file_utils
        from tims_cli_tools.tims_payroll import run

        def mock_create_path(*, filename_prefix):
            return tmp_path / f"{filename_prefix}.xlsx"

        config = PayrollConfig(
            config_file=temp_config_file,
            db_file=temp_db_file,
        )

        with patch.object(
            file_utils,
            "create_new_spreadsheet_central_tz_filepath",
            side_effect=mock_create_path,
        ):
            run(input_path=str(temp_input_excel), config=config)

        xlsx_files = list(tmp_path.glob("*.xlsx"))
        assert len(xlsx_files) > 0
        for f in xlsx_files:
            assert f.stat().st_size > 0

    def test_run_creates_consolidated_spreadsheet(
        self, temp_config_file, temp_db_file, temp_input_excel, tmp_path
    ):
        from tims_cli_tools import file_utils
        from tims_cli_tools.tims_payroll import run

        def mock_create_path(*, filename_prefix):
            return tmp_path / f"{filename_prefix}.xlsx"

        config = PayrollConfig(
            config_file=temp_config_file,
            db_file=temp_db_file,
        )

        with patch.object(
            file_utils,
            "create_new_spreadsheet_central_tz_filepath",
            side_effect=mock_create_path,
        ):
            run(input_path=str(temp_input_excel), config=config)

        consolidated_files = list(tmp_path.glob("*consolidated*.xlsx"))
        assert len(consolidated_files) == 1

    def test_run_creates_individual_spreadsheets(
        self, temp_config_file, temp_db_file, temp_input_excel, tmp_path
    ):
        from tims_cli_tools import file_utils
        from tims_cli_tools.tims_payroll import run

        def mock_create_path(*, filename_prefix):
            return tmp_path / f"{filename_prefix}.xlsx"

        config = PayrollConfig(
            config_file=temp_config_file,
            db_file=temp_db_file,
        )

        with patch.object(
            file_utils,
            "create_new_spreadsheet_central_tz_filepath",
            side_effect=mock_create_path,
        ):
            run(input_path=str(temp_input_excel), config=config)

        individual_files = list(tmp_path.glob("*john*.xlsx")) + list(
            tmp_path.glob("*jane*.xlsx")
        )
        assert len(individual_files) == 2

    def test_run_output_contains_expected_data(
        self, temp_config_file, temp_db_file, temp_input_excel, tmp_path
    ):
        from tims_cli_tools import file_utils
        from tims_cli_tools.tims_payroll import run

        def mock_create_path(*, filename_prefix):
            return tmp_path / f"{filename_prefix}.xlsx"

        config = PayrollConfig(
            config_file=temp_config_file,
            db_file=temp_db_file,
        )

        with patch.object(
            file_utils,
            "create_new_spreadsheet_central_tz_filepath",
            side_effect=mock_create_path,
        ):
            run(input_path=str(temp_input_excel), config=config)

        consolidated_files = list(tmp_path.glob("*consolidated*.xlsx"))
        assert len(consolidated_files) == 1

        result_df = pd.read_excel(consolidated_files[0], sheet_name="All_Payments")
        assert len(result_df) > 0
        assert "pay_to" in result_df.columns
        assert "John Doe" in result_df["pay_to"].values
        assert "Jane Doe" in result_df["pay_to"].values

    def test_run_raises_for_nonexistent_input_file(self, temp_config_file, tmp_path):
        from tims_cli_tools.tims_payroll import run

        config = PayrollConfig(
            config_file=temp_config_file,
            db_file=tmp_path / "test.db",
        )

        with pytest.raises(SystemExit):
            run(input_path="/nonexistent/file.xlsx", config=config)
