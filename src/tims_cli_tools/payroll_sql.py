from datetime import date, time
import pandas as pd
from duckdb import DuckDBPyConnection

CREATE_PAYMENTS_TABLE_SEQUENCE = """
    CREATE SEQUENCE sequence_payments START 1;
"""

CREATE_PAYMENTS_TABLE_SQL = """
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


def insert_payment(  # noqa: PLR0913
    *,
    con: DuckDBPyConnection,
    bu: int,
    inspection_date: date,
    crew_lead: str,
    pay_to: str,
    structure_type: str,
    tia_inspection: float = 0.0,
    additional_canister_level: float = 0.0,
    hvf: float = 0.0,
    lighting_inspection_price: float = 0.0,
    migratory_bird: float = 0.0,
    windsim: float = 0.0,
    tension: float = 0.0,
    hr_pay: float = 0.0,
    site_total: float = 0.0,
    maintenance: time = time(hour=0, minute=0),
    extra_cans: int = 0,
):
    """Insert row into payments table."""
    insert_values = [
        bu,
        inspection_date,
        crew_lead,
        pay_to,
        structure_type,
        tia_inspection,
        additional_canister_level,
        hvf,
        lighting_inspection_price,
        migratory_bird,
        windsim,
        tension,
        hr_pay,
        site_total,
        maintenance,
        extra_cans,
    ]

    con.execute(
        """
        insert into payments (
        bu,
        inspection_date,
        crew_lead,
        pay_to,
        structure_type,
        tia_inspection,
        additional_canister_level,
        hvf,
        lighting_inspection_price,
        migratory_bird,
        windsim,
        tension,
        hr_pay,
        site_total,
        maintenance,
        extra_cans)
        values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        insert_values,
    )


def get_payments_by_pay_to(
    *, con: DuckDBPyConnection, pay_to: str
) -> tuple[str, pd.DataFrame]:
    """Grab rows from the payments table based upon the crew member's name in the pay_to field."""
    result = con.execute(
        "select * from payments where pay_to = ? order by inspection_date,bu", [pay_to]
    )
    return (pay_to, result.df())


def get_all_payments(*, con: DuckDBPyConnection) -> pd.DataFrame:
    """Grab all rows from the payments table."""
    result = con.execute("select * from payments order by inspection_date,bu")
    return result.df()


def get_all_payments_totals(*, con: DuckDBPyConnection) -> pd.DataFrame:
    """Grab totals for all pay_to names from the payments table."""
    result = con.execute(
        """
        select
        pay_to,
        sum(tia_inspection) as tia_inspection,
        sum(additional_canister_level) as additional_canister_level,
        sum(hvf) as hvf,
        sum(lighting_inspection_price) as lighting_inspection_price,
        sum(migratory_bird) as migratory_bird,
        sum(windsim) as windsim,
        sum(tension) as tension,
        sum(hr_pay) as hr_pay,
        sum(site_total) as site_total,
        sum(extra_cans) as extra_cans
        from payments group by pay_to order by pay_to;
        """
    )
    return result.df()


def get_individual_payments_totals(
    *, con: DuckDBPyConnection, pay_to: str
) -> pd.DataFrame:
    """Grab totals for individual pay_to name from the payments table."""
    result = con.execute(
        """
        select
        pay_to,
        sum(tia_inspection) as tia_inspection,
        sum(additional_canister_level) as additional_canister_level,
        sum(hvf) as hvf,
        sum(lighting_inspection_price) as lighting_inspection_price,
        sum(migratory_bird) as migratory_bird,
        sum(windsim) as windsim,
        sum(tension) as tension,
        sum(hr_pay) as hr_pay,
        sum(site_total) as site_total,
        sum(extra_cans) as extra_cans
        from payments where pay_to = ? group by pay_to order by pay_to
        """,
        [pay_to],
    )
    return result.df()
