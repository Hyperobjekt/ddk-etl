# BASE INPUT AND OUTPUT DIRS
SOURCE_DIR = './source'
OUTPUT_DIR = './proc'
# Source file for states data to go on state shapes.
STATES_SRC = 'StateFipsUsps'
STATES_PROC = 'states'
# Columns with categorical data that we will change from string to number.
LONG_STRING_COLS = ['c5_ed_nat', 'c5_he_nat', 'c5_se_nat', 'c5_coi_nat', 'c5_ed_stt', 'c5_he_stt', 'c5_se_stt', 'c5_coi_stt', 'c5_ed_met', 'c5_he_met', 'c5_se_met', 'c5_coi_met']
# Columns to include on tracts json to go into tilesset
TRACT_GEOJSON_COLS = ['GEOID', 'in100', 'msaid15', 'countyfips', 'statefips', 'stateusps', 'pop_10', 'x_c5_e_n_10', 'x_c5_h_n_10', 'x_c5_o_n_10', 'x_c5_c_n_10', 'x_c5_e_s_10', 'x_c5_h_s_10', 'x_c5_o_s_10', 'x_c5_c_s_10', 'x_c5_e_m_10', 'x_c5_h_m_10', 'x_c5_o_m_10', 'x_c5_c_m_10', 'x_c5_e_n_15', 'x_c5_h_n_15', 'x_c5_o_n_15', 'x_c5_c_n_15', 'x_c5_e_s_15', 'x_c5_h_s_15', 'x_c5_o_s_15', 'x_c5_c_s_15', 'x_c5_e_m_15', 'x_c5_h_m_15', 'x_c5_o_m_15', 'x_c5_c_m_15']
# Key for these conversions of string to number.
REPLACE_DICT = {'Very Low': 0, 'Low': 1, 'Moderate': 2, 'High': 3, 'Very High': 4}
# Source file for metro data.
METROS_PROC = 'helpers/metros'
# Replace to shorten column headers and keep json small.
SEARCH_AND_REPLACE = {
    'geoid': 'GEOID',
    # Demographic
    'aian': 'ai', # American Indian or Native Alaskan, add to dot density
    'black': 'b',
    'api': 'ap', # Asian/Pacific Islander, add to dot density
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
    'se': 'o',
    'coi': 'c',
    # Geographic
    'nat': 'n',
    'stt': 's',
    'met': 'm',
}
