import csv
from contextlib import closing

from everystop import connect_db

with closing(connect_db()) as conn:
    c = conn.cursor()

    with open('stops.txt', mode='r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            print(row)
            o = c.execute('INSERT INTO stops VALUES(?, ?, ?, ?, ?, ?)', (row['stop_lat'], row['stop_lon'], row['stop_name'], 0, row['stop_id'], ''))
    conn.commit()
    c.close()
