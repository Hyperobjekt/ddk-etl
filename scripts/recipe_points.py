import os
import sys
import json

from constants import *

# To test locally: python3 ./scripts/recipe_points.py username 1.0.0 15

mapboxUser = sys.argv[1]
version = sys.argv[2]
year = sys.argv[3]

minZoom = MIN_ZOOM
maxZoom = MAX_ZOOM

def getPointsRecipe():
  r = {
    "version": 1,
    "layers": {
      "ai": {
        "source": f"mapbox://tileset-source/{mapboxUser}/ai_{version}",
        "minzoom": minZoom,
        "maxzoom": maxZoom,
        "features": {
          "id": ["concat", ['get', 'type'], '_', ["string", ["random"]]]
        },
      },
      "ap": {
        "source": f"mapbox://tileset-source/{mapboxUser}/ap_{version}",
        "minzoom": minZoom,
        "maxzoom": maxZoom,
        "features": {
          "id": ["concat", ['get', 'type'], '_', ["string", ["random"]]]
        },
      },
      "b": {
        "source": f"mapbox://tileset-source/{mapboxUser}/b_{version}",
        "minzoom": minZoom,
        "maxzoom": maxZoom,
        "features": {
          "id": ["concat", ['get', 'type'], '_', ["string", ["random"]]]
        },
      },
      "hi": {
        "source": f"mapbox://tileset-source/{mapboxUser}/hi_{version}",
        "minzoom": minZoom,
        "maxzoom": maxZoom,
        "features": {
          "id": ["concat", ['get', 'type'], '_', ["string", ["random"]]]
        },
      },
      "w": {
        "source": f"mapbox://tileset-source/{mapboxUser}/w_{version}",
        "minzoom": minZoom,
        "maxzoom": maxZoom,
        "features": {
          "id": ["concat", ['get', 'type'], '_', ["string", ["random"]]]
        },
      }
    }
  }
  print(json.dumps(r))

getPointsRecipe()
