#!/bin/bash
echo "./scripts/generate_tilesets.sh"

# To test locally:
# bash ./scripts/generate_tilesets.sh tracts,states,metros 1.0.0 1
# The size limit for mbtiles uploads is 25GB.

# Get types of shapes to fetch based on argument.
shape_types=(`echo $1 | tr ',' ' '`)
# Data version
version=$2
# Deploy shapes to mapbox?
deploy_shapes=$3
echo "deploy_shapes:"
echo ${deploy_shapes}
# years of tract shapes to build
shapes_years=(`echo $4 | tr ',' ' '`)
# Deploy points to mapbox?
deploy_points=$5
echo "deploy_points:"
echo ${deploy_points}
# Types of point years (for sources)
# years=( 10 15 )
points_year=$6
# Types of points (as sources)
# point_types=( ai ap b hi w )
point_types=(`echo $7 | tr ',' ' '`)
# Are we debugging?
debug=$8

# Max and min zoom
min_zoom=3
max_zoom=10 # Above 10 = increased processing and hosting costs.

# Source dir
SOURCE_DIR="source"
# Processed data dir
OUTPUT_DIR="proc"

ulimit -n 10000

if [ ! -d "./mbtiles" ]
then
  mkdir -p "./mbtiles"
fi

if [[ $DEBUG -eq 1 ]]; then
  ls -lah ./${OUTPUT_DIR}/geojson/
fi

if [[ $deploy_shapes -eq 1 ]]; then
  # Build tilesets for shapes.
  for year in "${shapes_years[@]}"
  do
    # tracts
    echo "Building tileset for tracts, year ${year}."
    tippecanoe -Z${min_zoom} -z${max_zoom} -l tracts -o "./mbtiles/tracts${year}_${version}.mbtiles" -x GEO_ID -x STATE -x COUNTY -x TRACT -x NAME -x LSAD -x CENSUSAREA --no-feature-limit --coalesce-densest-as-needed --use-attribute-for-id=GEOID --convert-stringified-ids-to-numbers --force "./${OUTPUT_DIR}/geojson/tracts${year}.geojson"
    # Deploy the tracts file.
    node ./scripts/deploy_tileset.js "./mbtiles/tracts${year}_${version}.mbtiles" "tracts${year}_${version}"
    # 2015
    # tippecanoe -Z${min_zoom} -z${max_zoom} -l tracts -o "./mbtiles/tracts_${version}.mbtiles" -x GEO_ID -x STATE -x COUNTY -x TRACT -x NAME -x LSAD -x CENSUSAREA --no-feature-limit --coalesce-densest-as-needed --use-attribute-for-id=GEOID --convert-stringified-ids-to-numbers --force "./${OUTPUT_DIR}/geojson/tracts.geojson"
    # # Deploy the tracts file.
    # node ./scripts/deploy_tileset.js "./mbtiles/tracts_${version}.mbtiles" "tracts_${version}"
  done
  # states
  echo "Building tileset for states."
  tippecanoe -Z${min_zoom} -z${max_zoom} -o "./mbtiles/states_${version}.mbtiles" -l states -x GEO_ID -x STATE -x NAME -x name -x LSAD -x CENSUSAREA --simplification=8 --drop-densest-as-needed --use-attribute-for-id=GEOID --convert-stringified-ids-to-numbers --force "./${OUTPUT_DIR}/geojson/states.geojson"
  # metros
  echo "Building tileset for metros."
  tippecanoe -Z${min_zoom} -z${max_zoom} -o "./mbtiles/metros_${version}.mbtiles" -l metros -x GEO_ID -x CENSUSAREA -x LSAD -x msaname15 -x NAME -x countyfips -x ALAND -x AWATER -x LSAD -x AFFGEOID -x CSAFP -x CBSAFP -x stateusps --drop-densest-as-needed --use-attribute-for-id=GEOID --convert-stringified-ids-to-numbers --force "./${OUTPUT_DIR}/geojson/metros.geojson"
  # Join tracts, states, and metros.
  # echo "Beginning join operation for tracts, states, and metros."
  # tile-join -pk -o ./mbtiles/shapes_${version}.mbtiles ./mbtiles/tracts_${version}.mbtiles ./mbtiles/states_${version}.mbtiles ./mbtiles/metros_${version}.mbtiles
  echo "Beginning join operation for states and metros."
  tile-join -pk -o ./mbtiles/shapes_${version}.mbtiles ./mbtiles/states_${version}.mbtiles ./mbtiles/metros_${version}.mbtiles
  # Deploy the combined file.
  node ./scripts/deploy_tileset.js "./mbtiles/shapes_${version}.mbtiles" "shapes_${version}"

  if [[ $DEBUG -eq 1 ]]; then
    tree ./mbtiles
    ls -lah ./mbtiles
  fi
fi

if [[ $deploy_points -eq 1 ]]; then
  # Build tilesets for points.
  echo "Processing points for year ${points_year}."

  for type in "${point_types[@]}"
  do
    echo "Generating tileset for for ${type}${points_year}."
    # Create tileset from points geojson file.
    tippecanoe -Z${min_zoom} -z${max_zoom} -o ./mbtiles/points_${type}${points_year}.mbtiles -l ${type} --generate-ids --no-feature-limit --drop-densest-as-needed --force ./${OUTPUT_DIR}/geojson/points_${type}${points_year}.geojson
    # Deploy tileset with version number.
    node ./scripts/deploy_tileset.js "./mbtiles/points_${type}${points_year}.mbtiles" "points_${type}${points_year}_${version}"
  done
fi

if [[ $DEBUG -eq 1 ]]; then
  tree ./mbtiles
  ls -lah ./mbtiles
fi
