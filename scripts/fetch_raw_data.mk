# Makefile for creating Census geography data for 2010 from source rather than S3
csv_types = index raw pop zscores 

DOWNLOADED_FILES = $(foreach t, $(csv_types), source_csvs/$(t).csv)
DOWNLOADED_TRACT_FILES = $(foreach t, $(csv_types), source/tract/$(t).csv)
DOWNLOADED_STATE_FILES = $(foreach t, $(csv_types), source/state/$(t).csv)
DOWNLOADED_COUNTY_FILES = $(foreach t, $(csv_types), source/county/$(t).csv)
DOWNLOADED_ZIP_FILES = $(foreach t, $(csv_types), source/zip/$(t).csv)

.PHONY: download tracts help

## all                 : Create all census GeoJSON
download: $(DOWNLOADED_FILES)

## tracts                 : Download tract files from client data repo.
tract: $(DOWNLOADED_TRACT_FILES)

state: $(DOWNLOADED_STATE_FILES)
county: $(DOWNLOADED_COUNTY_FILES)
zip: $(DOWNLOADED_ZIP_FILES)

# Based on https://swcarpentry.github.io/make-novice/08-self-doc/
## help                : Print help
help: census.mk
	perl -ne '/^## / && s/^## //g && print' $<

## source_csvs/%.csv   : Download the client data files.
.SECONDARY:
source_csvs/%.csv:
	mkdir -p source_csvs && cd source_csvs && curl $(RAW_DATA_PATH)$*/$*.csv -o $*.csv && ls && head --lines=5 $*.csv
	$(info Downloaded $*.csv)
	
/source/tract/%.csv:
	mkdir -p source && cd source && mkdir tract && cd tract && curl $(RAW_DATA_PATH)/tract/$*/$*.csv -o $*.csv && ls && head --lines=5 $*.csv
	$(info Downloaded tract file $*.csv)
	
/source/state/%.csv:
	mkdir -p source && cd source && mkdir state && cd state && curl $(RAW_DATA_PATH)/state/$*/$*.csv -o $*.csv && ls && head --lines=5 $*.csv
	$(info Downloaded state file $*.csv)
	
/source/county/%.csv:
	mkdir -p source && cd source && mkdir county && cd county && curl $(RAW_DATA_PATH)/county/$*/$*.csv -o $*.csv && ls && head --lines=5 $*.csv
	$(info Downloaded county file $*.csv)

/source/zip/%.csv:
	mkdir -p source && cd source && mkdir zip && cd zip && curl $(RAW_DATA_PATH)/zip/$*/$*.csv -o $*.csv && ls && head --lines=5 $*.csv
	$(info Downloaded zip file $*.csv)
