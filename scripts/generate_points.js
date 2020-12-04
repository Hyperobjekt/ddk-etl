// Generate random points w/in a tract for dot density layer.
// These are the pop cols that need dots generated for them:
//
// 'aian': 'ai', # American Indian or Native Alaskan, add to dot density
// 'black': 'b',
// 'api': 'ap', # Asian/Pacific Islander, add to dot density
// 'hisp': 'hi',
// 'white': 'w',
//
// These will all have trailing year suffixes: _10 and _15.
// And they will be different for the different year data.
// Overall, 10 sets of points.
//
// Each point needs the following properties:
//
// lat: latitude
// lng: longitude
// GEOID
// demo: demographic code, as, ap, b, hi, w
// msaid: msaid of associated metro area
// year: year of the data point
//
// Use Turf to:
// - get bounding box of the tract
// - generate point inside bounding box
// - discard if point not inside tract polygon
// - otherwise add to point count and add properties
// After all the points are generated, they will have to be made into a geojson
// feature collection and then into mbox tiles.
