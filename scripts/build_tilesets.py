import os
import sys
import json

from constants import *

# For local testing:
# python3 ./scripts/build_tilesets.py tracts,states,metros 1

shapetypes = sys.argv[1].split(',') # Shape types to process: `tracts`, `counties`, `states`, or `zips`.
print("shapetype array = ", shapetypes)

pointtypes = POINT_TYPES
print("pointtypes array = ", pointtypes)

years = YEARS

mapboxUser = sys.argv[2]
mapboxToken = sys.argv[3]

version = sys.argv[4]

minZoom = MIN_ZOOM
maxZoom = MAX_ZOOM


# Upload the source for each shape.
for shape in shapetypes:
  tilesets upload-source --replace mapboxUser f'{shape}_{version}'  f'{OUTPUT_DIR}/geojson/{shape}.geojson'

# Upload the source for each point type.
for points in pointtypes:
  for year in years:
    yr = str(year)
    tilesets upload-source --replace mapboxUser f'{points}_{version}' f'{OUTPUT_DIR}/geojson/points_{points}_{yr}.geojson'

# Create tileset for shapes.
separator = ', '
shapeList = separator.join(shapetypes)
tilesets create f'{mapboxUser}.shapes-{version}' --recipe getShapesRecipe() --name f"Tileset for shapes {shapeList}, version {version}."

for year in years:
  tilesets create f'{mapboxUser}.points-{year}-{version}' --recipe getShapesRecipe() --name f"Tileset for points year {str(year)}, version {version}."

# Publish tileset for shapes
tilesets publish f'{mapboxUser}.shapes-{version}'
for year in years:
  tilesets publish f'{mapboxUser}.points-{year}-{version}'
