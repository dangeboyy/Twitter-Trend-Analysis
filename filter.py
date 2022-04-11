from fileIO import read_stop_words, read_turkish_glossary
import pandas as pd
tr_library = read_turkish_glossary()
stop_words = read_stop_words()

for index,row in tr_library.iterrows():
    if(pd.notna(row['synonyms'])):
        if row['synonyms'] in stop_words:
            stop_words.remove(row['synonyms'])


print(len(stop_words))