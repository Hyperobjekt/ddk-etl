import os
import sys
import pandas as pd

print("Building dictionary...")

shapetypes = sys.argv[1].split(',') # Shape types to process: `tracts`, `counties`, `states`, or `zips`.
print("shapetype array = ", shapetypes)

SOURCE_DIR = './source/'
OUTPUT_DIR = './proc/'

# Get list of files.
csvs_arr = ['index', 'pop', 'raw', 'zscores'] # shapetypes # os.listdir(SOURCE_DIR)
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

# If not output path, create one.
if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)
if not os.path.exists(f'{OUTPUT_DIR}/helpers'):
    os.mkdir(f'{OUTPUT_DIR}/helpers')

dictionary = pd.DataFrame()

# For each file in the array...
for shape in shapetypes:
    for csv in csvs_arr:
        print(f'Processing {csv}_dict.csv.')
        # plot.savefig(f'hanning{num}.pdf')
        path = f'{SOURCE_DIR}/{shape}/{csv}_dict.csv'
        # print('Path is ' + path)
        # Make sure the file exists.
        if os.path.exists(path):
            # Get csv contents as dataframe.
            source = pd.read_csv(path)
            # print(source.head())
            if (csv == 'pop'):
                # Remove the first several lines.
                source = source.drop(columns=['Add to dot density layer'])
                source = source.drop([0,1,2,3,4,5,6,7,8,9])
            else:
                if (csv == 'index'):
                    source.rename(columns={'Choropleth map': 'ch'}, inplace=True)
                    source = source[['column', 'type', 'label', 'description', 'ch']]
                    # print(source.head())
                else:
                    if (csv == 'zscores'):
                        source['column'] = source['column'].str.replace('z', 'z_')
                        print('Prefixed zscores column column.')
                        print(source.head())
                    # raw, prefix with "r_"
                    if (csv == 'raw'):
                        source['column'] = 'r_' + source['column'].astype(str)
                        # source['column'] = source['column'].add_prefix('r_')
                        # source = source.rename(columns=REPLACE_RAW_DICT)
                        print('Prefixed raw column column.')
                        print(source.head())
                    source = source[['column', 'type', 'label', 'description']]
                source = source.drop([0,1,2,3,4,5,6,7,8,9,10])
                # print(source.head())
                source['column'] = source['column'].str.lower()
                # print(source.head())
            dictionary = pd.concat([dictionary, source])
            # print(dictionary.head())

        else:
            print(f'File at {path} doesn\'t seem to exist!')

# Process dictionary
# Replace to shorten column headers and keep json small.
# ed : e / education
# he: h / health
# se: s / socioeconomic
# coi: c / Child Opportunity Index
# nat: n / national 
# stt: s / state
# met: m / metro
# aian: as / asian
# black: b
# api: ap / asian pacific islander
# hisp: hi / hispanic
# other2: o2
# nonwhite: nw
# white: w
# total: t (population)
# Replace methods
# Indicator cats
# TODO: Abstract and optimize.
dictionary['column'] = dictionary['column'].str.replace('ed', 'e')
dictionary['column'] = dictionary['column'].str.replace('he', 'h')
dictionary['column'] = dictionary['column'].str.replace('se', 's')
dictionary['column'] = dictionary['column'].str.replace('coi', 'c')
# Geo
dictionary['column'] = dictionary['column'].str.replace('nat', 'n')
dictionary['column'] = dictionary['column'].str.replace('stt', 's')
dictionary['column'] = dictionary['column'].str.replace('met', 'm')
# Demo
dictionary['column'] = dictionary['column'].str.replace('aian', 'as')
dictionary['column'] = dictionary['column'].str.replace('black', 'b')
dictionary['column'] = dictionary['column'].str.replace('api', 'ap')
dictionary['column'] = dictionary['column'].str.replace('hisp', 'hi')
dictionary['column'] = dictionary['column'].str.replace('other2', 'o2')
dictionary['column'] = dictionary['column'].str.replace('nonwhite', 'nw')
dictionary['column'] = dictionary['column'].str.replace('white', 'w')
dictionary['column'] = dictionary['column'].str.replace('total', 't')
# zscores and raw
dictionary['column'] = dictionary['column'].str.replace('prxece', 'prxe')
dictionary['column'] = dictionary['column'].str.replace('prxhqece', 'prxh')
dictionary['column'] = dictionary['column'].str.replace('ecenrol', 'ecen')
dictionary['column'] = dictionary['column'].str.replace('reading', 'read')
dictionary['column'] = dictionary['column'].str.replace('hsgrad', 'hsgr')
dictionary['column'] = dictionary['column'].str.replace('apenr', 'apen')
dictionary['column'] = dictionary['column'].str.replace('college', 'coll')
dictionary['column'] = dictionary['column'].str.replace('schpov', 'schp')
dictionary['column'] = dictionary['column'].str.replace('teachxp', 'teac')
dictionary['column'] = dictionary['column'].str.replace('attain', 'atta')
dictionary['column'] = dictionary['column'].str.replace('green', 'gree')
dictionary['column'] = dictionary['column'].str.replace('vacancy', 'vaca')
dictionary['column'] = dictionary['column'].str.replace('suprfnd', 'supr')
dictionary['column'] = dictionary['column'].str.replace('ozone', 'ozon')
dictionary['column'] = dictionary['column'].str.replace('hlthins', 'hlth')
dictionary['column'] = dictionary['column'].str.replace('emprat', 'empr')
dictionary['column'] = dictionary['column'].str.replace('jobprox', 'jobp')
dictionary['column'] = dictionary['column'].str.replace('povrate', 'povr')
dictionary['column'] = dictionary['column'].str.replace('public', 'publ')
dictionary['column'] = dictionary['column'].str.replace('ecres', 'ecre')
dictionary['column'] = dictionary['column'].str.replace('single', 'sing')
# dictionary['column'] = dictionary['column'].str.replace()
dictionary.to_csv(OUTPUT_DIR + '/helpers/dictionary.csv', index=False)            
dictionary.to_json(OUTPUT_DIR + '/helpers/dictionary.json', 'records')
