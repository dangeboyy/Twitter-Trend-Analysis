
import json
from os import path
import os

def write_trends(trend_json):
    with open("trends.json", "w") as outfile:
        outfile.write(trend_json)


def append_to_JSON_file(filtered_array, trend_name):
    if (not path.exists(os.getcwd() + "/unfilteredtweets")):
        os.mkdir(os.getcwd() + "/unfilteredtweets")

    json_search_object = json.dumps(filtered_array, indent=4)
    with open("./unfilteredtweets/" + trend_name + ".json", "a+") as newfile:
        newfile.write(json_search_object)