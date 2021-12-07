import keys
from datetime import datetime
from datetime import timedelta
from src.base_twitter_client import BaseTwitterClient
from src.search_client import SearchClient
from src.tweet_lookup_client import TweetLookupClient

API_KEY = keys.API_KEY
API_SECRET_KEY = keys.API_SECRET_KEY
BEARER_TOKEN = keys.BEARER_TOKEN

start_date = datetime(2021, 11, 29, hour=3) # Monday
end_date = datetime(2021, 11, 29, hour=3, minute=30)
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
    lookup_client.write_tweets_to_file("data/Jeopardy_{}_{}_{}".format(start_date.year, start_date.month, ('0' + str(start_date.day))[-2:]))