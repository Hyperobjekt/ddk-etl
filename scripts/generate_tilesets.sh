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
# Deploy points to mapbox?
deploy_points=$4
# Are we debugging?
debug=$5

# Types of points (as sources)
point_types=( ai ap b hi w )

# Types of point years (for sources)
years=( 10 15 )

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
  # tracts
  echo "Building tileset for tracts."
  tippecanoe -Z7 -z${max_zoom} -l tracts -o "./mbtiles/tracts_${version}.mbtiles" -x GEO_ID -x STATE -x COUNTY -x TRACT -x NAME -x LSAD -x CENSUSAREA --no-feature-limit --drop-densest-as-needed --coalesce-densest-as-needed --use-attribute-for-id=GEOID --convert-stringified-ids-to-numbers --force "./${OUTPUT_DIR}/geojson/tracts.geojson"
  # states
  echo "Building tileset for states."
  tippecanoe -Z${min_zoom} -z${max_zoom} -o "./mbtiles/states_${version}.mbtiles" -l states -x GEO_ID -x STATE -x NAME -x name -x LSAD -x CENSUSAREA --simplification=8 --drop-densest-as-needed --use-attribute-for-id=GEOID --convert-stringified-ids-to-numbers --force "./${OUTPUT_DIR}/geojson/states.geojson"
  # metros
  echo "Building tileset for metros."
  tippecanoe -Z4 -z${max_zoom} -o "./mbtiles/metros_${version}.mbtiles" -l metros -x GEO_ID -x CENSUSAREA -x LSAD -x msaname15 -x NAME --drop-densest-as-needed --use-attribute-for-id=GEOID --convert-stringified-ids-to-numbers --force "./${OUTPUT_DIR}/geojson/metros.geojson"
  # Join tracts, states, and metros.
  echo "Beginning join operation for tracts, states, and metros."
  tile-join -pk -o ./mbtiles/shapes_${version}.mbtiles ./mbtiles/tracts_${version}.mbtiles ./mbtiles/states_${version}.mbtiles ./mbtiles/metros_${version}.mbtiles
  # Deploy the combined file.
  node ./scripts/deploy_tileset.js "./mbtiles/shapes_${version}.mbtiles" "shapes_${version}"

  if [[ $DEBUG -eq 1 ]]; then
    tree ./mbtiles
    ls -lah ./mbtiles
  fi
fi

if [[ $deploy_points -eq 1 ]]; then
  # Build tilesets for points.
  for year in "${years[@]}"
  do
    echo "Processing year ${year}."
    year_list=""

    for type in "${point_types[@]}"
    do
      echo "Generating tileset for for ${type}${year}."
      tippecanoe -Z${min_zoom} -z${max_zoom} -o ./mbtiles/points_${type}${year}.mbtiles -l ${type} --generate-ids --no-feature-limit --drop-densest-as-needed --force ./${OUTPUT_DIR}/geojson/points_${type}${year}.geojson
      # Create a list of all files to join (exclude white people).
      if [[ $type != 'w' ]]
      then
        echo "Adding tileset points_${type}${year} to year_list."
        year_list+="./mbtiles/points_${type}${year}.mbtiles "
      fi
    done

    echo "Attempting to join the following tiles: ${year_list}."
    # Merge all files for that year together.
    tile-join -pk -o ./mbtiles/points_${year}_${version}.mbtiles ${year_list}
    # Deploy tileset for year, everyone but white people.
    node ./scripts/deploy_tileset.js "./mbtiles/points_${year}_${version}.mbtiles" "points_${year}_${version}"
    # Deploy the white people all by themselves.
    node ./scripts/deploy_tileset.js "./mbtiles/points_w${year}.mbtiles" "points_w${year}_${version}"

  done
fi

if [[ $DEBUG -eq 1 ]]; then
  tree ./mbtiles
  ls -lah ./mbtiles
fi
