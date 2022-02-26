# AUTHOR: İBRAHİM MERT EGE
import tweepy

tweet_search_url = "https://api.twitter.com/1.1/search/tweets.json"

def authenticate_api():
    consumer_key = 'z9QiZqqYDtz2iuD6YbnuVo1NS'
    consumer_secret_key = 'hWdiLwJjRhDKRGmqRnrCeRnDifZCRK6l42QplQHx9akGAr2Qk6'
    accessToken = '2151490557-lq4g6HPL8MZxnaebT9foqC6Aa30FFFqXTY7Gtxp'
    accessSecret = 'XpNAnbkoj6p0EnLuYvqm5vh0AWfJaaIFe80i1QWJ6HMQM'

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
