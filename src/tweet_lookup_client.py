import json
import requests
import keys

from src.base_twitter_client import BaseTwitterClient
from src.tweet import Tweet

class TweetLookupClient(BaseTwitterClient):
    def __init__(self, api_key, api_secret_key, bearer_token):
        super().__init__(api_key, api_secret_key, bearer_token)
        self.api = "https://api.twitter.com/2/tweets"
        self.params = {}
        self.headers = {"Authorization" : "Bearer {}".format(bearer_token)}
        self.tweet_ids = []
        self.batch_size = 100

        self.tweets = []

    def add_tweet_ids(self, tweet_ids):
        for tweet_id in tweet_ids:
            self.tweet_ids.append(tweet_id)

    def _add_tweet_batch(self, tweet_batch):
        self.params["ids"] = ",".join(tweet_batch)

    def _add_fields(self):
        self.params["tweet.fields"] = "created_at"

    def build_params(self, tweet_batch):
        self._add_tweet_batch(tweet_batch)
        self._add_fields()

    def process_response(self, response):
        assert('data' in response)
        response_data = response['data']
        for tweet_data in response_data:
            self.tweets.append(Tweet(tweet_data['id'],
                                     tweet_data['created_at'],
                                     tweet_data['text']))

    def lookup_tweets(self, tweet_ids):

        def divide_chunks(l, n):
            # looping till length l
            for i in range(0, len(l), n):
                yield l[i:i + n]

        tweet_batches = list(divide_chunks(tweet_ids, self.batch_size))
        for tweet_batch in tweet_batches:
            self.build_params(tweet_batch)
            r = requests.get(self.api, params=self.params, headers=self.headers)
            response = json.loads(r.text)
            self.process_response(response)

        self.tweets.reverse()
    def write_tweets_to_file(self, file_name):
        f = open(file_name, 'w')
        for tweet in self.tweets:
            f.write(tweet.str().encode("unicode_escape").decode("utf-8") + '\n')
        f.close()
