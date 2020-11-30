#!/bin/bash

echo 'Fetching raw data.'
# Get types of shapes to fetch based on argument.
shape_types=($1)
echo "My array: ${shape_types[@]}"
# csv_types = index raw pop zscores 
csv_types=( index raw pop zscores )

mkdir source
cd source

for $shape in shape_types
do
  for $csv in csv_types
  do
    curl "${RAW_DATA_PATH}" + '/' + $shape + '/' + $csv + '/' + $csv + '.csv' -o $csv + '.csv'
    ls
    head --lines=5 $csv + '.csv'
  	echo 'Downloaded tract file' + $csv + '.csv'
  done
done
