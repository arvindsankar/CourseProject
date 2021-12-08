import keys
from datetime import datetime
from datetime import timedelta
from multiprocessing import Process, Queue

from src.base_twitter_client import BaseTwitterClient
from src.stream_client import StreamClient
from src.stream_client import StreamRulesClient
from src.search_client import SearchClient
from src.tweet_lookup_client import TweetLookupClient

API_KEY = keys.API_KEY
API_SECRET_KEY = keys.API_SECRET_KEY
BEARER_TOKEN = keys.BEARER_TOKEN
CONSUMPTION_COMPLETE_MESSAGE = "DONE"

def consume_tweet_stream(tweet_queue):
    stream_client = StreamClient(keys.API_KEY, keys.API_SECRET_KEY, keys.BEARER_TOKEN)
    rules_client = StreamRulesClient(keys.API_KEY, keys.API_SECRET_KEY, keys.BEARER_TOKEN)

    print("current rules: " + str(rules_client.list_rules()))
    rules_client.add_rule("cats")

    stream_client.start_stream(tweet_queue, datetime.now() + timedelta(seconds=30))

    for rule in rules_client.list_rules():
        rules_client.delete_rule(rule)

    print("current rules: " + str(rules_client.list_rules()))

    tweet_queue.put(CONSUMPTION_COMPLETE_MESSAGE)


if __name__ == '__main__':
    tweet_queue = Queue()
    model_process = Process(target=consume_tweet_stream, args=(tweet_queue,))
    model_process.start()

    while True:
        tweet = tweet_queue.get()
        if tweet == CONSUMPTION_COMPLETE_MESSAGE:
            break
        else:
            print(tweet)
