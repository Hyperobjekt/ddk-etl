# Columns with categorical data that we will change from string to number.
LONG_STRING_COLS = ['c5_ed_nat', 'c5_he_nat', 'c5_se_nat', 'c5_coi_nat', 'c5_ed_stt', 'c5_he_stt', 'c5_se_stt', 'c5_coi_stt', 'c5_ed_met', 'c5_he_met', 'c5_se_met', 'c5_coi_met']
# Key for these conversions of string to number.
REPLACE_DICT = {'Very Low': 0, 'Low': 1, 'Moderate': 2, 'High': 3, 'Very High': 4}

REPLACE_RAW_DICT = {
    'ed_prxece': 'r_ed_prxece',
    'ed_prxhqece': 'r_ed_prxhqece',
    'ed_ecenrol': 'r_ed_ecenrol',
    'ed_reading': 'r_ed_reading',
    'ed_math': 'r_ed_math',
    'ed_hsgrad': 'r_ed_hsgrad',
    'ed_apenr': 'r_ed_apenr',
    'ed_college': 'r_ed_college',
    'ed_schpov': 'r_ed_schpov',
    'ed_teachxp':'r_ed_teachxp',
    'ed_attain': 'r_ed_attain',
    'he_food':'r_he_food',
    'he_green': 'r_he_green',
    'he_walk': 'r_he_walk',
    'he_vacancy': 'r_he_vacancy',
    'he_suprfnd': 'r_he_suprfnd',
    'he_rsei': 'r_he_rsei',
    'he_pm25': 'r_he_pm25',
    'he_ozone': 'r_he_ozone',
    'he_heat': 'r_he_heat',
    'he_hlthins': 'r_he_hlthins',
    'se_emprat': 'r_se_emprat',
    'se_jobprox': 'r_se_jobprox',
    'se_povrate': 'r_se_povrate',
    'se_public': 'r_se_public',
    'se_home': 'r_se_home',
    'se_occ': 'r_se_occ',
    'se_mhe': 'r_se_mhe',
    'se_single': 'r_se_single'
}

# Replace to shorten column headers and keep json small.
SEARCH_AND_REPLACE = {
    # Demographic
    'aian': 'as', # Asian
    'black': 'b', 
    'api': 'ap', # Asian/Pacific Islander
    'hisp': 'hi',
    'other2': 'o2',
    'nonwhite': 'nw',
    'white': 'w',
    'total': 't',
    # zscores and raw
    'prxece': 'pe', # Early childhood education centers
    'prxhqece': 'ph', # High-quality early childhood education centers
    'ecenrol': 'ec', # Early childhood education enrollment
    'reading': 're', # Third grade reading proficiency
    'math': 'ma', # Third grade math proficiency
    'hsgrad': 'hs', # High school graduation rate
    'apenr': 'ap', # Advanced Placement course enrollment
    'college': 'co', # College enrollment in nearby institutions 
    'schpov': 'sc', # School poverty
    'teachxp': 'te', # Teacher experience
    'attain': 'at', # Adult educational attainment
    'food': 'fo', # Access to healthy food
    'green': 'gr', # Access to green space
    'walk': 'wa', # Walkability
    'vacancy': 'va', # Housing vacancy rate
    'suprfnd': 'su', # Hazardous waste dump sites
    'rsei': 'rs', # Industrial pollutants in air, water or soil
    'pm25': 'pm', # Airborne microparticles
    'ozone': 'oz', # Ozone concentration
    'heat': 'he', # Extreme heat exposure
    'hlthins': 'hl', # Health insurance coverage
    'emprat': 'em', # Employment rate
    'jobprox': 'jo', # Commute duration
    'povrate': 'po', # Poverty rate
    'public': 'pu', # Public assistance rate
    'ecres': 'er', # Economic resource index
    'home': 'ho', # Homeownership rate
    'occ': 'oc', # High-skill employment
    'mhe': 'mh', # Median household income
    'single': 'si', # Single-headed households
    # Basic replacements for "domains"
    'ed': 'e',
    'he': 'h',
    'se': 's',
    'coi': 'c',
    # Geographic
    'nat': 'n',
    'stt': 's',
    'met': 'm',
}
