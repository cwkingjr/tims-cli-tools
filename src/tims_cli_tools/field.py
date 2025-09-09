ADD_CAN_PRICE = "Additional Canister Price"
ADD_CAN_LEVEL = "Additional Canister Level"
BASE_FOR_INV = "Base for Inv."
BU = "BU"
CREW = "Crew"
CREW_MEMBER = "Crew Member"
DATE = "Date"
DESCRIPTION = "DESCRIPTION"
ECS_CONCEALMENT_TYPE = "ECS Concealment Type"
EXTRA_CANS = "X_CANS"
HR_PAY = "HR.PAY"
HVF_WITH_SPACE = "HVF "
HVF_NO_SPACE = "HVF"
INVOICED = "Invoiced"
LIGHT_INSP = "Lighting Inspection Price"
MAINT = "MAINTENANCE"
MAN_LIFT = "Manlift Charge"
MIG_BIRD = "Migratory Bird"
QUANTITY = "QUANTITY"
SITE_TOTAL = "Site Total"
SORT_BY = "SORT_BY"
STRUCTURE = "Structure"
STRUCTURE_TYPE = "Structure Type"
SUB_CATEGORY = "SUB CATEGORY"
TENSION = "Tension Price"
TIA_INSP = "TIA Inspection"
TTP_INIT_READ = "TTP Initial Reading Price"
WINDSIM = "Windsim"

# Fields/columns used for processing
# This is the order seen in the input spreadsheet
REQUIRED_INPUT_COLS = [
    BU,
    STRUCTURE,
    BASE_FOR_INV,
    TIA_INSP,
    ADD_CAN_LEVEL,
    HVF_WITH_SPACE,
    LIGHT_INSP,
    MIG_BIRD,
    WINDSIM,
    TTP_INIT_READ,
    TENSION,
    HR_PAY,
    SITE_TOTAL,
    MAINT,
    MAN_LIFT,
]

CLEAN_REQUIRED_INPUT_COLS = [
    HVF_NO_SPACE if x == HVF_WITH_SPACE else x for x in REQUIRED_INPUT_COLS
]

OUTPUT_COLS = [
    SORT_BY,
    BU,
    SUB_CATEGORY,
    DESCRIPTION,
    QUANTITY,
    TIA_INSP,
    ADD_CAN_PRICE,
    HVF_NO_SPACE,
    LIGHT_INSP,
    MIG_BIRD,
    WINDSIM,
    TTP_INIT_READ,
    TENSION,
    HR_PAY,
    SITE_TOTAL,
    MAINT,
    MAN_LIFT,
    STRUCTURE,  # leave this column so user can see what we the extra cans source data
    EXTRA_CANS,  # leave this column so the user can see how many extra cans we derived
]

# Fields/columns used for processing
# This is the order seen in the input spreadsheet
PAYROLL_REQUIRED_INPUT_COLS = [
    BU,
    DATE,
    INVOICED,
    CREW,
    STRUCTURE,
    BASE_FOR_INV,
    TIA_INSP,
    ADD_CAN_LEVEL,
    HVF_WITH_SPACE,
    LIGHT_INSP,
    MIG_BIRD,
    WINDSIM,
    TTP_INIT_READ,
    TENSION,
    HR_PAY,
    SITE_TOTAL,
    MAINT,
    MAN_LIFT,
    ECS_CONCEALMENT_TYPE,
    STRUCTURE_TYPE,
]

PAYROLL_INDIVIDUAL_COLS = [
    BU,
    DATE,
    CREW,
    CREW_MEMBER,
    STRUCTURE_TYPE,
    TIA_INSP,
    ADD_CAN_LEVEL,
    HVF_NO_SPACE,
    LIGHT_INSP,
    HR_PAY,
    SITE_TOTAL,
    MAINT,
]

PAYROLL_VALID_CREW_LEAD_PAY_TYPES = ["LEAD_STD", "EQ_SPLIT", "LEAD_64_SPLIT"]
PAYROLL_VALID_CREW_SECOND_PAY_TYPES = [
    "EQ_SPLIT",
    "SECOND_64_SPLIT",
    "1T2",
    "2T2",
    "3T2",
]
