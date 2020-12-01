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
            # Replace categorical strings in each categorical column with numbers.
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
                    source = source[['column', 'type', 'label', 'description']]
                source = source.drop([0,1,2,3,4,5,6,7,8,9,10])
                # print(source.head())
                source['column'] = source['column'].str.lower()
                # print(source.head())
            dictionary = pd.concat([dictionary, source])
            # print(dictionary.head())

        else:
            print(f'File at {path} doesn\'t seem to exist!')

dictionary.to_csv(OUTPUT_DIR + '/helpers/dictionary.csv', index=False)            
dictionary.to_json(OUTPUT_DIR + '/helpers/dictionary.json', 'records')
