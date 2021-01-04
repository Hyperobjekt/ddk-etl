#!/bin/bash
echo 'build_tilesets.sh'

# To test locally:
# bash ./scripts/build_tilesets.sh tracts,states,metros $MAPBOX_USER $MAPBOX_TOKEN 1.0.0 1

# Get types of shapes to fetch based on argument.
shape_types=(`echo $1 | tr ',' ' '`)
# Mapbox user
user=$2
echo "User is ${user}."
# Mapbox token
token=$3
# Data version
version=$4
# Are we debugging?
debug=$5

# Types of points (as sources)
point_types=( ai ap b hi w )
# Types of point years (for sources)
years=( 10 15 )

# Build tilesets for shapes.
for shape in "${shape_types[@]}"
do
  echo "Uploading source for ${shape}."
  tilesets upload-source "${user}" "${shape}_${version}"  "${OUTPUT_DIR}/geojson/${shape}.geojson" --token ${token} --replace
done

# Build tilesets for points.
for points in "${point_types[@]}"
do
  for year in "${years[@]}"
  do
    echo "Uploading source for ${points}_${years}."
    tilesets upload-source  "${user}" "${points}_${version}" "${OUTPUT_DIR}/geojson/points_${points}_${yr}.geojson" --replace --token ${token}
  done
done

# Create tileset for shapes.
shapeList=$(join , ${shape_types[@]})
shapes_recipe=$(python ./recipe_shapes.py ${user} ${version})
echo 'shapes_recipe:'
echo shapes_recipe
tilesets create "${user}.shapes-${version}" --recipe ${shapes_recipe} --name "Tileset for shapes ${shapeList}, version ${version}." --token ${token}

for year in "${years[@]}"
do
  points_recipe=$(python ./recipe_points.py ${user} ${version} ${year})
  echo 'points_recipe:'
  echo points_recipe
  tilesets create "${user}.points-${year}-${version}" --recipe ${points_recipe} --name "Tileset for points year ${year}, version ${version}." --token ${token}
done

# Publish tilesets.
echo "Publishing tilesets."
tilesets publish "${user}.shapes-${version}" --token ${token}
for year in "${years[@]}"
do
  tilesets publish "${user}.points-${year}-${version}" --token ${token}
done
