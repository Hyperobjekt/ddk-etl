#!/bin/bash

########
# This script is a placeholder entry point for the dockerfile
# At some point, this script will run when the dockerfile is run
# and will handle running the tasks needed to fetch the source data
# perform any data shaping / tileset builds, and then deploy.
########

echo "fetching source geojson"

make -f fetch_geo.mk all

