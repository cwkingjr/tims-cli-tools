from datetime import date, time
from pathlib import Path
import tempfile

import pytest

from tims_cli_tools.payroll_calculations import PaymentValues
from tims_cli_tools.payroll_repository import (
    DuckDBPaymentRepository,
    create_repository,
)


@pytest.fixture
def temp_db():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = Path(f.name)
    yield db_path
    if db_path.exists():
        db_path.unlink()


@pytest.fixture
def repository(temp_db):
    if temp_db.exists():
        temp_db.unlink()
    repo = DuckDBPaymentRepository(temp_db)
    repo.connect()
    yield repo
    repo.close()


@pytest.fixture
def sample_payment():
    return PaymentValues(
        bu=12345,
        inspection_date=date(2025, 1, 15),
        crew_lead="John Doe",
        pay_to="John Doe",
        structure_type="Guyed",
        tia_inspection=5.0,
        additional_canister_level=2.0,
        hvf=10.0,
        lighting_inspection_price=5.0,
        migratory_bird=2.5,
        windsim=4.0,
        tension=10.0,
        hr_pay=15.0,
        site_total=53.5,
        maintenance=time(hour=0, minute=30),
        extra_cans=2,
    )


class TestDuckDBPaymentRepository:
    def test_insert_and_retrieve(self, repository, sample_payment):
        repository.insert(sample_payment)

        df = repository.get_all()

        assert len(df) == 1
        assert df.iloc[0]["bu"] == 12345
        assert df.iloc[0]["pay_to"] == "John Doe"

    def test_get_all_totals_single_payee(self, repository, sample_payment):
        repository.insert(sample_payment)

        totals = repository.get_all_totals()

        assert len(totals) == 1
        assert totals.iloc[0]["pay_to"] == "John Doe"
        assert totals.iloc[0]["tia_inspection"] == 5.0

    def test_get_all_totals_multiple_payments(self, repository):
        payment1 = PaymentValues(
            bu=1,
            inspection_date=date(2025, 1, 15),
            crew_lead="Lead",
            pay_to="Worker A",
            structure_type="Guyed",
            tia_inspection=5.0,
            additional_canister_level=0.0,
            hvf=0.0,
            lighting_inspection_price=0.0,
            migratory_bird=0.0,
            windsim=0.0,
            tension=0.0,
            hr_pay=0.0,
            site_total=5.0,
            maintenance=None,
            extra_cans=0,
        )
        payment2 = PaymentValues(
            bu=2,
            inspection_date=date(2025, 1, 16),
            crew_lead="Lead",
            pay_to="Worker A",
            structure_type="Guyed",
            tia_inspection=5.0,
            additional_canister_level=0.0,
            hvf=0.0,
            lighting_inspection_price=0.0,
            migratory_bird=0.0,
            windsim=0.0,
            tension=0.0,
            hr_pay=0.0,
            site_total=5.0,
            maintenance=None,
            extra_cans=0,
        )

        repository.insert(payment1)
        repository.insert(payment2)

        totals = repository.get_all_totals()

        assert len(totals) == 1
        assert totals.iloc[0]["pay_to"] == "Worker A"
        assert totals.iloc[0]["tia_inspection"] == 10.0

    def test_get_by_payee(self, repository):
        payment_a = PaymentValues(
            bu=1,
            inspection_date=date(2025, 1, 15),
            crew_lead="Lead",
            pay_to="Worker A",
            structure_type="Guyed",
            tia_inspection=5.0,
            additional_canister_level=0.0,
            hvf=0.0,
            lighting_inspection_price=0.0,
            migratory_bird=0.0,
            windsim=0.0,
            tension=0.0,
            hr_pay=0.0,
            site_total=5.0,
            maintenance=None,
            extra_cans=0,
        )
        payment_b = PaymentValues(
            bu=2,
            inspection_date=date(2025, 1, 16),
            crew_lead="Lead",
            pay_to="Worker B",
            structure_type="Guyed",
            tia_inspection=3.0,
            additional_canister_level=0.0,
            hvf=0.0,
            lighting_inspection_price=0.0,
            migratory_bird=0.0,
            windsim=0.0,
            tension=0.0,
            hr_pay=0.0,
            site_total=3.0,
            maintenance=None,
            extra_cans=0,
        )

        repository.insert(payment_a)
        repository.insert(payment_b)

        name, df = repository.get_by_payee("Worker A")

        assert name == "Worker A"
        assert len(df) == 1
        assert df.iloc[0]["bu"] == 1

    def test_get_individual_totals(self, repository):
        payment_a1 = PaymentValues(
            bu=1,
            inspection_date=date(2025, 1, 15),
            crew_lead="Lead",
            pay_to="Worker A",
            structure_type="Guyed",
            tia_inspection=5.0,
            additional_canister_level=0.0,
            hvf=0.0,
            lighting_inspection_price=0.0,
            migratory_bird=0.0,
            windsim=0.0,
            tension=0.0,
            hr_pay=10.0,
            site_total=15.0,
            maintenance=None,
            extra_cans=0,
        )
        payment_a2 = PaymentValues(
            bu=2,
            inspection_date=date(2025, 1, 16),
            crew_lead="Lead",
            pay_to="Worker A",
            structure_type="SS",
            tia_inspection=3.0,
            additional_canister_level=0.0,
            hvf=0.0,
            lighting_inspection_price=0.0,
            migratory_bird=0.0,
            windsim=0.0,
            tension=0.0,
            hr_pay=5.0,
            site_total=8.0,
            maintenance=None,
            extra_cans=0,
        )

        repository.insert(payment_a1)
        repository.insert(payment_a2)

        totals = repository.get_individual_totals("Worker A")

        assert len(totals) == 1
        assert totals.iloc[0]["tia_inspection"] == 8.0
        assert totals.iloc[0]["hr_pay"] == 15.0

    def test_insert_without_maintenance(self, repository):
        payment = PaymentValues(
            bu=12345,
            inspection_date=date(2025, 1, 15),
            crew_lead="Lead",
            pay_to="Worker",
            structure_type="Guyed",
            tia_inspection=5.0,
            additional_canister_level=0.0,
            hvf=0.0,
            lighting_inspection_price=0.0,
            migratory_bird=0.0,
            windsim=0.0,
            tension=0.0,
            hr_pay=0.0,
            site_total=5.0,
            maintenance=None,
            extra_cans=0,
        )

        repository.insert(payment)

        df = repository.get_all()
        assert len(df) == 1

    def test_close(self, repository):
        repository.close()

        with pytest.raises(RuntimeError, match="not connected"):
            repository.insert(
                PaymentValues(
                    bu=1,
                    inspection_date=date(2025, 1, 1),
                    crew_lead="Lead",
                    pay_to="Worker",
                    structure_type="Guyed",
                    tia_inspection=0.0,
                    additional_canister_level=0.0,
                    hvf=0.0,
                    lighting_inspection_price=0.0,
                    migratory_bird=0.0,
                    windsim=0.0,
                    tension=0.0,
                    hr_pay=0.0,
                    site_total=0.0,
                    maintenance=None,
                    extra_cans=0,
                )
            )


class TestCreateRepository:
    def test_creates_and_connects(self, temp_db):
        repo = create_repository(temp_db)

        assert repo._con is not None

        repo.close()
        temp_db.unlink(missing_ok=True)

    def test_deletes_existing_db(self, temp_db):
        temp_db.write_text("existing content")

        repo = create_repository(temp_db)

        df = repo.get_all()
        assert len(df) == 0

        repo.close()
