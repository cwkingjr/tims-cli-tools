from datetime import datetime
from pathlib import Path
import tempfile

import pytest
import pytz

from tims_cli_tools import file_utils


class TestGetTomlData:
    def test_raises_when_file_not_found(self):
        with pytest.raises(ValueError, match="no config file exists"):
            file_utils.get_toml_data(config_path=Path("/nonexistent/path.toml"))

    def test_loads_valid_toml_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            f.write('key = "value"\n')
            f.write("number = 42\n")
            toml_path = Path(f.name)

        try:
            result = file_utils.get_toml_data(config_path=toml_path)
            assert result["key"] == "value"
            assert result["number"] == 42
        finally:
            toml_path.unlink(missing_ok=True)


class TestValidateTomlData:
    def test_passes_with_valid_data(self):
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
            },
            "required": ["name"],
        }
        data = {"name": "test"}

        file_utils.validate_toml_data(toml_data=data, json_schema=schema)

    def test_raises_with_invalid_data(self):
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
            },
            "required": ["name"],
        }
        data = {"number": 42}

        with pytest.raises(ValueError, match="Validation error"):
            file_utils.validate_toml_data(toml_data=data, json_schema=schema)

    def test_raises_with_wrong_type(self):
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
            },
            "required": ["name"],
        }
        data = {"name": 123}

        with pytest.raises(ValueError, match="Validation error"):
            file_utils.validate_toml_data(toml_data=data, json_schema=schema)


class TestCreateCleanedFilepath:
    def test_creates_path_with_prefix_and_timestamp(self):
        dt = datetime(2025, 1, 15, 10, 30, 0, tzinfo=pytz.timezone("US/Central"))
        result = file_utils.create_cleaned_filepath(
            in_path=Path("/input/file.xlsx"),
            filename_prefix="transformed",
            dt_with_tz=dt,
        )

        assert result.parent.name == "Documents"
        assert "file" in result.stem
        assert "transformed" in result.stem
        assert "20250115" in result.stem

    def test_replaces_spaces_in_filename(self):
        dt = datetime(2025, 1, 15, 10, 30, 0, tzinfo=pytz.timezone("US/Central"))
        result = file_utils.create_cleaned_filepath(
            in_path=Path("/input/my file.xlsx"),
            filename_prefix="test",
            dt_with_tz=dt,
        )

        assert "my_file" in result.stem


class TestCreateNewSpreadsheetCentralTzFilepath:
    def test_creates_path_in_documents(self):
        result = file_utils.create_new_spreadsheet_central_tz_filepath(
            filename_prefix="report"
        )

        assert result.parent.name == "Documents"
        assert result.suffix == ".xlsx"
        assert "report" in result.stem

    def test_path_has_timestamp(self):
        result = file_utils.create_new_spreadsheet_central_tz_filepath(
            filename_prefix="report"
        )

        assert result.stem.split("_")[1].isdigit()
