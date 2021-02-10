#!/bin/bash

# This script fetches CSV data for each bucket passed in the second argument.
# ARG 1 = Path to the repo where raw data resides.
# ARG 2 = Comma-delineated list of subdirectories.
# Test locally with:
# bash ./scripts/fetch_raw_data.sh https://raw.githubusercontent.com/Hyperobjekt/ddk-data/deploy tracts,states,metros 1 1

echo 'Fetching raw data.'
# Path to the source data.
data_path=$1
# Data version
version=$2
# Name of repo where we pull the zip tag archive from.
repo="ddk-data"
# Get types of shapes to fetch based on argument.
# shape_types=(`echo $2 | tr ',' ' '`)
# Whether or not to fetch bar chart data.
# bar_charts=$3
# Are we debugging?
debug=$3

wget "${data_path}${version}.zip"
if [ -e "${version}.zip" ]
then
  if [[ $DEBUG -eq 1 ]]; then
    echo "Download of zip file successful. Unzipping..."
  fi
  unzip ${version}.zip
  mv ${repo}-${version} source
  if [ -d source ]
  then
    echo "Successfully unzipped source directory."
    tree source
  fi
fi
