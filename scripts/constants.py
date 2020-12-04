# Columns with categorical data that we will change from string to number.
LONG_STRING_COLS = ['c5_ed_nat', 'c5_he_nat', 'c5_se_nat', 'c5_coi_nat', 'c5_ed_stt', 'c5_he_stt', 'c5_se_stt', 'c5_coi_stt', 'c5_ed_met', 'c5_he_met', 'c5_se_met', 'c5_coi_met']
# Key for these conversions of string to number.
REPLACE_DICT = {'Very Low': 0, 'Low': 1, 'Moderate': 2, 'High': 3, 'Very High': 4}

# Replace to shorten column headers and keep json small.
SEARCH_AND_REPLACE = {
    'geoid': 'GEOID',
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
