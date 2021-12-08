import keys
import datetime
from src.search_client import SearchClient
from src.tweet_lookup_client import TweetLookupClient

API_KEY = keys.API_KEY
API_SECRET_KEY = keys.API_SECRET_KEY
BEARER_TOKEN = keys.BEARER_TOKEN

class Download():
	def __init__(self, topic, start_time, end_time, output_):

		if start_time > end_time:
			raise "End Time needs to be after Start Time!"
		if start_time < datetime.datetime.now() - datetime.timedelta(days=7):
			raise "Start Time needs to be within the last week!"

		self.topic = topic
		self.start_time = start_time
		self.end_time = end_time
		self.output = output_

	def execute(self):
		print("Download - Topic: {}, Start Time: {}, End Time: {}, Saving output to: {}"
			.format(self.topic, self.start_time, self.end_time, self.output))

		search_client = SearchClient(keys.API_KEY, keys.API_SECRET_KEY, keys.BEARER_TOKEN)
		search_client.collect_tweets(self.topic, self.start_time.isoformat() + 'Z', self.end_time.isoformat() + 'Z')

		lookup_client = TweetLookupClient(keys.API_KEY, keys.API_SECRET_KEY, keys.BEARER_TOKEN)
		lookup_client.lookup_tweets(search_client.tweet_ids)
		lookup_client.write_tweets_to_file(self.output)
