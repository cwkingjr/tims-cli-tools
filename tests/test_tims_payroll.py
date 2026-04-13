from datetime import date, time
from pathlib import Path
import tempfile

import pandas as pd
import pytest

from tims_cli_tools import field
from tims_cli_tools.payroll_classes import (
    AdditionalPay,
    Crew,
    CrewLead,
    CrewSecond,
    Crews,
    PayType,
)
from tims_cli_tools.payroll_repository import create_repository
from tims_cli_tools.payroll_writers import (
    ConsolidatedSpreadsheetWriter,
    IndividualSpreadsheetWriter,
)
from tims_cli_tools.tims_payroll import ProcessPayrollConfig


class MockConsolidatedWriter(ConsolidatedSpreadsheetWriter):
    def __init__(self):
        self.written = []

    def write(
        self,
        *,
        original_df: pd.DataFrame,
        all_payments_df: pd.DataFrame,
        all_payments_totals_df: pd.DataFrame,
        payee_tuples: list[tuple[str, pd.DataFrame]],
    ) -> Path:
        self.written.append(
            {
                "original_df": original_df,
                "all_payments_df": all_payments_df,
                "all_payments_totals_df": all_payments_totals_df,
                "payee_tuples": payee_tuples,
            }
        )
        return Path("/tmp/consolidated.xlsx")


class MockIndividualWriter(IndividualSpreadsheetWriter):
    def __init__(self):
        self.written = []

    def write(
        self,
        *,
        pay_to_name: str,
        individual_payments_totals_df: pd.DataFrame,
        individual_payments_df: pd.DataFrame,
    ) -> Path:
        self.written.append(
            {
                "pay_to_name": pay_to_name,
                "totals": individual_payments_totals_df,
                "payments": individual_payments_df,
            }
        )
        return Path(f"/tmp/payroll_{pay_to_name}.xlsx")


@pytest.fixture
def crews():
    lead_type = PayType(
        name="Lead", code="LEAD", guyed=5.0, ss=3.0, mp=4.0, mp_cans=7.0
    )
    second_type = PayType(
        name="Second", code="2ND", guyed=3.0, ss=2.0, mp=3.0, mp_cans=6.0
    )
    return Crews(
        crews=[
            Crew(
                lead=CrewLead(
                    name="John Doe",
                    spreadsheet_name="John",
                    pay_type=lead_type,
                ),
                second=CrewSecond(
                    name="Jane Doe",
                    crew_lead_name="John Doe",
                    pay_type=second_type,
                ),
            )
        ]
    )


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
def sample_input_df():
    return pd.DataFrame(
        data={
            field.BU: [12345],
            field.DATE: [date(2025, 1, 15)],
            field.CREW: ["John"],
            field.STRUCTURE: [3],
            field.BASE_FOR_INV: ["Inspection"],
            field.TIA_INSP: [1.0],
            field.ADD_CAN_LEVEL: [3],
            field.HVF_WITH_SPACE: [1.0],
            field.LIGHT_INSP: [1.0],
            field.MIG_BIRD: [1.0],
            field.WINDSIM: [1.0],
            field.TTP_INIT_READ: [1.0],
            field.TENSION: [700.0],
            field.HR_PAY: [60.0],
            field.SITE_TOTAL: [100.0],
            field.MAINT: [time(hour=0, minute=15)],
            field.MAN_LIFT: [1.0],
            field.ECS_CONCEALMENT_TYPE: [None],
            field.STRUCTURE_TYPE: ["Guyed"],
            field.EXTRA_CANS: [2],
        }
    )


@pytest.fixture
def temp_db():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = Path(f.name)
    yield db_path
    if db_path.exists():
        db_path.unlink()


class TestProcessPayroll:
    def test_process_payroll_single_row(
        self, crews, additional_pay, sample_input_df, temp_db
    ):
        from tims_cli_tools.tims_payroll import process_payroll

        repo = create_repository(temp_db)
        writer = MockConsolidatedWriter()

        try:
            process_payroll(
                ProcessPayrollConfig(
                    input_df=sample_input_df,
                    crews=crews,
                    additional_pay=additional_pay,
                    repository=repo,
                    create_crew_spreadsheets=False,
                    consolidated_writer=writer,
                )
            )

            assert len(writer.written) == 1
            result = writer.written[0]
            assert len(result["all_payments_df"]) == 2
            assert len(result["all_payments_totals_df"]) == 2
        finally:
            repo.close()

    def test_process_payroll_creates_two_payments_per_row(
        self, crews, additional_pay, sample_input_df, temp_db
    ):
        from tims_cli_tools.tims_payroll import process_payroll

        repo = create_repository(temp_db)
        writer = MockConsolidatedWriter()

        try:
            process_payroll(
                ProcessPayrollConfig(
                    input_df=sample_input_df,
                    crews=crews,
                    additional_pay=additional_pay,
                    repository=repo,
                    create_crew_spreadsheets=False,
                    consolidated_writer=writer,
                )
            )

            result = writer.written[0]
            payees = result["all_payments_df"]["pay_to"].tolist()
            assert "John Doe" in payees
            assert "Jane Doe" in payees
        finally:
            repo.close()

    def test_process_payroll_with_individual_spreadsheets(
        self, crews, additional_pay, sample_input_df, temp_db
    ):
        from tims_cli_tools.tims_payroll import process_payroll

        repo = create_repository(temp_db)
        consolidated_writer = MockConsolidatedWriter()
        individual_writer = MockIndividualWriter()

        try:
            process_payroll(
                ProcessPayrollConfig(
                    input_df=sample_input_df,
                    crews=crews,
                    additional_pay=additional_pay,
                    repository=repo,
                    create_crew_spreadsheets=True,
                    consolidated_writer=consolidated_writer,
                    individual_writer=individual_writer,
                )
            )

            assert len(individual_writer.written) == 2
            payee_names = [w["pay_to_name"] for w in individual_writer.written]
            assert "John Doe" in payee_names
            assert "Jane Doe" in payee_names
        finally:
            repo.close()

    def test_process_payroll_calculates_totals_correctly(
        self, crews, additional_pay, sample_input_df, temp_db
    ):
        from tims_cli_tools.tims_payroll import process_payroll

        repo = create_repository(temp_db)
        writer = MockConsolidatedWriter()

        try:
            process_payroll(
                ProcessPayrollConfig(
                    input_df=sample_input_df,
                    crews=crews,
                    additional_pay=additional_pay,
                    repository=repo,
                    create_crew_spreadsheets=False,
                    consolidated_writer=writer,
                )
            )

            result = writer.written[0]
            totals_df = result["all_payments_totals_df"]

            for _, row in totals_df.iterrows():
                assert row["extra_cans"] == 2
        finally:
            repo.close()
