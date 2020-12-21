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

console.log('Generating points for dot density layer(s).')
// To run locally: node ./scripts/generate_points.js

const fs = require('fs');
const JSONStream = require('JSONStream');
const es = require('event-stream');
const turf = require("@turf/turf");

const source_dir = 'source'
const output_dir = 'proc'
const tracts_geo_source = `./geojson/tracts.geojson`
const tracts_data_source = `./${output_dir}/pop.json`
const pop_cols = ['ai_10','ap_10','b_10','hi_10','w_10','ai_15','ap_15','b_15','hi_15','w_15']

let notFound = []; // Tracks the number of tracts not found in feature set.
let features;
const featureCollectionPrefix = '{"type":"FeatureCollection","features":['
const featureCollectionSuffix = ']}'

const isFirst = {}
pop_cols.forEach(col => {
  isFirst[col] = 0
})

const getPoints = ({ GEOID, column, value, met }) => {
  console.log('getPoints, ', GEOID, column, value, met)
  // No points to generate, stop.
  if (value === 0) return;

  let points = featureCollectionPrefix
  // Get feature.
  const feature = features.find(el => {
    // console.log('filtering, ', el.properties.GEOID, row.GEOID)
     return Number(el.properties.GEOID) === Number(GEOID)
  })
  // console.log('feature is, ', feature)
  if (!!feature) {
    // Get bounding box of the feature.
    feature_bbox = turf.bbox(feature);
    // console.log('feature_bbox, ', feature_bbox)
    // Set bounds coords for the feature.
    const minX = feature_bbox[0];
    const minY = feature_bbox[1];
    const maxX = feature_bbox[2];
    const maxY = feature_bbox[3];

    // For the amount that is value,
    // Generate random point inside bounding box.
    // Discard if point not inside tract polygon.
    // Otherwise add to point count and add properties.
    const limit = value * 10; // limit test to 10x the population.
    // Legitimate points to add to collection.
    let hits = 0;
    // Attempts to generate a point.
    let attempts = 0;

    while (hits < value - 1 && attempts < limit) {

      // Generate latlng in bounding box.
      const lat = minY + Math.random() * (maxY - minY);
      const lng = minX + Math.random() * (maxX - minX);

      const randomPoint = turf.point([lng, lat], {
        tract: GEOID,
        type: column,
        met: met
      });

      if (turf.booleanPointInPolygon(randomPoint, feature)) {
        // console.log('point is in tract, ', randomPoint);
        // Append points as stringified json since we are streaming.
        const pointJSON = JSON.stringify(randomPoint);
        // Add commas only if it's not the first ever entry in the array of features.
        if (isFirst[column] === 0) {
          points += pointJSON;
        } else {
          points += ',' + pointJSON;
        }
        hits++;
      }
      attempts++;
    }
    return points
  } else {
    notFound.push(row.GEOID);
    // console.log(`Feature not found! Tract: ${row.GEOID}.`)
  }
}

fs.readFile(tracts_geo_source, 'utf8', (err, data) => {

    if (err) {
        console.log(`Error reading file from disk: ${err}`);
    } else {
        console.log('Loaded tracts geojson.');
        const tracts = JSON.parse(data);
        features = tracts.features;

        pop_cols.forEach(col => {
          console.log('foreach, ', col)
          activeColumn = col;
          const streamParse = JSONStream.parse('*')
          const outFile = `./${output_dir}/geojson/points_${col}.geojson`
          // const append = fs.appendFile(outFile, featureCollectionSuffix, (err) => {console.log(`There was an error: ${err}.`)})
          const out = fs.createWriteStream(outFile).on('close', function() {
            console.log(`File ${col} closed. Calling append.`)
            fs.appendFile(outFile, featureCollectionSuffix, (err) => {console.log(`There was an error: ${err}.`)})
          });

          fs.createReadStream(tracts_data_source)
            .pipe(streamParse)
            .pipe(es.mapSync(function (d) {
              return { GEOID: d.GEOID, c: col, v: d[col], m: d.msaid15 };
            }))
            .pipe(es.mapSync(function (d) {
              return getPoints(d)
            }))
            // .pipe(JSONStream.stringify())
            .pipe(out)
        });
        fs.writeFile(`./${output_dir}/not_found.json`, JSON.stringify(notFound), (err) => {
          console.log(`Error! ${err}`)
        })
    }

});
