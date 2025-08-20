from tims_cli_tools import field, desc, classes, subcat
import pytest


def test_HVFColumnProcessor(df_series_input_cols, eight_twos):
    expected = {
        "BU": eight_twos,
        "DESCRIPTION": desc.HEIGHT_VERIF,
        "QUANTITY": 1,
        "SUB CATEGORY": subcat.ADDER,
    }
    assert (
        classes.HVFColumnProcessor(row=df_series_input_cols).get_derived_row()
        == expected
    )


def test_HVFColumnProcessor_invalid(df_series_input_cols):
    df_series_input_cols[field.HVF_NO_SPACE] = "invalid"
    with pytest.raises(ValueError):
        assert classes.HVFColumnProcessor(row=df_series_input_cols).get_derived_row()


def test_LIGHT_INSPColumnProcessor(df_series_input_cols, eight_twos):
    expected = {
        "BU": eight_twos,
        "DESCRIPTION": desc.LIGHT_INSP,
        "QUANTITY": 1,
        "SUB CATEGORY": subcat.ADDER,
    }
    assert (
        classes.LIGHT_INSPColumnProcessor(row=df_series_input_cols).get_derived_row()
        == expected
    )


def test_LIGHT_INSPColumnProcessor_invalid(df_series_input_cols):
    df_series_input_cols[field.LIGHT_INSP] = "invalid"
    with pytest.raises(ValueError):
        assert classes.LIGHT_INSPColumnProcessor(
            row=df_series_input_cols
        ).get_derived_row()


def test_MIG_BIRDColumnProcessor(df_series_input_cols, eight_twos):
    expected = {
        "BU": eight_twos,
        "DESCRIPTION": desc.BIRD_WATCH,
        "QUANTITY": 1,
        "SUB CATEGORY": subcat.ADDER,
    }
    assert (
        classes.MIG_BIRDColumnProcessor(row=df_series_input_cols).get_derived_row()
        == expected
    )


def test_MIG_BIRDColumnProcessor_invalid(df_series_input_cols):
    df_series_input_cols[field.MIG_BIRD] = "invalid"
    with pytest.raises(ValueError):
        assert classes.MIG_BIRDColumnProcessor(
            row=df_series_input_cols
        ).get_derived_row()


def test_WINDSIMColumnProcessor(df_series_input_cols, eight_twos):
    expected = {
        "BU": eight_twos,
        "DESCRIPTION": desc.WINDSIM,
        "QUANTITY": 1,
        "SUB CATEGORY": subcat.ADDER,
    }
    assert (
        classes.WINDSIMColumnProcessor(row=df_series_input_cols).get_derived_row()
        == expected
    )


def test_WINDSIMColumnProcessor_invalid(df_series_input_cols):
    df_series_input_cols[field.WINDSIM] = "invalid"
    with pytest.raises(ValueError):
        assert classes.WINDSIMColumnProcessor(
            row=df_series_input_cols
        ).get_derived_row()


def test_TTP_INIT_READColumnProcessor(df_series_input_cols, eight_twos):
    expected = {
        "BU": eight_twos,
        "DESCRIPTION": desc.GUY_TTP_INIT,
        "QUANTITY": 1,
        "SUB CATEGORY": subcat.ADDER,
    }
    assert (
        classes.TTP_INIT_READColumnProcessor(row=df_series_input_cols).get_derived_row()
        == expected
    )


def test_TTP_INIT_READColumnProcessor_invalid(df_series_input_cols):
    df_series_input_cols[field.TTP_INIT_READ] = "invalid"
    with pytest.raises(ValueError):
        assert classes.TTP_INIT_READColumnProcessor(
            row=df_series_input_cols
        ).get_derived_row()


def test_MAN_LIFTColumnProcessor(df_series_input_cols, eight_twos):
    expected = {
        "BU": eight_twos,
        "DESCRIPTION": desc.MANLIFT_RENTAL,
        "QUANTITY": 1,
        "SUB CATEGORY": subcat.WORK_AUTH,
    }
    assert (
        classes.MAN_LIFTColumnProcessor(row=df_series_input_cols).get_derived_row()
        == expected
    )


def test_MAN_LIFTColumnProcessor_invalid(df_series_input_cols):
    df_series_input_cols[field.MAN_LIFT] = "invalid"
    with pytest.raises(ValueError):
        assert classes.MAN_LIFTColumnProcessor(
            row=df_series_input_cols
        ).get_derived_row()


def test_EXTRA_CANSColumnProcessor(df_series_input_cols, eight_twos):
    expected = {
        "BU": eight_twos,
        "DESCRIPTION": desc.ADDITIONAL_CAN,
        "QUANTITY": 1,
        "SUB CATEGORY": subcat.BASE,
    }
    assert (
        classes.EXTRA_CANSColumnProcessor(row=df_series_input_cols).get_derived_row()
        == expected
    )


def test_EXTRA_CANSColumnProcessor_invalid(df_series_input_cols):
    df_series_input_cols[field.EXTRA_CANS] = "invalid"
    with pytest.raises(ValueError):
        assert classes.EXTRA_CANSColumnProcessor(
            row=df_series_input_cols
        ).get_derived_row()


def test_TENSIONColumnProcessor_700(df_series_input_cols, eight_twos):
    expected = {
        "BU": eight_twos,
        "DESCRIPTION": desc.GUY_TTP_1_6,
        "QUANTITY": 1,
        "SUB CATEGORY": subcat.ADDER,
    }
    assert (
        classes.TENSIONColumnProcessor(row=df_series_input_cols).get_derived_row()
        == expected
    )


def test_TENSIONColumnProcessor_850(df_series_input_cols, eight_twos):
    df_series_input_cols[field.TENSION] = "850.00"
    expected = {
        "BU": eight_twos,
        "DESCRIPTION": desc.GUY_TTP_7_12,
        "QUANTITY": 1,
        "SUB CATEGORY": subcat.ADDER,
    }
    assert (
        classes.TENSIONColumnProcessor(row=df_series_input_cols).get_derived_row()
        == expected
    )


def test_TENSIONColumnProcessor_1000(df_series_input_cols, eight_twos):
    df_series_input_cols[field.TENSION] = "1,000"
    expected = {
        "BU": eight_twos,
        "DESCRIPTION": desc.GUY_TTP_12_PLUS,
        "QUANTITY": 1,
        "SUB CATEGORY": subcat.ADDER,
    }
    assert (
        classes.TENSIONColumnProcessor(row=df_series_input_cols).get_derived_row()
        == expected
    )


def test_TENSIONColumnProcessor_invalid(df_series_input_cols):
    df_series_input_cols[field.TENSION] = "invalid"
    with pytest.raises(ValueError):
        assert classes.TENSIONColumnProcessor(
            row=df_series_input_cols
        ).get_derived_row()

        # # set correct description based upon price
        # if my_value == price.PRICE_700:
        #     self.description = desc.GUY_TTP_1_6
        # elif my_value == price.PRICE_850:
        #     self.description = desc.GUY_TTP_7_12
        # elif my_value == price.PRICE_1000:
        #     self.description = desc.GUY_TTP_12_PLUS
