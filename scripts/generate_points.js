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
const turf = require("@turf/turf");

const source_dir = 'source'
const output_dir = 'proc'
// const tracts_geo_source = `./geojson/tracts.geojson`
const tracts_geo_source = `./proc/geojson/tracts.geojson`
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

const getPoints = ({ GEOID, c, v, m }) => {
  const column = c
  const value = v
  const met = m
  // console.log('getPoints, ', GEOID, column, value, met)
  // No points to generate, stop.
  if (!value) return '';
  // Set string to collect points.
  let points = ''
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
        if (isFirst[column] == 0) {
          // console.log(`isFirst for ${column} is 0. ${pointJSON}`);
          points = points + pointJSON;
          // console.log('points, ', points);
          isFirst[column] = 1;
          // console.log('points = ', points)
        } else {
          points = points + ',' + pointJSON;
        }
        // console.log('points = ', points)
        hits++;
      }
      attempts++;
    }
    return points
  } else {
    notFound.push(GEOID);
  }
}

fs.readFile(tracts_geo_source, 'utf8', (err, data) => {

    if (err) {
        console.log(`Error reading file from disk: ${err}`);
    } else {
      console.log('Loaded tracts geojson.');
      const tracts = JSON.parse(data);
      features = tracts.features;

      fs.readFile(tracts_data_source, 'utf8', (err, data) => {
        if (err) {
            console.log(`Error reading rows from disk: ${err}`);
        } else {
          console.log('Loaded demographic json.');
          const rows = JSON.parse(data);
          console.log('rows.length, ', rows.length)
          // Make files to write to.
          for (var v = 0; v < pop_cols.length; v++) {
            // console.log(`Writing file ${v}`, featureCollectionPrefix)
            fs.writeFileSync(`./${output_dir}/geojson/points_${pop_cols[v]}.geojson`, featureCollectionPrefix, 'utf8', (err) => {
              if (err)
                console.log(`Error creating demo file ${pop_cols[v]}!`, err)
              else {
                console.log("File written successfully\n");
              }
            })
          }

          // Iterate over each row, creating points for each demographic, appending points to the appropriate file.
          for (var b = 0; b < rows.length; b++) {
            const d = rows[b]
            if (b % 1000 === 0) {
              console.log(`Working on row ${b}, msaid ${d.msaid15}.`);
            }
            for (var v = 0; v < pop_cols.length; v++) {
              // const d = rows[b]
              const p = { GEOID: d.GEOID, c: pop_cols[v], v: d[pop_cols[v]], m: d.msaid15 };
              const points = getPoints(p);
              if (points && points.length > 0) {
                fs.appendFileSync(`./${output_dir}/geojson/points_${pop_cols[v]}.geojson`, points, (err) => {
                  console.log(`Error creating demo file ${pop_cols[v]}!`, err)
                })
              } else {
                // console.log(`Points was null for ${d.GEOID}.`, p)
              }
            }
          }
          // Append closing info to files.
          for (var v = 0; v < pop_cols.length; v++) {
            fs.appendFileSync(`./${output_dir}/geojson/points_${pop_cols[v]}.geojson`, featureCollectionSuffix, (err) => {
              console.log(`Error appending points to demo file ${pop_cols[v]} in row ${b}!`, err)
            })
          }
        }
        fs.writeFileSync(`./${output_dir}/geojson/points_features_not_found.json`, JSON.stringify(notFound), (err) => {
          console.log(`Error writing not found file!`, err)
        })
      })
    }
});
