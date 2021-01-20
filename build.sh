#!/bin/bash

# Fetch environment values.
# Should the data be deployed?
SHOULD_DEPLOY=$(if [ "${DEPLOY}" -eq 1 ]; then echo 1; else echo 0; fi)
# Clean up? Boolean.
SHOULD_CLEAN=$(if [ "${CLEAN}" -eq 1 ]; then echo 1; else echo 0; fi)
# Should download census tract file and build raw geojson?
SHOULD_GEOJSON=$(if [ "${BUILD_GEOJSON}" -eq 1 ]; then echo 1; else echo 0; fi)
# BUILD_TYPES options in .env should be a comma-delineated list.
# options are: tracts, states, counties, zips
# ex: BUILD_TYPES=tracts,states
SHOULD_BUILD=$(if [ ! -z "${BUILD_TYPES}" ]; then echo "${BUILD_TYPES}"; else echo "tracts"; fi)
# Whether or not to fetch and process bar chart data. Boolean.
# SHOULD_BARCHART=$(if [ ! -z "${BAR_CHARTS}" ]; then echo "${BAR_CHARTS}"; else echo 1; fi)
SHOULD_BARCHART=$(if [ "${BAR_CHARTS}" -eq 1 ]; then echo 1; else echo 0; fi)
# Build dictionaries list of strings. Boolean.
# SHOULD_DICT=$(if [ ! -z "${BUILD_DICT}" ]; then echo "${BUILD_DICT}"; else echo 0; fi)
# Build metro list. Boolean.
# SHOULD_METRO=$(if [ ! -z "${BUILD_METRO_LIST}" ]; then echo "${BUILD_METRO_LIST}"; else echo 0; fi)
SHOULD_METRO=$(if [ "${BUILD_METRO_LIST}" -eq 1 ]; then echo 1; else echo 0; fi)
# Mapbox username and token for building tilesets.
MAPBOX_USER=$(if [ ! -z "${MAPBOX_USERNAME}" ]; then echo "${MAPBOX_USERNAME}"; else echo ""; fi)
MAPBOX_TKN=$(if [ ! -z "${MAPBOX_TOKEN}" ]; then echo "${MAPBOX_TOKEN}"; else echo ""; fi)
# Data version
DATA_VERSION=$(if [ ! -z "${DATA_VERSION}" ]; then echo "${DATA_VERSION}"; else echo 1.0.0; fi)
# Should the script upload mapbox shapes?
DEPLOY_SHAPES=$(if [ "${UPLOAD_MAPBOX_SHAPES}" -eq 1 ]; then echo 1; else echo 0; fi)
# Should the script upload mapbox points?
DEPLOY_POINTS=$(if [ "${UPLOAD_MAPBOX_POINTS}" -eq 1 ]; then echo 1; else echo 0; fi)
# Print extra debug info?
DEBUG=$(if [ "${DEBUG}" -eq 1 ]; then echo 1; else echo 0; fi)

startDate=`date +"%Y-%m-%d %T"`
echo "Starting build run: ${startDate}"

# Clean up files before starting. Helpful if you're running scripts locally.
if [[ $SHOULD_CLEAN -eq 1 ]]; then
    echo "Cleaning up..."
    # make clean
    rm -rf ./source
    rm -rf ./proc
    rm -rf ./geojson
    # tree .
fi

echo 'Configuring S3.'
if [[ -z "${AWS_ACCESS_ID}" ]]; then
    printf '%s\n' "Missing AWS_ACCESS_ID environment variable, could not configure AWS CLI." >&2
    exit 1
fi
if [[ -z "${AWS_SECRET_KEY}" ]]; then
    printf '%s\n' "Missing AWS_SECRET_KEY environment variable, could not configure AWS CLI." >&2
    exit 1
fi
aws configure set aws_access_key_id ${AWS_ACCESS_ID}
aws configure set aws_secret_access_key ${AWS_SECRET_KEY}
aws configure set default.region us-east-1

# Fetch tract source data.
if [ ! -z $SHOULD_BUILD ]; then

    # Fetch source geojson.
    echo "Fetching source geojson."
    if [ $SHOULD_GEOJSON -eq 1 ]; then
      # If deploy, upload files.
      make -f ./scripts/fetch_geo.mk all deploy
    fi

    echo "Downloading processed geojson."
    # No deploy, just download, unzip, and make geojson.
    bash ./scripts/fetch_proc_geojson.sh $SHOULD_BUILD $DEBUG

    echo "Fetching raw data."
    bash ./scripts/fetch_raw_data.sh $RAW_DATA_PATH $DATA_VERSION $DEBUG
    tree ./source

    echo "Preparing source data."
    python3 ./scripts/process_shape_data.py $SHOULD_BUILD $SHOULD_METRO $DEBUG
    tree ./source

    # Build dictionary string set.
    echo "Building dictionary data into string set."
    # ex: python3 ./scripts/build_dictionary.py tracts 1
    python3 ./scripts/build_dictionary.py $SHOULD_BUILD $DEBUG

    if [[ $SHOULD_BARCHART -eq 1 ]]; then
      # Generate barchart data.
      echo "Building dictionary data into string set."
      # ex: python3 ./scripts/process_barchart_data.py 1
      python3 ./scripts/process_barchart_data.py $DEBUG
    fi

    # Merge data with geojson.
    # ex: bash ./scripts/join_geojson.sh tracts 1
    bash ./scripts/join_geojson.sh $SHOULD_BUILD $DEBUG

    # Generate points for population data.
    node ./scripts/generate_points.js

    # Build tilesets.
    if [[ -z "${MAPBOX_TKN}" ]] || [[ -z "${MAPBOX_USER}" ]]; then
      echo "Mapbox token or Mapbox username not provided. You need to get that into the .env file  before you can build the tilesets."
    else
      # Generate tilesets.
      bash ./scripts/generate_tilesets.sh $SHOULD_BUILD $DATA_VERSION $DEPLOY_SHAPES $DEPLOY_POINTS $DEBUG
    fi

    # Deploy the data that was built.
    if [[ $SHOULD_DEPLOY -eq 1 ]]; then
      if [[ $DEBUG -eq 1 ]]; then
        echo "Deploying... "
        echo "Here's what's in ./source:"
        tree ./source
        echo "Here's what's in ./proc:"
        tree ./proc
        echo "Here's what's in ./geojson:"
        tree ./geojson
      fi
      # Remove geojson files before uploading.
      rm -rf ./proc/geojson/*
      # Deploy files into the appropriate version directory.
      aws s3 cp --recursive ./proc s3://ddk-source/proc/${DATA_VERSION}/ \
       --acl=public-read \
       --region=us-east-1 \
		   --cache-control max-age=2628000
    fi

    finishDate=`date +"%Y-%m-%d %T"`
    echo "Build run complete: ${finishDate}"
    execution_time=`date -u -d @$(($(date -d "${finishDate}" '+%s') - $(date -d "${startDate}" '+%s'))) '+%H:%M'`
    echo "Execution time: ${execution_time}"

fi
