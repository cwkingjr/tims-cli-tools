from dataclasses import dataclass
from datetime import date, time

from . import field, price
from .payroll_classes import AdditionalPay, Crew, Crews
from .pandas_utils import get_value_from_series_col
import pandas as pd


@dataclass
class PaymentInput:
    bu: int
    inspection_date: date
    crew_lead_spreadsheet_name: str
    tia_inspection: float
    extra_cans: int | None
    hvf: float
    lighting_inspection_price: float
    migratory_bird: float
    windsim: float
    tension: float
    maint: time | None
    ecs_concealment_type: str | None
    structure_type: str


@dataclass
class PaymentValues:
    bu: int
    inspection_date: date
    crew_lead: str
    pay_to: str
    structure_type: str
    tia_inspection: float
    additional_canister_level: float
    hvf: float
    lighting_inspection_price: float
    migratory_bird: float
    windsim: float
    tension: float
    hr_pay: float
    site_total: float
    maintenance: time | None
    extra_cans: int


class PayrollCalculator:
    def __init__(self, crews: Crews, additional_pay: AdditionalPay) -> None:
        self.crews = crews
        self.additional_pay = additional_pay

    def calculate_lead_payment(self, input_data: PaymentInput) -> PaymentValues:
        crew = self.crews.get_crew_by_lead_spreadsheet_name(
            spreadsheet_name=input_data.crew_lead_spreadsheet_name
        )
        return self._calculate_payment(input_data, crew, crew.lead.name)

    def calculate_second_payment(self, input_data: PaymentInput) -> PaymentValues:
        crew = self.crews.get_crew_by_lead_spreadsheet_name(
            spreadsheet_name=input_data.crew_lead_spreadsheet_name
        )
        return self._calculate_payment(input_data, crew, crew.second.name)

    def _calculate_payment(
        self, input_data: PaymentInput, crew: Crew, pay_to_name: str
    ) -> PaymentValues:
        structure_type = self._normalize_structure_type(
            input_data.structure_type, input_data.ecs_concealment_type
        )

        additional_canister_level = self._calculate_additional_canister_level(
            input_data.extra_cans
        )
        hvf_pay = self._calculate_hvf_pay(input_data.hvf)
        lighting_inspection_pay = self._calculate_lighting_inspection_pay(
            input_data.lighting_inspection_price
        )
        migratory_bird_pay = self._calculate_migratory_bird_pay(
            input_data.migratory_bird
        )
        windsim_pay = self._calculate_windsim_pay(input_data.windsim)
        tension_pay = self._calculate_tension_pay(input_data.tension)
        hr_pay = self._calculate_hr_pay(input_data.maint)

        tia_inspection = crew.lead.pay_type.get_pay_by_str(structure_type)
        if pay_to_name == crew.second.name:
            tia_inspection = crew.second.pay_type.get_pay_by_str(structure_type)

        common_total = (
            additional_canister_level
            + hvf_pay
            + lighting_inspection_pay
            + migratory_bird_pay
            + windsim_pay
            + tension_pay
            + hr_pay
        )

        site_total = tia_inspection + common_total

        return PaymentValues(
            bu=input_data.bu,
            inspection_date=input_data.inspection_date,
            crew_lead=crew.lead.name,
            pay_to=pay_to_name,
            structure_type=structure_type,
            tia_inspection=tia_inspection,
            additional_canister_level=additional_canister_level,
            hvf=hvf_pay,
            lighting_inspection_price=lighting_inspection_pay,
            migratory_bird=migratory_bird_pay,
            windsim=windsim_pay,
            tension=tension_pay,
            hr_pay=hr_pay,
            site_total=site_total,
            maintenance=input_data.maint,
            extra_cans=input_data.extra_cans or 0,
        )

    def _normalize_structure_type(
        self, structure_type: str, ecs_concealment_type: str | None
    ) -> str:
        normalized = structure_type.strip()
        if (
            normalized.lower() == "mp"
            and isinstance(ecs_concealment_type, str)
            and ecs_concealment_type.strip().lower() == "flagpole"
        ):
            normalized = "MP_CANS"
        return normalized

    def _calculate_additional_canister_level(self, extra_cans: int | None) -> float:
        if not isinstance(extra_cans, int | float) or int(extra_cans) <= 0:
            return 0.0
        return self.additional_pay.extra_cans_each * extra_cans

    def _calculate_hvf_pay(self, hvf: float) -> float:
        if not isinstance(hvf, int | float) or float(hvf) <= 0.0:
            return 0.0
        return self.additional_pay.hvf

    def _calculate_lighting_inspection_pay(self, value: float) -> float:
        if not isinstance(value, int | float) or float(value) <= 0.0:
            return 0.0
        return self.additional_pay.lighting_inspection

    def _calculate_migratory_bird_pay(self, value: float) -> float:
        if not isinstance(value, int | float) or float(value) <= 0.0:
            return 0.0
        return self.additional_pay.migratory_bird

    def _calculate_windsim_pay(self, value: float) -> float:
        if not isinstance(value, int | float) or float(value) <= 0.0:
            return 0.0
        return self.additional_pay.windsim

    def _calculate_tension_pay(self, tension: float) -> float:
        if not isinstance(tension, int | float):
            return 0.0
        tension_val = float(tension)
        if tension_val == price.PRICE_700:
            return self.additional_pay.tension_700
        if tension_val == price.PRICE_850:
            return self.additional_pay.tension_850
        if tension_val == price.PRICE_1000:
            return self.additional_pay.tension_1000
        return 0.0

    def _calculate_hr_pay(self, maint: time | None) -> float:
        if not isinstance(maint, time) or (maint.hour == 0 and maint.minute == 0):
            return 0.0
        minutes = maint.hour * 60 + maint.minute
        pay_per_minute = self.additional_pay.hr_pay_per_hour / 60
        return minutes * pay_per_minute


def extract_payment_input(row: pd.Series) -> PaymentInput:
    return PaymentInput(
        bu=get_value_from_series_col(series=row, column_name=field.BU),
        inspection_date=get_value_from_series_col(series=row, column_name=field.DATE),
        crew_lead_spreadsheet_name=get_value_from_series_col(
            series=row, column_name=field.CREW
        ).strip(),
        tia_inspection=_coerce_to_float(
            get_value_from_series_col(series=row, column_name=field.TIA_INSP)
        ),
        extra_cans=_coerce_to_int_or_none(
            get_value_from_series_col(series=row, column_name=field.EXTRA_CANS)
        ),
        hvf=_coerce_to_float(
            get_value_from_series_col(series=row, column_name=field.HVF_WITH_SPACE)
        ),
        lighting_inspection_price=_coerce_to_float(
            get_value_from_series_col(series=row, column_name=field.LIGHT_INSP)
        ),
        migratory_bird=_coerce_to_float(
            get_value_from_series_col(series=row, column_name=field.MIG_BIRD)
        ),
        windsim=_coerce_to_float(
            get_value_from_series_col(series=row, column_name=field.WINDSIM)
        ),
        tension=_coerce_to_float(
            get_value_from_series_col(series=row, column_name=field.TENSION)
        ),
        maint=get_value_from_series_col(series=row, column_name=field.MAINT),
        ecs_concealment_type=_coerce_to_str_or_none(
            get_value_from_series_col(
                series=row, column_name=field.ECS_CONCEALMENT_TYPE
            )
        ),
        structure_type=get_value_from_series_col(
            series=row, column_name=field.STRUCTURE_TYPE
        ),
    )


def _coerce_to_float(value) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(value)
    except TypeError, ValueError:
        return 0.0


def _coerce_to_int_or_none(value) -> int | None:
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    try:
        return int(value)
    except TypeError, ValueError:
        return None


def _coerce_to_str_or_none(value) -> str | None:
    if isinstance(value, str):
        return value.strip() or None
    return None
