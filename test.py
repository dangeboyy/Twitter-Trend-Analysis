from difflib import SequenceMatcher

similarity_threshold = 0.7

def similarity(a, b):
        return SequenceMatcher(None, a, b).ratio()

latest_tweets = ()
duplicate_tweet = next((t for t in latest_tweets if similarity(data.text, t) > similarity_threshold), None)

def on_status(self, data):
    tw = next((t for t in latest_tweets if similarity(data.text, t) > similarity_threshold), None)

    if tw == None:
        ## this is a new tweet
        latest_tweets.append(tw)

    return True