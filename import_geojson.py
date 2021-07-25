import json
import sqlite3

conn = sqlite3.connect('stops.db')

geojson = json.loads(open("export.json", "r").read())

c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS stops(lat real, lon real, name text, visited bool, id int)
''')

for el in geojson['elements']:
    # print(el)
    o = c.execute('INSERT INTO stops VALUES(?, ?, ?, ?, ?)', (el['lat'], el['lon'], el['tags']['name'], False, el['id']))
conn.commit()

c.close()
conn.close()
