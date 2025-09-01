from pydantic import BaseModel


class PayType(BaseModel):
    """Model representing a pay type with pay rates."""

    name: str
    code: str
    guyed: float
    ss: float
    mp: float
    mp_cans: float

    def get_pay_by_str(self, text) -> float:
        my_text = text.lower()
        match my_text:
            case "guyed":
                return self.guyed
            case "ss":
                return self.ss
            case "mp":
                return self.mp
            case "mp_cans":
                return self.mp_cans
            case _:
                msg = f"Unknown PayType element of {text}."
                raise ValueError(msg)


class PayTypes(BaseModel):
    """List of PayType"""

    types: list[PayType]

    def get_pay_type_from_key(self, *, key):
        for one_pay_type in self.types:
            if one_pay_type.code == key:
                return one_pay_type
        msg = f"Couldn't find pay type of {key}."
        raise ValueError(msg)


class CrewLead(BaseModel):
    """Inspection Crew Lead."""

    name: str
    spreadsheet_name: str
    pay_type: PayType


class CrewSecond(BaseModel):
    """Inspection Crew Second."""

    name: str
    crew_lead_name: str
    pay_type: PayType


class Crew(BaseModel):
    """Team of two folks, one lead and one second."""

    lead: CrewLead
    second: CrewSecond


class Crews(BaseModel):
    crews: list[Crew]

    def get_crew_by_lead_spreadsheet_name(self, *, spreadsheet_name) -> Crew:
        """Convenience method for grabbing the crew lead.

        Input spreadsheet uses mixed names (short/long) for crew leads, so we capture
        the spreadsheet value, whether sort or long, as spreadsheet_name for crew leads.
        This method is here to allow us to quickly find the crew lead for a certain
        spreadsheet row so we can calculate payroll for that lead and that crew's second.
        """
        for crew in self.crews:
            if crew.lead.spreadsheet_name == spreadsheet_name:
                return crew
        msg = f"Could not find crew with lead spreadsheet_name of {spreadsheet_name}."
        raise ValueError(msg)


def build_pay_types(*, config_pay_types) -> PayTypes:
    """Builds a PayTypes list based upon config file data."""
    # example config input:
    #  pay_types=[
    #   {'name': 'Lead TIA Inspection Pay', 'pay_type_key': 'LEAD_STD', 'guyed': 5.0, 'ss': 3.0, 'mp': 4.0, 'mp_cans': 7.0},
    #   {'name': '1st Tier Second TIA Inspection Pay', 'pay_type_key': '1T2', 'guyed': 3.0, 'ss': 2.0, 'mp': 3.0, 'mp_cans': 6.0},
    #  ]

    pay_type_list = [
        PayType(
            name=x["name"],
            code=x["pay_type_key"],
            guyed=x["guyed"],
            ss=x["ss"],
            mp=x["mp"],
            mp_cans=x["mp_cans"],
        )
        for x in config_pay_types
    ]

    return PayTypes(types=pay_type_list)


def build_crew_leads(*, config_crew_leads, pay_types: PayTypes) -> list[CrewLead]:
    """Builds a Crew lead list based upon config file data."""
    # example config input:
    # crew_leads=[
    #  {'name': 'John Doe', 'spreadsheet_name': 'John', 'pay_type_key': 'LEAD_STD'},
    #  {'name': 'Jane Doe', 'spreadsheet_name': 'Jane Doe', 'pay_type_key': 'LEAD_STD'},
    # ]

    crew_lead_list = [
        CrewLead(
            name=x["name"],
            spreadsheet_name=x["spreadsheet_name"],
            pay_type=pay_types.get_pay_type_from_key(key=x["pay_type_key"]),
        )
        for x in config_crew_leads
    ]
    return crew_lead_list


def build_crew_seconds(*, config_crew_seconds, pay_types: PayTypes) -> list[CrewSecond]:
    """Builds a Crew second list based upon config file data."""
    # example config input:
    # crew_seconds=[
    #  {'name': 'Jessie James', 'pay_type_key': '3T2','crew_lead_name': 'Wild Bill'},
    #  {'name': 'Buffalo Bill', 'pay_type_key': '1T2', 'crew_lead_name': 'Joe Dirt'},
    # ]

    crew_second_list = [
        CrewSecond(
            name=x["name"],
            crew_lead_name=x["crew_lead_name"],
            pay_type=pay_types.get_pay_type_from_key(key=x["pay_type_key"]),
        )
        for x in config_crew_seconds
    ]
    return crew_second_list


def build_crews(*, config_crew_leads, config_crew_seconds, config_pay_types) -> Crews:
    """Build crews from config info."""
    my_pay_types = build_pay_types(config_pay_types=config_pay_types)

    my_crew_leads = build_crew_leads(
        config_crew_leads=config_crew_leads, pay_types=my_pay_types
    )

    my_crew_seconds = build_crew_seconds(
        config_crew_seconds=config_crew_seconds, pay_types=my_pay_types
    )

    def get_lead_from_name(name) -> CrewLead:
        """Convenience fn for use in list comprehension."""
        for one_lead in my_crew_leads:
            if one_lead.name == name:
                return one_lead
        msg = f"Couldn't find crew lead with name of {one_lead}."
        raise ValueError(msg)

    crew_list = [
        Crew(second=x, lead=get_lead_from_name(x.crew_lead_name))
        for x in my_crew_seconds
    ]

    return Crews(crews=crew_list)


class AdditionalPay(BaseModel):
    """Additional Pay Rates.

    These apply equally across crew members, regardless of PayType.
    """

    extra_cans_each: float
    hr_pay_per_hour: float
    hvf: float
    lighting_inspection: float
    migratory_bird: float
    tension_1000: float
    tension_700: float
    tension_850: float
    ttp_initial_reading: float
    windsim: float


def build_additional_pay(config_add_pay) -> AdditionalPay:
    """Build AditionalPay from config info."""
    return AdditionalPay(**config_add_pay)
