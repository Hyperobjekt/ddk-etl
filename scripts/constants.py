# BASE INPUT AND OUTPUT DIRS
SOURCE_DIR = './source'
OUTPUT_DIR = './proc'
# Source file for states data to go on state shapes.
STATES_SRC = 'StateFipsUsps'
STATES_PROC = 'states'
# Source file for metro data.
METROS_PROC = 'metros'
# Columns with categorical data that we will change from string to number.
LONG_STRING_COLS = ['c5_ed_nat', 'c5_he_nat', 'c5_se_nat', 'c5_coi_nat', 'c5_ed_stt', 'c5_he_stt', 'c5_se_stt', 'c5_coi_stt', 'c5_ed_met', 'c5_he_met', 'c5_se_met', 'c5_coi_met']
# Columns to include on tracts json to go into tilesset
# TRACT_GEOJSON_COLS = ['GEOID', 'in100', 'msaid15', 'countyfips', 'statefips', 'stateusps', 'pop', 'xc5en10', 'xc5hn10', 'xc5on10', 'xc5cn10', 'xc5es10', 'xc5hs10', 'xc5os10', 'xc5cs10', 'xc5em10', 'xc5hm10', 'xc5om10', 'xc5cm10', 'xc5en15', 'xc5hn15', 'xc5on15', 'xc5cn15', 'xc5es15', 'xc5hs15', 'xc5os15', 'xc5cs15', 'xc5em15', 'xc5hm15', 'xc5om15', 'xc5cm15']
# With shortened index prefix.
TRACT_GEOJSON_COLS = ['GEOID', 'in100', 'msaid15', 'countyfips', 'statefips', 'stateusps', 'pop', 'xen10', 'xhn10', 'xon10', 'xcn10', 'xes10', 'xhs10', 'xos10', 'xcs10', 'xem10', 'xhm10', 'xom10', 'xcm10', 'xen15', 'xhn15', 'xon15', 'xcn15', 'xes15', 'xhs15', 'xos15', 'xcs15', 'xem15', 'xhm15', 'xom15', 'xcm15']
# For json file for download
# TRACT_APP_COLS =
# ['GEOID', 'in100', 'msaid15', 'countyfips', 'statefips', 'stateusps', 'pop', 'xen10', 'xhn10', 'xon10', 'xcn10', 'xes10', 'xhs10', 'xos10', 'xcs10', 'xem10', 'xhm10', 'xom10', 'xcm10', 'xen15', 'xhn15', 'xon15', 'xcn15', 'xes15', 'xhs15', 'xos15', 'xcs15', 'xem15', 'xhm15', 'xom15', 'xcm15'
TRACT_APP_COLS = ["GEOID","in100","msaid15","countyfips","statefips","stateusps","pop10","xzen10","xzhn10","xzon10","xzcn10","xen10","xhn10","xon10","xcn10","xren10","xrhn10","xron10","xrcn10","xes10","xhs10","xos10","xcs10","xres10","xrhs10","xros10","xrcs10","xem10","xhm10","xom10","xcm10","xrem10","xrhm10","xrom10","xrcm10","pop15","xzen15","xzhn15","xzon15","xzcn15","xen15","xhn15","xon15","xcn15","xren15","xrhn15","xron15","xrcn15","xes15","xhs15","xos15","xcs15","xres15","xrhs15","xros15","xrcs15","xem15","xhm15","xom15","xcm15","xrem15","xrhm15","xrom15","xrcm15","ai10","ap10","b10","hi10","o210","nw10","w10","t10","ai15","ap15","b15","hi15","o215","nw15","w15","t15","reap10","reat10","reco10","reec10","rehs10","rema10","rere10","resc10","rete10","repe10","reph10","rhfo10","rhgr10","rhha10","rhhl10","rhoz10","rhpm10","rhva10","rhwa10","rhsu10","rhrs10","ropo10","ropu10","roho10","rooc10","romh10","roem10","rojo10","rosi10","reap15","reat15","reco15","reec15","rehs15","rema15","rere15","resc15","rete15","repe15","reph15","rhfo15","rhgr15","rhha15","rhhl15","rhoz15","rhpm15","rhva15","rhwa15","rhsu15","rhrs15","ropo15","ropu15","roho15","rooc15","romh15","roem15","rojo15","rosi15"]
# Columns for year-specific tract csv files.
TRACT_BY_YEAR_COLS = ["GEOID","in100","msaid15","statefips","pop","xzen","xzhn","xzon","xzcn","xen","xhn","xon","xcn","xren","xrhn","xron","xrcn","xes","xhs","xos","xcs","xres","xrhs","xros","xrcs","xem","xhm","xom","xcm","xrem","xrhm","xrom","xrcm","reap","reat","reco","reec","rehs","rema","rere","resc","rete","repe","reph","rhfo","rhgr","rhha","rhhl","rhoz","rhpm","rhva","rhwa","rhsu","rhrs","ropo","ropu","roho","rooc","romh","roem","rojo","rosi","ai", "ap", "b", "hi", "w"]
# Columns for population exports.
POP_COLS = ['GEOID', 'in100',	'msaid15', 'countyfips', 'statefips', 'pop', 'ai10', 'ap10', 'b10', 'hi10', 'o210', 'nw10', 'w10', 't10', 'ai15', 'ap15', 'b15', 'hi15', 'o215', 'nw15', 'w15', 't15']
YEAR_AGNOSTIC_POP_COLS = ['GEOID', 'in100',	'msaid15', 'countyfips', 'statefips', 'pop', 'ai', 'ap', 'b', 'hi', 'o2', 'nw', 'w', 't']
# Key for these conversions of string to number.
REPLACE_DICT = {'Very Low': 0, 'Low': 1, 'Moderate': 2, 'High': 3, 'Very High': 4}
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
    'heat': 'ha', # Extreme heat exposure
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
    # Shorten index prefix
    'x_c5': 'x',
    # Remove underscores
    '_': '',
}

# Point types for processing the point data.
POINT_TYPES = ['ai', 'ap', 'b', 'hi', 'w']
# Years types for data
YEARS = [10, 15]
# Zoom min and max for layers
MAX_ZOOM = 14
MIN_ZOOM = 3
