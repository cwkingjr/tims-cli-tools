import pytest

from tims_cli_tools.payroll_toml_validations import (
    get_create_crew_spreadsheets,
    get_process_logging,
    verify_crew_lead_pay_types_are_valid,
    verify_crew_second_pay_types_are_valid,
    verify_crew_leads_listed_in_seconds_exist,
    verify_same_number_of_leads_and_seconds,
    verify_no_duplicate_second_names,
    verify_no_duplicate_lead_names,
    verify_no_duplicate_second_crew_lead_names,
)


class TestGetCreateCrewSpreadsheets:
    def test_returns_true_for_Y(self):
        result = get_create_crew_spreadsheets(create_crew_spreadsheets="Y")
        assert result is True

    def test_returns_false_for_N(self):
        result = get_create_crew_spreadsheets(create_crew_spreadsheets="N")
        assert result is False

    def test_returns_false_for_other_value(self):
        result = get_create_crew_spreadsheets(create_crew_spreadsheets="other")
        assert result is False


class TestGetProcessLogging:
    def test_returns_true_for_Y(self):
        result = get_process_logging(process_logging="Y")
        assert result is True

    def test_returns_false_for_N(self):
        result = get_process_logging(process_logging="N")
        assert result is False


class TestVerifyCrewLeadPayTypesAreValid:
    def test_passes_with_valid_pay_type(self):
        crew_leads = [
            {"name": "John Doe", "pay_type_key": "LEAD_STD"},
        ]
        verify_crew_lead_pay_types_are_valid(crew_leads=crew_leads)

    def test_raises_with_invalid_pay_type(self):
        crew_leads = [
            {"name": "John Doe", "pay_type_key": "INVALID"},
        ]
        with pytest.raises(ValueError, match="invalid pay_key_type"):
            verify_crew_lead_pay_types_are_valid(crew_leads=crew_leads)


class TestVerifyCrewSecondPayTypesAreValid:
    def test_passes_with_valid_pay_type(self):
        crew_seconds = [
            {"name": "Jane Doe", "pay_type_key": "1T2"},
        ]
        verify_crew_second_pay_types_are_valid(crew_seconds=crew_seconds)

    def test_raises_with_invalid_pay_type(self):
        crew_seconds = [
            {"name": "Jane Doe", "pay_type_key": "INVALID"},
        ]
        with pytest.raises(ValueError, match="invalid pay_key_type"):
            verify_crew_second_pay_types_are_valid(crew_seconds=crew_seconds)


class TestVerifyCrewLeadsListedInSecondsExist:
    def test_passes_when_all_seconds_reference_valid_leads(self):
        crew_leads = [{"name": "John Doe"}]
        crew_seconds = [{"name": "Jane Doe", "crew_lead_name": "John Doe"}]
        verify_crew_leads_listed_in_seconds_exist(
            crew_seconds=crew_seconds, crew_leads=crew_leads
        )

    def test_raises_when_second_references_nonexistent_lead(self):
        crew_leads = [{"name": "John Doe"}]
        crew_seconds = [{"name": "Jane Doe", "crew_lead_name": "Unknown"}]
        with pytest.raises(ValueError, match="non-existent crew lead"):
            verify_crew_leads_listed_in_seconds_exist(
                crew_seconds=crew_seconds, crew_leads=crew_leads
            )


class TestVerifySameNumberOfLeadsAndSeconds:
    def test_passes_when_counts_match(self):
        crew_leads = [{"name": "John Doe"}]
        crew_seconds = [{"name": "Jane Doe"}]
        verify_same_number_of_leads_and_seconds(
            crew_seconds=crew_seconds, crew_leads=crew_leads
        )

    def test_raises_when_counts_differ(self):
        crew_leads = [{"name": "John Doe"}, {"name": "Jane Doe"}]
        crew_seconds = [{"name": "Worker 1"}]
        with pytest.raises(ValueError, match="mismatching number"):
            verify_same_number_of_leads_and_seconds(
                crew_seconds=crew_seconds, crew_leads=crew_leads
            )


class TestVerifyNoDuplicateSecondNames:
    def test_passes_when_no_duplicates(self):
        crew_seconds = [
            {"name": "Worker A"},
            {"name": "Worker B"},
        ]
        verify_no_duplicate_second_names(crew_seconds=crew_seconds)

    def test_raises_when_duplicates_exist(self):
        crew_seconds = [
            {"name": "Worker A"},
            {"name": "Worker A"},
        ]
        with pytest.raises(ValueError, match="duplicated second names"):
            verify_no_duplicate_second_names(crew_seconds=crew_seconds)


class TestVerifyNoDuplicateLeadNames:
    def test_passes_when_no_duplicates(self):
        crew_leads = [
            {"name": "Lead A"},
            {"name": "Lead B"},
        ]
        verify_no_duplicate_lead_names(crew_leads=crew_leads)

    def test_raises_when_duplicates_exist(self):
        crew_leads = [
            {"name": "Lead A"},
            {"name": "Lead A"},
        ]
        with pytest.raises(ValueError, match="duplicated lead names"):
            verify_no_duplicate_lead_names(crew_leads=crew_leads)


class TestVerifyNoDuplicateSecondCrewLeadNames:
    def test_passes_when_no_duplicates(self):
        crew_seconds = [
            {"name": "Second A", "crew_lead_name": "Lead A"},
            {"name": "Second B", "crew_lead_name": "Lead B"},
        ]
        verify_no_duplicate_second_crew_lead_names(crew_seconds=crew_seconds)

    def test_raises_when_duplicates_exist(self):
        crew_seconds = [
            {"name": "Second A", "crew_lead_name": "Lead A"},
            {"name": "Second B", "crew_lead_name": "Lead A"},
        ]
        with pytest.raises(ValueError, match="duplicated second crew lead names"):
            verify_no_duplicate_second_crew_lead_names(crew_seconds=crew_seconds)
