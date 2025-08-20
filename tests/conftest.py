import pytest
import pandas as pd
from tims_cli_tools import field


@pytest.fixture
def eight_twos():
    return 22222222  # shut up linter


@pytest.fixture
def df_clean_input_cols(eight_twos):
    return pd.DataFrame(
        data={
            field.BU: [eight_twos],
            field.STRUCTURE: ["3"],
            field.BASE_FOR_INV: ["Inspection"],
            field.TIA_INSP: ["1,000.00"],
            field.ADD_CAN_LEVEL: [3],
            field.HVF_NO_SPACE: ["1,000.00"],
            field.LIGHT_INSP: ["1,000.00"],
            field.MIG_BIRD: ["1,000.00"],
            field.WINDSIM: ["1,000.00"],
            field.TTP_INIT_READ: ["1,000.00"],
            field.TENSION: ["700.00"],
            field.HR_PAY: ["122.50"],
            field.SITE_TOTAL: ["1,000.00"],
            field.MAINT: ["00:15"],
            field.MAN_LIFT: ["$1234.56"],
            # generated rows added here just for processor testing
            field.EXTRA_CANS: [1],
        },
    )


@pytest.fixture
def df_series_input_cols(df_clean_input_cols):
    _, my_series = next(df_clean_input_cols.iterrows())
    return my_series
