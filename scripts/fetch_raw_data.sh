#!/bin/bash

# This script fetches CSV data for each bucket passed in the second argument.
# ARG 1 = Path to the repo where raw data resides.
# ARG 2 = Comma-delineated list of subdirectories.

echo 'Fetching raw data.'
# Path to the source data.
data_path=$1
# Get types of shapes to fetch based on argument.
shape_types=(`echo $2 | tr ',' ' '`)
# Whether or not to fetch bar chart data.
bar_charts=$3

# Array of files to fetch for map data.
csv_types=( index raw pop zscores )
# Array of files to fetch for bar chart data.
bar_chart_types=( msaname15 nation stateusps )

if [ ! -d source ]   # For file "if [ -f /home/rama/file ]"
then
  mkdir source
fi
cd source

for shape in "${shape_types[@]}"
do
  # echo "shape is ${shape}."
  for csv in "${csv_types[@]}"
  do
    curl_status=`curl --silent --connect-timeout 8 --output /dev/null "${data_path}/${shape}/${csv}/${csv}.csv" -I -w "%{http_code}\n"`
    # echo "curl_status = ${curl_status}."
    if [ ${curl_status} -eq 200 ]
    then
      if [ ! -d "${shape}" ]
      then
        mkdir "${shape}"
      fi
      curl "${data_path}/${shape}/${csv}/${csv}.csv" -o "${shape}/${csv}.csv" 
      if [ -e "${shape}/${csv}.csv" ]
      then
        ls -la ${shape}
        head -n 5 "${shape}/${csv}.csv"
        echo "Downloaded ${shape} file ${csv}.csv."
      fi
    else
      echo "File at ${data_path}/${shape}/${csv}/${csv}.csv doesn't appear to be available."
    fi
    curl_status=`curl --silent --connect-timeout 8 --output /dev/null "${data_path}/${shape}/${csv}/dictionary.csv" -I -w "%{http_code}\n"`
    # echo "curl_status = ${curl_status}."
    if [ ${curl_status} -eq 200 ]
    then
      if [ ! -d "${shape}" ]
      then
        mkdir "${shape}"
      fi
      curl "${data_path}/${shape}/${csv}/dictionary.csv" -o "${shape}/${csv}_dict.csv" 
      if [ -e "${shape}/${csv}_dict.csv" ]
      then
        ls -la ${shape}
        head -n 5 "${shape}/${csv}_dict.csv"
        echo "Downloaded ${shape} dictionary file ${csv}_dict.csv."
      fi
    else
      echo "File at ${data_path}/${shape}/${csv}/dictionary.csv doesn't appear to be available."
    fi
  done
done

# Fetch bar chart data.
if [ ${bar_charts} -eq "1" ]
then
  echo 'Fetching bar charts data.'
  for csv in "${bar_chart_types[@]}"
  do
    echo "csv is ${csv}."
    curl_status=`curl --silent --connect-timeout 8 --output /dev/null "${data_path}/barcharts/${csv}.csv" -I -w "%{http_code}\n"`
    echo "curl_status = ${curl_status}." 
    if [ ${curl_status} -eq 200 ]
      then
        if [ ! -d barcharts ]
          then
            mkdir barcharts
            ls
        fi
        curl "${data_path}/barcharts/${csv}.csv" -o "barcharts/${csv}.csv"
        ls -la barcharts
        head -n 5 "barcharts/${csv}.csv"
        echo "Downloaded barcharts file ${csv}.csv."
      else
        echo "Unable to download barcharts/${csv}.csv."
    fi
  done
fi
