# AUTHOR: İBRAHİM MERT EGE
import json

import services
import fileIO
import utility
import analysis


def traversingTrends(tweeter_trends):
    for i in range(len(tweeter_trends['trends'])):
        trend_name = tweeter_trends['trends'][i + 1]['name']
        print("Trend Name: " + trend_name)

        filtered_tweet_array = []
        full_array = []

        total_positive = 0
        total_negative = 0
        total_neutral = 0
        total_polarity = 0

        tweets = services.get_tweets(trend_name,30)

        for tweet in tweets:
            print(tweet.full_text)
            
            tweet_text_polarity = analysis.get_text_polarity_english(tweet.full_text.replace(trend_name, ""))

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
        utility.create_charts(formated_positive, formated_negative, formated_neutral)

        full_array.clear()
        
        break


trend_data = services.get_trends()
trend_json = json.dumps(trend_data, indent=4)

fileIO.write_trends(trend_json)

traversingTrends(trend_data[0])