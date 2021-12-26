import matplotlib.pyplot as plt
import numpy as np


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

def print_results(positive_vdr, negative_vdr, neutral_vdr,total_polarity_vdr):
    print_vader_total(positive_vdr, negative_vdr, neutral_vdr)
    print_polarity_result(total_polarity_vdr)

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
    x = np.arange(len(labels))
    width = 0.35
    fig, ax = plt.subplots()
    rects = ax.bar(x, sentiment, width, label='pos')
    ax.set_ylabel('number of users')
    ax.set_title('Sentiment analysis result of ')
    ax.set_xticks(x, labels)

    ax.bar_label(rects, padding=3)

    plt.bar(labels, sentiment, color= ['Blue', 'Red', 'green'])
    plt.show()

def create_charts(positive_vdr, negative_vdr, neutral_vdr):
    pie_chart(positive_vdr, negative_vdr, neutral_vdr)
    bar_chart(positive_vdr, negative_vdr, neutral_vdr)

def create_tweet_json_object(tweet,vader_result):
    tweet_json_object = {
        "id": tweet.id,
        "lang": tweet.lang,
        "retweet_count": tweet.retweet_count,
        "favorite_count": tweet.favorite_count,
        "full_text": tweet.full_text,
        "vader_result" : vader_result,
        "by_hand_result" : ""
    }

    return tweet_json_object