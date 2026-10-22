"""Table 3 and the data behind Figure 4: fault episodes and distinct locations by state.

Each onset location (coordinates from 37011GEO.csv, aggregated in 17_ROUTE) is assigned
to an Indian state by point-in-polygon against the DataMeet state boundaries
(https://github.com/datameet/maps). The resulting table3_states_v4.csv is joined to the
state layer in QGIS to draw Figure 4.

Run from ANALYSIS3:  python TABLE3_STATES.py states.geojson
  states.geojson: https://raw.githubusercontent.com/datameet/maps/master/website/docs/data/geojson/states.geojson
Reads  OUTPUT/v4/rev_route_coordinates.csv     Writes  OUTPUT/v4/table3_states_v4.csv
Requires shapely.
"""
import collections, csv, json, sys
from shapely.geometry import Point, shape

geo = json.load(open(sys.argv[1], encoding="utf-8"))
polys = [(f["properties"]["ST_NM"], shape(f["geometry"])) for f in geo["features"]]
RENAME = {"NCT of Delhi": "Delhi"}          # match the state names of the QGIS layer

onsets, locations = collections.Counter(), collections.Counter()
for r in csv.DictReader(open("OUTPUT/v4/rev_route_coordinates.csv", encoding="utf-8")):
    pt = Point(float(r["LONGTITUDE"]), float(r["LATITUDE"]))
    inside = [n for n, poly in polys if poly.contains(pt)]
    state = inside[0] if inside else min(polys, key=lambda np: np[1].distance(pt))[0]
    state = RENAME.get(state, state)
    onsets[state] += int(r["onsets"])
    locations[state] += len(r["names"].split(";"))   # several names can share one coordinate

with open("OUTPUT/v4/table3_states_v4.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["state", "unique_locations", "occurrences"])
    for s in sorted(onsets):
        w.writerow([s, locations[s], onsets[s]])
print(f"{sum(locations.values())} locations, {sum(onsets.values()):,} episodes in {len(onsets)} states")
