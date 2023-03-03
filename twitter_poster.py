from dotenv import load_dotenv
import os
import tweepy

from everystop import get_random_stop, mark_visited

load_dotenv()

auth = tweepy.OAuthHandler(os.getenv('TWITTER_API_KEY'), os.getenv('TWITTER_API_SECRET'))
auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN'), os.getenv('TWITTER_ACCESS_SECRET'))
api = tweepy.API(auth)

record = get_random_stop()
post = api.update_with_media('sv.jpg', record['name'])
mark_visited(record['id'], post['id'])
