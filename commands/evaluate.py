import joblib
import numpy as np
import random
from src.preprocessor import PreProcessor
from sklearn.feature_extraction.text import TfidfVectorizer

class Evaluate():
	def __init__(self, model, vectorizer, input_, output_):
		try:
			self.model = joblib.load(model)
			self.vectorizer = joblib.load(vectorizer)
		except:
			raise 'Failed to load model via joblib!'

		self.input = input_
		self.output = output_

	def execute(self):
		print("Evaluate - Model: {}, Input: {}, Output: {}"
			.format(self.model, self.input, self.output))

		try:
			input_file = open(self.input, 'r')
		except BaseException:
			raise 'Input file provided not found!'

		output_file = open(self.output, 'w')
		for tweet in input_file:
			modified_tweet = PreProcessor(tweet).run()
			prediction = int(self.model.predict(self.vectorizer.transform([modified_tweet]))[0])
			next_line = "{},{}".format(prediction, tweet)
			output_file.write(next_line)
