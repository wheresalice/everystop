import json
import sys
from contextlib import closing

from everystop import connect_db

filename = "export.json"
if len(sys.argv) == 2:
    filename = sys.argv[1]

geojson = json.loads(open(filename, "r").read())

with closing(connect_db()) as conn:
    c = conn.cursor()
    if 'elements' in geojson:
        for el in geojson['elements']:
            # print(el)
            o = c.execute('INSERT INTO stops VALUES(?, ?, ?, ?, ?, ?)', (el['lat'], el['lon'], el['tags']['name'], 0, el['id'], ''))
    if 'features' in geojson:
        for el in geojson['features']:
            if el['geometry']['type'] == 'Point':
                name = ''
                if  'name' in el['properties']:
                    name = el['properties']['name']
                stop_id = int(''.join(filter(str.isdigit, el['id'])))
                o = c.execute('INSERT INTO stops VALUES(?, ?, ?, ?, ?, ?)', (el['geometry']['coordinates'][1], el['geometry']['coordinates'][0], name, 0, stop_id, ''))
    conn.commit()
    c.close()

