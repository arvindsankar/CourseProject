import csv
import re
import html
import csv
import nltk
from csv import writer
from ast import literal_eval
import numpy as np
import pandas as pd
import pylab as pl
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import wordnet

#Load dataframe for any data
def ppAnyLoadToDF(file):
  DATASET_COLUMNS=['tweet_Id','date','text1','text2','text3','text4','text5']
  DATASET_ENCODING = "ISO-8859-1"
  df = pd.read_csv(file, header = None, names=DATASET_COLUMNS, quoting=csv.QUOTE_NONE)
  print('Found the file!')
  return df

#Combine tweet columns to one
def ppCombineToFullLen(df):
  #preprocess-combine multiple columns of tweets to full length tweets
  df['fulltweet'] = df['text1'].fillna('').fillna('NaN').map(str) + '' + df['text2'].fillna('').fillna('NaN').map(str) + '' + df['text3'].fillna('').fillna('NaN').map(str)+ ''+ df['text4'].fillna('').fillna('NaN').map(str)+ '' + df['text5'].fillna('').fillna('NaN').map(str)
  #dropping multiple columns of tweets after combining into fulltweet
  df.drop(['text1','text2','text3','text4','text5'], axis=1, inplace=True)
  print(df.sample(5))
  return df

#Removing punctuations
def ppRemovePunct(df):
  import string
  english_punctuations = string.punctuation
  punctuations_list = english_punctuations

  def cleaning_punctuations(text):
    translator = str.maketrans('', '', punctuations_list)
    return text.translate(translator)

  df['fulltweet']= df['fulltweet'].apply(lambda x: cleaning_punctuations(x))
  df['fulltweet'].tail()
  print('cleaned punctuations!')
  return df


def ppAllCleanTweets(df):
  token = TreebankWordTokenizer()
  mentions = r'@[A-Za-z0-9]+'
  url_https = 'https?://[A-Za-z0-9./]+'
  url_www = r'www.[^ ]+'

  negations = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",
             "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
             "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
             "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
             "mustn't":"must not"
            }

  stopwordlist = ['a', 'about', 'above', 'after', 'again', 'ain', 'all', 'am', 'an',
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
             "youve", 'your', 'yours', 'yourself', 'yourselves','jeopardy','rt']

  def tweet_cleaning(fulltweet):
    fulltweet = html.unescape(fulltweet)
    fulltweet = re.sub(mentions, '', fulltweet)
    fulltweet = re.sub(url_https, '', fulltweet)
    tefulltweetxt = re.sub(url_www, '', fulltweet)
    fulltweet = fulltweet.lower()
    for a, b in negations.items():
        if a in fulltweet:
            fulltweet = fulltweet.replace(a,b)
    #Removing characters except letters
    fulltweet = re.sub("[^a-zA-Z]", " ", fulltweet)
    #Removing unnecessary white spaces using tokenizer
    word_list = token.tokenize(fulltweet)
    fulltweet = " ".join(word_list).strip()
    return fulltweet
  
  df['fulltweet'] = df['fulltweet'].apply(lambda x: tweet_cleaning(x)) 
  
  #removing stopwords
  STOPWORDS = set(stopwordlist)
  def cleaning_stopwords(text):
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])
  
  df['fulltweet'] = df['fulltweet'].apply(lambda x: cleaning_stopwords(x))
  
  #stemming- Stemming refers to the process of normalization, 
  #where we reduce a word to its base stem, for example, “automate”, “automatic”, “automation,” “automations” 
  #will be reduced to “automat” such that all these forms refer to automat.
  st = nltk.PorterStemmer()
  def stemming_on_text(data):
    text = [st.stem(word) for word in data]
    return data
  df['fulltweet']= df['fulltweet'].apply(lambda x: stemming_on_text(x))
  
  #lemmatize- Lemmatization on the other hand usually refers to doing things properly 
  #with the use of a vocabulary and morphological analysis, normally aiming to remove 
  #inflectional endings only and to return the dictionary form of a word.
  lm = nltk.WordNetLemmatizer()
  def lemmatizer_on_text(data):
    text = [lm.lemmatize(word) for word in data]
    return data
  df['fulltweet'] = df['fulltweet'].apply(lambda x: lemmatizer_on_text(x))
  print(df.sample(5))
  print('cleaned tweets-(removed urls,mentions,hashtags,negations and stopwords),Lemmatization and Stemming done!')


datafile = ppAnyLoadToDF('../data/Jeopardy_2021_12_04')
datafile = ppCombineToFullLen(datafile)
ppRemovePunct(datafile)
ppAllCleanTweets(datafile)
datafile.to_csv('my_csv.csv', mode='a', header=False)


