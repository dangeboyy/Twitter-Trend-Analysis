from pymongo import MongoClient
client = MongoClient("mongodb+srv://dbAdmin:Zombi123@cluster0.xv6ij.mongodb.net/cluster0?retryWrites=true&w=majority")
db=client.data_analysis

tweets = db.tweets

def insertIntoDB(tweet_list):
    tweets.insert_many(tweet_list)

#db.collection.ensureIndex( { record_id:1 }, { unique:true, dropDups:true } )