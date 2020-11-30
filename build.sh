#!/bin/bash

########
# This script is a placeholder entry point for the dockerfile
# At some point, this script will run when the dockerfile is run
# and will handle running the tasks needed to fetch the source data
# perform any data shaping / tileset builds, and then deploy.
########

SHOULD_DEPLOY=$(if [ "${DEPLOY}" -eq 1 ]; then echo 1; else echo 0; fi)
SHOULD_CLEAN=$(if [ "${CLEAN}" -eq 1 ]; then echo 1; else echo 0; fi)
SHOULD_BUILD=$(if [ -z "${BUILD_TYPES}" ]; then echo "${BUILD_TYPES}"; else echo "tract"; fi)
DEBUG=$(if [ "${DEBUG}" -eq 1 ]; then echo 1; else echo 0; fi)

# clean existing build
if [[ $SHOULD_CLEAN -eq 1 ]]; then
    echo "Cleaning up..."
    make clean
fi

# Fetch tract source data.
if [ ! -z $SHOULD_BUILD ]; then
    echo "Fetching tract source data."
    # make -f ./scripts/fetch_raw_data.mk $SHOULD_BUILD
    bash ./scripts/fetch_raw_data.sh $SHOULD_BUILD
    # echo "Processing tract source data."
    # python3 ./scripts/process_source_data.py tract
fi

# Fetch state source data.
# if [[ $SHOULD_BUILD_STATES -eq 1 ]]; then
#     echo "Fetching state source data."
#     make -f ./scripts/fetch_raw_data.mk states
#     echo "Processing tract source data."
#     python3 ./scripts/process_source_data.py tract
# fi
# 
# # Fetch state county data.
# if [[ $SHOULD_BUILD_COUNTIES -eq 1 ]]; then
#     echo "Fetching county source data."
#     make -f ./scripts/fetch_raw_data.mk counties
# fi
# 
# # Fetch state county data.
# if [[ $SHOULD_BUILD_ZIPS -eq 1 ]]; then
#     echo "Fetching zip source data."
#     make -f ./scripts/fetch_raw_data.mk zips
# fi

# echo "Fetching tract source data."
# make -f ./scripts/fetch_raw_data.mk download

# Fetch tract source data.
# if [[ $SHOULD_BUILD_TRACTS -eq 1 ]]; then
    # echo "Processing tract source data."
    # python3 ./scripts/process_source_data.py tract
# fi
# 
# # Fetch state source data.
# if [[ $SHOULD_BUILD_STATES -eq 1 ]]; then
#     echo "Processing state source data."
#     python3 ./scripts/process_source_data.py states
# fi
# 
# # Fetch state county data.
# if [[ $SHOULD_BUILD_COUNTIES -eq 1 ]]; then
#     echo "Processing county source data."
#     python3 ./scripts/process_source_data.py counties
# fi
# 
# # Fetch state county data.
# if [[ $SHOULD_BUILD_ZIPS -eq 1 ]]; then
#     echo "Processing zip source data."
#     python3 ./scripts/process_source_data.py zips
# fi

# echo "Processing source data."
# python3 ./scripts/process_source_data.py

# Deploy the data that was built
if [[ $SHOULD_DEPLOY -eq 1 ]]; then

      # echo 'aws version = '
      # aws --version
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

fi







echo "Fetching source geojson."

# make -f ./scripts/fetch_geo.mk all deploy
