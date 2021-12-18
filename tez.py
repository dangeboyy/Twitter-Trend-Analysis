# AUTHOR: İBRAHİM MERT EGE
import requests
import base64
import json
import csv
from os import path, remove
import os
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pandas import DataFrame
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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


def append_to_JSON_file(filtered_array, trend_name):
    if (not path.exists(os.getcwd() + "/unfilteredtweets")):
        os.mkdir(os.getcwd() + "/unfilteredtweets")

    json_search_object = json.dumps(filtered_array, indent=4)
    with open("./unfilteredtweets/" + trend_name + ".json", "a+") as newfile:
        newfile.write(json_search_object)


def parse_tweet(search):
    pass


def pie_chart(positive, negative, neutral):
    y = np.array([positive, negative, neutral])
    mylabels = ["Positives", "Negatives", "Neutrals"]
    p, tx, autotexts = plt.pie(y, labels=mylabels,
                               autopct="", shadow=True)

    for i, a in enumerate(autotexts):
        a.set_text("{}".format(y[i]))
    plt.axis('equal')
    plt.show()


def bar_chart(positive, negative, neutral):
    labels = ['positive', 'negative', 'neutral']
    sentiment = [float(positive), float(negative), float(neutral)]
    plt.bar(labels, sentiment, color= ['Blue', 'Red', 'green'])
    plt.show()


tweet_id_url = "https://api.twitter.com/2/tweets"

choices = {"İ": "I", "ş": "s", "ı": "i", "Ş": "S", "Ö": "O", "ö": "o", "Ü": "U", "ü": "u", "Ç": "C", "ç": "c",
           "Ğ": "G", "ğ": "g"}
f = open('filtered_data.csv', 'a+', encoding='UTF8')
writer = csv.writer(f)


# traversing the twitter trends of the last 24 hours(at least)
def calculatePercentage(a, b):
    return 100 * float(a) / float(b)


def add_to_same_array(full_array, tweets):
    rt_count = 0
    for tweet in tweets:
        if "retweeted_status" in dir(tweet):
            rt_count += 1

        full_array.append(tweet)

    return rt_count


def vader_analysis(analyzer, tweet):
    if (analyzer.polarity_scores(tweet))["compound"] == 0:
        print("Neutral for Vader")
        return 1, 0, 0
    elif (analyzer.polarity_scores(tweet))["compound"] > 0.00:
        print("Positive for Vader")
        return 0, 1, 0
    elif (analyzer.polarity_scores(tweet))["compound"] < 0.00:
        print("Negative for Vader")
        return 0, 0, 1


def print_vader_total(positive_vdr, negative_vdr, neutral_vdr):
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
        trend_name = tweeter_trends['trends'][i + 1]['name']
        print("Trend Name: " + trend_name)

        filtered_tweet_array = []

        total_positive_vdr = 0
        total_negative_vdr = 0
        total_neutral_vdr = 0
        total_polarity_vdr = 0

        tweets = tweepy.Cursor(api.search_tweets, q=trend_name + " -RT", lang='en', tweet_mode="extended").items(100)
        full_array = []
        positive_values = []
        negative_values = []
        polarity_values = []

        rt_count = add_to_same_array(trend_name, full_array, tweets)
        analyzer = SentimentIntensityAnalyzer()

        for tweet in full_array:
            tweet.full_text = tweet.full_text.replace(trend_name, "")

            print(tweet.full_text)

            total_polarity_vdr += (analyzer.polarity_scores(tweet.full_text))["compound"]
            neut_vdr, pos_vdr, neg_vdr = vader_analysis(analyzer, tweet.full_text)
            total_neutral_vdr += neut_vdr
            total_positive_vdr += pos_vdr
            total_negative_vdr += neg_vdr

            positive_values.append(analyzer.polarity_scores(tweet.full_text)["pos"] + 1)
            negative_values.append(analyzer.polarity_scores(tweet.full_text)["neg"] + 1)
            polarity_values.append(analyzer.polarity_scores(tweet.full_text)["compound"] + 1)

            tweet_json_object = {
                "id": tweet.id,
                "lang": tweet.lang,
                "retweet_count": tweet.retweet_count,
                "favorite_count": tweet.favorite_count,
                "full_text": tweet.full_text
            }

            filtered_tweet_array.append(tweet_json_object)

        # append_single_tweet_to_JSON(filtered_tweet_array, trend_name)

        append_to_JSON_file(filtered_tweet_array, trend_name)

        # numberOfTweets=positive+negative+neutral
        # positive=calculatePercentage(positive,numberOfTweets)
        # negative = calculatePercentage(negative, numberOfTweets)
        # neutral = calculatePercentage(neutral, numberOfTweets)

        positive_vdr = format(total_positive_vdr, '.2f')
        negative_vdr = format(total_negative_vdr, '.2f')
        neutral_vdr = format(total_neutral_vdr, '.2f')

        print_vader_total(positive_vdr, negative_vdr, neutral_vdr)
        print_polarity_result(total_polarity_vdr)
        print("full size: " + str(len(full_array)))
        print("retweet size: " + str(rt_count))

       
        full_array.clear()
        pie_chart(positive_vdr, negative_vdr, neutral_vdr)
        bar_chart(positive_vdr, negative_vdr, neutral_vdr)
        break

    f.close()


tweet_data = trend_resp.json()
json_object = json.dumps(tweet_data, indent=4)

with open("trends.json", "w") as outfile:
    outfile.write(json_object)

traversingTrends(tweet_data[0])
