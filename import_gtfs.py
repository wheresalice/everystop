import csv
import sqlite3

conn = sqlite3.connect('stops.db')
c = conn.cursor()
c.execute('''
     CREATE TABLE IF NOT EXISTS stops(lat real, lon real, name text, visited bool, id int)
''')

with open('stops.txt', mode='r') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        print(row)
        o = c.execute('INSERT INTO stops VALUES(?, ?, ?, ?, ?)', (row['stop_lat'], row['stop_lon'], row['stop_name'], False, row['stop_code']))
conn.commit()
c.close()
conn.close()
