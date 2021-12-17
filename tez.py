# AUTHOR: İBRAHİM MERT EGE
import requests
import base64
import json
import csv
from os import path, remove
import os
import textblob
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


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




def add_to_same_array(trend_name, full_array,tweets):
    rt_count = 0
    for tweet in tweets:
        
        text = tweet.full_text
        text = text.replace(trend_name,"")
        if "retweeted_status" in dir(tweet):
            rt_count +=1

        full_array.append(text)

    return rt_count

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

def print_vader_total(positive_vdr,negative_vdr,neutral_vdr):
    print('-----------------------Vader-----------------------------------------------------')
    print("Pozitif:" + positive_vdr)
    print("Negatif:" + negative_vdr)
    print("Neutral:" + neutral_vdr)
    print("-----------------------------------------------------------------------------------")

def print_polarity_result(polarity_vdr):
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
        trend_name = tweeter_trends['trends'][i+5]['name']
        print("Trend Name: " + trend_name)
     
        filtered_tweet_array = []

        positive_vdr = 0
        negative_vdr = 0
        neutral_vdr= 0
        polarity_vdr = 0


        tweets = tweepy.Cursor(api.search_tweets, q=trend_name + " -RT", lang='en',tweet_mode="extended").items(1000)
        full_array=[]

        rt_count = add_to_same_array(trend_name, full_array, tweets)
        analyzer=SentimentIntensityAnalyzer()

        for tweet in full_array:
            print(tweet)

            polarity_vdr+=(analyzer.polarity_scores(tweet))["compound"]
            neut_vdr,pos_vdr,neg_vdr = vader_analysis(analyzer,tweet)
            neutral_vdr += neut_vdr
            positive_vdr += pos_vdr
            negative_vdr += neg_vdr
            

        #append_single_tweet_to_JSON(filtered_tweet_array, trend_name)

        append_to_JSON_file(full_array,trend_name)
        

        # numberOfTweets=positive+negative+neutral
        # positive=calculatePercentage(positive,numberOfTweets)
        # negative = calculatePercentage(negative, numberOfTweets)
        # neutral = calculatePercentage(neutral, numberOfTweets)


        positive_vdr = format(positive_vdr, '.2f')
        negative_vdr = format(negative_vdr, '.2f')
        neutral_vdr = format(neutral_vdr, '.2f')


        print_vader_total(positive_vdr,negative_vdr,neutral_vdr)
        print_polarity_result(polarity_vdr)
        print("full size: " + str(len(full_array)))
        print("retweet size: " + str(rt_count))
        full_array.clear()
        break

    f.close()


tweet_data = trend_resp.json()
json_object = json.dumps(tweet_data, indent=4)

with open("trends.json", "w") as outfile:
    outfile.write(json_object)

traversingTrends(tweet_data[0])
