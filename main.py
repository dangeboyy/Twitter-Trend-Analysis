# AUTHOR: İBRAHİM MERT EGE
import json
import services
import fileIO
import utility
import analysis
from vader_turkish_test import update_library_for_turkish
from dbCon import insert_trends, insert_tweets, find_unique_tweets

def traversing_english_trends(tweeter_trends):
    trend_array = list()
    for i in range(len(tweeter_trends['trends'])):
        trend_name = tweeter_trends['trends'][i + 1]['name']
        print("Trend Name: " + trend_name)

        filtered_tweet_array = []
        full_array = []

        total_positive = 0
        total_negative = 0
        total_neutral = 0
        total_polarity = 0

        tweets = services.get_english_tweets(trend_name,30)
        
        json_tweets = utility.create_tweet_json_array(tweets)
        
        find_unique_tweets(json_tweets)
        for tweet in json_tweets:
            print(tweet.full_text)
            
            tweet_text_polarity = analysis.get_text_polarity(tweet.full_text.replace(trend_name, ""))

            total_polarity += tweet_text_polarity
            if tweet.unique:
                neut, pos, neg = analysis.update_trend_polarity_result(tweet_text_polarity)
                total_neutral += neut
                total_positive += pos
                total_negative += neg

            tweet_json_object = utility.create_tweet_json_object(tweet, tweet_text_polarity, trend_name)
            filtered_tweet_array.append(tweet_json_object)

        fileIO.append_to_JSON_file(filtered_tweet_array, trend_name)
        insert_tweets(tweets)

        formated_positive = format(total_positive, '.2f')
        formated_negative = format(total_negative, '.2f')
        formated_neutral = format(total_neutral, '.2f')
        
        utility.print_results(formated_positive, formated_negative, formated_neutral, total_polarity)
        #utility.create_charts(formated_positive, formated_negative, formated_neutral)

        full_array.clear()
        
        
        trend_json_object = utility.create_trend_json_object(tweeter_trends['trends'][i+1],total_positive,total_negative,total_neutral)
        trend_array.append(trend_json_object)

        break
    insert_trends(trend_array)
    

# TODO parametre olarak en tr giricek
def traversing_turkish_trends(tweeter_trends):
    morphology = analysis.init_morphology_analiser()
    normalizer = analysis.init_normalizer(morphology)
    turkish_analyzer = update_library_for_turkish()
    for i in range(len(tweeter_trends['trends'])):
        trend_name = tweeter_trends['trends'][i + 1]['name']
        print("Trend Name: " + trend_name)

        filtered_tweet_array = []
        full_array = []

        total_positive = 0
        total_negative = 0
        total_neutral = 0
        total_polarity = 0

        tweets = services.get_turkish_tweets(trend_name,30)

        for tweet in tweets:
            #print(tweet.full_text)
            tweet_text_polarity = analysis.get_turkish_text_polarity(tweet.full_text.replace(trend_name, ""), turkish_analyzer, morphology, normalizer)

            total_polarity += tweet_text_polarity
            neut, pos, neg = analysis.update_trend_polarity_result(tweet_text_polarity)
            total_neutral += neut
            total_positive += pos
            total_negative += neg

            tweet_json_object = utility.create_tweet_json_object(tweet, tweet_text_polarity)
            filtered_tweet_array.append(tweet_json_object)

        fileIO.append_to_JSON_file(filtered_tweet_array, trend_name)

        formated_positive = format(total_positive, '.2f')
        formated_negative = format(total_negative, '.2f')
        formated_neutral = format(total_neutral, '.2f')
        
        utility.print_results(formated_positive, formated_negative, formated_neutral, total_polarity)
        #utility.create_charts(formated_positive, formated_negative, formated_neutral)

        full_array.clear()
        break
    
    

def write_trends(trend_data):
    trend_json = json.dumps(trend_data, indent=4)
    fileIO.write_trends(trend_json)

def initialize():
    api = services.authenticate_api()
    #choice_input = utility.choose_country()
    choice_input = 1

    # english = 1 turkish = 2
    if choice_input == 1:
        trend_data = services.get_english_trends(api)
        write_trends(trend_data)
        traversing_english_trends(trend_data[0])
    elif choice_input == 2:
        trend_data = services.get_turkish_trends(api)
        write_trends(trend_data)
        traversing_turkish_trends(trend_data[0])

initialize()