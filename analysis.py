from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from vader_turkish_test import update_library_for_turkish
analyzer = SentimentIntensityAnalyzer()

def update_trend_polarity_result(analysis_score):
    if analysis_score == 0:
        print("Neutral for Vader")
        return 1, 0, 0
    elif analysis_score > 0.00:
        print("Positive for Vader")
        return 0, 1, 0
    elif analysis_score < 0.00:
        print("Negative for Vader")
        return 0, 0, 1

def get_text_polarity(text):
    return (analyzer.polarity_scores(text))["compound"]

def get_turkish_text_polarity(text):
    turkish_analyzer = update_library_for_turkish()
    return (turkish_analyzer.polarity_scores(text))["compound"]

