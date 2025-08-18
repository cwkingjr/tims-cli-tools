import pytest
import pandas as pd
from tims_cli_tools import field

TWOS = 22222222  # shut up linter


@pytest.fixture
def df_clean_input_cols():
    return pd.DataFrame(
        data={
            field.BU: [TWOS],
            field.STRUCTURE: ["3"],
            field.BASE_FOR_INV: ["Inspection"],
            field.TIA_INSP: [1],
            field.ADD_CAN_LEVEL: [3],
            field.HVF_NO_SPACE: [1],
            field.LIGHT_INSP: [1],
            field.MIG_BIRD: [1],
            field.WINDSIM: [1],
            field.TTP_INIT_READ: [1],
            field.TENSION: [1],
            field.HR_PAY: [100.0],
            field.SITE_TOTAL: [200.0],
            field.MAINT: ["00:00:15"],
            field.MAN_LIFT: ["$1234.56"],
        },
    )


@pytest.fixture
def df_series_input_cols(df_clean_input_cols):
    _, my_series = next(df_clean_input_cols.iterrows())
    return my_series
