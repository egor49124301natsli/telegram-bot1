import os
import tweepy

API_KEY = os.getenv('TWITTER_API_KEY')
API_SECRET = os.getenv('TWITTER_API_SECRET')
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

def get_latest_tweets(keyword, count=3, lang='en'):
    try:
        tweets = api.search_tweets(q=keyword, lang=lang, count=count, tweet_mode='extended')
        return [tweet.full_text for tweet in tweets]
    except Exception as e:
        return [f"Ошибка Twitter API: {e}"]
