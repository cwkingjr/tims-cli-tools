from datetime import time

import pandas as pd
import pytest

from tims_cli_tools import field, subcat, desc
from tims_cli_tools.invoice_transform import (
    add_extra_cans_column,
    build_derived_rows,
    create_derived_rows_list,
    reformat_maintenance_to_string,
    transform_input_dataframe,
)


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


class TestAddExtraCansColumn:
    def test_adds_extra_cans_for_structure_greater_than_one(self):
        df = pd.DataFrame({field.STRUCTURE: [3]})
        result = add_extra_cans_column(df)
        assert result[field.EXTRA_CANS].iloc[0] == 2

    def test_adds_none_for_structure_of_one(self):
        df = pd.DataFrame({field.STRUCTURE: [1]})
        result = add_extra_cans_column(df)
        assert result[field.EXTRA_CANS].iloc[0] is pd.NA

    def test_adds_none_for_non_integer(self):
        df = pd.DataFrame({field.STRUCTURE: ["not an int"]})
        result = add_extra_cans_column(df)
        assert result[field.EXTRA_CANS].iloc[0] is pd.NA


class TestReformatMaintenanceToString:
    def test_converts_time_to_string(self):
        df = pd.DataFrame({field.MAINT: [time(hour=1, minute=30)]})
        result = reformat_maintenance_to_string(df)
        assert result[field.MAINT].iloc[0] == "01:30"

    def test_preserves_non_time_values(self):
        df = pd.DataFrame({field.MAINT: [None]})
        result = reformat_maintenance_to_string(df)
        assert result[field.MAINT].iloc[0] is None


class TestCreateDerivedRowsList:
    def test_creates_hvf_row(self):
        df = pd.DataFrame(
            {
                field.BU: [12345],
                field.SORT_BY: [1000000],
                field.HVF_NO_SPACE: ["1,000.00"],
            }
        )
        row = df.iloc[0]
        rows = create_derived_rows_list(row)

        hvf_rows = [r for r in rows if r[field.DESCRIPTION] == desc.HEIGHT_VERIF]
        assert len(hvf_rows) == 1
        assert hvf_rows[0][field.SUB_CATEGORY] == subcat.ADDER
        assert hvf_rows[0][field.QUANTITY] == 1

    def test_creates_tension_row_with_correct_description(self):
        df = pd.DataFrame(
            {
                field.BU: [12345],
                field.SORT_BY: [1000000],
                field.TENSION: ["700.00"],
            }
        )
        row = df.iloc[0]
        rows = create_derived_rows_list(row)

        tension_rows = [r for r in rows if r[field.SUB_CATEGORY] == subcat.ADDER]
        assert len(tension_rows) == 1
        assert tension_rows[0][field.DESCRIPTION] == desc.GUY_TTP_1_6

    def test_sorts_rows_by_subcategory_and_description(self):
        df = pd.DataFrame(
            {
                field.BU: [12345],
                field.SORT_BY: [1000000],
                field.HVF_NO_SPACE: ["1,000.00"],
                field.LIGHT_INSP: ["1,000.00"],
            }
        )
        row = df.iloc[0]
        rows = create_derived_rows_list(row)

        assert rows[0][field.DESCRIPTION] == desc.HEIGHT_VERIF
        assert rows[1][field.DESCRIPTION] == desc.LIGHT_INSP


class TestBuildDerivedRows:
    def test_processes_multiple_rows(self):
        df = pd.DataFrame(
            {
                field.BU: [12345, 67890],
                field.SORT_BY: [1000000, 1000100],
                field.HVF_NO_SPACE: ["1,000.00", "2,000.00"],
            }
        )
        rows = build_derived_rows(df)

        assert len(rows) == 2

    def test_returns_empty_list_for_empty_dataframe(self):
        df = pd.DataFrame()
        rows = build_derived_rows(df)
        assert rows == []


class TestTransformInputDataframe:
    def test_includes_output_columns(self, sample_input_df):
        result = transform_input_dataframe(sample_input_df)

        for col in field.OUTPUT_COLS:
            assert col in result.columns

    def test_renames_columns(self, sample_input_df):
        result = transform_input_dataframe(sample_input_df)

        assert field.DESCRIPTION in result.columns
        assert field.ADD_CAN_PRICE in result.columns
        assert field.HVF_NO_SPACE in result.columns

    def test_adds_base_subcategory(self, sample_input_df):
        result = transform_input_dataframe(sample_input_df)

        base_rows = result[result[field.SUB_CATEGORY] == subcat.BASE]
        assert len(base_rows) > 0

    def test_adds_sort_by_column(self, sample_input_df):
        result = transform_input_dataframe(sample_input_df)

        assert field.SORT_BY in result.columns
        assert result[field.SORT_BY].iloc[0] == 1000000

    def test_adds_extra_cans_column(self, sample_input_df):
        result = transform_input_dataframe(sample_input_df)

        assert field.EXTRA_CANS in result.columns

    def test_reformats_maintenance_to_string(self, sample_input_df):
        result = transform_input_dataframe(sample_input_df)

        maint_value = result[field.MAINT].iloc[0]
        assert isinstance(maint_value, str)
        assert ":" in maint_value

    def test_sorts_by_sort_by_column(self, sample_input_df):
        result = transform_input_dataframe(sample_input_df)

        sort_values = result[field.SORT_BY].tolist()
        assert sort_values == sorted(sort_values)

    def test_raises_on_missing_required_column(self):
        df = pd.DataFrame({field.BU: [12345]})

        with pytest.raises(ValueError, match="Missing required fields"):
            transform_input_dataframe(df)
