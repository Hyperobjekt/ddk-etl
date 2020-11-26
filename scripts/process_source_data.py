# This script processes source CSVs from client.
# The CSVs have data for 2010 and 2015 on subsequent lines.
# This won't work for the Mapbox Tilesets.
# So each CSV must be broken up into separate dataframes,
# the column titles altered, and then the dataframes merged 
# back together again.
# The client has also used several strings to indicate 
# categorical scales. To keep the mapbox tilesets smaller
# these strings must be replaced with numbers.

print("Processing source data...")

# Work from list of files.
# Replace categorical strings in each with numbers.
# Split rows into 2010 and 2015 data.
# Rename columns in each dataframe with 10 or 15 suffix.
# Merge dataframes using geoid column.
# Save each merged dataframe to a new directory for the processed files..
