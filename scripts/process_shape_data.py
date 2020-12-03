import os
import sys
import pandas as pd

from constants import *

print("Processing source shape data...")

shapetypes = sys.argv[1].split(',') # Shape types to process: `tracts`, `counties`, `states`, or `zips`.
print("shapetype array = ", shapetypes)
build_metro = bool(sys.argv[2])

SOURCE_DIR = './source'
OUTPUT_DIR = './proc'
# print('source dir is ', SOURCE_DIR)

# Get list of files.
csvs_arr = ['index', 'pop', 'raw', 'zscores'] # shapetypes # os.listdir(SOURCE_DIR)
# csvs_arr = [item.replace('.csv', '') for item in csvs_arr]
# print('csvs_arr is ', csvs_arr)

# If not output path, create one.
if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)
if not os.path.exists(f'{OUTPUT_DIR}/helpers'):
    os.mkdir(f'{OUTPUT_DIR}/helpers')
# print(os.listdir('.'))

# For each file in the array...
for shape in shapetypes:
    for csv in csvs_arr:
        print(f'Processing {csv}.')
        # plot.savefig(f'hanning{num}.pdf')
        path = f'{SOURCE_DIR}/{shape}/{csv}.csv'
        # print('Path is ' + path)
        # Make sure the file exists.
        if os.path.exists(path):
            # Get csv contents as dataframe.
            source = pd.read_csv(path)
            # Make all columns lowercase.
            source.columns = source.columns.str.lower()
            # Fill empty values so we can convert to rm decimal points.
            source['msaid15'] = source['msaid15'].fillna(0).astype(int)
            source['in100'] = source['in100'].fillna(0).astype(int)
            # zscores, replace "z" with "z_"
            if (csv == 'zscores'):
                source.columns = source.columns.str.replace('z', 'z_')
                print('Prefixed zscores columns.')
                print(source.head())
            # raw, prefix with "r_"
            if (csv == 'raw'):
                source = source.rename(columns=REPLACE_RAW_DICT)
                print('Prefixed raw columns.')
                print(source.head())
            # Replace categorical strings in each categorical column with numbers.
            if (csv == 'index'):
                print('Processing categorical columns...')
                source[LONG_STRING_COLS] = source[LONG_STRING_COLS].replace(REPLACE_DICT, inplace=False)
                print(source[LONG_STRING_COLS].head())

            # Replace to shorten column headers and keep json small.  
            for key, value in SEARCH_AND_REPLACE.items():
              source.columns = source.columns.str.replace(str(key), str(value))
            print(source.head())
            
            # Split out 2010 data.
            source10 = source[(source["year"] == 2010)]
            
            # Isolate metadata columns.
            pre10 = source10.iloc[:, [0,2,3,4,5,6,7]]
            
            # Isolate data columns and rename with '10' suffix.
            data10 = source10.iloc[:, 8:300].add_suffix("_10")
            
            # Join renamed.
            proc10 = pre10.join(data10)
            # print('proc10')
            # print(proc10.iloc[:,0:15].head())
            
            # Split out 2015 data.
            source15 = source[source['year'] == 2015]
            # print('source15')
            # print(source15.head())

            # Isolate metadata columns.
            pre15 = source15.iloc[:, [0,2,3,4,5,6,7]]

            # Isolate data columns and rename with '15' suffix.
            data15 = source15.iloc[:, 8:300].add_suffix("_15")
            
            # Join renamed.
            proc15 = pre15.join(data15)
            # print('proc15')
            # print(proc15.iloc[:,0:15].head())
            
            # Merge '10 and '15 dataframes.
            proc = proc10.merge(proc15)
            # print('proc')
            # print(proc.iloc[:,20:40].head())
            # Create shape dir if not exists.
            if not os.path.exists(f'{OUTPUT_DIR}/{shape}'):
                os.mkdir(f'{OUTPUT_DIR}/{shape}')

            # Save each merged dataframe to a new directory for the processed files..
            proc.to_csv(OUTPUT_DIR + '/' + shape + '/' + csv + '.csv', index=False)
            proc.to_json(OUTPUT_DIR + '/' + shape + '/' + csv + '.json', 'records')
            
            # Export a list of metro areas plus codes.
            if (csv == 'index'):
                if (build_metro == True):
                    print('building metros')
                    metros = proc.loc[:, ['msaid15', 'msaname15', 'countyfips', 'statefips', 'stateusps', 'in100']]
                    metros = metros.drop_duplicates(subset=['msaid15'], keep='first')
                    metros = metros.dropna(axis=0)
                    # print('metros')
                    # print(metros.head())
                    metros.to_csv(OUTPUT_DIR + '/helpers/metros.csv', index=False)
                    metros.to_json(OUTPUT_DIR + '/helpers/metros.json', 'records')
            
        else:
            print(f'File at {path} doesn\'t seem to exist!')
