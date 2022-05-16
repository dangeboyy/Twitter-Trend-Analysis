# AUTHOR: İBRAHİM MERT EGE
import tweepy
from dotenv import load_dotenv
import os

load_dotenv()

tweet_search_url = "https://api.twitter.com/1.1/search/tweets.json"

def authenticate_api():
    consumer_key = os.environ.get('consumer_key')
    consumer_secret_key = os.environ.get('consumer_secret_key')
    accessToken = os.environ.get('accessToken')
    accessSecret = os.environ.get('accessSecret')

    authentication = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret_key)
    authentication.set_access_token(accessToken, accessSecret)
    api = tweepy.API(authentication)

    return api


def get_english_trends(api):
    woeid = 23424977
    trends = api.get_place_trends(woeid)
    return trends

def get_english_tweets(trend_name,tweet_count):
    tweets = tweepy.Cursor(authenticate_api().search_tweets, q=trend_name + " -RT", lang='en', tweet_mode="extended").items(tweet_count)
    return tweets

def get_turkish_trends(api):
    woeid = 23424969
    trends = api.get_place_trends(woeid)
    return trends

def get_turkish_tweets(trend_name,tweet_count):
    tweets = tweepy.Cursor(authenticate_api().search_tweets, q=trend_name + " -RT", lang='tr', tweet_mode="extended").items(tweet_count)
    return tweets
