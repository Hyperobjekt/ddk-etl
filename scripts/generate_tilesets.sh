#!/bin/bash
echo "./scripts/generate_tilesets.sh"

# To test locally:
# bash ./scripts/generate_tilesets.sh tracts,states,metros 1.0.0 1
# The size limit for mbtiles uploads is 25GB.

# Get types of shapes to fetch based on argument.
shape_types=(`echo $1 | tr ',' ' '`)
# Data version
version=$2
# Are we debugging?
debug=$3

# Types of points (as sources)
point_types=( ai ap b hi w )
# Types of point years (for sources)
years=( 10 15 )
# Max and min zoom
min_zoom=3
max_zoom=14
# Attribution for tilesets
attribution="© diversitydatakids.org"


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

# Build tilesets for shapes.
# tracts
echo "Building tileset for tracts."
tippecanoe -Z7 -z${max_zoom} -l tracts -o "./mbtiles/tracts_${version}.mbtiles" -x GEO_ID -x STATE -x COUNTY -x TRACT -x NAME -x LSAD -x CENSUSAREA --no-feature-limit --drop-densest-as-needed --coalesce-densest-as-needed --use-attribute-for-id=GEOID --convert-stringified-ids-to-numbers --force "./${OUTPUT_DIR}/geojson/tracts.geojson"
node ./scripts/deploy_tileset.js "./mbtiles/tracts_${version}.mbtiles" "tracts_${version}"
# states
echo "Building tileset for states."
tippecanoe -Z${min_zoom} -z${max_zoom} -o "./mbtiles/states_${version}.mbtiles" -l states -x GEO_ID -x STATE -x NAME -x name -x LSAD -x CENSUSAREA --simplification=8 --drop-densest-as-needed --use-attribute-for-id=GEOID --convert-stringified-ids-to-numbers --force "./${OUTPUT_DIR}/geojson/states.geojson"
node ./scripts/deploy_tileset.js "./mbtiles/states_${version}.mbtiles" "states_${version}"
# metros
echo "Building tileset for metros."
tippecanoe -Z4 -z${max_zoom} -o "./mbtiles/metros_${version}.mbtiles" -l metros -x GEO_ID -x CENSUSAREA -x LSAD -x msaname15 -x NAME --drop-densest-as-needed --use-attribute-for-id=GEOID --convert-stringified-ids-to-numbers --force "./${OUTPUT_DIR}/geojson/metros.geojson"
node ./scripts/deploy_tileset.js "./mbtiles/metros_${version}.mbtiles" "metros_${version}"

tile-join -pk -o ./mbtiles/shapes_${version}.mbtiles ./mbtiles/tracts_${version}.mbtiles ./mbtiles/states_${version}.mbtiles ./mbtiles/metros_${version}.mbtiles
node ./scripts/deploy_tileset.js "./mbtiles/shapes_${version}.mbtiles" "shapes_${version}"

if [[ $DEBUG -eq 1 ]]; then
  tree ./mbtiles
  ls -lah ./mbtiles
fi


# shapes_list=""
# for shape in "${shape_types[@]}"
# do
#   echo "Generating tileset for ${shape}."
#   # -Z 2 -z 7
#   tippecanoe -Z ${min_zoom} -z ${max_zoom} -x GEO_ID -x STATE -x COUNTY -x TRACT -x NAME -x LSAD -x CENSUSAREA -o "./mbtiles/${shape}_${version}.mbtiles" -l ${shape} "./${OUTPUT_DIR}/geojson/${shape}.geojson" --simplification=8 --coalesce-densest-as-needed --use-attribute-for-id=GEOID --convert-stringified-ids-to-numbers --force
#   node ./scripts/deploy_tileset.js "./mbtiles/${shape}_${version}.mbtiles" "${shape}_${version}"
#   # shapes_list+="./mbtiles/${shape}.mbtiles "
# done

# echo "Shapes list: ${shapes_list}"
# Merge all those tilesets.
# tile-join -o -pk "./mbtiles/shapes_${version}.mbtiles" ${shapes_list} --force


# Build tilesets for points.
for year in "${years[@]}"
do
  echo "Processing year ${year}."
  year_list=""

  for type in "${point_types[@]}"
  do
    echo "Generating tileset for for ${type}_${year}."
    tippecanoe -Z${min_zoom} -z${max_zoom} -o ./mbtiles/points_${type}_${year}.mbtiles -l ${type} --generate-ids --no-feature-limit --extend-zooms-if-still-dropping --drop-densest-as-needed --force ./${OUTPUT_DIR}/geojson/points_${type}_${year}.geojson
    if [[ $type -ne 'w' ]]
    then
      echo "Adding tileset points_${type}_${year} to year_list."
      year_list+="./mbtiles/points_${type}_${year}.mbtiles "
    fi
  done

  # echo "year_list list: ${year_list}"
  # Merge all files for that year together.
  tile-join -pk -o "./mbtiles/points_${year}_${version}.mbtiles" --force ${year_list}
  # Deploy tileset for year.
  node ./scripts/deploy_tileset.js "./mbtiles/points_${year}_${version}.mbtiles" "points_${year}_${version}"
  # Deploy the white people all by themselves.
  node ./scripts/deploy_tileset.js "./mbtiles/points_w_${year}.mbtiles" "points_${year}_${version}"

done

if [[ $DEBUG -eq 1 ]]; then
  tree ./mbtiles
  ls -lah ./mbtiles
fi
