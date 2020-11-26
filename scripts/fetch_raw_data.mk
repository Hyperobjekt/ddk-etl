# Makefile for creating Census geography data for 2010 from source rather than S3

csv_types = index raw pop zscores 

DOWNLOADED_FILES = $(foreach t, $(csv_types), csvs/$(t).csv)

.PHONY: download help

## all                 : Create all census GeoJSON
download: $(DOWNLOADED_FILES)

# Based on https://swcarpentry.github.io/make-novice/08-self-doc/
## help                : Print help
help: census.mk
	perl -ne '/^## / && s/^## //g && print' $<

## geojson/%.geojson   : Download and clean census GeoJSON
.SECONDARY:
csvs/%.csv:
	mkdir -p csvs && cd csvs && curl $(RAW_DATA_PATH)/$*/$*.csv -o $*.csv && ls
	echo '-----> Done downloading csvs. <-----'
