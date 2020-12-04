# Tasks

## Initial

1. Dockerfile: setup a docker environment containing the required build environment for data files and tilesets. Build the local Dockerfile with: `docker build -t hyperobjekt/ddk-etl .`

2. Source storage setup: setup a place (e.g. AWS bucket) to store the "source" files for the pipeline (e.g. tract geojson, data source files)

3. Add source files to source bucket:

   - GeoJSON for tracts
   - Data for tracts
   - Data for dot density layers

4. Write makefile / scripts that:
   - download source data / geojson from source bucket (`wget` or `aws cp`)
   - join data into geojson files (see [tippecanoe-json-tool](https://github.com/mapbox/tippecanoe#tippecanoe-json-tool))
   - generate tilesets (`.mbtiles`) from geojson files with data (see [tippecanoe](https://github.com/mapbox/tippecanoe))
   - deploy generated tilesets to mapbox (see `deploy_tilesets` [make command](https://github.com/Hyperobjekt/seda-etl/blob/master/Makefile#L465) and [deploy script](https://github.com/Hyperobjekt/seda-etl/blob/master/scripts/deploy_tilesets.js))

the entire chain of scripts should be run from `./build.sh` so that running the dockerfile completes the entire build.

e.g. `docker run hyperobjekt/ddk-etl`

```
docker run --env-file .env hyperobjekt/ddk-etl
```

### Flags

- `--env-file` indicates the `.env` file to pass to Docker

## Future

- Add docker image to dockerhub
- Setup AWS Batch (or other container service) to automatically build on source changes

### Configuration

Configure the pipeline using the `.env` file: 

```
RAW_DATA_PATH=https://... # Path to source data files on github (or elsewhere avail to curl)
DATA_BUCKET=ddk-source # AWS bucket
AWS_ACCESS_ID=... # AWS Access ID
AWS_SECRET_KEY=... # AWS Secret Key
MAPBOX_USERNAME=... # Mapbox username
MAPBOX_TOKEN=... # Mapbox token
DATA_VERSION=1.0.0 # Data version (fetched from github repo tags when writing .env), use semantic versioning
DEBUG=1 # Boolean
DEPLOY=0 # Boolean, cp processed files to AWS S3 bucket, disable for faster testing.
CLEAN=1 # Clean up before starting. Use if you're testing scripts locally.
BUILD_GEOJSON=0 # Boolean. Build geojson from census data? Don't need to do this every time.
BUILD_TYPES=tracts,states # Comma-delineated string of shape types to download and process
BUILD_DICT=1 # Build dictionary files? 
BUILD_METRO_LIST=1 # Build list of featured metros? 
BAR_CHARTS=1 # Process bar charts data?
```
