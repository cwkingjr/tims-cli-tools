from datetime import date, time

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


def insert_payment(
    *,
    connection,
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

    connection.execute(
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
