import json
import requests
import keys

from datetime import datetime
from src.base_twitter_client import BaseTwitterClient
from src.tweet import Tweet

class StreamRulesClient(BaseTwitterClient):
    def __init__(self, api_key, api_secret_key, bearer_token):
        super().__init__(api_key, api_secret_key, bearer_token)
        self.api = "https://api.twitter.com/2/tweets/search/stream/rules"
        self.headers = {"Authorization" : f"Bearer {bearer_token}"}
        self.data = {}

    def add_rule(self, search_term):
        self.data["add"] = [{"value": search_term}]
        response = requests.post(self.api, headers=self.headers, json=self.data)
        del self.data["add"]

    def list_rules(self):
        response = requests.get(self.api, headers=self.headers)
        data_blob = response.json()
        if 'data' in data_blob:
            return [rule['id'] for rule in data_blob['data']]
        else:
            return []

    def delete_rule(self, rule_id):
        assert (type(rule_id) == str)
        self.data["delete"] = {"ids": [rule_id]}
        response = requests.post(self.api, headers=self.headers, json=self.data)
        del self.data["delete"]

class StreamClient(BaseTwitterClient):
    def __init__(self, api_key, api_secret_key, bearer_token):
        super().__init__(api_key, api_secret_key, bearer_token)
        self.api = "https://api.twitter.com/2/tweets/search/stream"
        self.params = {}
        self.headers = {"Authorization" : f"Bearer {bearer_token}"}

    def start_stream(self, queue, end_time):
        # Source: https://gist.github.com/hiway/4427458
        response = requests.get(self.api, headers=self.headers, stream=True)
        print(response.status_code)
        for tweet_blob in response.iter_lines(chunk_size=1, decode_unicode=True):
            try:
                tweet = json.loads(tweet_blob)
                if tweet_blob:
                    queue.put(tweet["data"]["text"])
            except:
                pass
            
            if datetime.now() > end_time:
                return