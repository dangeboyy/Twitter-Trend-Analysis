# AUTHOR: İBRAHİM MERT EGE
import requests
import base64
import json
import csv
from os import path, remove
import os
import textblob
import tweepy
from vaderSentiment import SentimentIntensityAnalyzer


consumer_key = 'z9QiZqqYDtz2iuD6YbnuVo1NS'
consumer_secret_key = 'hWdiLwJjRhDKRGmqRnrCeRnDifZCRK6l42QplQHx9akGAr2Qk6'

key_secret = '{}:{}'.format(consumer_key, consumer_secret_key).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)

auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}

auth_data = {
    'grant_type': 'client_credentials'
}

auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
access_token = auth_resp.json()['access_token']
accessToken = '2151490557-lq4g6HPL8MZxnaebT9foqC6Aa30FFFqXTY7Gtxp'
accessSecret = 'XpNAnbkoj6p0EnLuYvqm5vh0AWfJaaIFe80i1QWJ6HMQM'
authentication = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret_key)
authentication.set_access_token(accessToken, accessSecret)
api = tweepy.API(authentication)



trend_headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}

trend_params = {
    'id': 23424977,
}

tweet_search_url = "https://api.twitter.com/1.1/search/tweets.json"

trend_url = 'https://api.twitter.com/1.1/trends/place.json'
trend_resp = requests.get(trend_url, headers=trend_headers, params=trend_params)


def append_to_JSON_file(search_response, trend_name):
    if (not path.exists(os.getcwd() + "/unfilteredtweets")):
        os.mkdir(os.getcwd() + "/unfilteredtweets")

    json_search_object = json.dumps(search_response, indent=4)
    with open("./unfilteredtweets/" + trend_name + ".json", "a+") as newfile:
        newfile.write(json_search_object)


def append_single_tweet_to_JSON(tweet_response, trend_name):
    if (not path.exists(os.getcwd() + "/filteredtweets")):
        os.mkdir(os.getcwd() + "/filteredtweets")

    json_tweet_obj = json.dumps(tweet_response, indent=4)
    with open("./filteredtweets/" + trend_name + ".json", "a+") as newfile:
        newfile.write(json_tweet_obj)


def parse_tweet(search):
    pass


tweet_id_url = "https://api.twitter.com/2/tweets"

choices = {"İ": "I", "ş": "s", "ı": "i", "Ş": "S", "Ö": "O", "ö": "o", "Ü": "U", "ü": "u", "Ç": "C", "ç": "c",
           "Ğ": "G", "ğ": "g"}
f = open('filtered_data.csv', 'a+', encoding='UTF8')
writer = csv.writer(f)


# traversing the twitter trends of the last 24 hours(at least)
def calculatePercentage(a, b):
    return 100 * float(a) / float(b)

def add_to_same_array(removed_same, full_array,tweets):
    for tweet in tweets:
        if 'retweeted_status' in tweet._json:
            text=tweet._json['retweeted_status']['full_text']
        else:
            text =tweet.full_text

        removed_same.add(text)
        full_array.append(text)

def text_blob_analysis(currentAnalysis):
    if currentAnalysis.sentiment.polarity == 0:
        print("Neutral for TextBlob")
        return 1,0,0
    elif currentAnalysis.sentiment.polarity > 0.00:
        print("Positive for TextBlob")
        return 0,1,0
    elif currentAnalysis.sentiment.polarity < 0.00:
        print("Negative for TextBlob")
        return 0,0,1

def vader_analysis(analyzer,tweet):
    if (analyzer.polarity_scores(tweet))["compound"]==0:
        print("Neutral for Vader")
        return 1,0,0
    elif (analyzer.polarity_scores(tweet))["compound"] > 0.00:
        print("Positive for Vader")
        return 0,1,0
    elif (analyzer.polarity_scores(tweet))["compound"] < 0.00:
        print("Negative for Vader")
        return 0,0,1

def print_text_blob_total(positive_tb,negative_tb,neutral_tb):
    print('---------------------TextBlob-------------------------------------------------------')
    print("Pozitif:" + positive_tb)
    print("Negatif:" + negative_tb)
    print("Neutral:" + neutral_tb)

def print_vader_total(positive_vdr,negative_vdr,neutral_vdr):
    print('-----------------------Vader-----------------------------------------------------')
    print("Pozitif:" + positive_vdr)
    print("Negatif:" + negative_vdr)
    print("Neutral:" + neutral_vdr)
    print("-----------------------------------------------------------------------------------")

def print_polarity_result(polarity_tb,polarity_vdr):
    print("##########TextBlob###########")
    if polarity_tb > 0:
        print('Positive')
    elif polarity_tb < 0:
        print('Negative')
    elif polarity_tb == 0:
        print('Neutral')
    print("##########Vader###########")
    if polarity_vdr > 0:
        print('Positive')
    elif polarity_vdr < 0:
        print('Negative')
    elif polarity_vdr == 0:
        print('Neutral')
    print("#################################")

def traversingTrends(tweeter_trends):
    for i in range(len(tweeter_trends['trends'])):
        trend_name = tweeter_trends['trends'][i+1]['name']
        print("Trend Name:"+trend_name)
        parameters = {"q": trend_name, "tweet_mode": 'extended'}

        # getting tweets of trending topics via the search endpoint of twitter standard api v1.1
        search_resp = requests.get(tweet_search_url, headers=trend_headers, params=parameters).json()

     
        filtered_tweet_array = []
        positive_tb = 0
        negative_tb = 0
        neutral_tb = 0
        polarity_tb = 0

        positive_vdr = 0
        negative_vdr = 0
        neutral_vdr= 0
        polarity_vdr = 0


        tweets = tweepy.Cursor(api.search_tweets, q=trend_name, lang='en',tweet_mode="extended").items(1200)


        #tweets=api.search_tweets(trend_name,count=1000,tweet_mode='extended', lang='en')

        removed_same = set()
        full_array=[]

        add_to_same_array(removed_same, full_array, tweets)
        analyzer=SentimentIntensityAnalyzer()

        for tweet in removed_same:
            currentAnalysis = textblob.TextBlob(tweet)
            polarity_tb += currentAnalysis.sentiment.polarity
            print(tweet)
            neut_tb,pos_tb,neg_tb = text_blob_analysis(currentAnalysis)
            neutral_tb += neut_tb
            positive_tb += pos_tb
            negative_tb += neg_tb

            polarity_vdr+=(analyzer.polarity_scores(tweet))["compound"]
            neut_vdr,pos_vdr,neg_vdr = text_blob_analysis(currentAnalysis)
            neutral_vdr += neut_vdr
            positive_vdr += pos_vdr
            negative_vdr += neg_vdr
            

        append_single_tweet_to_JSON(filtered_tweet_array, trend_name)

        append_to_JSON_file(search_resp, trend_name)

        # numberOfTweets=positive+negative+neutral
        # positive=calculatePercentage(positive,numberOfTweets)
        # negative = calculatePercentage(negative, numberOfTweets)
        # neutral = calculatePercentage(neutral, numberOfTweets)

        positive_tb = format(positive_tb, '.2f')
        negative_tb = format(negative_tb, '.2f')
        neutral_tb = format(neutral_tb, '.2f')

        positive_vdr = format(positive_vdr, '.2f')
        negative_vdr = format(negative_vdr, '.2f')
        neutral_vdr = format(neutral_vdr, '.2f')


        print_text_blob_total(positive_tb,negative_tb,neutral_tb)
        print_vader_total(positive_vdr,negative_vdr,neutral_vdr)
        print_polarity_result(polarity_tb,polarity_vdr)
        print("Removed_Same Size:" + str(len(removed_same)))
        print("full size:"+str(len(full_array)))
        removed_same.clear()
        full_array.clear()
        break

    f.close()


tweet_data = trend_resp.json()
json_object = json.dumps(tweet_data, indent=4)

with open("trends.json", "w") as outfile:
    outfile.write(json_object)

traversingTrends(tweet_data[0])
