#!/bin/bash

# To run locally:
# bash ./scripts/join_geojson.sh tracts,states,metros 1

# Merges processed data with geojson.
echo 'join_geojson.sh'

# Get types of shapes to fetch based on argument.
shape_types=(`echo $1 | tr ',' ' '`)
# Are we debugging?
debug=$2
# Source dir
SOURCE_DIR="source"
# Processed data dir
OUTPUT_DIR="proc"

if [ ! -d "./${SOURCE_DIR}/geojson" ]
then
  mkdir -p "./${SOURCE_DIR}/geojson"
fi

if [ ! -d "./${OUTPUT_DIR}/geojson" ]
then
  mkdir -p "./${OUTPUT_DIR}/geojson"
fi

# For each shapetype, merge the shapetype data with the geojson file.
for shape in "${shape_types[@]}"
do
  echo "======== Processing geojson for ${shape}."
  # head -5 "geojson/${shape}.geojson"
  tippecanoe-json-tool -e GEOID "geojson/${shape}.geojson" | LC_ALL=C sort > "${SOURCE_DIR}/geojson/${shape}.sort.geojson"
  tippecanoe-json-tool -pe -w -c "${OUTPUT_DIR}/${shape}.csv" "${SOURCE_DIR}/geojson/${shape}.sort.geojson" > "${OUTPUT_DIR}/geojson/${shape}.geojson"
  if [[ $debug -eq 1 ]]; then
    echo "========== Joined GeoJSON for ${shape}."
    if [[ $shape -eq "tracts" ]]; then
      head -2 "./${OUTPUT_DIR}/geojson/${shape}.geojson"
    fi
  fi
done

echo "Done merging csv into geojson."
if [[ $debug -eq 1 ]]; then
  # head -2 "${OUTPUT_DIR}/geojson/${shape}.geojson"
  tree "./${OUTPUT_DIR}"
  ls -lah "./${OUTPUT_DIR}/geojson/"
fi
