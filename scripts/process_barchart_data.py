import os
import sys
import pandas as pd

print("Processing bar chart data...")

SOURCE_DIR = './source/'
OUTPUT_DIR = './proc/'

# Key for these conversions of string to number.
REPLACE_DICT = {'Very Low': 0, 'Low': 1, 'Moderate': 2, 'High': 3, 'Very High': 4}

# Get list of files.
chart_data_arr = ['msaname15', 'nation', 'stateusps']

# If not output path, create one.
if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)
if not os.path.exists(f'{OUTPUT_DIR}/barcharts'):
    os.mkdir(f'{OUTPUT_DIR}/barcharts')
# print(os.listdir('.'))

# For each file in the array...
for csv in chart_data_arr:
    print(f'Processing {csv}.')
    # plot.savefig(f'hanning{num}.pdf')
    path = f'{SOURCE_DIR}/barcharts/{csv}.csv'
    # print('Path is ' + path)
    # Make sure the file exists.
    if os.path.exists(path):
        # Get csv contents as dataframe.
        source = pd.read_csv(path)
        # Make all columns lowercase.
        source.columns = source.columns.str.lower()
        
        # Replace msaname with msaid.
        # Rename other columns to be shorter. (Can do this in pop file too.)
        # Replace categorical strings with numbers.
        # Split by year.
        # Sort by msaid, then group.
        # Generate a json file of arrays of objects, with the msaid as key.
        # { 2010: { msaid: [{very low}, {low}, {middle}, {high}, {very high}] } }
        
        
        # Fill empty values so we can convert to rm decimal points.
        source['msaid15'] = source['msaid15'].fillna(0).astype(int)
        source['in100'] = source['in100'].fillna(0).astype(int)
        # print(pd.to_numeric(source['msaid15']).round())
        print(source.head())
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
                # print('metros')
                # print(metros.head())
                metros.to_csv(OUTPUT_DIR + '/helpers/metros.csv', index=False)
                metros.to_json(OUTPUT_DIR + '/helpers/metros.json', 'records')
        
    else:
        print(f'File at {path} doesn\'t seem to exist!')
