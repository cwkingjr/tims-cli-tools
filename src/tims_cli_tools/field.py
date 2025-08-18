ADD_CAN_PRICE = "Additional Canister Price"
ADD_CAN_LEVEL = "Additional Canister Level"
BASE_FOR_INV = "Base for Inv."
BU = "BU"
DESCRIPTION = "DESCRIPTION"
EXTRA_CANS = "EXTRA_CANS"
HR_PAY = "HR.PAY"
HVF_WITH_SPACE = "HVF "
HVF_NO_SPACE = "HVF"
LIGHT_INSP = "Lighting Inspection Price"
MAINT = "MAINTENANCE"
MAN_LIFT = "Manlift Charge"
MIG_BIRD = "Migratory Bird"
QUANTITY = "QUANTITY"
SITE_TOTAL = "Site Total"
SORT_BY = "SORT_BY"
STRUCTURE = "Structure"
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
