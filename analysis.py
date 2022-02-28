from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from vader_turkish_test import update_library_for_turkish
from zemberek import TurkishMorphology
import string

analyzer = SentimentIntensityAnalyzer()


def update_trend_polarity_result(analysis_score): 
    if analysis_score > 0.1:
        print("Positive for Vader")
        return 0, 1, 0
    elif analysis_score < -0.05:
        print("Negative for Vader")
        return 0, 0, 1
    else:
        print("Neutral for Vader")
        return 1, 0, 0

def get_text_polarity(text):
    return (analyzer.polarity_scores(text))["compound"]

def get_turkish_text_polarity(text, morphology):
    turkish_analyzer = update_library_for_turkish()
    stemmed_sentence = stem_turkish_words(text, morphology)
    polarity_score = (turkish_analyzer.polarity_scores(stemmed_sentence))["compound"]
    print("----------- " , turkish_analyzer.polarity_scores(stemmed_sentence) , " -----------")
    return polarity_score

def init_morphology_analiser():
    return TurkishMorphology.create_with_defaults()

def stem_turkish_words(sentence, morphology):
    split_sentence = sentence.translate(str.maketrans('', '', string.punctuation)).split()
    word_to_be_analised = ""
    for word in split_sentence:
        results = morphology.analyze(word[0])
        for result in results:
            contains_without = False
            for i in range(len(result.get_morphemes())):
                if str(result.get_morphemes()[i]) == 'Without:Without' or str(result.get_morphemes()[i]) == 'Negative:Neg':
                    contains_without = True
                    break

            if contains_without:
                word_to_be_analised += word[0] + " "
            else:
                word_to_be_analised += result.item.lemma + " "

            break
            
    stemmed_sentece = word_to_be_analised.rstrip()
    return stemmed_sentece