# Makefile for creating Census geography data for 2010 from source rather than S3

csv_types = index raw pop zscores 

DOWNLOADED_FILES = $(foreach t, $(csv_types), csvs/$(t).csv)

.PHONY: download split help

## all                 : Create all census GeoJSON
download: $(DOWNLOADED_FILES)

# Based on https://swcarpentry.github.io/make-novice/08-self-doc/
## help                : Print help
help: census.mk
	perl -ne '/^## / && s/^## //g && print' $<

## deploy              : Deploy gzipped census data to S3
# deploy:
# 	cd geojson && ls
# 	cd ..
# 	echo 'Gzipping geojson.'
# 	for f in geojson/*.geojson; do gzip $$f; done
# 	echo 'Uploading gzips.'
	# for f in geojson/*.gz; do aws s3 cp $$f s3://ddk-source/$$(basename $$f) --acl=public-read; done

split: 
	for f in csvs/*.csv; do csvgrep -c year -r "2010" $$(basename $$f).csv > $$(basename $$f)10.csv
	# Insert modified header row
	for f in csvs/*.csv; do csvgrep -c year -r "2015" $$(basename $$f).csv > $$(basename $$f)15.csv
	# Insert modified header row

## geojson/%.geojson   : Download and clean census GeoJSON
.SECONDARY:
csvs/%.csv:
	mkdir -p csvs/$*
	wget --no-use-server-timestamps -np -nd -r -P geojson/$* -A '$($*-pattern)' $(RAW_DATA_PATH/RAW_DATA_PATH)
	cd csvs && ls && cd ..
	echo '-----> Done downloading csvs. <-----'
