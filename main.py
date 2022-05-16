# AUTHOR: İBRAHİM MERT EGE
import json
import services
import fileIO
import utility
import analysis
from utility import update_library_for_turkish
from dbCon import insert_trends, insert_tweets, find_unique_tweets


def traversing_english_trends(tweeter_trends):
    print("start english")
    lang = "en"
    trend_array = list()
    trend_as_of = tweeter_trends['as_of']
    trend_created_at = tweeter_trends['created_at']
    for i in range(10):
        trend_name = tweeter_trends['trends'][i]['name']

        total_positive = 0
        total_negative = 0
        total_neutral = 0
        total_polarity = 0

        tweets = services.get_english_tweets(trend_name, 100)

        json_tweets = utility.create_tweet_json_array(tweets)

        find_unique_tweets(json_tweets)
        for tweet in json_tweets:
            tweet_text_polarity = analysis.get_text_polarity(tweet['full_text'].replace(trend_name, ""))

            total_polarity += tweet_text_polarity
            if tweet['unique']:
                neut, pos, neg = analysis.update_trend_polarity_result(tweet_text_polarity)
                total_neutral += neut
                total_positive += pos
                total_negative += neg

            tweet['vader_result'] = tweet_text_polarity
            tweet['trend_name'] = trend_name
            tweet.pop("unique")
        fileIO.append_to_JSON_file(json_tweets, trend_name)
        insert_tweets(json_tweets)

        # utility.print_results(total_positive, total_negative, total_neutral, total_polarity)
        # utility.create_charts(formated_positive, formated_negative, formated_neutral)

        trend_json_object = utility.create_trend_json_object(tweeter_trends['trends'][i], total_positive,
                                                             total_negative, total_neutral, trend_as_of, trend_created_at, lang)
        trend_array.append(trend_json_object)

    insert_trends(trend_array)
    print("success english")


# TODO parametre olarak en tr giricek
def traversing_turkish_trends(tweeter_trends):
    print("start turkish")
    lang = "tr"
    trend_array = list()
    morphology = analysis.init_morphology_analiser()
    normalizer = analysis.init_normalizer(morphology)
    turkish_analyzer = update_library_for_turkish()
    trend_as_of = tweeter_trends['as_of']
    trend_created_at = tweeter_trends['created_at']
    for i in range(10):
        trend_name = tweeter_trends['trends'][i]['name']

        total_positive = 0
        total_negative = 0
        total_neutral = 0
        total_polarity = 0

        tweets = services.get_turkish_tweets(trend_name, 25)
        json_tweets = utility.create_tweet_json_array(tweets)

        find_unique_tweets(json_tweets)
        for tweet in json_tweets:
            tweet_text_polarity = analysis.get_turkish_text_polarity(tweet['full_text'].replace(trend_name, ""),
                                                                     turkish_analyzer, morphology, normalizer)

            total_polarity += tweet_text_polarity
            neut, pos, neg = analysis.update_trend_polarity_result(tweet_text_polarity)
            total_neutral += neut
            total_positive += pos
            total_negative += neg

            tweet['vader_result'] = tweet_text_polarity
            tweet['trend_name'] = trend_name
            tweet.pop("unique")

        # fileIO.append_to_JSON_file(json_tweets, trend_name)
        insert_tweets(json_tweets)
        # utility.print_results(total_positive, total_negative, total_neutral, total_polarity)
        # utility.create_charts(formated_positive, formated_negative, formated_neutral)
        trend_json_object = utility.create_trend_json_object(tweeter_trends['trends'][i], total_positive,
                                                             total_negative, total_neutral, trend_as_of, trend_created_at, lang)
        trend_array.append(trend_json_object)

    insert_trends(trend_array)
    print("success turkish")


def write_trends(trend_data):
    trend_json = json.dumps(trend_data, indent=4)
    fileIO.write_trends(trend_json)


def initialize():
    api = services.authenticate_api()
    # choice_input = utility.choose_country()

    # english
    trend_data = services.get_english_trends(api)
    # write_trends(trend_data)
    traversing_english_trends(trend_data[0])
    # turkish
    trend_data = services.get_turkish_trends(api)
    # write_trends(trend_data)
    traversing_turkish_trends(trend_data[0])


initialize()
