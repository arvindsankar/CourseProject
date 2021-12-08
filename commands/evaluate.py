import joblib
import numpy as np
import random

class Evaluate():
	def __init__(self, model, input_, output_):
		try:
			self.model = joblib.load(model)
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
			# TODO: figure out how to predict using the model
			# print(self.model.predict(np.array(tweet).reshape(-1, 1)))
			next_line = "{},{}".format(str(random.randint(0,1)), tweet)
			output_file.write(next_line)
