import os
import sys
import json

from constants import *

# To test locally: python3 ./scripts/recipe_shapes.py username 1.0.0

mapboxUser = sys.argv[1]
version = sys.argv[2]

minZoom = MIN_ZOOM
maxZoom = MAX_ZOOM

# Function to build the shapes recipe.
# tracts,states,metros
def getShapesRecipe():
  r = {
    "version": 1,
    "layers": {
      "states": {
        "source": f"mapbox://tileset-source/{mapboxUser}/states_{version}",
        "minzoom": minZoom,
        "maxzoom": maxZoom,
        "features": {
          "id": [ "get", "GEOID" ]
        },
        "tiles": {

        }
      },
      "tracts": {
        "source": f"mapbox://tileset-source/{mapboxUser}/tracts_{version}",
        "minzoom": minZoom,
        "maxzoom": maxZoom,
        "features": {
          "id": [ "get", "GEOID" ]
        },
        "tiles": {

        }
      },
      "metros": {
        "source": f"mapbox://tileset-source/{mapboxUser}/metros_{version}",
        "minzoom": minZoom,
        "maxzoom": maxZoom,
        "features": {
          "id": [ "get", "GEOID" ]
        },
        "tiles": {

        }
      }
    }
  }
  print(json.dumps(r))

getShapesRecipe()
