#!/bin/bash

# This script fetches processed geojson files.
# ARG 1 = Path to the repo where raw data resides.
# ARG 2 = Comma-delineated list of subdirectories.

echo 'fetch_proc_geojson.sh'
# Path to the source data.
# data_path=$1
# Get types of shapes to fetch based on argument.
shape_types=(`echo $1 | tr ',' ' '`)
# Are we debugging?
debug=$2
# Source dir
SOURCE_DIR="source"
# Processed data dir
OUTPUT_DIR="proc"

for shape in "${shape_types[@]}"
do
  mkdir -p "./geojson"
  mkdir -p "./${SOURCE_DIR}/geojson"
  aws s3 cp s3://ddk-source/geojson/${shape}.geojson.gz ./geojson/${shape}.geojson.gz
  gunzip ./geojson/${shape}.geojson.gz
done

if [[ $DEBUG -eq 1 ]]; then
  tree ./geojson
fi
