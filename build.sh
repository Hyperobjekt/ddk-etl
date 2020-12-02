#!/bin/bash

# Fetch environment values.
# Should the data be deployed? 
SHOULD_DEPLOY=$(if [ "${DEPLOY}" -eq 1 ]; then echo 1; else echo 0; fi)
# Clean up? Boolean.
SHOULD_CLEAN=$(if [ "${CLEAN}" -eq 1 ]; then echo 1; else echo 0; fi)
# BUILD_TYPES options in .env should be a comma-delineated list.
# options are: tracts, states, counties, zips
# ex: BUILD_TYPES=tracts,states
SHOULD_BUILD=$(if [ ! -z "${BUILD_TYPES}" ]; then echo "${BUILD_TYPES}"; else echo "tracts"; fi)
# Whether or not to fetch and process bar chart data. Boolean.
SHOULD_BARCHART=$(if [ ! -z "${BAR_CHARTS}" ]; then echo "${BAR_CHARTS}"; else echo 1; fi)
# Build dictionaries list of strings. Boolean.
SHOULD_DICT=$(if [ ! -z "${BUILD_DICT}" ]; then echo "${BUILD_DICT}"; else echo 0; fi)
# Build metro list. Boolean.
SHOULD_METRO=$(if [ ! -z "${BUILD_METRO_LIST}" ]; then echo "${BUILD_METRO_LIST}"; else echo 0; fi)

# Print extra debug info?
DEBUG=$(if [ "${DEBUG}" -eq 1 ]; then echo 1; else echo 0; fi)

# Deploy the data that was built
if [[ $SHOULD_DEPLOY -eq 1 ]]; then

      echo 'Configuring S3.'
      if [[ -z "${AWS_ACCESS_ID}" ]]; then
          printf '%s\n' "Missing AWS_ACCESS_ID environment variable, could not configure AWS CLI." >&2
          exit 1
      fi
      if [[ -z "${AWS_SECRET_KEY}" ]]; then
          printf '%s\n' "Missing AWS_SECRET_KEY environment variable, could not configure AWS CLI." >&2
          exit 1
      fi
      aws configure set aws_access_key_id $AWS_ACCESS_ID
      aws configure set aws_secret_access_key $AWS_SECRET_KEY
      aws configure set default.region us-east-1
      # make deploy_s3
      # aws s3 cp --recursive ./proc s3://ddk-source/proc --acl=public-read; done

fi

# Fetch tract source data.
if [ ! -z $SHOULD_BUILD ]; then
    # Fetch source geojson.
    echo "Fetching source geojson."
    make -f ./scripts/fetch_geo.mk all deploy
  
    echo "Fetching tract source data."
    bash ./scripts/fetch_raw_data.sh ${RAW_DATA_PATH} $SHOULD_BUILD $SHOULD_BARCHART
    
    echo "Preparing source data."
    python3 ./scripts/process_shape_data.py $SHOULD_BUILD $SHOULD_METRO
    
    # If dictionary files need to be rebuild, do that too.
    if [ ! -z $SHOULD_DICT ]; then
      # Build dictionary string set.
      python3 ./scripts/build_dictionary.py $SHOULD_BUILD
    fi
    
    # Deploy the data that was built
    if [[ $SHOULD_DEPLOY -eq 1 ]]; then
      echo "Deploying... "
      echo "Here's what's in .source:"
      tree ./source
      echo "Here's what's in .proc:"
      tree ./proc
      echo "Here's what's in .geojson:"
      tree ./geojson
      aws s3 cp --recursive ./proc s3://ddk-source/proc --acl=public-read
    fi
fi

# clean existing build
if [[ $SHOULD_CLEAN -eq 1 ]]; then
    echo "Cleaning up..."
    # make clean
    rm -rf ./source
    rm -rf ./proc
fi
