import os
import sys
import pandas as pd
import json

print("Processing bar chart data...")

SOURCE_DIR = './source/'
OUTPUT_DIR = './proc/'

# Key for these conversions of string to number.
REPLACE_DICT = {'Very Low': 0, 'Low': 1, 'Moderate': 2, 'High': 3, 'Very High': 4}
# Key for these conversions of string to number.
REPLACE_COLS_DICT = {'aian': 'as', 'api': 'ap', 'black': 'b', 'hisp': 'hi', 'white': 'w'}

# Get list of files.
chart_data_arr = ['msaname15', 'nation', 'stateusps']

# JSON result we are building.
result = {
    '2010': {
        'metros': {},
        'states': {},
        'nation': [],
    },
    '2015': {
        'metros': {},
        'states': {},
        'nation': [],
    }
}

# Get metro data to make dict.
metros = pd.DataFrame()
metros_path = f'{OUTPUT_DIR}/helpers/metros.csv'
if os.path.exists(metros_path):
    metros = pd.read_csv(metros_path)
    metros = metros.drop(['countyfips', 'statefips', 'stateusps', 'in100'], axis=1)
    metros_list = metros.to_dict('records')
states = pd.DataFrame()
# Prep list of states to receive state info.
states_path = f'{SOURCE_DIR}/barcharts/stateusps.csv'
if os.path.exists(states_path):
    states = pd.read_csv(states_path)
    states = states.drop(['grp','year','aian','api','black','hisp','white'], axis=1)
    states_list = states.to_dict('records')

for metro in metros_list:
    result['2010']['metros'][metro['msaid15']] = []
    result['2015']['metros'][metro['msaid15']] = []

for state in states_list:
    result['2010']['states'][state['stateusps']] = []
    result['2015']['states'][state['stateusps']] = []

# If not output path, create one.
if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)
if not os.path.exists(f'{OUTPUT_DIR}/barcharts'):
    os.mkdir(f'{OUTPUT_DIR}/barcharts')

# For each file in the array...
for csv in chart_data_arr:
    print(f'Processing {csv}.')
    path = f'{SOURCE_DIR}/barcharts/{csv}.csv'
    # print('Path is ' + path)
    # Make sure the file exists.
    if os.path.exists(path):
        # Get csv contents as dataframe.
        source = pd.read_csv(path)
        # Make all columns lowercase.
        source.columns = source.columns.str.lower()
        # For each file:
        # Rename columns
        source.rename(columns=REPLACE_COLS_DICT, inplace=True)
        # Replace strings in High/Low/etc column
        source['grp'] = source['grp'].replace(REPLACE_DICT, inplace=False)
        # Sort by msaname and then by grp.
        if (csv == 'msaname15'):
            source = pd.merge(source, metros, left_on="msaname15", right_on="msaname15")
            source = source[['msaid15', 'grp', 'year', 'as', 'ap', 'b', 'hi', 'w']]
            source = source.sort_values(by=['year', 'msaid15', 'grp'])
            # Also write the data to a dict that will be exported as JSON.
            dict = source.to_dict('records')
            for item in dict:
                year = str(item.get('year'))
                id = item.get('msaid15')
                result[year]['metros'][id].append(item)
        if (csv == 'nation'):
            source = source[['grp', 'year', 'as', 'ap', 'b', 'hi', 'w']]
            source = source.sort_values(by=['year', 'grp'])
            # Also write the data to a dict that will be exported as JSON.
            dict = source.to_dict('records')
            for item in dict:
                year = str(item.get('year'))
                result[year]['nation'].append(item)
        if (csv == 'stateusps'):
            source = source.sort_values(by=['year', 'stateusps', 'grp'])
            # Also write the data to a dict that will be exported as JSON.
            dict = source.to_dict('records')
            for item in dict:
                year = str(item.get('year'))
                result[year]['states'][item['stateusps']].append(item)
        
        # Save each merged dataframe to a new directory for the processed files..
        source.to_csv(OUTPUT_DIR + '/barcharts/' + csv + '.csv', index=False)
        source.to_json(OUTPUT_DIR + '/barcharts/' + csv + '.json', 'records')
    else:
        print(f'File at {path} doesn\'t seem to exist!')
# Also write total 
with open(OUTPUT_DIR + '/barcharts/barcharts.json','w') as f:
    json.dump(result,f)
