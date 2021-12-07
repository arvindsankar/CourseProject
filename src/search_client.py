import requests
import json

from src.base_twitter_client import BaseTwitterClient

class SearchClient(BaseTwitterClient):
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