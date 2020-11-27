# Makefile for creating Census geography data for 2010 from source rather than S3

csv_types = index raw pop zscores 

DOWNLOADED_FILES = $(foreach t, $(csv_types), source_csvs/$(t).csv)

.PHONY: download help

## all                 : Create all census GeoJSON
download: $(DOWNLOADED_FILES)

# Based on https://swcarpentry.github.io/make-novice/08-self-doc/
## help                : Print help
help: census.mk
	perl -ne '/^## / && s/^## //g && print' $<

## source_csvs/%.csv   : Download the client data files.
.SECONDARY:
source_csvs/%.csv:
	mkdir -p source_csvs && cd source_csvs && curl $(RAW_DATA_PATH)$*/$*.csv -o $*.csv && ls && head --lines=5 $*.csv
	$(info Downloaded $*.csv)
