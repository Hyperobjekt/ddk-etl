import os
import sys
import pandas as pd

print("Processing source shape data...")

shapetypes = sys.argv[1].split(',') # Shape types to process: `tracts`, `counties`, `states`, or `zips`.
print("shapetype array = ", shapetypes)
build_metro = bool(sys.argv[2])

SOURCE_DIR = './source/'
OUTPUT_DIR = './proc/'
# print('source dir is ', SOURCE_DIR)

# Columns with categorical data that we will change from string to number.
LONG_STRING_COLS = ['c5_ed_nat', 'c5_he_nat', 'c5_se_nat', 'c5_coi_nat', 'c5_ed_stt', 'c5_he_stt', 'c5_se_stt', 'c5_coi_stt', 'c5_ed_met', 'c5_he_met', 'c5_se_met', 'c5_coi_met']
# Key for these conversions of string to number.
REPLACE_DICT = {'Very Low': 0, 'Low': 1, 'Moderate': 2, 'High': 3, 'Very High': 4}

REPLACE_RAW_DICT = {
    'ed_prxece': 'r_ed_prxece',
    'ed_prxhqece': 'r_ed_prxhqece',
    'ed_ecenrol': 'r_ed_ecenrol',
    'ed_reading': 'r_ed_reading',
    'ed_math': 'r_ed_math',
    'ed_hsgrad': 'r_ed_hsgrad',
    'ed_apenr': 'r_ed_apenr',
    'ed_college': 'r_ed_college',
    'ed_schpov': 'r_ed_schpov',
    'ed_teachxp':'r_ed_teachxp',
    'ed_attain': 'r_ed_attain',
    'he_food':'r_he_food',
    'he_green': 'r_he_green',
    'he_walk': 'r_he_walk',
    'he_vacancy': 'r_he_vacancy',
    'he_suprfnd': 'r_he_suprfnd',
    'he_rsei': 'r_he_rsei',
    'he_pm25': 'r_he_pm25',
    'he_ozone': 'r_he_ozone',
    'he_heat': 'r_he_heat',
    'he_hlthins': 'r_he_hlthins',
    'se_emprat': 'r_se_emprat',
    'se_jobprox': 'r_se_jobprox',
    'se_povrate': 'r_se_povrate',
    'se_public': 'r_se_public',
    'se_home': 'r_se_home',
    'se_occ': 'r_se_occ',
    'se_mhe': 'r_se_mhe',
    'se_single': 'r_se_single'
}


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
            # ed : e / education
            # he: h / health
            # se: s / socioeconomic
            # coi: c / Child Opportunity Index
            # nat: n / national 
            # stt: s / state
            # met: m / metro
            # aian: as / asian
            # black: b
            # api: ap / asian pacific islander
            # hisp: hi / hispanic
            # other2: o2
            # nonwhite: nw
            # white: w
            # total: t (population)
            # Raw and zscore indicators, shortened to 4 chars or less.
            # prxece: prxe
            # prxhqece: prxh
            # ecenrol: ecen
            # reading: read
            # hsgrad: hsgr
            # apenr: apen
            # college: coll
            # schpov: schp
            # teachxp: teac
            # attain: atta
            # green: gree
            # vacancy: vaca
            # suprfnd: supr
            # ozone: ozon
            # hlthins: hlth
            # emprat: empr
            # jobprox: jobp
            # povrate: povr
            # public: publ
            # ecres: ecre
            # single: sing
            # Replace methods
            # TODO: Abstract and optimize.
            # Indicator cats
            source.columns = source.columns.str.replace('ed', 'e')
            source.columns = source.columns.str.replace('he', 'h')
            source.columns = source.columns.str.replace('se', 's')
            source.columns = source.columns.str.replace('coi', 'c')
            # Geo
            source.columns = source.columns.str.replace('nat', 'n')
            source.columns = source.columns.str.replace('stt', 's')
            source.columns = source.columns.str.replace('met', 'm')
            # Demo
            source.columns = source.columns.str.replace('aian', 'as')
            source.columns = source.columns.str.replace('black', 'b')
            source.columns = source.columns.str.replace('api', 'ap')
            source.columns = source.columns.str.replace('hisp', 'hi')
            source.columns = source.columns.str.replace('other2', 'o2')
            source.columns = source.columns.str.replace('nonwhite', 'nw')
            source.columns = source.columns.str.replace('white', 'w')
            source.columns = source.columns.str.replace('total', 't')
            source.columns = source.columns.str.replace('prxece', 'prxe')
            source.columns = source.columns.str.replace('prxhqece', 'prxh')
            source.columns = source.columns.str.replace('ecenrol', 'ecen')
            source.columns = source.columns.str.replace('reading', 'read')
            source.columns = source.columns.str.replace('hsgrad', 'hsgr')
            source.columns = source.columns.str.replace('apenr', 'apen')
            source.columns = source.columns.str.replace('college', 'coll')
            source.columns = source.columns.str.replace('schpov', 'schp')
            source.columns = source.columns.str.replace('teachxp', 'teac')
            source.columns = source.columns.str.replace('attain', 'atta')
            source.columns = source.columns.str.replace('green', 'gree')
            source.columns = source.columns.str.replace('vacancy', 'vaca')
            source.columns = source.columns.str.replace('suprfnd', 'supr')
            source.columns = source.columns.str.replace('ozone', 'ozon')
            source.columns = source.columns.str.replace('hlthins', 'hlth')
            source.columns = source.columns.str.replace('emprat', 'empr')
            source.columns = source.columns.str.replace('jobprox', 'jobp')
            source.columns = source.columns.str.replace('povrate', 'povr')
            source.columns = source.columns.str.replace('public', 'publ')
            source.columns = source.columns.str.replace('ecres', 'ecre')
            source.columns = source.columns.str.replace('single', 'sing')
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
                    # print('metros')
                    # print(metros.head())
                    metros.to_csv(OUTPUT_DIR + '/helpers/metros.csv', index=False)
                    metros.to_json(OUTPUT_DIR + '/helpers/metros.json', 'records')
            
        else:
            print(f'File at {path} doesn\'t seem to exist!')
