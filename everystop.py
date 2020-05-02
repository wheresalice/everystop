from dotenv import load_dotenv
import os
import requests
import sqlite3
import tweepy

load_dotenv()

gmaps_api_key = os.getenv('GMAPS_API_KEY')

SVAPI = "https://maps.googleapis.com/maps/api/streetview"
GCAPI = "https://maps.googleapis.com/maps/api/geocode/json"


conn = sqlite3.connect('stops.db')
curs = conn.execute('SELECT * FROM stops WHERE visited=false ORDER BY RANDOM() LIMIT 1;')
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


auth = tweepy.OAuthHandler(os.getenv('TWITTER_API_KEY'), os.getenv('TWITTER_API_SECRET'))
auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN'), os.getenv('TWITTER_ACCESS_SECRET'))
api = tweepy.API(auth)

api.update_with_media('sv.jpg', record['name'])

conn.execute(f"UPDATE stops SET visited=true WHERE id={record['id']}")
conn.commit()
conn.close()