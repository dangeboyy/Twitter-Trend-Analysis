from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from zemberek import TurkishMorphology, TurkishSentenceNormalizer
from utility import remove_stop_words
import string

analyzer = SentimentIntensityAnalyzer()


def update_trend_polarity_result(analysis_score): 
    if analysis_score > 0.05:

        return 0, 1, 0
    elif analysis_score < -0.05:

        return 0, 0, 1
    else:

        return 1, 0, 0

def get_text_polarity(text):
    return (analyzer.polarity_scores(text))["compound"]

def get_turkish_text_polarity(text, turkish_analyzer, morphology, normalizer):
    normalized_sentence = normalize_sentence(text,normalizer)
    no_stop_words_sentence = remove_stop_words(normalized_sentence)
    stemmed_sentence = stem_turkish_words(no_stop_words_sentence, morphology)

    polarity_score = (turkish_analyzer.polarity_scores(stemmed_sentence))["compound"]

    return polarity_score

def normalize_sentence(text, normalizer):
    normalized_sentence = normalizer.normalize(text)
    normalized_sentence = remove_whitespace(normalized_sentence)
    split_normalized_sentence = normalized_sentence.split()
    for word in split_normalized_sentence:
        if word.startswith('#'):
            split_normalized_sentence.remove(word)
    
    final_sentence = " ".join(split_normalized_sentence)
    return final_sentence

def remove_whitespace(x):
    try:
        x = " ".join(x.split())
    except:
        pass
    return x

def init_morphology_analiser():
    return TurkishMorphology.create_with_defaults()

def init_normalizer(morphology):
    return TurkishSentenceNormalizer(morphology)

def stem_turkish_words(sentence, morphology):
    split_sentence = sentence.translate(str.maketrans('', '', string.punctuation)).split()
    word_to_be_analised = ""
    for word in split_sentence:
        results = morphology.analyze(word)
        for result in results:
            contains_without = False
            for i in range(len(result.get_morphemes())):
                if str(result.get_morphemes()[i]) == 'Without:Without' or str(result.get_morphemes()[i]) == 'Negative:Neg':
                    contains_without = True
                    break

            # eğer sız siz varsa istemsiz şeklinde alıyor. Yoksa normal bir şekilde stemmliyoruz
            if contains_without:
                word_to_be_analised += word + " "
            else:
                word_to_be_analised += result.item.lemma + " "

            break
            
    stemmed_sentece = word_to_be_analised.rstrip()
    return stemmed_sentece