import os
import sys
import pandas as pd

from constants import *

print("Processing source shape data...")

# To run locally:
# python3 ./scripts/process_shape_data.py tracts,states,metros 1 1

shapetypes = sys.argv[1].split(',') # Shape types to process: `tracts`, `counties`, `states`, or `zips`.
print("shapetype array = ", shapetypes)
build_metro = bool(sys.argv[2])

debug = bool(sys.argv[3])

SOURCE_DIR = './source'
OUTPUT_DIR = './proc'
# print('source dir is ', SOURCE_DIR)

# Get list of files.
csvs_arr = ['index', 'pop', 'raw'] # ['index', 'pop', 'raw', 'zscores'] # shapetypes # os.listdir(SOURCE_DIR)
states_src = STATES_SRC
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
    shape_all_10 = pd.DataFrame()
    shape_all_15 = pd.DataFrame()
    if (shape == 'tracts'):
      for csv in csvs_arr:
          print(f'Processing {csv}.')
          # plot.savefig(f'hanning{num}.pdf')
          path = f'{SOURCE_DIR}/{shape}/{csv}/{csv}.csv'
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
                  # print('Prefixed zscores columns.')
                  # print(source.head())
              # raw, prefix with "r_"
              if (csv == 'raw'):
                  # Preface all columns in raw with an _r
                  # new_cols = list(source.columns)
                  # for i, val in enumerate(new_cols, start=0):
                  #   if i > 8:
                  #     new_cols[i] = 'r_' + val
                  # source.columns = new_cols
                  # print('Prefixed raw columns')
                  print(source.head())
              # Replace categorical strings in each categorical column with numbers.
              if (csv == 'index'):
                  print('Processing categorical columns...')
                  source[LONG_STRING_COLS] = source[LONG_STRING_COLS].replace(REPLACE_DICT, inplace=False)
                  print(source[LONG_STRING_COLS].head())
                  new_cols = list(source.columns)
                  for i, val in enumerate(new_cols, start=0):
                    if i > 8:
                      new_cols[i] = 'x_' + val
                  source.columns = new_cols
                  print('Prefixed index columns')
                  print(source.head())
              # source["geoid"] = "0" + source["geoid"].astype(str)
              source["geoid"] = source["geoid"].astype(str).str.pad(11, side='left', fillchar='0')
              print('Padded geoid column.')
              print(source.head())
              # Replace to shorten column headers and keep json small.
              for key, value in SEARCH_AND_REPLACE.items():
                source.columns = source.columns.str.replace(str(key), str(value))
              source = source.sort_values(by=['GEOID'])
              print(source.head())

              # Split out 2010 data.
              source10 = source[(source["year"] == 2010)]

              # Isolate metadata columns.
              pre10 = source10.iloc[:, [0,1,2,3,4,5,6,7,8]]

              # Isolate data columns and rename with '10' suffix.
              data10 = source10.iloc[:, 9:].round(2)

              # Round data columns to 10 decimal places.
              # proc10 = source10.iloc[:, 8:].round(3)

              # Join renamed.
              proc10 = pre10.join(data10)
              print('proc10')
              print(proc10.iloc[:,0:15].head())

              # Split out 2015 data.
              source15 = source[source['year'] == 2015]
              # print('source15')
              # print(source15.head())

              # Isolate metadata columns.
              pre15 = source15.iloc[:, [0,1,2,3,4,5,6,7,8]]

              # Isolate data columns and rename with '15' suffix.
              data15 = source15.iloc[:, 9:].round(2)

              # Round data columns to 10 decimal places.
              # proc15 = source15.iloc[:, 8:].round(3)

              # Join renamed.
              proc15 = pre15.join(data15)
              print('proc15')
              print(proc15.iloc[:,0:15].head())

              # Merge '10 and '15 dataframes.
              # proc = proc10.merge(proc15)
              # print('proc')
              # print(proc.iloc[:,20:40].head())
              # Create shape dir if not exists.
              # if not os.path.exists(f'{OUTPUT_DIR}/{shape}'):
              #     os.mkdir(f'{OUTPUT_DIR}/{shape}')

              # Export a list of metro areas plus codes.
              if (csv == 'index'):
                  if (build_metro == True):
                      print('building metros')
                      metros = source.loc[:, ['m', 'msaname15', 'countyfips', 's', 'stateusps', 'i']]
                      metros = metros.drop_duplicates(subset=['m'], keep='first')
                      # Add a column for whether it's a dual-state metro area.
                      metros['du'] = metros['msaname15'].str.contains(',\s[A-Z]{2}-[A-Z]{2}', regex=True)
                      metros['du'] = metros['du'].fillna(0).astype(int)
                      metros.rename(columns={'m': 'GEOID'}, inplace=True)
                      # Type as number because we're getting mismatches.
                      metros['GEOID'] = metros['GEOID'].astype(str)
                      metros = metros.dropna(axis=0)
                      metros = metros.sort_values(by=['GEOID'])
                      print('metros')
                      print(metros.head())
                      metros.to_csv(OUTPUT_DIR + '/' + METROS_PROC + '.csv', index=False)
                      metros.to_json(OUTPUT_DIR + '/' + METROS_PROC + '.json', 'records')

              # Export population data for use building points.
              if (csv == 'pop'):
                  print('building pop data')
                  pop10 = proc10[YEAR_AGNOSTIC_POP_COLS]
                  pop15 = proc15[YEAR_AGNOSTIC_POP_COLS]
                  pop10 = pop10.sort_values(by=['GEOID'])
                  pop15 = pop15.sort_values(by=['GEOID'])
                  print('pop10')
                  print(pop10.head())
                  print('pop15')
                  print(pop15.head())
                  pop10.to_csv(OUTPUT_DIR + '/' + 'pop10' + '.csv', index=False)
                  pop10.to_json(OUTPUT_DIR + '/' + 'pop10' + '.json', 'records')
                  pop15.to_csv(OUTPUT_DIR + '/' + 'pop15' + '.csv', index=False)
                  pop15.to_json(OUTPUT_DIR + '/' + 'pop15' + '.json', 'records')

              # Remove verbose metro title after all other gen work done.
              # proc = proc.drop('msaname15', 1)
              proc10 = proc10.drop('msaname15', 1)
              proc15 = proc15.drop('msaname15', 1)

              # Combine all processed csvs into a single dataframe for export.
              # print("Is shape_all empty? " + str(shape_all.empty))
              if shape_all_10.empty == True:
                # shape_all = proc
                shape_all_10 = proc10
              else:
                # shape_all = shape_all.merge(proc)
                shape_all_10 = shape_all_10.merge(proc10)

              if shape_all_15.empty == True:
                # shape_all = proc
                shape_all_15 = proc15
              else:
                shape_all_15 = shape_all_15.merge(proc15)
              print('shape_all_10')
              print(shape_all_10.head())
              print('shape_all_10 columns:')
              print(shape_all_10.columns.values.tolist())
              print('shape_all_15')
              print(shape_all_15.head())
          else:
              print(f'File at {path} doesn\'t seem to exist!')
      if shape_all_10.empty != True:
        # If shape is tracts, write an limited set to go on tiles.
        # tracts = shape_all[TRACT_GEOJSON_COLS]
        # tracts.to_csv(f'{OUTPUT_DIR}/tracts.csv', index=False)
        # tracts.to_json(f'{OUTPUT_DIR}/tracts.json', 'records')

        tracts10 = shape_all_10[TRACT_BY_YEAR_COLS]
        print('tracts10')
        print(tracts10.head())
        tracts10.to_csv(f'{OUTPUT_DIR}/tracts10.csv', index=False)
        tracts10.to_json(f'{OUTPUT_DIR}/tracts10.json', 'records')
        # Raw data for indicators
        raw10 = shape_all_10[RAW_DATA_COLS]
        raw10.to_csv(f'{OUTPUT_DIR}/raw10.csv', index=False)
        raw10.to_json(f'{OUTPUT_DIR}/raw10.json', 'records')
        # Also write combined dataframe for all included CSV files to CSV and JSON files.
        shape_all_10.to_csv(f'{OUTPUT_DIR}/{shape}10-all-data.csv', index=False)
        shape_all_10.to_json(f'{OUTPUT_DIR}/{shape}10-all-data.json', 'records')

      if shape_all_15.empty != True:
        tracts15 = shape_all_15[TRACT_BY_YEAR_COLS]
        tracts15.to_csv(f'{OUTPUT_DIR}/tracts15.csv', index=False)
        tracts15.to_json(f'{OUTPUT_DIR}/tracts15.json', 'records')
        # Raw data for indicators
        raw15 = shape_all_15[RAW_DATA_COLS]
        raw15.to_csv(f'{OUTPUT_DIR}/raw15.csv', index=False)
        raw15.to_json(f'{OUTPUT_DIR}/raw15.json', 'records')
        # Also write combined dataframe for all included CSV files to CSV and JSON files.
        shape_all_15.to_csv(f'{OUTPUT_DIR}/{shape}15-all-data.csv', index=False)
        shape_all_15.to_json(f'{OUTPUT_DIR}/{shape}15-all-data.json', 'records')

        # Make a smaller set for download.
        # tracts_sm = shape_all[TRACT_APP_COLS]
        # tracts_sm.to_csv(f'{OUTPUT_DIR}/tracts-sm.csv', index=False)
        # tracts_sm.to_json(f'{OUTPUT_DIR}/tracts-sm.json', 'records')

        # # Also write combined dataframe for all included CSV files to CSV and JSON files.
        # shape_all_10.to_csv(f'{OUTPUT_DIR}/{shape}10-all-data.csv', index=False)
        # shape_all_10.to_json(f'{OUTPUT_DIR}/{shape}10-all-data.json', 'records')
        # shape_all_15.to_csv(f'{OUTPUT_DIR}/{shape}15-all-data.csv', index=False)
        # shape_all_15.to_json(f'{OUTPUT_DIR}/{shape}15-all-data.json', 'records')

    if (shape == 'states'):
      path = f'{SOURCE_DIR}/{shape}/{states_src}.csv'
      print('Path is ' + path)
      # Make sure the file exists.
      if os.path.exists(path):
        # Get csv contents as dataframe.
        source = pd.read_csv(path)
        # Make all columns lowercase.
        source.columns = source.columns.str.lower()
        source['GEOID'] = source['fips'].astype(str)
        source['GEOID'] = source['GEOID'].str.rjust(2, '0')
        source = source[['GEOID', 'name', 'fips', 'usps']]
        source = source.sort_values(by=['GEOID'])
        print('state source')
        print(source.head())
        source.to_csv(f'{OUTPUT_DIR}/{shape}.csv', index=False)
        source.to_json(f'{OUTPUT_DIR}/{shape}.json', 'records')
