from datetime import time

import pandas as pd
import pytest

from tims_cli_tools import desc, field, subcat
from tims_cli_tools.invoice_classes import (
    BaseColumnProcessor,
    EXTRA_CANSColumnProcessor,
    HVFColumnProcessor,
    LIGHT_INSPColumnProcessor,
    MAINTColumnProcessor,
    MAN_LIFTColumnProcessor,
    MIG_BIRDColumnProcessor,
    MoneyColumnProcessor,
    TENSIONColumnProcessor,
    TTP_INIT_READColumnProcessor,
    WINDSIMColumnProcessor,
)


@pytest.fixture
def base_row():
    return pd.Series(
        {
            field.BU: 22222222,
            field.STRUCTURE: 3,
            field.BASE_FOR_INV: "Inspection",
            field.TIA_INSP: 1000.00,
            field.ADD_CAN_LEVEL: 3,
            field.HVF_NO_SPACE: "$1,000.00",
            field.LIGHT_INSP: "$1,000.00",
            field.MIG_BIRD: "$1,000.00",
            field.WINDSIM: "$1,000.00",
            field.TTP_INIT_READ: "$1,000.00",
            field.TENSION: "$700.00",
            field.HR_PAY: 122.50,
            field.SITE_TOTAL: 1000.00,
            field.MAINT: time(hour=0, minute=15),
            field.MAN_LIFT: "$1,234.56",
            field.EXTRA_CANS: 2,
        }
    )


class TestBaseColumnProcessor:
    def test_get_column_value_returns_value(self, base_row):
        processor = BaseColumnProcessor(base_row)
        processor.column_name = field.BU
        assert processor._get_column_value(field.BU) == 22222222

    def test_get_column_value_raises_when_missing(self, base_row):
        processor = BaseColumnProcessor(base_row)
        processor.column_name = field.BU
        with pytest.raises(
            ValueError, match="Could not find value for field NONEXISTENT"
        ):
            processor._get_column_value("NONEXISTENT")

    def test_get_derived_row_returns_dict(self, base_row):
        processor = HVFColumnProcessor(base_row)
        result = processor.get_derived_row()

        assert field.BU in result
        assert field.SUB_CATEGORY in result
        assert field.DESCRIPTION in result
        assert field.QUANTITY in result
        assert result[field.BU] == 22222222
        assert result[field.SUB_CATEGORY] == subcat.ADDER
        assert result[field.DESCRIPTION] == desc.HEIGHT_VERIF
        assert result[field.QUANTITY] == 1


class TestMoneyColumnProcessor:
    def test_get_my_compare_value_from_string(self, base_row):
        processor = MoneyColumnProcessor(base_row)
        processor.column_name = field.HVF_NO_SPACE
        assert processor._get_my_compare_value() == 1000.00

    def test_get_my_compare_value_from_float(self, base_row):
        base_row[field.HVF_NO_SPACE] = 500.50
        processor = MoneyColumnProcessor(base_row)
        processor.column_name = field.HVF_NO_SPACE
        assert processor._get_my_compare_value() == 500.50

    def test_get_my_compare_value_from_int(self, base_row):
        base_row[field.HVF_NO_SPACE] = 500
        processor = MoneyColumnProcessor(base_row)
        processor.column_name = field.HVF_NO_SPACE
        assert processor._get_my_compare_value() == 500.00


class TestHVFColumnProcessor:
    def test_returns_correct_derived_row(self, base_row):
        processor = HVFColumnProcessor(base_row)
        result = processor.get_derived_row()

        assert result[field.SUB_CATEGORY] == subcat.ADDER
        assert result[field.DESCRIPTION] == desc.HEIGHT_VERIF
        assert result[field.QUANTITY] == 1
        assert result[field.BU] == 22222222


class TestLIGHT_INSPColumnProcessor:
    def test_returns_correct_derived_row(self, base_row):
        processor = LIGHT_INSPColumnProcessor(base_row)
        result = processor.get_derived_row()

        assert result[field.SUB_CATEGORY] == subcat.ADDER
        assert result[field.DESCRIPTION] == desc.LIGHT_INSP


class TestMIG_BIRDColumnProcessor:
    def test_returns_correct_derived_row(self, base_row):
        processor = MIG_BIRDColumnProcessor(base_row)
        result = processor.get_derived_row()

        assert result[field.SUB_CATEGORY] == subcat.ADDER
        assert result[field.DESCRIPTION] == desc.BIRD_WATCH


class TestWINDSIMColumnProcessor:
    def test_returns_correct_derived_row(self, base_row):
        processor = WINDSIMColumnProcessor(base_row)
        result = processor.get_derived_row()

        assert result[field.SUB_CATEGORY] == subcat.ADDER
        assert result[field.DESCRIPTION] == desc.WINDSIM


class TestTTP_INIT_READColumnProcessor:
    def test_returns_correct_derived_row(self, base_row):
        processor = TTP_INIT_READColumnProcessor(base_row)
        result = processor.get_derived_row()

        assert result[field.SUB_CATEGORY] == subcat.ADDER
        assert result[field.DESCRIPTION] == desc.GUY_TTP_INIT


class TestMAN_LIFTColumnProcessor:
    def test_returns_correct_derived_row(self, base_row):
        processor = MAN_LIFTColumnProcessor(base_row)
        result = processor.get_derived_row()

        assert result[field.SUB_CATEGORY] == subcat.WORK_AUTH
        assert result[field.DESCRIPTION] == desc.MANLIFT_RENTAL


class TestEXTRA_CANSColumnProcessor:
    def test_quantity_from_extra_cans_value(self, base_row):
        processor = EXTRA_CANSColumnProcessor(base_row)
        result = processor.get_derived_row()

        assert result[field.SUB_CATEGORY] == subcat.BASE
        assert result[field.DESCRIPTION] == desc.ADDITIONAL_CAN
        assert result[field.QUANTITY] == 2


class TestTENSIONColumnProcessor:
    def test_price_700_returns_correct_description(self, base_row):
        base_row[field.TENSION] = "$700.00"
        processor = TENSIONColumnProcessor(base_row)
        result = processor.get_derived_row()

        assert result[field.DESCRIPTION] == desc.GUY_TTP_1_6

    def test_price_850_returns_correct_description(self, base_row):
        base_row[field.TENSION] = "$850.00"
        processor = TENSIONColumnProcessor(base_row)
        result = processor.get_derived_row()

        assert result[field.DESCRIPTION] == desc.GUY_TTP_7_12

    def test_price_1000_returns_correct_description(self, base_row):
        base_row[field.TENSION] = "$1,000.00"
        processor = TENSIONColumnProcessor(base_row)
        result = processor.get_derived_row()

        assert result[field.DESCRIPTION] == desc.GUY_TTP_12_PLUS

    def test_unknown_price_raises_error(self, base_row):
        base_row[field.TENSION] = "$999.99"
        processor = TENSIONColumnProcessor(base_row)

        with pytest.raises(ValueError, match="Unexpected Tension Price value"):
            processor.get_derived_row()

    def test_price_as_float(self, base_row):
        base_row[field.TENSION] = 700.00
        processor = TENSIONColumnProcessor(base_row)
        result = processor.get_derived_row()

        assert result[field.DESCRIPTION] == desc.GUY_TTP_1_6


class TestMAINTColumnProcessor:
    def test_time_to_minutes_conversion(self, base_row):
        processor = MAINTColumnProcessor(base_row)
        result = processor.get_derived_row()

        assert result[field.SUB_CATEGORY] == subcat.ADDER
        assert result[field.DESCRIPTION] == desc.MAINT_MIN_RATE
        assert result[field.QUANTITY] == 15

    def test_hour_and_minute_conversion(self, base_row):
        base_row[field.MAINT] = time(hour=1, minute=30)
        processor = MAINTColumnProcessor(base_row)
        result = processor.get_derived_row()

        assert result[field.QUANTITY] == 90

    def test_invalid_time_format_raises_error(self, base_row):
        base_row[field.MAINT] = "invalid"
        processor = MAINTColumnProcessor(base_row)

        with pytest.raises(ValueError, match="Unexpected MAINTENANCE value"):
            processor.get_derived_row()
