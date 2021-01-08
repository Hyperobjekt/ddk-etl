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
csvs_arr = ['index', 'pop', 'raw', 'zscores'] # shapetypes # os.listdir(SOURCE_DIR)
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
    shape_all = pd.DataFrame()
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
                  new_cols = list(source.columns)
                  for i, val in enumerate(new_cols, start=0):
                    if i > 8:
                      new_cols[i] = 'r_' + val
                  source.columns = new_cols
                  print('Prefixed raw columns')
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
              source["geoid"] = "0" + source["geoid"].astype(str)
              print('Prefixed geoid column.')
              print(source.head())
              # Replace to shorten column headers and keep json small.
              for key, value in SEARCH_AND_REPLACE.items():
                source.columns = source.columns.str.replace(str(key), str(value))
              source = source.sort_values(by=['GEOID'])
              print(source.head())

              # Split out 2010 data.
              source10 = source[(source["year"] == 2010)]

              # Isolate metadata columns.
              pre10 = source10.iloc[:, [0,2,3,4,5,6,7,8]]

              # Isolate data columns and rename with '10' suffix.
              data10 = source10.iloc[:, 9:].add_suffix("_10")

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
              data15 = source15.iloc[:, 8:].add_suffix("_15")

              # Join renamed.
              proc15 = pre15.join(data15)
              # print('proc15')
              # print(proc15.iloc[:,0:15].head())

              # Merge '10 and '15 dataframes.
              proc = proc10.merge(proc15)
              # print('proc')
              # print(proc.iloc[:,20:40].head())
              # Create shape dir if not exists.
              # if not os.path.exists(f'{OUTPUT_DIR}/{shape}'):
              #     os.mkdir(f'{OUTPUT_DIR}/{shape}')

              # Export a list of metro areas plus codes.
              if (csv == 'index'):
                  if (build_metro == True):
                      print('building metros')
                      metros = proc.loc[:, ['msaid15', 'msaname15', 'countyfips', 'statefips', 'stateusps', 'in100']]
                      metros = metros.drop_duplicates(subset=['msaid15'], keep='first')
                      # Add a column for whether it's a dual-state metro area.
                      metros['dual_st'] = metros['msaname15'].str.contains(',\s[A-Z]{2}-[A-Z]{2}', regex=True)
                      metros['dual_st'] = metros['dual_st'].fillna(0).astype(int)
                      metros.rename(columns={'msaid15': 'GEOID'}, inplace=True)
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
                  pop = proc.loc[:, POP_COLS]
                  pop = pop.sort_values(by=['GEOID'])
                  print('pop')
                  print(pop.head())
                  pop.to_csv(OUTPUT_DIR + '/' + csv + '.csv', index=False)
                  pop.to_json(OUTPUT_DIR + '/' + csv + '.json', 'records')

              # Remove verbose metro title after all other gen work done.
              proc = proc.drop('msaname15', 1)

              # Combine all processed csvs into a single dataframe for export.
              # print("Is shape_all empty? " + str(shape_all.empty))
              if shape_all.empty == True:
                shape_all = proc
              else:
                shape_all = shape_all.merge(proc)
              print('shape_all')
              print(shape_all.head())
          else:
              print(f'File at {path} doesn\'t seem to exist!')
      if shape_all.empty != True:
        # If shape is tracts, write an limited set to go on tiles.
        tracts = shape_all[TRACT_GEOJSON_COLS]
        tracts.to_csv(f'{OUTPUT_DIR}/tracts.csv', index=False)
        tracts.to_json(f'{OUTPUT_DIR}/tracts.json', 'records')

        # Also write combined dataframe for all included CSV files to CSV and JSON files.
        shape_all.to_csv(f'{OUTPUT_DIR}/{shape}-all-data.csv', index=False)
        shape_all.to_json(f'{OUTPUT_DIR}/{shape}-all-data.json', 'records')

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
