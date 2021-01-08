import os
import sys
import pandas as pd
import json

from constants import *

# Test locally with:
# python3 ./scripts/build_dictionary.py tracts,states 1

print("Building dictionary...")

shapetypes = sys.argv[1].split(',') # Shape types to process: `tracts`, `counties`, `states`, or `zips`.
print("shapetype array = ", shapetypes)
debug = sys.argv[2]

# Get list of files.
csvs_arr = ['index', 'pop', 'raw', 'zscores'] # shapetypes # os.listdir(SOURCE_DIR)

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
        path = f'{SOURCE_DIR}/{shape}/{csv}/dictionary.csv'
        # print('Path is ' + path)
        # Make sure the file exists.
        if os.path.exists(path):
            # Get csv contents as dataframe.
            source = pd.read_csv(path)
            # print(source.head())
            if (csv == 'pop'):
                # Remove extraneous column and the first several lines.
                # source = source.drop(columns=['Add to dot density layer'])
                source = source.drop(source.index[0:7])
            else:
                if (csv == 'index'):
                    # source.rename(columns={'Choropleth map': 'ch', 'Visualize on map': 'map'}, inplace=True)
                    source.rename(columns={'Scale': 'scale', 'Visualize on map': 'map'}, inplace=True)
                    source = source[['column', 'type', 'label', 'description', 'scale', 'map']]
                    source['column'] = 'x_' + source['column'].astype(str)
                    source['map'] = source['map'].replace(regex={r'[no|No]': 0, r'[yes|Yes]': 1})
                    print(source.head())
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
                source = source.drop([0,1,2,3,4,5,6,7,8,9])
                # print(source.head())
                source['column'] = source['column'].str.lower()
                # print(source.head())
            dictionary = pd.concat([dictionary, source])
            # print(dictionary.head())

        else:
            print(f'File at {path} doesn\'t seem to exist!')

# Replace to shorten column headers and keep json small.
for key, value in SEARCH_AND_REPLACE.items():
  dictionary['column'] = dictionary['column'].str.replace(str(key), str(value))
# print(source.head())

# Build a simple object that lists the variables and their labels and descriptions
# that can be merged into the i18n us_EN lang object in the app.
en_US = {}
dict = dictionary.to_dict('records')
for item in dict:
    en_US[item['column']] = item['label']
    en_US[f"{item['column']}_desc"] = item['description']
# Add state names
states = pd.read_csv(f'{OUTPUT_DIR}/{STATES_PROC}.csv')
states = states.to_dict('records')
for item in states:
  en_US[item['usps']] = item['name']
# Source file for metro data.
metros = pd.read_csv(f'{OUTPUT_DIR}/{METROS_PROC}.csv')
metros = metros.to_dict('records')
for item in metros:
  en_US[item['GEOID']] = item['msaname15']
# Also write total
with open(OUTPUT_DIR + '/helpers/en_US.json','w') as f:
    json.dump(en_US,f)

dictionary.to_csv(OUTPUT_DIR + '/helpers/dictionary.csv', index=False)
dictionary.to_json(OUTPUT_DIR + '/helpers/dictionary.json', 'records')
