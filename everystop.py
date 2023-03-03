import sqlite3
import os
import time

import requests

from contextlib import closing

SVAPI = "https://maps.googleapis.com/maps/api/streetview"


def get_random_stop():
    gmaps_api_key = os.getenv('GMAPS_API_KEY')

    with closing(connect_db()) as conn:
        curs = conn.execute('SELECT * FROM stops WHERE visited=0 ORDER BY RANDOM() LIMIT 1;')
        keys = [c[0] for c in curs.description]
        record = dict(zip(keys, curs.fetchone()))

    params = {
        "location": f"{record['lat']}, {record['lon']}",
        "key": gmaps_api_key,
        "size": "1000x1000",
        "fov": 65,
        "pitch": 10
    }

    print(record['name'], params)
    r = requests.get(SVAPI, params=params)
    with open('sv.jpg', 'wb') as f:
        f.write(r.content)

    return {"id": record['id'], "name": record['name']}


def mark_visited(stop_id, url):
    with closing(connect_db()) as conn:
        conn.execute(f"UPDATE stops SET visited={int(time.time())}, url={url} WHERE id={stop_id}")
        conn.commit()
    conn.close()


def connect_db():
    conn = sqlite3.connect('stops.db')
    run_migrations(conn)
    return conn


def run_migrations(conn):
    try:
        current_migration = conn.execute(
            """
            select max(migration) from migrations
        """
        ).fetchall()[0][0]
    except sqlite3.OperationalError:
        # If there was no migrations table, the DB does not exist yet.
        current_migration = -1

    # initial migration
    if current_migration < 0:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS stops(lat real, lon real, name text, visited bool, id int)
        ''')
        conn.execute('CREATE TABLE IF NOT EXISTS migrations(migration int)')
        conn.execute('INSERT INTO migrations VALUES(0)')
        conn.commit()
        print("performed initial setup of db")

    if current_migration < 1:
        conn.execute('''
            create table stops_dg_tmp(lat real, lon real, name text, visited int, id int, url text)
        ''')
        conn.execute('''
            insert into stops_dg_tmp(lat, lon, name, visited, id) select lat, lon, name, visited, id from stops;
        ''')
        conn.execute('''
            drop table stops
        ''')
        conn.execute('''
            alter table stops_dg_tmp rename to stops;
        ''')
        # noinspection SqlWithoutWhere
        conn.execute('''
            UPDATE migrations SET migration=1;
        ''')
        conn.commit()
        print("Upgraded DB to version 1")

if __name__ == '__main__':
    connect_db()
    stop = get_random_stop()
    print(stop)
    print("See README.md for usage instructions")
