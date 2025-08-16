import pytest

from tims_cli_tools.tims_invoice_transformer import (
    ensure_int,
    check_for_required_fields,
)
from tims_cli_tools import field

import pandas as pd


@pytest.fixture
def pd_series():
    return pd.Series(
        {
            field.BU: "22222222",
            field.HVF: "1",
            field.SORT_BY: "1000200",
            field.SUB_CATEGORY: "ADDER",
            field.DESCRIPTION: "Description1",
            field.QUANTITY: "1",
            field.TIA_INSP: "1",
            field.ADD_CAN: "3",
            field.LIGHT_INSP: "1",
            field.MIG_BIRD: "1",
            field.WINDSIM: "1",
            field.TTP_INIT_READ: "1",
            field.TENSION: "1",
            field.HR_PAY: "100.0",
            field.SITE_TOTAL: "200.0",
            field.MAINT: "00:00:15",
        },
    )


def test_check_for_required_fields(pd_series):
    assert check_for_required_fields(pd_series) is None

    # remove a required field to test the failure case
    pd_series_copy = pd_series.copy()
    del pd_series_copy[field.BU]
    with pytest.raises(ValueError):
        assert check_for_required_fields(pd_series_copy)


@pytest.mark.parametrize(
    "number, col_name, expected",
    [
        (3, field.HVF, True),
        (3.5, field.HVF, True),
        (None, field.HVF, False),
        ("string", field.HVF, False),
        (3, "non_existent_field", False),  # Non-existent field
    ],
)
def test_ensure_int(number, col_name, expected, pd_series):
    assert ensure_int(number=number, col_name=col_name, row=pd_series) == expected
