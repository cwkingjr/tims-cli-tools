BU = "BU"
DESCRIPTION = "DESCRIPTION"
SUB_CATEGORY = "SUB CATEGORY"
QUANTITY = "QUANTITY"
SORT_BY = "SORT_BY"
TIA_INSP = "TIA Inspection"
ADD_CAN = "Additional Canister Price"
HVF = "HVF"  # Note: no trailing space
LIGHT_INSP = "Lighting Inspection Price"
MIG_BIRD = "Migratory Bird"
WINDSIM = "Windsim"
TTP_INIT_READ = "TTP Initial Reading Price"
TENSION = "Tension Price"
HR_PAY = "HR.PAY"
SITE_TOTAL = "Site Total"
MAINT = "MAINTENANCE"
MAN_LIFT = "Manlift Charge"
STRUCTURE = "Structure"
EXTRA_CANS = "EXTRA_CANS"

# Fields/columns used for processing
REQUIRED_FIELDS = [
    "BU",
    "Base for Inv.",
    "Structure",
    "TIA Inspection",
    "Additional Canister Level",
    "HVF ",  # note the trailing space in the column name
    "Lighting Inspection Price",
    "Migratory Bird",
    "Windsim",
    "TTP Initial Reading Price",
    "Tension Price",
    "HR.PAY",
    "Site Total",
    "MAINTENANCE",
    "Manlift Charge",
]

OUTPUT_COLUMNS = [
    "SORT_BY",
    "BU",
    "SUB CATEGORY",
    "DESCRIPTION",
    "QUANTITY",
    "TIA Inspection",
    "Additional Canister Price",
    "HVF",  # Note: no trailing space
    "Lighting Inspection Price",
    "Migratory Bird",
    "Windsim",
    "TTP Initial Reading Price",
    "Tension Price",
    "HR.PAY",
    "Site Total",
    "MAINTENANCE",
    "Manlift Charge",
    "Structure",  # leave this column so user can see what we the extra cans source data
    "EXTRA_CANS",  # leave this column so the user can see how many extra cans we derived
]
