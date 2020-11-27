import os
import pandas as pd

print("Processing source data...")

SOURCE_DIR = './source_csvs'
print('source dir is ', SOURCE_DIR)
LONG_STRING_COLS = ['c5_ed_nat', 'c5_he_nat', 'c5_se_nat', 'c5_coi_nat', 'c5_ed_stt', 'c5_he_stt', 'c5_se_stt', 'c5_coi_stt']
REPLACE_DICT = {'Very Low': 0, 'Low': 1, 'Moderate': 2, 'High': 3, 'Very High': 4}

# Get list of files.
csvs_arr = os.listdir(SOURCE_DIR)
print('csvs_arr is ', csvs_arr)
# For each file in the array...
for csv in csvs_arr:
    print("Processing " + csv)
    path = SOURCE_DIR + '/' + csv
    print('Path is ' + path)
    # Get csv contents as dataframe.
    source = pd.read_csv(path)
    print(source.head())
    # Make all columns lowercase.
    source.columns = source.columns.str.lower()
    print(source.head())
    # Replace categorical strings in each categorical column with numbers.
    # df['Country'].replace(["Republic of Korea", "South Korea"],["United States of America", "United States"],["United Kingdom of Great Britain and Northern Ireland", "United Kingdom"],["China, Hong Kong Special Administrative Region", "Hong Kong"], inplace=True)
    if (csv == 'index.csv'):
        print('Processing categorical columns...')
        source[LONG_STRING_COLS] = source[LONG_STRING_COLS].replace(REPLACE_DICT, inplace=True)
        print(source[LONG_STRING_COLS].head())
    
    # Split rows into 2010 and 2015 data.
    # source10 = 
    # source15 = 

    # Rename columns in each dataframe with 10 or 15 suffix.
    # Merge dataframes using geoid column.
    # Save each merged dataframe to a new directory for the processed files..
