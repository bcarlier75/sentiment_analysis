from credentials import *
from twython import TwythonStreamer
import re
import os


def retrieve_key_and_token():
    # Consumer API keys:
    consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
    consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")

    # Access token & access token secret:
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    access_secret = os.environ.get("TWITTER_ACCESS_SECRET")

    return consumer_key, consumer_secret, access_token, access_secret


class MyStreamer(TwythonStreamer):
    # We retrieve only tweets or replies (not retweets) with macron in the tweet
    def on_success(self, data):
        match = re.search("macron", data['text'], flags=re.IGNORECASE)
        if data['text'][:2] != 'RT' and data['in_reply_to_status_id'] is None and match:
            tweets.append(data)
            print('+1 tweet')
        if len(tweets) >= 10:
            self.disconnect()

    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()


def print_tweet_list(tweet_list: list):
    for tweet in tweet_list:
        print("_______________")
        if tweet['truncated'] is True:
            print(tweet['extended_tweet']['full_text'])
        else:
            print(tweet['text'])
        print('-----------------------------------')

tweets = []
k, k_secret, t, t_secret = retrieve_key_and_token()
stream = MyStreamer(k, k_secret, t, t_secret)
stream.statuses.filter(track='macron', language='fr')
print_tweet_list(tweets)
