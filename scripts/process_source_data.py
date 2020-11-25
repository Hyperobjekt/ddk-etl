# This script processes source CSVs from client.
# The CSVs have data for 2010 and 2015 on subsequent lines.
# This won't work for the Mapbox Tilesets.
# So each CSV must be broken up into separate dataframes,
# the column titles altered, and then the dataframes merged 
# back together again.
# The client has also used several strings to indicate 
# categorical scales. To keep the mapbox tilesets smaller
# these strings must be replaced with numbers.
