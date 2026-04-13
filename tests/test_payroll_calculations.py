from datetime import date, time

import pytest

from tims_cli_tools.payroll_calculations import (
    PaymentInput,
    PayrollCalculator,
    extract_payment_input,
    _coerce_to_float,
    _coerce_to_int_or_none,
    _coerce_to_str_or_none,
)
from tims_cli_tools.payroll_classes import (
    AdditionalPay,
    Crew,
    CrewLead,
    CrewSecond,
    Crews,
    PayType,
)


@pytest.fixture
def lead_pay_type():
    return PayType(
        name="Lead TIA",
        code="LEAD_STD",
        guyed=5.0,
        ss=3.0,
        mp=4.0,
        mp_cans=7.0,
    )


@pytest.fixture
def second_pay_type():
    return PayType(
        name="Second TIA",
        code="1T2",
        guyed=3.0,
        ss=2.0,
        mp=3.0,
        mp_cans=6.0,
    )


@pytest.fixture
def crew(lead_pay_type, second_pay_type):
    return Crew(
        lead=CrewLead(
            name="John Doe",
            spreadsheet_name="John",
            pay_type=lead_pay_type,
        ),
        second=CrewSecond(
            name="Jane Doe",
            crew_lead_name="John Doe",
            pay_type=second_pay_type,
        ),
    )


@pytest.fixture
def crews(crew):
    return Crews(crews=[crew])


@pytest.fixture
def additional_pay():
    return AdditionalPay(
        extra_cans_each=1.0,
        hr_pay_per_hour=60.0,
        hvf=10.0,
        lighting_inspection=5.0,
        migratory_bird=2.5,
        tension_1000=15.0,
        tension_700=10.0,
        tension_850=12.0,
        ttp_initial_reading=3.0,
        windsim=4.0,
    )


@pytest.fixture
def calculator(crews, additional_pay):
    return PayrollCalculator(crews=crews, additional_pay=additional_pay)


class TestPayrollCalculator:
    def test_calculate_lead_payment_guyed_structure(self, calculator, crews):
        input_data = PaymentInput(
            bu=12345,
            inspection_date=date(2025, 1, 15),
            crew_lead_spreadsheet_name="John",
            tia_inspection=100.0,
            extra_cans=None,
            hvf=0.0,
            lighting_inspection_price=0.0,
            migratory_bird=0.0,
            windsim=0.0,
            tension=0.0,
            maint=None,
            ecs_concealment_type=None,
            structure_type="Guyed",
        )

        payment = calculator.calculate_lead_payment(input_data)

        assert payment.bu == 12345
        assert payment.crew_lead == "John Doe"
        assert payment.pay_to == "John Doe"
        assert payment.structure_type == "Guyed"
        assert payment.tia_inspection == 5.0
        assert payment.site_total == 5.0

    def test_calculate_lead_payment_ss_structure(self, calculator, crews):
        input_data = PaymentInput(
            bu=12345,
            inspection_date=date(2025, 1, 15),
            crew_lead_spreadsheet_name="John",
            tia_inspection=100.0,
            extra_cans=None,
            hvf=0.0,
            lighting_inspection_price=0.0,
            migratory_bird=0.0,
            windsim=0.0,
            tension=0.0,
            maint=None,
            ecs_concealment_type=None,
            structure_type="SS",
        )

        payment = calculator.calculate_lead_payment(input_data)

        assert payment.tia_inspection == 3.0

    def test_calculate_second_payment(self, calculator, crews):
        input_data = PaymentInput(
            bu=12345,
            inspection_date=date(2025, 1, 15),
            crew_lead_spreadsheet_name="John",
            tia_inspection=100.0,
            extra_cans=None,
            hvf=0.0,
            lighting_inspection_price=0.0,
            migratory_bird=0.0,
            windsim=0.0,
            tension=0.0,
            maint=None,
            ecs_concealment_type=None,
            structure_type="Guyed",
        )

        payment = calculator.calculate_second_payment(input_data)

        assert payment.pay_to == "Jane Doe"
        assert payment.tia_inspection == 3.0

    def test_calculate_payment_with_extra_cans(self, calculator, crews):
        input_data = PaymentInput(
            bu=12345,
            inspection_date=date(2025, 1, 15),
            crew_lead_spreadsheet_name="John",
            tia_inspection=100.0,
            extra_cans=3,
            hvf=0.0,
            lighting_inspection_price=0.0,
            migratory_bird=0.0,
            windsim=0.0,
            tension=0.0,
            maint=None,
            ecs_concealment_type=None,
            structure_type="Guyed",
        )

        payment = calculator.calculate_lead_payment(input_data)

        assert payment.additional_canister_level == 3.0
        assert payment.extra_cans == 3

    def test_calculate_payment_with_hvf(self, calculator, crews):
        input_data = PaymentInput(
            bu=12345,
            inspection_date=date(2025, 1, 15),
            crew_lead_spreadsheet_name="John",
            tia_inspection=100.0,
            extra_cans=None,
            hvf=1.0,
            lighting_inspection_price=0.0,
            migratory_bird=0.0,
            windsim=0.0,
            tension=0.0,
            maint=None,
            ecs_concealment_type=None,
            structure_type="Guyed",
        )

        payment = calculator.calculate_lead_payment(input_data)

        assert payment.hvf == 10.0

    def test_calculate_payment_with_maintenance(self, calculator, crews):
        input_data = PaymentInput(
            bu=12345,
            inspection_date=date(2025, 1, 15),
            crew_lead_spreadsheet_name="John",
            tia_inspection=100.0,
            extra_cans=None,
            hvf=0.0,
            lighting_inspection_price=0.0,
            migratory_bird=0.0,
            windsim=0.0,
            tension=0.0,
            maint=time(hour=0, minute=30),
            ecs_concealment_type=None,
            structure_type="Guyed",
        )

        payment = calculator.calculate_lead_payment(input_data)

        assert payment.hr_pay == 30.0

    def test_calculate_payment_with_tension_700(self, calculator, crews):
        input_data = PaymentInput(
            bu=12345,
            inspection_date=date(2025, 1, 15),
            crew_lead_spreadsheet_name="John",
            tia_inspection=100.0,
            extra_cans=None,
            hvf=0.0,
            lighting_inspection_price=0.0,
            migratory_bird=0.0,
            windsim=0.0,
            tension=700.0,
            maint=None,
            ecs_concealment_type=None,
            structure_type="Guyed",
        )

        payment = calculator.calculate_lead_payment(input_data)

        assert payment.tension == 10.0

    def test_calculate_payment_with_tension_1000(self, calculator, crews):
        input_data = PaymentInput(
            bu=12345,
            inspection_date=date(2025, 1, 15),
            crew_lead_spreadsheet_name="John",
            tia_inspection=100.0,
            extra_cans=None,
            hvf=0.0,
            lighting_inspection_price=0.0,
            migratory_bird=0.0,
            windsim=0.0,
            tension=1000.0,
            maint=None,
            ecs_concealment_type=None,
            structure_type="Guyed",
        )

        payment = calculator.calculate_lead_payment(input_data)

        assert payment.tension == 15.0

    def test_calculate_payment_mp_flagpole_becomes_mp_cans(self, calculator, crews):
        input_data = PaymentInput(
            bu=12345,
            inspection_date=date(2025, 1, 15),
            crew_lead_spreadsheet_name="John",
            tia_inspection=100.0,
            extra_cans=None,
            hvf=0.0,
            lighting_inspection_price=0.0,
            migratory_bird=0.0,
            windsim=0.0,
            tension=0.0,
            maint=None,
            ecs_concealment_type="Flagpole",
            structure_type="MP",
        )

        payment = calculator.calculate_lead_payment(input_data)

        assert payment.structure_type == "MP_CANS"
        assert payment.tia_inspection == 7.0

    def test_calculate_payment_all_additions(self, calculator, crews):
        input_data = PaymentInput(
            bu=12345,
            inspection_date=date(2025, 1, 15),
            crew_lead_spreadsheet_name="John",
            tia_inspection=100.0,
            extra_cans=2,
            hvf=1.0,
            lighting_inspection_price=1.0,
            migratory_bird=1.0,
            windsim=1.0,
            tension=700.0,
            maint=time(hour=0, minute=15),
            ecs_concealment_type=None,
            structure_type="Guyed",
        )

        payment = calculator.calculate_lead_payment(input_data)

        assert payment.additional_canister_level == 2.0
        assert payment.hvf == 10.0
        assert payment.lighting_inspection_price == 5.0
        assert payment.migratory_bird == 2.5
        assert payment.windsim == 4.0
        assert payment.tension == 10.0
        assert payment.hr_pay == 15.0
        assert payment.tia_inspection == 5.0
        expected_total = 5.0 + 2.0 + 10.0 + 5.0 + 2.5 + 4.0 + 10.0 + 15.0
        assert payment.site_total == expected_total

    def test_unknown_structure_type_raises(self, calculator, crews):
        input_data = PaymentInput(
            bu=12345,
            inspection_date=date(2025, 1, 15),
            crew_lead_spreadsheet_name="John",
            tia_inspection=100.0,
            extra_cans=None,
            hvf=0.0,
            lighting_inspection_price=0.0,
            migratory_bird=0.0,
            windsim=0.0,
            tension=0.0,
            maint=None,
            ecs_concealment_type=None,
            structure_type="Unknown",
        )

        with pytest.raises(ValueError, match="Unknown PayType"):
            calculator.calculate_lead_payment(input_data)

    def test_unknown_crew_lead_raises(self, calculator, crews):
        input_data = PaymentInput(
            bu=12345,
            inspection_date=date(2025, 1, 15),
            crew_lead_spreadsheet_name="Unknown",
            tia_inspection=100.0,
            extra_cans=None,
            hvf=0.0,
            lighting_inspection_price=0.0,
            migratory_bird=0.0,
            windsim=0.0,
            tension=0.0,
            maint=None,
            ecs_concealment_type=None,
            structure_type="Guyed",
        )

        with pytest.raises(ValueError, match="Could not find crew"):
            calculator.calculate_lead_payment(input_data)


class TestExtractPaymentInput:
    def test_extract_payment_input(self):
        import pandas as pd
        from tims_cli_tools import field

        df = pd.DataFrame(
            data={
                field.BU: [12345],
                field.DATE: [date(2025, 1, 15)],
                field.CREW: ["John"],
                field.TIA_INSP: [100.0],
                field.EXTRA_CANS: [2],
                field.HVF_WITH_SPACE: [1.0],
                field.LIGHT_INSP: [0.5],
                field.MIG_BIRD: [1.0],
                field.WINDSIM: [2.0],
                field.TENSION: [700.0],
                field.MAINT: [time(hour=0, minute=30)],
                field.ECS_CONCEALMENT_TYPE: ["Flagpole"],
                field.STRUCTURE_TYPE: ["MP"],
            }
        )

        row = df.iloc[0]
        input_data = extract_payment_input(row)

        assert input_data.bu == 12345
        assert input_data.crew_lead_spreadsheet_name == "John"
        assert input_data.extra_cans == 2
        assert input_data.tension == 700.0


class TestCoerceFunctions:
    def test_coerce_to_float_from_int(self):
        assert _coerce_to_float(5) == 5.0

    def test_coerce_to_float_from_float(self):
        assert _coerce_to_float(5.5) == 5.5

    def test_coerce_to_float_from_string(self):
        assert _coerce_to_float("123.45") == 123.45

    def test_coerce_to_float_from_invalid_returns_zero(self):
        assert _coerce_to_float(None) == 0.0
        assert _coerce_to_float([]) == 0.0
        assert _coerce_to_float("$1,234.56") == 0.0

    def test_coerce_to_int_or_none_from_int(self):
        assert _coerce_to_int_or_none(5) == 5

    def test_coerce_to_int_or_none_from_float_whole_number(self):
        assert _coerce_to_int_or_none(5.0) == 5

    def test_coerce_to_int_or_none_from_string(self):
        assert _coerce_to_int_or_none("42") == 42

    def test_coerce_to_int_or_none_from_invalid_returns_none(self):
        assert _coerce_to_int_or_none(None) is None
        assert _coerce_to_int_or_none("not a number") is None

    def test_coerce_to_int_or_none_from_non_whole_float_coerces(self):
        assert _coerce_to_int_or_none(5.5) == 5

    def test_coerce_to_str_or_none_from_string(self):
        assert _coerce_to_str_or_none("  hello  ") == "hello"

    def test_coerce_to_str_or_none_from_empty_string_returns_none(self):
        assert _coerce_to_str_or_none("   ") is None

    def test_coerce_to_str_or_none_from_non_string_returns_none(self):
        assert _coerce_to_str_or_none(123) is None
        assert _coerce_to_str_or_none(None) is None
