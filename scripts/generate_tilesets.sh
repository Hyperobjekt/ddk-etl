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

# Build tilesets for shapes.
shapes_list=""
for shape in "${shape_types[@]}"
do

  echo "Generating tileset for ${shape}."
  tippecanoe --maximum-zoom=${max_zoom} --minimum-zoom=${min_zoom} --maximum-tile-bytes=500000 --simplification=10 --no-tile-stats --no-feature-limit --coalesce-densest-as-needed --detect-shared-borders --use-attribute-for-id=GEOID --force -aI -o "./mbtiles/${shape}.mbtiles" -l ${shape} "./${OUTPUT_DIR}/geojson/${shape}.geojson"
  shapes_list+="./mbtiles/${shape}.mbtiles "

done

# echo "Shapes list: ${shapes_list}"
# Merge all those tilesets.
tile-join -o "./mbtiles/shapes_${version}.mbtiles" ${shapes_list} --force
# Deploy tileset.
nodejs ./scripts/deploy_tileset.js ./mbtiles/shapes_${version}.mbtiles "shapes_${version}"

# Build tilesets for points.
for year in "${years[@]}"
do
  echo "Processing year ${year}."
  year_list=""

  for type in "${point_types[@]}"
  do
    echo "Generating tileset for for ${type}_${year}."
    # -zg --drop-densest-as-needed --extend-zooms-if-still-dropping
    tippecanoe --minimum-zoom=${min_zoom} --maximum-tile-bytes=500000 --generate-ids -zg --extend-zooms-if-still-dropping --no-feature-limit --drop-densest-as-needed --no-tile-stats --force -o ./mbtiles/points_${type}_${year}.mbtiles -l ${type} ${OUTPUT_DIR}/geojson/points_${type}_${year}.geojson
    year_list+="./mbtiles/points_${type}_${year}.mbtiles "
  done

  echo "year_list list: ${year_list}"
  # Merge all files for that year together.
  tile-join -o "./mbtiles/points_${year}_${version}.mbtiles" ${year_list} --force
  # Deploy tileset for year.
  nodejs ./scripts/deploy_tileset.js "./mbtiles/points_${year}_${version}.mbtiles" "points_${year}_${version}"

done
