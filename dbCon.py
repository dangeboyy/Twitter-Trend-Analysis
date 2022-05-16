from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient("mongodb+srv://dbAdmin:" + os.environ.get('DB_PASSWORD') + "@" + os.environ.get(
    'DB_NAME') + ".mongodb.net/cluster0?retryWrites=true&w=majority")
db = client.data_analysis

tweets = db.tweets
trends = db.trends



def find_unique_tweets(tweet_list):
    ids = []
    for tweet in tweet_list:
        tweet['unique'] = True
        ids.append(tweet['id'])

    same_tweets_not_updated = tweets.find({"id" : { "$in" : ids }})
    
    for tweet in tweet_list:
        for same_tweet in same_tweets_not_updated:
            if tweet['id'] == same_tweet['id']:
                tweet['unique'] = False
                break
    


def insert_tweets(tweet_list):
    tweets.insert_many(tweet_list)
    for tweet in tweet_list:
        tweets.find_one_and_update({"id": tweet['id']},
                                   {"$set": {
                                       "lang": tweet['lang'],
                                       "retweet_count": tweet['retweet_count'],
                                       "favorite_count": tweet['favorite_count'],
                                       "full_text": tweet['full_text'],
                                       "vader_result": tweet['vader_result']
                                   }
                                   },
                                   upsert=True)


def insert_trends(trend_list):
    for trend in trend_list:
        trends.find_one_and_update({"name": trend['name']},
                                   {"$set": {
                                       "name": trend['name'],
                                       "tweet_volume": trend['tweet_volume'],
                                       "lang": trend['lang'],
                                       "created_at": trend['created_at'],
                                       "as_of": trend['as_of']
                                   },
                                    "$inc": {
                                           "pos_result": trend['pos_result'],
                                           "neg_result": trend['neg_result'],
                                           "neu_result": trend['neu_result']
                                       }

                                   },
                                   upsert=True)
