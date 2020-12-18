# Makefile for creating Census geography data for 2010 from source rather than S3
census_ftp_base = ftp://ftp2.census.gov/geo/tiger/GENZ2010/

block-groups-pattern = gz_*_*_150_*_500k.zip
tracts-pattern = gz_*_*_140_*_500k.zip
cities-pattern = gz_*_*_160_*_500k.zip
counties-pattern = gz_*_*_050_*_500k.zip
states-pattern = gz_*_*_040_*_500k.zip
metros-pattern = gz_*_*_310_*_500k.zip

block-groups-geoid = "this.properties.GEOID = this.properties.STATE + this.properties.COUNTY + this.properties.TRACT + this.properties.BLKGRP"
tracts-geoid = "this.properties.GEOID = this.properties.STATE + this.properties.COUNTY + this.properties.TRACT"
cities-geoid = "this.properties.GEOID = this.properties.STATE + this.properties.PLACE"
counties-geoid = "this.properties.GEOID = this.properties.STATE + this.properties.COUNTY"
states-geoid =  "this.properties.GEOID = this.properties.STATE"
metros-geoid =  "this.properties.GEOID = this.properties.CBSA"

geo_types = tracts states metros
GENERATED_FILES = $(foreach t, $(geo_types), geojson/$(t).geojson)

.PHONY: all deploy help

## all                 : Create all census GeoJSON
all: $(GENERATED_FILES)

# Based on https://swcarpentry.github.io/make-novice/08-self-doc/
## help                : Print help
help: census.mk
	perl -ne '/^## / && s/^## //g && print' $<

## deploy              : Deploy gzipped census data to S3
deploy:
	cd geojson && ls
	cd ..
	echo 'Gzipping geojson.'
	for f in geojson/*.geojson; do gzip $$f; done
	echo 'Uploading gzips.'
	for f in geojson/*.gz; do aws s3 cp $$f s3://ddk-source/geojson/$$(basename $$f) --acl=public-read; done

## geojson/%.geojson   : Download and clean census GeoJSON
.SECONDARY:
geojson/%.geojson:
	mkdir -p geojson/$*
	wget --no-use-server-timestamps -np -nd -r -P geojson/$* -A '$($*-pattern)' $(census_ftp_base)
	for f in ./geojson/$*/*.zip; do unzip -d ./geojson/$* $$f; done
	mapshaper ./geojson/$*/*.shp combine-files \
		-each $($*-geoid) \
		-filter "!this.properties.GEOID.startsWith('72')" \
		-o $@ combine-layers format=geojson
	echo 'Done writing geojson.'
