# Tasks

## Initial

- Dockerfile: setup a docker environment containing the required build environment for data files and tilesets
- Source storage setup: setup a place (e.g. AWS bucket) to store the "source" files for the pipeline (e.g. tract geojson, data source files)
- Pepare source files:
  - GeoJSON for tracts
  - Data for tracts
  - Data for dot density layers
- Write script to generate tilesets
- Write script to deploy tilesets

## Future

- Add docker image to dockerhub
- Setup AWS Batch (or other container service) to automatically build on source changes
