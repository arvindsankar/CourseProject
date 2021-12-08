import csv
import re
import html
import csv
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TreebankWordTokenizer
import string

class PreProcessor():
	def __init__(self, base_string):
		self.string = base_string

	def run(self):
		self.remove_punctuations()
		self.clean()
		self.negation()
		self.remove_chars()
		self.remove_stop_words()
		#self.stemming()
		#self.lemmatize()
		return self.string

	def remove_punctuations(self):
		punctuations_list = string.punctuation
		translator = str.maketrans('', '', punctuations_list)
		self.string = self.string.translate(translator)

	def clean(self):
		mentions = r'@[A-Za-z0-9]+'
		url_https = 'https?://[A-Za-z0-9./]+'
		url_www = r'www.[^ ]+'

		tweet = self.string
		tweet = html.unescape(tweet)
		tweet = re.sub(mentions, '', tweet)
		tweet = re.sub(url_https, '', tweet)
		tweet = re.sub(url_www, '', tweet)
		tweet = tweet.lower()
		self.string = tweet

	def negation(self):
		negations = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",
			 "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
			 "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
			 "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
			 "mustn't":"must not"}

		tweet = self.string
		for a, b in negations.items():
			if a in tweet:
				tweet = tweet.replace(a,b)

		tweet = re.sub("[^a-zA-Z]", " ", tweet)
		self.string = tweet

	def remove_chars(self):
		#Removing characters except letters
		tweet = self.string
		tweet = re.sub("[^a-zA-Z]", " ", tweet)
		#Removing unnecessary white spaces using tokenizer
		token = TreebankWordTokenizer()
		word_list = token.tokenize(tweet)
		tweet = " ".join(word_list).strip()
		self.string = tweet

	def remove_stop_words(self):
		tweet = self.string
		stopwords = set(['a', 'about', 'above', 'after', 'again', 'ain', 'all', 'am', 'an',
			 'and','any','are', 'as', 'at', 'be', 'because', 'been', 'before',
			 'being', 'below', 'between','both', 'by', 'can', 'd', 'did', 'do',
			 'does', 'doing', 'down', 'during', 'each','few', 'for', 'from',
			 'further', 'had', 'has', 'have', 'having', 'he', 'her', 'here',
			 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in',
			 'into','is', 'it', 'its', 'itself', 'just', 'll', 'm', 'ma',
			 'me', 'more', 'most','my', 'myself', 'now', 'o', 'of', 'on', 'once',
			 'only', 'or', 'other', 'our', 'ours','ourselves', 'out', 'own', 're','s', 'same', 'she', "shes", 'should', "shouldve",'so', 'some', 'such',
			 't', 'than', 'that', "thatll", 'the', 'their', 'theirs', 'them',
			 'themselves', 'then', 'there', 'these', 'they', 'this', 'those',
			 'through', 'to', 'too','under', 'until', 'up', 've', 'very', 'was',
			 'we', 'were', 'what', 'when', 'where','which','while', 'who', 'whom',
			 'why', 'will', 'with', 'won', 'y', 'you', "youd","youll", "youre",
			 "youve", 'your', 'yours', 'yourself', 'yourselves','jeopardy','rt'])
		self.string = " ".join([word for word in str(self.string).split() if word not in stopwords])

	def stemming(self):
		st = nltk.PorterStemmer()
		self.string = " ".join([st.stem(word) for word in self.string])

	def lemmatize(self):
		lm = nltk.WordNetLemmatizer()
		self.string = " ".join([lm.lemmatize(word) for word in self.string])
