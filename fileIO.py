import json
from os import path
import os
import pandas as pd
from database.dbCon import insertIntoDB 


def write_trends(trend_json):
    with open("trends.json", "w") as outfile:
        outfile.write(trend_json)


def append_to_JSON_file(filtered_array, trend_name):
    if (not path.exists(os.getcwd() + "/unfilteredtweets")):
        os.mkdir(os.getcwd() + "/unfilteredtweets")

    json_search_object = json.dumps(filtered_array, indent=4)
    insertIntoDB(filtered_array)
    with open("./unfilteredtweets/" + trend_name + ".json", "a+") as newfile:
        newfile.write(json_search_object)


def read_stop_words():
    with open("stop_words.txt", 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return list(frozenset(stop_set))


def read_turkish_glossary():
    return pd.read_excel("STN.xlsx",dtype=str)
