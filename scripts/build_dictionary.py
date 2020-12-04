import os
import sys
import pandas as pd

from constants import *

print("Building dictionary...")

shapetypes = sys.argv[1].split(',') # Shape types to process: `tracts`, `counties`, `states`, or `zips`.
print("shapetype array = ", shapetypes)
debug = sys.argv[2]

SOURCE_DIR = './source'
OUTPUT_DIR = './proc'

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
                    source['column'] = 'x_' + source['column'].astype(str)
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

# Replace to shorten column headers and keep json small.  
for key, value in SEARCH_AND_REPLACE.items():
  dictionary['column'] = dictionary['column'].str.replace(str(key), str(value))
# print(source.head())

dictionary.to_csv(OUTPUT_DIR + '/helpers/dictionary.csv', index=False)            
dictionary.to_json(OUTPUT_DIR + '/helpers/dictionary.json', 'records')
