from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def english_analysis(text):
    if (analyzer.polarity_scores(text))["compound"] == 0:
        print("Neutral for Vader")
        return 1, 0, 0
    elif (analyzer.polarity_scores(text))["compound"] > 0.00:
        print("Positive for Vader")
        return 0, 1, 0
    elif (analyzer.polarity_scores(text))["compound"] < 0.00:
        print("Negative for Vader")
        return 0, 0, 1

def get_text_polarity_english(text):
    return (analyzer.polarity_scores(text))["compound"]
