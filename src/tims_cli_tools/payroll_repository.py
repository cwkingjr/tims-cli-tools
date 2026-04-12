from datetime import time
from pathlib import Path
from typing import Protocol, Self

import pandas as pd
import duckdb

from .payroll_calculations import PaymentValues


class PaymentRepository(Protocol):
    def insert(self, payment: PaymentValues) -> None: ...

    def get_all(self) -> pd.DataFrame: ...

    def get_all_totals(self) -> pd.DataFrame: ...

    def get_by_payee(self, pay_to: str) -> tuple[str, pd.DataFrame]: ...

    def get_individual_totals(self, pay_to: str) -> pd.DataFrame: ...

    def close(self) -> None: ...


class DuckDBPaymentRepository:
    CREATE_SEQUENCE = "CREATE SEQUENCE sequence_payments START 1;"

    CREATE_TABLE = """
        CREATE TABLE payments (
            id integer PRIMARY KEY DEFAULT nextval('sequence_payments'),
            bu integer,
            inspection_date date,
            crew_lead VARCHAR,
            pay_to VARCHAR,
            structure_type VARCHAR,
            tia_inspection float,
            additional_canister_level float,
            hvf float,
            lighting_inspection_price float,
            migratory_bird float,
            windsim float,
            tension float,
            hr_pay float,
            site_total float,
            maintenance time,
            extra_cans int,
        )
    """

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        self._con: duckdb.DuckDBPyConnection | None = None

    def connect(self) -> Self:
        self._con = duckdb.connect(database=str(self._db_path))
        self._con.execute(self.CREATE_SEQUENCE)
        self._con.execute(self.CREATE_TABLE)
        return self

    def insert(self, payment: PaymentValues) -> None:
        if self._con is None:
            msg = "Repository not connected. Call connect() first."
            raise RuntimeError(msg)

        self._con.execute(
            """
            INSERT INTO payments (
                bu, inspection_date, crew_lead, pay_to, structure_type,
                tia_inspection, additional_canister_level, hvf,
                lighting_inspection_price, migratory_bird, windsim,
                tension, hr_pay, site_total, maintenance, extra_cans
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            [
                payment.bu,
                payment.inspection_date,
                payment.crew_lead,
                payment.pay_to,
                payment.structure_type,
                payment.tia_inspection,
                payment.additional_canister_level,
                payment.hvf,
                payment.lighting_inspection_price,
                payment.migratory_bird,
                payment.windsim,
                payment.tension,
                payment.hr_pay,
                payment.site_total,
                payment.maintenance or time(hour=0, minute=0),
                payment.extra_cans,
            ],
        )

    def get_all(self) -> pd.DataFrame:
        if self._con is None:
            msg = "Repository not connected."
            raise RuntimeError(msg)
        result = self._con.execute(
            "SELECT * FROM payments ORDER BY inspection_date, bu"
        )
        return result.df()

    def get_all_totals(self) -> pd.DataFrame:
        if self._con is None:
            msg = "Repository not connected."
            raise RuntimeError(msg)
        result = self._con.execute(
            """
            SELECT
                pay_to,
                SUM(tia_inspection) as tia_inspection,
                SUM(additional_canister_level) as additional_canister_level,
                SUM(hvf) as hvf,
                SUM(lighting_inspection_price) as lighting_inspection_price,
                SUM(migratory_bird) as migratory_bird,
                SUM(windsim) as windsim,
                SUM(tension) as tension,
                SUM(hr_pay) as hr_pay,
                SUM(site_total) as site_total,
                SUM(extra_cans) as extra_cans
            FROM payments
            GROUP BY pay_to
            ORDER BY pay_to
            """
        )
        return result.df()

    def get_by_payee(self, pay_to: str) -> tuple[str, pd.DataFrame]:
        if self._con is None:
            msg = "Repository not connected."
            raise RuntimeError(msg)
        result = self._con.execute(
            "SELECT * FROM payments WHERE pay_to = ? ORDER BY inspection_date, bu",
            [pay_to],
        )
        return (pay_to, result.df())

    def get_individual_totals(self, pay_to: str) -> pd.DataFrame:
        if self._con is None:
            msg = "Repository not connected."
            raise RuntimeError(msg)
        result = self._con.execute(
            """
            SELECT
                pay_to,
                SUM(tia_inspection) as tia_inspection,
                SUM(additional_canister_level) as additional_canister_level,
                SUM(hvf) as hvf,
                SUM(lighting_inspection_price) as lighting_inspection_price,
                SUM(migratory_bird) as migratory_bird,
                SUM(windsim) as windsim,
                SUM(tension) as tension,
                SUM(hr_pay) as hr_pay,
                SUM(site_total) as site_total,
                SUM(extra_cans) as extra_cans
            FROM payments
            WHERE pay_to = ?
            GROUP BY pay_to
            ORDER BY pay_to
            """,
            [pay_to],
        )
        return result.df()

    def close(self) -> None:
        if self._con is not None:
            self._con.close()
            self._con = None


def create_repository(db_path: Path) -> DuckDBPaymentRepository:
    if db_path.exists():
        db_path.unlink()
    repo = DuckDBPaymentRepository(db_path)
    repo.connect()
    return repo
