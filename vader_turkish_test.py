from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

def update_library_for_turkish():
    analyzer = SentimentIntensityAnalyzer()
    tr_library=pd.read_excel("STN.xlsx",dtype=str)

    words_to_add = dict()

    for index,row in tr_library.iterrows():
        if(pd.notna(row['synonyms'])):
            word = row['synonyms']
            neg_pol = float(row['neg value'])
            pos_pol = float(row['pos value'])
            neu_pol = float(row['obj value'])
            
            if neu_pol < 0.74:
                if neg_pol > pos_pol:
                    polarity_difference = float(neg_pol) - float(pos_pol)
                    polarity_difference *= -1
                else:
                    polarity_difference = float(pos_pol) - float(neg_pol)

                polarity_difference *= 4

                words = word.split(' , ')
                for synonym in words:
                    words_to_add[synonym] = polarity_difference
            
    analyzer.lexicon.update(words_to_add) 

    return analyzer