#!/bin/bash

# Fetches, processes, and uploads metro shapefile.
# echo "Fetching metros geo shapes."
# Path to the source data.
data_path="ftp://ftp2.census.gov/geo/tiger/GENZ2015/shp/"
# Metros file.
metros_file="cb_2015_us_cbsa_500k"
# Are we debugging?
debug=$1

# If geojson file doesn't exist, create it.
if [ ! -d "./geojson" ];
then
  mkdir -p "./geojson"
fi
# Move into the dir.
# Get the file.
wget "${data_path}${metros_file}.zip"
# If fetch was successful, unzip and shape.
if [ -e "${metros_file}.zip" ];
then
  # Unzip.
  unzip -d ./geojson/ "${metros_file}.zip"
  # Shape the file.
  mapshaper ./geojson/${metros_file}.shp combine-files \
    -each "this.properties.GEOID = this.properties.CBSAFP" \
    -o combine-layers format=geojson ./geojson/metros.geojson
  # Zip the geojson up.
  gzip ./geojson/metros.geojson
  # Upload the file to AWS.
  aws s3 cp ./geojson/metros.geojson.gz s3://ddk-source/geojson/ \
   --acl=public-read \
   --region=us-east-1 \
   --cache-control max-age=2628000
  echo 'Done writing geojson.'
else
  echo 'Something went wrong when downloading the file.'
fi








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
