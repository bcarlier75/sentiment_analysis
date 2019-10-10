from credentials import *
from twython import TwythonStreamer
import re


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
stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
stream.statuses.filter(track='macron', language='fr')
print_tweet_list(tweets)
