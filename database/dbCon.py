from pymongo import MongoClient
client = MongoClient("mongodb+srv://dbAdmin:Zombi123@cluster0.xv6ij.mongodb.net/cluster0?retryWrites=true&w=majority")
db=client.data_analysis

tweets = db.tweets
trends = db.trends

def insert_tweets(tweet_list):
    tweets.insert_many(tweet_list)

def insert_trends(trend_list):
    for trend in trend_list:
        trends.find_one_and_update({"name": trend['name']},
                               {"$set": {"data": trend}},
                               upsert=True)
                               
#db.collection.ensureIndex( { record_id:1 }, { unique:true, dropDups:true } )