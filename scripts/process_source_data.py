import os
import sys
import pandas as pd

print("Processing source data...")

shapetype = sys.argv[1] # `tract`, `county`, `state`, or `zip`.

SOURCE_DIR = './source/' + shapetype
OUTPUT_DIR = './proc' + shapetype
# print('source dir is ', SOURCE_DIR)

# Columns with categorical data that we will change from string to number.
LONG_STRING_COLS = ['c5_ed_nat', 'c5_he_nat', 'c5_se_nat', 'c5_coi_nat', 'c5_ed_stt', 'c5_he_stt', 'c5_se_stt', 'c5_coi_stt']
# Key for these conversions of string to number.
REPLACE_DICT = {'Very Low': 0, 'Low': 1, 'Moderate': 2, 'High': 3, 'Very High': 4}

# Get list of files.
csvs_arr = os.listdir(SOURCE_DIR)
csvs_arr = [item.replace('.csv', '') for item in csvs_arr]
# print('csvs_arr is ', csvs_arr)

# If not output path, create one.
if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)
# print(os.listdir('.'))

# For each file in the array...
for csv in csvs_arr:
    print("Processing " + csv)
    path = SOURCE_DIR + '/' + csv + '.csv'
    # print('Path is ' + path)
    # Get csv contents as dataframe.
    source = pd.read_csv(path)
    # print(source.head())
    # Make all columns lowercase.
    source.columns = source.columns.str.lower()
    # print(source.head())
    # Replace categorical strings in each categorical column with numbers.
    if (csv == 'index'):
        print('Processing categorical columns...')
        source[LONG_STRING_COLS] = source[LONG_STRING_COLS].replace(REPLACE_DICT, inplace=False)
        print(source[LONG_STRING_COLS].head())
    
    # Split out 2010 data.
    source10 = source[(source["year"] == 2010)]
    
    # Isolate metadata columns.
    pre10 = source10.iloc[:, [0,2,3,4,5,6,7]] # source10.iloc[:, [0, 2:7]] # df.iloc[1:3, 0:3]
    
    # Isolate data columns and rename with '10' suffix.
    data10 = source10.iloc[:, 8:300].add_suffix(10)
    
    # Join renamed.
    proc10 = pre10.join(data10)
    # print('proc10')
    # print(proc10.iloc[:,0:15].head())
    
    # Split out 2015 data.
    source15 = source[source['year'] == 2015]
    # print('source15')
    # print(source15.head())

    # Isolate metadata columns.
    pre15 = source15.iloc[:, [0,2,3,4,5,6,7]] # source10.iloc[:, [0, 2:7]] # df.iloc[1:3, 0:3]
    
    # Isolate data columns and rename with '15' suffix.
    data15 = source15.iloc[:, 8:300].add_suffix(15)
    
    # Join renamed.
    proc15 = pre15.join(data15)
    # print('proc15')
    # print(proc15.iloc[:,0:15].head())
    
    # Merge '10 and '15 dataframes.
    proc = proc10.merge(proc15)
    # print('proc')
    # print(proc.iloc[:,20:40].head())

    # Save each merged dataframe to a new directory for the processed files..
    proc.to_csv(OUTPUT_DIR + '/' + csv + '.csv', index=False)
    proc.to_json(OUTPUT_DIR + '/' + csv + '.json', 'records')
