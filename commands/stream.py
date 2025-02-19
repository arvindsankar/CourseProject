import datetime
import joblib
import keys
import random
import time

from multiprocessing import Process, Queue
from src.preprocessor import PreProcessor
from src.stream_client import StreamClient
from src.stream_client import StreamRulesClient

API_KEY = keys.API_KEY
API_SECRET_KEY = keys.API_SECRET_KEY
BEARER_TOKEN = keys.BEARER_TOKEN
CONSUMPTION_COMPLETE_MESSAGE = "DONE"

class Stream():
	def __init__(self, topic, model, vectorizer, output_, duration=datetime.timedelta(seconds=30)):
		self.topic = topic
		self.output = output_
		self.stream_client = StreamClient(keys.API_KEY, keys.API_SECRET_KEY, keys.BEARER_TOKEN)
		self.rules_client = StreamRulesClient(keys.API_KEY, keys.API_SECRET_KEY, keys.BEARER_TOKEN)
		self.duration = duration

		try:
			self.model = joblib.load(model)
			self.vectorizer = joblib.load(vectorizer)
		except:
			raise 'Failed to load model via joblib!'
		

	def consume_tweet_stream(self, tweet_queue):

		# Step 1: Clear all existing rules
		for rule in self.rules_client.list_rules():
			self.rules_client.delete_rule(rule)

		# Step 2: Add a rule for the topic
		self.rules_client.add_rule(self.topic)

		# Step 3: Start streaming and store in a queue
		self.stream_client.start_stream(tweet_queue, datetime.datetime.now() + self.duration)

		# Step 4: Clear all existing rules
		for rule in self.rules_client.list_rules():
			self.rules_client.delete_rule(rule)

		tweet_queue.put(CONSUMPTION_COMPLETE_MESSAGE)

	def execute(self):
		print("Stream - Topic: {}, Model: {}, Output: {}"
			.format(self.topic, self.model, self.output))

		output_file = open(self.output, 'w')

		tweet_queue = Queue()
		model_process = Process(target=self.consume_tweet_stream, args=(tweet_queue,))
		model_process.start()

		while True:
			tweet = tweet_queue.get()
			if tweet == CONSUMPTION_COMPLETE_MESSAGE:
				break
			else:
				tweet = tweet.encode("unicode_escape").decode("utf-8")
				modified_tweet = PreProcessor(tweet).run()
				prediction = int(self.model.predict(self.vectorizer.transform([modified_tweet]))[0])
				next_line = "{},{}\n".format(prediction, tweet)
				output_file.write(next_line)

class StreamSimulator(Stream):
	def __init__(self, model, vectorizer, input_, output_, duration=datetime.timedelta(seconds=30)):
		super().__init__("Simulated", model, vectorizer, output_, duration)
		self.input = input_

	def consume_tweet_stream(self, tweet_queue):
		try:
			input_file = open(self.input, 'r')
		except BaseException:
			raise 'Input file provided not found!'

		tweets = input_file.readlines()
		random.shuffle(tweets)
		delta = (self.duration.seconds * 1.0) / len(tweets)
		variance = delta * 0.1


		for tweet in tweets:
			time.sleep(delta + random.uniform(-variance, variance))
			tweet_queue.put(tweet)

		tweet_queue.put(CONSUMPTION_COMPLETE_MESSAGE)
