# DiversityDataKids Map App Data Processing Pipeline

The Docker image built from this repository processes data for consumption by the DiversityDataKids map app.

## What does it do?

1. Optionally fetches and processes shapefiles from census.gov
2. Processes a series of CSVs into:
  - CSVs
  - JSON
  - GeoJSON
3. Merges processed data into GeoJSON feature collections
4. Converts GeoJSON to Mapbox tilesets
5. Generates point density data, in the form of GeoJSON point feature collections, for indicated demographics
6. Converts point feature GeoJSON to Mapbox tilesets
7. Uploads Mapbox tilesets to Mapbox
8. Uploads remaining CSV and JSON files to AWS bucket

## When does it run?

Full and partial Github Action runs of this Docker image are triggered from [the DiversityDataKids data repository](https://github.com/Hyperobjekt/ddk-data). Full runs (data files and tilesets) are triggered by pushing a new tag to that repository. Partial runs (data files only) are triggered by pushing a new commit to branch `build-data-only`.

The entire chain of scripts runs from entrypoint `./build.sh`, as indicated in the `Dockerfile`.

## Contributing

Builds of the docker image are triggered by commits to branch `trigger-build`.

1. Check out your working branch off of `master`.
2. Build and run the docker image locally for testing. # :fire::fire: Before testing, check [the DiversityDataKids data repository](https://github.com/Hyperobjekt/ddk-data) tags and be sure you aren't setting a data version in your `.env` file that would override files that are in use! :fire::fire:
3. When you are ready to build the new image, merge your work back into `master`, then merge `master` into `trigger-build`. Push `trigger-build` to `origin` and watch the build progress in DockerHub.

### Useful Docker Commands

```bash
# Build
docker build -t hyperobjekt/ddk-etl .
# Run
docker run --env-file .env hyperobjekt/ddk-etl
# List containers
docker container list
# Prune images
docker image prune -a
# Clean up even more stuff
docker system prune
# REmove all stopped containers
docker container prune
# List containers
docker ps -a
# Write logs to a more accessible file
docker logs [containername] > ~/Desktop/docker-logs.log
```

### Flags

- `--env-file` indicates the `.env` file to pass to Docker

### Configuration

Configure the pipeline using the `.env` file:

```
RAW_DATA_PATH=https://... # Path to source data files on github (or elsewhere avail to curl)
DATA_BUCKET=ddk-source # AWS bucket
AWS_ACCESS_ID=... # AWS Access ID
AWS_SECRET_KEY=... # AWS Secret Key
MAPBOX_USERNAME=... # Mapbox username
MAPBOX_TOKEN=... # Mapbox token
DATA_VERSION=1.0.0 # Data version (fetched from github repo tags when writing .env), use semantic versioning.
DEPLOY=0 # Boolean, cp processed files to AWS S3 bucket, disable for faster testing.
CLEAN=1 # Clean up before starting. Use if you're testing scripts locally.
BUILD_GEOJSON=0 # Boolean. Build geojson from census data? Don't need to do this every time.
BUILD_TYPES=tracts,states # Comma-delineated string of shape types to download and process
BUILD_DICT=1 # Build dictionary files?
BUILD_METRO_LIST=1 # Build list of featured metros?
BAR_CHARTS=1 # Process bar charts data?
UPLOAD_MAPBOX_SHAPES=1 # Disable (0) to reduce use of upload API
SHAPES_YEARS=10,15 # What years to build tract tilesets for
UPLOAD_MAPBOX_POINTS=1 # Disable (0) to reduce use of upload API
MAPBOX_POINTS_YEAR=10 # Year of points to generate, for splitting into several jobs.
MAPBOX_POINTS_DEMOGRAPHICS=ai,ap,b,hi,w # Which demographics to use for point generation.
DEBUG=1 # Boolean, display additional debugging info
```
