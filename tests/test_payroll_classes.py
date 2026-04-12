import pytest

from tims_cli_tools.payroll_classes import (
    PayType,
    PayTypes,
    CrewLead,
    CrewSecond,
    Crew,
    Crews,
    build_pay_types,
    build_crew_leads,
    build_crew_seconds,
    build_crews,
    build_additional_pay,
)


class TestPayType:
    def test_get_pay_by_str_guyed(self):
        pay_type = PayType(
            name="Test", code="T", guyed=5.0, ss=3.0, mp=4.0, mp_cans=7.0
        )
        assert pay_type.get_pay_by_str("guyed") == 5.0

    def test_get_pay_by_str_ss(self):
        pay_type = PayType(
            name="Test", code="T", guyed=5.0, ss=3.0, mp=4.0, mp_cans=7.0
        )
        assert pay_type.get_pay_by_str("ss") == 3.0

    def test_get_pay_by_str_mp(self):
        pay_type = PayType(
            name="Test", code="T", guyed=5.0, ss=3.0, mp=4.0, mp_cans=7.0
        )
        assert pay_type.get_pay_by_str("mp") == 4.0

    def test_get_pay_by_str_mp_cans(self):
        pay_type = PayType(
            name="Test", code="T", guyed=5.0, ss=3.0, mp=4.0, mp_cans=7.0
        )
        assert pay_type.get_pay_by_str("mp_cans") == 7.0

    def test_get_pay_by_str_raises_for_unknown(self):
        pay_type = PayType(
            name="Test", code="T", guyed=5.0, ss=3.0, mp=4.0, mp_cans=7.0
        )
        with pytest.raises(ValueError, match="Unknown PayType"):
            pay_type.get_pay_by_str("unknown")


class TestPayTypes:
    def test_get_pay_type_from_key(self):
        pay_type = PayType(
            name="Lead", code="LEAD", guyed=5.0, ss=3.0, mp=4.0, mp_cans=7.0
        )
        pay_types = PayTypes(types=[pay_type])
        result = pay_types.get_pay_type_from_key(key="LEAD")
        assert result.code == "LEAD"

    def test_get_pay_type_from_key_raises_for_missing(self):
        pay_type = PayType(
            name="Lead", code="LEAD", guyed=5.0, ss=3.0, mp=4.0, mp_cans=7.0
        )
        pay_types = PayTypes(types=[pay_type])
        with pytest.raises(ValueError, match="Couldn't find pay type"):
            pay_types.get_pay_type_from_key(key="MISSING")


class TestCrews:
    def test_get_crew_by_lead_spreadsheet_name(self):
        lead = CrewLead(
            name="John Doe",
            spreadsheet_name="John",
            pay_type=PayType(
                name="Lead", code="L", guyed=5.0, ss=3.0, mp=4.0, mp_cans=7.0
            ),
        )
        second = CrewSecond(
            name="Jane Doe",
            crew_lead_name="John Doe",
            pay_type=PayType(
                name="Second", code="S", guyed=3.0, ss=2.0, mp=3.0, mp_cans=6.0
            ),
        )
        crew = Crew(lead=lead, second=second)
        crews = Crews(crews=[crew])

        result = crews.get_crew_by_lead_spreadsheet_name(spreadsheet_name="John")
        assert result.lead.name == "John Doe"

    def test_get_crew_by_lead_spreadsheet_name_raises_for_missing(self):
        crew = Crew(
            lead=CrewLead(
                name="John",
                spreadsheet_name="John",
                pay_type=PayType(
                    name="Lead", code="L", guyed=5.0, ss=3.0, mp=4.0, mp_cans=7.0
                ),
            ),
            second=CrewSecond(
                name="Jane",
                crew_lead_name="John",
                pay_type=PayType(
                    name="Second", code="S", guyed=3.0, ss=2.0, mp=3.0, mp_cans=6.0
                ),
            ),
        )
        crews = Crews(crews=[crew])

        with pytest.raises(ValueError, match="Could not find crew"):
            crews.get_crew_by_lead_spreadsheet_name(spreadsheet_name="Unknown")


class TestBuildPayTypes:
    def test_build_pay_types(self):
        config = [
            {
                "name": "Lead TIA",
                "pay_type_key": "LEAD",
                "guyed": 5.0,
                "ss": 3.0,
                "mp": 4.0,
                "mp_cans": 7.0,
            }
        ]
        result = build_pay_types(config_pay_types=config)
        assert len(result.types) == 1
        assert result.types[0].code == "LEAD"


class TestBuildCrewLeads:
    def test_build_crew_leads(self):
        pay_types = PayTypes(
            types=[
                PayType(
                    name="Lead TIA",
                    code="LEAD",
                    guyed=5.0,
                    ss=3.0,
                    mp=4.0,
                    mp_cans=7.0,
                )
            ]
        )
        config = [
            {
                "name": "John Doe",
                "spreadsheet_name": "John",
                "pay_type_key": "LEAD",
            }
        ]
        result = build_crew_leads(config_crew_leads=config, pay_types=pay_types)
        assert len(result) == 1
        assert result[0].name == "John Doe"


class TestBuildCrewSeconds:
    def test_build_crew_seconds(self):
        pay_types = PayTypes(
            types=[
                PayType(
                    name="Second TIA",
                    code="2ND",
                    guyed=3.0,
                    ss=2.0,
                    mp=3.0,
                    mp_cans=6.0,
                )
            ]
        )
        config = [
            {
                "name": "Jane Doe",
                "pay_type_key": "2ND",
                "crew_lead_name": "John Doe",
            }
        ]
        result = build_crew_seconds(config_crew_seconds=config, pay_types=pay_types)
        assert len(result) == 1
        assert result[0].name == "Jane Doe"


class TestBuildCrews:
    def test_build_crews(self):
        config_pay_types = [
            {
                "name": "Lead TIA",
                "pay_type_key": "LEAD",
                "guyed": 5.0,
                "ss": 3.0,
                "mp": 4.0,
                "mp_cans": 7.0,
            },
            {
                "name": "Second TIA",
                "pay_type_key": "2ND",
                "guyed": 3.0,
                "ss": 2.0,
                "mp": 3.0,
                "mp_cans": 6.0,
            },
        ]
        config_crew_leads = [
            {"name": "John Doe", "spreadsheet_name": "John", "pay_type_key": "LEAD"}
        ]
        config_crew_seconds = [
            {
                "name": "Jane Doe",
                "pay_type_key": "2ND",
                "crew_lead_name": "John Doe",
            }
        ]

        result = build_crews(
            config_crew_leads=config_crew_leads,
            config_crew_seconds=config_crew_seconds,
            config_pay_types=config_pay_types,
        )

        assert len(result.crews) == 1
        assert result.crews[0].lead.name == "John Doe"
        assert result.crews[0].second.name == "Jane Doe"

    def test_build_crews_raises_when_lead_not_found(self):
        config_pay_types = [
            {
                "name": "Second TIA",
                "pay_type_key": "2ND",
                "guyed": 3.0,
                "ss": 2.0,
                "mp": 3.0,
                "mp_cans": 6.0,
            },
        ]
        config_crew_leads = []
        config_crew_seconds = [
            {
                "name": "Jane Doe",
                "pay_type_key": "2ND",
                "crew_lead_name": "Unknown Lead",
            }
        ]

        with pytest.raises(ValueError, match="Couldn't find crew lead"):
            build_crews(
                config_crew_leads=config_crew_leads,
                config_crew_seconds=config_crew_seconds,
                config_pay_types=config_pay_types,
            )


class TestAdditionalPay:
    def test_build_additional_pay(self):
        config = {
            "extra_cans_each": 1.0,
            "hr_pay_per_hour": 60.0,
            "hvf": 10.0,
            "lighting_inspection": 5.0,
            "migratory_bird": 2.5,
            "tension_1000": 15.0,
            "tension_700": 10.0,
            "tension_850": 12.0,
            "ttp_initial_reading": 3.0,
            "windsim": 4.0,
        }

        result = build_additional_pay(config_add_pay=config)

        assert result.extra_cans_each == 1.0
        assert result.hvf == 10.0
        assert result.tension_700 == 10.0
