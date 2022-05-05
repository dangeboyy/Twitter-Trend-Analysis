from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv() 


client = MongoClient("mongodb+srv://dbAdmin:" + os.environ.get('DB_PASSWORD') + "@" + os.environ.get('DB_NAME') + ".mongodb.net/cluster0?retryWrites=true&w=majority")
db=client.data_analysis

tweets = db.tweets
trends = db.trends

#tweets.ensure_index( { id:1 }, { unique : True, dropDups : True } )

def insert_tweets(tweet_list):
    tweets.insert_many(tweet_list)
    for tweet in tweet_list:
        tweets.find_one_and_update({"id": tweet['id']},
                               {"$set": {"data": tweet}},
                               upsert=True)
    

def insert_trends(trend_list):
    for trend in trend_list:
        trends.find_one_and_update({"name": trend['name']},
                               {"$set": {"data": trend}},
                               upsert=True)
                               