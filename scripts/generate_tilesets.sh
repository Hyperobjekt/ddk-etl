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
max_zoom=13
# Attribution for tilesets
attribution="© diversitydatakids.org"


# Source dir
SOURCE_DIR="source"
# Processed data dir
OUTPUT_DIR="proc"

if [ ! -d "./mbtiles" ]
then
  mkdir -p "./mbtiles"
fi

ls -lah ./${OUTPUT_DIR}/geojson/

# Build tilesets for shapes.
# tracts
tippecanoe -Z 7 -z 14 -o "./mbtiles/tracts_${version}.mbtiles" -l ${shape} "./${OUTPUT_DIR}/geojson/tracts.geojson" --drop-densest-as-needed --use-attribute-for-id=GEOID --convert-stringified-ids-to-numbers --force
node ./scripts/deploy_tileset.js "./mbtiles/tracts_${version}.mbtiles" "tracts_${version}"
# states
tippecanoe -Z ${min_zoom} -z ${max_zoom} -o "./mbtiles/states_${version}.mbtiles" -l ${shape} "./${OUTPUT_DIR}/geojson/states.geojson" --simplification=8 --drop-densest-as-needed --use-attribute-for-id=GEOID --convert-stringified-ids-to-numbers --force
node ./scripts/deploy_tileset.js "./mbtiles/states_${version}.mbtiles" "states_${version}"
# metros
tippecanoe -Z 4 -z ${max_zoom} -o "./mbtiles/metros_${version}.mbtiles" -l ${shape} "./${OUTPUT_DIR}/geojson/metros.geojson" --drop-densest-as-needed --use-attribute-for-id=GEOID --convert-stringified-ids-to-numbers --force
node ./scripts/deploy_tileset.js "./mbtiles/metros_${version}.mbtiles" "metros_${version}"




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
tree ./mbtiles
# Deploy tileset.
# node ./scripts/deploy_tileset.js ./mbtiles/shapes_${version}.mbtiles "shapes_${version}"

# Build tilesets for points.
# for year in "${years[@]}"
# do
#   echo "Processing year ${year}."
#   year_list=""
#
#   for type in "${point_types[@]}"
#   do
#     echo "Generating tileset for for ${type}_${year}."
#     # -zg --drop-densest-as-needed --extend-zooms-if-still-dropping
#     tippecanoe --minimum-zoom=${min_zoom} --maximum-tile-bytes=500000 --generate-ids -zg --extend-zooms-if-still-dropping --no-feature-limit --drop-densest-as-needed --no-tile-stats --force -o ./mbtiles/points_${type}_${year}.mbtiles -l ${type} ./${OUTPUT_DIR}/geojson/points_${type}_${year}.geojson
#     year_list+="./mbtiles/points_${type}_${year}.mbtiles "
#   done
#
#   echo "year_list list: ${year_list}"
#   # Merge all files for that year together.
#   tile-join -o "./mbtiles/points_${year}_${version}.mbtiles" ${year_list} --force
#   # Deploy tileset for year.
#   node ./scripts/deploy_tileset.js "./mbtiles/points_${year}_${version}.mbtiles" "points_${year}_${version}"
#
# done
