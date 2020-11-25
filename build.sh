#!/bin/bash

########
# This script is a placeholder entry point for the dockerfile
# At some point, this script will run when the dockerfile is run
# and will handle running the tasks needed to fetch the source data
# perform any data shaping / tileset builds, and then deploy.
########

SHOULD_DEPLOY=1
SHOULD_CLEAN=1
SHOULD_BUILD_TRACTS=1
SHOULD_BUILD_STATES=0
SHOULD_BUILD_COUNTIES=0
SHOULD_BUILD_ZIPS=0

# Loop through arguments and process them
for arg in "$@"
do
    case $arg in
        -v=*|--version=*)
        DATA_VERSION="${arg#*=}"
        shift # Remove --file= from processing
        ;;
        --no-clean)
        SHOULD_CLEAN=0
        shift # Remove --no-clean from processing
        ;;
        --no-deploy)
        SHOULD_DEPLOY=0
        shift # Remove --no-deploy from processing
        ;;
        --build-tracts)
        SHOULD_BUILD_TRACTS=1
        shift # Remove --build-tracts from processing
        ;;
        --build-states)
        SHOULD_BUILD_STATES=1
        shift # Remove --tiles from processing
        ;;
        --build-counties)
        SHOULD_BUILD_COUNTIES=1
        shift # Remove --tiles from processing
        ;;
        --build-zips)
        SHOULD_BUILD_ZIPS=1
        shift # Remove --tiles from processing
        ;;
        --prepare-only)
        PREPARE_ONLY=1
        shift # Remove --prepare-only from processing
        ;;
        -f=*|--file=*)
        SOURCE_FILE="${arg#*=}"
        shift # Remove --file= from processing
        ;;
        *)
        OTHER_ARGUMENTS+=("$1")
        shift # Remove generic argument from processing
        ;;
    esac
done

# clean existing build
if [[ $SHOULD_CLEAN -eq 1 ]]; then
    echo "Cleaning up..."
    make clean
fi

# Deploy the data that was built
if [[ $SHOULD_DEPLOY -eq 1 ]]; then

      echo 'aws version = '
      aws --version
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
      make deploy_s3

fi

echo "fetching source geojson"

# make -f ./scripts/fetch_geo.mk all deploy
