import json
import requests
import keys

class Tweet:
    def __init__(self, _id, created_at, text):
        self.id = _id
        self.created_at = created_at
        self.text = text

    def str(self):
        return ",".join([self.id, self.created_at, str(self.text)])

class TwitterClient:
    def __init__(self, api_key, api_secret_key, bearer_token):
        self._API_KEY_ = api_key
        self._API_SECRET_KEY_ = api_secret_key
        self._BEARER_TOKEN_ = bearer_token
        self.api = None

class SearchClient(TwitterClient):
    def __init__(self, api_key, api_secret_key, bearer_token):
        super().__init__(api_key, api_secret_key, bearer_token)
        self.api = "https://api.twitter.com/2/tweets/search/recent"
        self.params = {}
        self.headers = {"Authorization" : f"Bearer {bearer_token}"}
        self.max_results = 100
        self.tweet_ids = []

    def _add_tweet_fields(self):
        self.params["tweet.fields"] = ""
        self.params["tweet.fields"] += "id,"
        self.params["tweet.fields"] += "created_at"

    def _add_query(self, query):
        self.params["query"] = query

    def _add_start_time(self, start_time):
        self.params["start_time"] = start_time

    def _add_end_time(self, end_time):
        self.params["end_time"] = end_time

    def _add_max_results(self, max_results):
        self.params["max_results"] = max_results

    def _add_next_token(self, next_token):
        self.params["next_token"] = next_token

    def build_params(self, query, start_time=None, end_time=None,
                            max_results=None, next_token=None):
        self._add_tweet_fields()
        self._add_query(query)
        if start_time:
            self._add_start_time(start_time)
        if end_time:
            self._add_end_time(end_time)
        if max_results:
            self._add_max_results(max_results)
        if next_token:
            self._add_next_token(next_token)

    def process_response(self, response):
        assert('data' in response)
        response_data = response['data']
        for tweet_data in response_data:
            _tweet_id = tweet_data['id']
            _tweet_text = tweet_data['text']
            self.tweet_ids.append(_tweet_id)

    def collect_tweets(self, query, start_time, end_time):
        print("Collecting Tweets from {} to {}".format(start_time, end_time))
        self.build_params(query, start_time, end_time,
                              max_results=self.max_results)
        r = requests.get(self.api, params=self.params, headers=self.headers)
        response = json.loads(r.text)
        self.process_response(response)

        while True:
            if 'next_token' not in response['meta']:
                return
            else:
                self.build_params(query, start_time, end_time,
                              max_results=self.max_results,
                              next_token=response['meta']['next_token'])
                r = requests.get(self.api, params=self.params, headers=self.headers)
                response = json.loads(r.text)
                self.process_response(response)

class TweetLookupClient(TwitterClient):
    def __init__(self, api_key, api_secret_key, bearer_token):
        super().__init__(api_key, api_secret_key, bearer_token)
        self.api = "https://api.twitter.com/2/tweets"
        self.params = {}
        self.headers = {"Authorization" : f"Bearer {bearer_token}"}
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

from datetime import datetime
from datetime import timedelta

start_date = datetime(2021, 11, 8, hour=3) # Monday
end_date = datetime(2021, 11, 8, hour=3, minute=30)
buffer = timedelta(minutes=5)

for _ in range(5):
    start_date += timedelta(days=1)
    end_date += timedelta(days=1)

    start_time = start_date - buffer
    end_time = end_date + buffer

    print(start_time, end_time)
    search_client = SearchClient(keys.API_KEY, keys.API_SECRET_KEY, keys.BEARER_TOKEN)
    search_client.collect_tweets("Jeopardy", start_time.isoformat() + 'Z', end_time.isoformat() + 'Z')

    lookup_client = TweetLookupClient(keys.API_KEY, keys.API_SECRET_KEY, keys.BEARER_TOKEN)
    lookup_client.lookup_tweets(search_client.tweet_ids)
    lookup_client.write_tweets_to_file("Jeopardy_{}_{}_{}".format(start_date.year, start_date.month, ('0' + str(start_date.day))[-2:]))
