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
SHOULD_BARCHART=$(if [ "${BAR_CHARTS}" -eq 1 ]; then echo 1; else echo 0; fi)
# Build metro list. Boolean.
SHOULD_METRO=$(if [ "${BUILD_METRO_LIST}" -eq 1 ]; then echo 1; else echo 0; fi)
# Mapbox username and token for building tilesets.
MAPBOX_USER=$(if [ ! -z "${MAPBOX_USERNAME}" ]; then echo "${MAPBOX_USERNAME}"; else echo ""; fi)
MAPBOX_TKN=$(if [ ! -z "${MAPBOX_TOKEN}" ]; then echo "${MAPBOX_TOKEN}"; else echo ""; fi)
# Data version
DATA_VERSION=$(if [ ! -z "${DATA_VERSION}" ]; then echo "${DATA_VERSION}"; else echo 1.0.0; fi)
# Should the script upload mapbox shapes?
DEPLOY_SHAPES=$(if [ "${UPLOAD_MAPBOX_SHAPES}" -eq 1 ]; then echo 1; else echo 0; fi)
# What years of tract shapes to build
SHAPES_YEARS=$(if [ ! -z "${SHAPES_YEARS}" ]; then echo "${SHAPES_YEARS}"; else echo "10,15"; fi)
# Should the script upload mapbox points?
DEPLOY_POINTS=$(if [ "${UPLOAD_MAPBOX_POINTS}" -eq 1 ]; then echo 1; else echo 0; fi)
# Get the year of mapbox points to generate (for splitting jobs up).
POINTS_YEAR=$(if [ ! -z "${MAPBOX_POINTS_YEAR}" ]; then echo "${MAPBOX_POINTS_YEAR}"; else echo "10"; fi)
# Demographics to loop through when generating point features.
POINTS_DEMOGRAPHICS=$(if [ ! -z "${MAPBOX_POINTS_DEMOGRAPHICS}" ]; then echo "${MAPBOX_POINTS_DEMOGRAPHICS}"; else echo "ai,ap,b,hi,w"; fi)
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
    if [ $SHOULD_GEOJSON -eq 1 ]; then
      echo "Fetching source geojson."
      # If deploy, upload files.
      make -f ./scripts/fetch_geo.mk all deploy
      echo "Fetching metros geojson."
      # If deploy, upload files.
      bash -f ./scripts/fetch_metros_geo.sh $DEBUG
    fi

    echo "Downloading processed geojson."
    # No deploy, just download, unzip, and make geojson.
    bash ./scripts/fetch_proc_geojson.sh $SHOULD_BUILD $DEBUG

    echo "Fetching raw data."
    bash ./scripts/fetch_raw_data.sh $RAW_DATA_PATH $DATA_VERSION $DEBUG
    tree ./source

    echo "Preparing source data."
    # TODO: Add $SHAPES_YEARS to args here and make tract year
    # point generation dynamic.
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
    bash ./scripts/join_geojson.sh $SHOULD_BUILD $SHAPES_YEARS $DEBUG

    if [[ $DEPLOY_POINTS -eq 1 ]]; then
      # Generate points for population data.
      node ./scripts/generate_points.js $POINTS_YEAR $POINTS_DEMOGRAPHICS
    fi

    # Build tilesets.
    if [[ -z "${MAPBOX_TKN}" ]] || [[ -z "${MAPBOX_USER}" ]]; then
      echo "Mapbox token or Mapbox username not provided. You need to get that into the .env file  before you can build the tilesets."
    else
      # Generate tilesets.
      # TODO: UPDATE THIS SCRIPT TO ONLY PROCESS ONE YEAR AND THE LIST OF DEMOGRAPHICS.
      bash ./scripts/generate_tilesets.sh $SHOULD_BUILD $DATA_VERSION $DEPLOY_SHAPES $SHAPES_YEARS $DEPLOY_POINTS $POINTS_YEAR $POINTS_DEMOGRAPHICS $DEBUG
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
      # Copy files that need to be gzipped to a new dir and gzip them.
      csv_files=( pop raw )
      csv_years=(`echo $SHAPES_YEARS | tr ',' ' '`)
      mkdir gzip
      cp ./proc/helpers/en_US.json gzip
      cp ./proc/metros.json gzip
      cp ./proc/barcharts/barcharts.json gzip
      cp ./proc/helpers/indicators.json gzip
      for file in "${csv_files[@]}"
      do
        for year in "${csv_years[@]}"
        do
          cp "./proc/${file}${year}.csv" gzip
        done
      done
      echo 'Copied files to uploads dir.'
      ls -la gzip
      gzip -r gzip
      tree gzip
      aws s3 cp --recursive ./gzip s3://ddk-source/proc/${DATA_VERSION}/gzip/ \
       --acl=public-read \
       --content-encoding=gzip \
       --region=us-east-1 \
		   --cache-control max-age=2628000
      # aws s3 cp ./tilesets s3://$(S3_TILESETS_BUCKET)/$(BUILD_ID) --recursive --acl=public-read --content-encoding=gzip --region=us-east-2 --cache-control max-age=2628000
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
